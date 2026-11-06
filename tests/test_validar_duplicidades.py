"""
Testes automatizados para validar informações de duplicidade na interpretação IA.

Execute na raiz do projeto:
    pytest -v tests/test_validar_duplicidades.py

Nesta etapa são testes de especificação: alguns podem falhar porque a
verificação de duplicidades ainda não foi implementada no validador.
"""

import sys
from pathlib import Path

import pandas as pd
import pytest

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
                    "registros": [
                        {"linha_arquivo": 6, "id_cliente": 5, "valor": 5},
                        {"linha_arquivo": 7, "id_cliente": 5, "valor": 5},
                    ],
                }
            ]
        }
    }


def validar(texto, df_teste, relatorio_tecnico):
    return validar_interpretacao_ia(
        interpretacao=SECOES + "\n" + texto,
        relatorio_tecnico=relatorio_tecnico,
        df=df_teste,
    )


def alertas_tipo(resultado, tipo):
    return [a for a in resultado["alertas"] if a["tipo"] == tipo]


def texto_base_ausencias():
    return """
    Total de valores ausentes: 2.
    Valores ausentes em idade: linha CSV 4.
    Valores ausentes em email: linha CSV 5.
    """


def test_duplicidade_correta_nao_gera_alerta(
    df_teste, relatorio_tecnico
):
    texto = texto_base_ausencias() + """
    Duplicidade em id_cliente: ID 5 aparece em 2 ocorrências,
    nas linhas CSV 6 e 7.
    """
    resultado = validar(texto, df_teste, relatorio_tecnico)

    assert alertas_tipo(resultado, "DUPLICIDADES") == []


def test_id_duplicado_incorreto_deve_gerar_alerta(
    df_teste, relatorio_tecnico
):
    texto = texto_base_ausencias() + """
    Duplicidade em id_cliente: ID 8 aparece em 2 ocorrências,
    nas linhas CSV 6 e 7.
    """
    resultado = validar(texto, df_teste, relatorio_tecnico)

    assert alertas_tipo(resultado, "DUPLICIDADES")


def test_quantidade_incorreta_de_ocorrencias_deve_gerar_alerta(
    df_teste, relatorio_tecnico
):
    texto = texto_base_ausencias() + """
    Duplicidade em id_cliente: ID 5 aparece em 3 ocorrências,
    nas linhas CSV 6 e 7.
    """
    resultado = validar(texto, df_teste, relatorio_tecnico)

    assert alertas_tipo(resultado, "DUPLICIDADES")


def test_linhas_incorretas_da_duplicidade_devem_gerar_alerta(
    df_teste, relatorio_tecnico
):
    texto = texto_base_ausencias() + """
    Duplicidade em id_cliente: ID 5 aparece em 2 ocorrências,
    nas linhas CSV 5 e 8.
    """
    resultado = validar(texto, df_teste, relatorio_tecnico)

    assert alertas_tipo(resultado, "DUPLICIDADES")


def test_id_duplicado_inventado_deve_gerar_alerta(
    df_teste, relatorio_tecnico
):
    texto = texto_base_ausencias() + """
    Duplicidade em id_cliente: ID 5 aparece em 2 ocorrências,
    nas linhas CSV 6 e 7. Também foi identificado ID 99 duplicado.
    """
    resultado = validar(texto, df_teste, relatorio_tecnico)

    assert alertas_tipo(resultado, "DUPLICIDADES")
