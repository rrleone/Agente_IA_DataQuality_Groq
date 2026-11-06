
import pandas as pd


def analisar_qualidade(df: pd.DataFrame) -> dict:
    """
    Realiza análise genérica de Data Quality.
    Não modifica os dados originais.
    """

    total_linhas = len(df)
    total_colunas = len(df.columns)

    if total_linhas == 0:
        raise ValueError("O arquivo não possui registros para analisar.")

    valores_ausentes = df.isnull().sum()
    percentual_ausentes = (
        valores_ausentes / total_linhas * 100
    ).round(2)

    valores_unicos = df.nunique()
    percentual_unicos = (
        valores_unicos / total_linhas * 100
    ).round(2)

    duplicidades = int(df.duplicated().sum())

    colunas_constantes = [
        coluna
        for coluna in df.columns
        if df[coluna].nunique(dropna=False) <= 1
    ]

    possiveis_identificadores = [
        coluna
        for coluna in df.columns
        if (
            df[coluna].nunique(dropna=True) == total_linhas
            and df[coluna].isnull().sum() == 0
        )
    ]

    estatisticas_numericas = {}

    for coluna in df.select_dtypes(include="number").columns:
        estatisticas_numericas[coluna] = {
            "minimo": df[coluna].min(),
            "maximo": df[coluna].max(),
            "media": round(df[coluna].mean(), 2),
            "mediana": round(df[coluna].median(), 2),
        }

    estatisticas_categoricas = {}

    for coluna in df.select_dtypes(
        include=["object", "string", "category"]
    ).columns:

        moda = df[coluna].mode()

        estatisticas_categoricas[coluna] = {
            "valores_distintos": int(df[coluna].nunique()),
            "valor_mais_frequente": (
                moda.iloc[0] if not moda.empty else None
            ),
        }

    return {
        "total_linhas": total_linhas,
        "total_colunas": total_colunas,
        "linhas_duplicadas": duplicidades,
        "valores_ausentes": valores_ausentes.to_dict(),
        "percentual_ausentes": percentual_ausentes.to_dict(),
        "valores_unicos": valores_unicos.to_dict(),
        "percentual_unicos": percentual_unicos.to_dict(),
        "colunas_constantes": colunas_constantes,
        "possiveis_identificadores": possiveis_identificadores,
        "tipos_dados": df.dtypes.astype(str).to_dict(),
        "estatisticas_numericas": estatisticas_numericas,
        "estatisticas_categoricas": estatisticas_categoricas,
    }


def analisar_duplicidades_colunas(df: pd.DataFrame) -> dict:
    """
    Identifica valores repetidos individualmente em cada coluna.
    Não modifica os dados originais.
    """

    resultado = {}

    for coluna in df.columns:

        quantidade = int(df[coluna].duplicated().sum())

        percentual = (
            round(quantidade / len(df) * 100, 2)
            if len(df) > 0
            else 0
        )

        resultado[coluna] = {
            "valores_duplicados": quantidade,
            "percentual_duplicado": percentual,
        }

    return resultado
