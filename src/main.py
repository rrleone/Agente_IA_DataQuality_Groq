import json
import os
import pandas as pd

from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

from data_quality import (
    analisar_qualidade,
    analisar_duplicidades_colunas,
)

from regras_qualidade import validar_regras
from plano_tratamento import gerar_plano_tratamento
from validar_interpretacao import validar_interpretacao_ia


# ============================================================
# CONFIGURAÇÕES
# ============================================================

CAMINHO_CSV = Path("01_data/clientes_teste.csv")
PASTA_RELATORIOS = Path("03_reports")

MODELO_GROQ = "openai/gpt-oss-20b"


# ============================================================
# INTERPRETAÇÃO COM IA
# ============================================================

def interpretar_com_ia(relatorio: dict) -> str:
    """
    Envia o relatório técnico para a Groq e retorna
    uma interpretação profissional em português.
    """

    load_dotenv()

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError(
            "GROQ_API_KEY não encontrada no arquivo .env"
        )

    cliente = Groq(api_key=api_key)

    dados_json = json.dumps(
        relatorio,
        ensure_ascii=False,
        indent=2,
        default=str,
    )

    resposta = cliente.chat.completions.create(
        model=MODELO_GROQ,
        messages=[
            {
                "role": "system",
                "content": """
Você é um especialista sênior em Data Quality,
Governança de Dados e Business Intelligence.

Sua função é interpretar resultados técnicos
produzidos por um sistema Python.

REGRAS OBRIGATÓRIAS:

1. Utilize somente os fatos presentes no relatório técnico.
2. Não invente números, registros, regras ou ocorrências.
3. Diferencie claramente fatos, riscos e hipóteses.
4. Não considere valores repetidos como erros automaticamente.
5. Só classifique uma violação quando houver regra configurada.
6. Não considere float64 um erro automaticamente.
7. Valores ausentes podem influenciar o tipo de dado.
8. Não recomende exclusão automática de registros.
9. Não execute nem simule correções.
10. Todas as recomendações dependem de aprovação humana.
11. Não afirme que os dados foram corrigidos ou tratados.
12. Se uma informação não estiver disponível, informe isso
    explicitamente em vez de inferi-la.
13. Diferencie quantidade de regras violadas de quantidade
    de ocorrências.
14. Ao citar registros afetados, utilize somente os registros
    listados no relatório técnico.

ESTRUTURA DO RELATÓRIO:

1. Resumo Executivo
2. Indicadores Gerais de Qualidade
3. Problemas Identificados
4. Violações das Regras de Negócio
5. Registros Afetados
6. Riscos para o Negócio
7. Recomendações
8. Priorização das Ações
9. Conclusão

Produza um relatório profissional, objetivo, completo
e em português brasileiro.

Evite repetir informações desnecessariamente.
Não interrompa o relatório antes da conclusão.
"""
            },
            {
                "role": "user",
                "content": (
                    "Gere o relatório interpretativo completo "
                    "com base exclusivamente nestes dados técnicos:\n\n"
                    + dados_json
                ),
            },
        ],
        temperature=0.2,
        max_completion_tokens=6000,
    )

    conteudo = resposta.choices[0].message.content

    if not conteudo or not conteudo.strip():
        raise ValueError(
            "A Groq retornou uma resposta vazia."
        )

    return conteudo.strip()


# ============================================================
# EXECUÇÃO DO AGENTE
# ============================================================

def main():

    print("=" * 60)
    print("AGENTE DE IA - DATA QUALITY")
    print("=" * 60)

    # --------------------------------------------------------
    # 1. Carregar dados
    # --------------------------------------------------------

    if not CAMINHO_CSV.exists():
        raise FileNotFoundError(
            f"Arquivo CSV não encontrado: {CAMINHO_CSV}"
        )

    df = pd.read_csv(CAMINHO_CSV)

    # --------------------------------------------------------
    # 2. Análise técnica
    # --------------------------------------------------------

    resultado = analisar_qualidade(df)

    duplicidades = analisar_duplicidades_colunas(df)

    # --------------------------------------------------------
    # 3. Regras de negócio
    # --------------------------------------------------------

    regras = validar_regras(df)

    # --------------------------------------------------------
    # 4. Gerar plano de tratamento
    # --------------------------------------------------------

    plano_tratamento = gerar_plano_tratamento(regras)

    # --------------------------------------------------------
    # 5. Consolidar relatório técnico
    # --------------------------------------------------------

    relatorio = {
        "arquivo_analisado": str(CAMINHO_CSV),

        "data_analise": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),

        "analise_geral": resultado,

        "duplicidades_por_coluna": duplicidades,

        "regras_negocio": regras,

        "plano_tratamento": plano_tratamento,
    }

    # --------------------------------------------------------
    # 6. Exibir análise técnica
    # --------------------------------------------------------

    print("\nANÁLISE TÉCNICA")
    print("-" * 60)

    print(f"Arquivo: {CAMINHO_CSV}")
    print(f"Registros: {resultado['total_linhas']}")
    print(f"Colunas: {resultado['total_colunas']}")
    print(f"Linhas duplicadas: {resultado['linhas_duplicadas']}")

    # --------------------------------------------------------
    # 7. Exibir regras de negócio
    # --------------------------------------------------------

    print("\nVALIDAÇÃO DAS REGRAS DE NEGÓCIO")
    print("-" * 60)

    print(
        f"Regras violadas: "
        f"{regras['total_regras_violadas']}"
    )

    print(
        f"Total de ocorrências: "
        f"{regras['total_ocorrencias']}"
    )

    for item in regras["regras_violadas"]:

        print(f"\nRegra: {item['regra']}")
        print(f"Coluna: {item['coluna']}")
        print(f"Severidade: {item['severidade']}")
        print(f"Ocorrências: {item['quantidade']}")

        for registro in item["registros_afetados"]:

            print(
                f"  Linha CSV: {registro['linha_arquivo']} | "
                f"ID: {registro['id_cliente']} | "
                f"Valor: {registro['valor']}"
            )

    # --------------------------------------------------------
    # 8. Exibir plano de tratamento
    # --------------------------------------------------------

    print("\nPLANO DE TRATAMENTO")
    print("-" * 60)

    print(
        "Ações recomendadas: "
        f"{plano_tratamento['total_acoes_recomendadas']}"
    )

    print(
        "Ações pendentes: "
        f"{plano_tratamento['acoes_pendentes']}"
    )

    for acao in plano_tratamento["plano"]:

        print(f"\nAção {acao['id_plano']}")
        print(f"Regra: {acao['regra']}")
        print(f"Coluna: {acao['coluna']}")
        print(f"Severidade: {acao['severidade']}")

        print(
            f"Registros envolvidos: "
            f"{acao['quantidade_registros']}"
        )

        print(
            f"Recomendação: "
            f"{acao['acao_recomendada']}"
        )

        print(
            f"Justificativa: "
            f"{acao['justificativa']}"
        )

        print(
            f"Status: {acao['status']}"
        )

        print(
            "Aprovação humana: "
            f"{acao['requer_aprovacao_humana']}"
        )

    # --------------------------------------------------------
    # 9. Salvar relatório técnico JSON
    # --------------------------------------------------------

    PASTA_RELATORIOS.mkdir(
        parents=True,
        exist_ok=True,
    )

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    caminho_json = (
        PASTA_RELATORIOS
        / f"relatorio_data_quality_{timestamp}.json"
    )

    with open(
        caminho_json,
        "w",
        encoding="utf-8",
    ) as arquivo:

        json.dump(
            relatorio,
            arquivo,
            ensure_ascii=False,
            indent=4,
            default=str,
        )

    print("\nRELATÓRIO TÉCNICO SALVO")
    print(caminho_json)

    # --------------------------------------------------------
    # 10. Interpretar com Groq
    # --------------------------------------------------------

    print("\nSOLICITANDO INTERPRETAÇÃO À GROQ...")
    print("-" * 60)

    try:

        interpretacao = interpretar_com_ia(relatorio)

        print("\nRELATÓRIO INTERPRETATIVO DA IA")
        print("=" * 60)

        print(interpretacao)

        caminho_txt = (
            PASTA_RELATORIOS
            / f"interpretacao_ia_{timestamp}.txt"
        )

        with open(
            caminho_txt,
            "w",
            encoding="utf-8",
        ) as arquivo:

            arquivo.write(interpretacao)

        print("\nINTERPRETAÇÃO SALVA")
        print(caminho_txt)

        # ----------------------------------------------------
        # 11. Validar interpretação da IA
        # ----------------------------------------------------

        print("\nVALIDANDO INTERPRETAÇÃO DA IA...")
        print("-" * 60)

        resultado_validacao = validar_interpretacao_ia(
            interpretacao=interpretacao,
            relatorio_tecnico=relatorio,
            df=df,
        )

        print(
            f"Status da validação: "
            f"{resultado_validacao['status']}"
        )

        print(
            f"Total de alertas: "
            f"{resultado_validacao['total_alertas']}"
        )

        for alerta in resultado_validacao["alertas"]:

            print(f"- {alerta}")

        caminho_validacao = (
            PASTA_RELATORIOS
            / f"validacao_interpretacao_ia_{timestamp}.json"
        )

        with open(
            caminho_validacao,
            "w",
            encoding="utf-8",
        ) as arquivo:

            json.dump(
                resultado_validacao,
                arquivo,
                ensure_ascii=False,
                indent=4,
            )

        print("\nVALIDAÇÃO DA IA SALVA")
        print(caminho_validacao)

    except Exception as erro:

        print("\nERRO NA INTERPRETAÇÃO OU VALIDAÇÃO DA IA")
        print("-" * 60)

        print(f"Detalhes: {erro}")
        print("O relatório técnico foi preservado.")

    print("\n" + "=" * 60)
    print("PROCESSO CONCLUÍDO")
    print("=" * 60)


if __name__ == "__main__":
    main()