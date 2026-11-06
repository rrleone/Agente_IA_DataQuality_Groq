"""
Testes automatizados do validador de interpretação da IA.

Execute na raiz do projeto:
    pytest -v tests/test_validar_interpretacao.py
"""

import sys
from pathlib import Path

import pandas as pd
import pytest

# Garante que o diretório src seja encontrado pelo pytest no macOS/VS Code.
RAIZ_PROJETO = Path(__file__).resolve().parents[1]
DIRETORIO_SRC = RAIZ_PROJETO / "src"
sys.path.insert(0, str(DIRETORIO_SRC))

from validar_interpretacao import validar_interpretacao_ia


SECOES = """
1. Resumo Executivo
2. Indicadores Gerais de Qualidade
3. Problemas Identificados
4. Violações das Regras de Negócio
5. Registros Afetados
6. Riscos para o Negócio
7. Recomendações
8. Priorização das Ações
9. Conclusão
"""


@pytest.fixture
def df_teste():
    return pd.DataFrame(
        {
            "id_cliente": [1, 2, 3, 4, 5, 5, 6],
            "nome": ["Ana", "Bruno", "Carlos", "Diana", "Bruno", "Bruno", "Elena"],
            "idade": [28, 35, None, 42, 35, 35, 29],
            "email": [
                "ana@email.com",
                "bruno@email.com",
                "carlos@email.com",
                None,
                "bruno@email.com",
                "bruno@email.com",
                "elena@email.com",
            ],
        }
    )


@pytest.fixture
def relatorio_tecnico():
    return {
        "regras_qualidade": {
            "violacoes": [
                {
                    "regra": "valor_unico",
                    "coluna": "id_cliente",
                    "severidade": "ALTA",
                    "ocorrencias": 2,
                }
            ]
        }
    }


def executar(texto, df_teste, relatorio_tecnico):
    return validar_interpretacao_ia(
        interpretacao=SECOES + "\n" + texto,
        relatorio_tecnico=relatorio_tecnico,
        df=df_teste,
    )


def test_linhas_corretas_para_ausencias_aprovam_localizacao(
    df_teste, relatorio_tecnico
):
    texto = """
    Valores ausentes em idade: 1 registro (linha CSV 4).
    Valores ausentes em email: 1 registro (linha CSV 5).
    """
    resultado = executar(texto, df_teste, relatorio_tecnico)

    alertas_localizacao = [
        alerta for alerta in resultado["alertas"]
        if alerta["tipo"] == "LOCALIZAÇÃO DE AUSÊNCIAS"
    ]
    assert alertas_localizacao == []


def test_linhas_incorretas_sao_detectadas(df_teste, relatorio_tecnico):
    texto = """
    Valores ausentes em idade: 1 registro (linha CSV 6).
    Valores ausentes em email: 1 registro (linha CSV 7).
    """
    resultado = executar(texto, df_teste, relatorio_tecnico)

    alertas_localizacao = [
        alerta for alerta in resultado["alertas"]
        if alerta["tipo"] == "LOCALIZAÇÃO DE AUSÊNCIAS"
    ]
    assert len(alertas_localizacao) == 2


def test_linha_de_outra_coluna_nao_e_evidencia(
    df_teste, relatorio_tecnico
):
    texto = """
    Valores ausentes em idade: 1 registro.
    Valores ausentes em email: 1 registro (linha CSV 4).
    """
    resultado = executar(texto, df_teste, relatorio_tecnico)

    alertas_localizacao = [
        alerta for alerta in resultado["alertas"]
        if alerta["tipo"] == "LOCALIZAÇÃO DE AUSÊNCIAS"
    ]
    assert len(alertas_localizacao) == 2


def test_severidade_critica_divergente_e_detectada(
    df_teste, relatorio_tecnico
):
    texto = """
    A severidade da duplicidade é CRÍTICA.
    Valores ausentes em idade: linha CSV 4.
    Valores ausentes em email: linha CSV 5.
    """
    resultado = executar(texto, df_teste, relatorio_tecnico)

    assert any(alerta["tipo"] == "SEVERIDADE" for alerta in resultado["alertas"])


def test_afirmacao_de_correcao_automatica_e_detectada(
    df_teste, relatorio_tecnico
):
    texto = """
    Os dados foram corrigidos automaticamente.
    Valores ausentes em idade: linha CSV 4.
    Valores ausentes em email: linha CSV 5.
    """
    resultado = executar(texto, df_teste, relatorio_tecnico)

    assert any(
        alerta["tipo"] == "CORREÇÃO NÃO AUTORIZADA"
        for alerta in resultado["alertas"]
    )
