
import pandas as pd


# ============================================================
# CONFIGURAÇÃO DAS REGRAS DE NEGÓCIO
# ============================================================

REGRAS_QUALIDADE = {

    "colunas_obrigatorias": [
        "id_cliente",
        "nome",
        "idade",
        "email",
    ],

    "campos_obrigatorios": [
        "id_cliente",
        "nome",
    ],

    "colunas_unicas": [
        "id_cliente",
    ],

    "validar_email": True,
    "coluna_email": "email",

    "validar_idade": True,
    "coluna_idade": "idade",
    "idade_minima": 0,
    "idade_maxima": 120,
}


# ============================================================
# MOTOR DE REGRAS DE QUALIDADE
# ============================================================

def validar_regras(
    df: pd.DataFrame,
    regras: dict = REGRAS_QUALIDADE,
) -> dict:

    """
    Executa regras de negócio configuráveis.

    Identifica os registros afetados sem modificar
    os dados originais.
    """

    resultados = []

    def registrar(
        regra,
        coluna,
        severidade,
        registros,
        descricao,
    ):

        resultados.append({
            "regra": regra,
            "coluna": coluna,
            "severidade": severidade,
            "quantidade": len(registros),
            "descricao": descricao,
            "registros_afetados": registros,
        })

    def identificar_registros(mask, coluna):

        registros = []

        posicoes = [
            posicao
            for posicao, afetado in enumerate(mask)
            if afetado
        ]

        for posicao in posicoes:

            linha = df.iloc[posicao]

            identificador = (
                linha["id_cliente"]
                if "id_cliente" in df.columns
                else None
            )

            valor = (
                linha[coluna]
                if coluna in df.columns
                else None
            )

            registros.append({
                "linha_arquivo": posicao + 2,
                "indice_dataframe": str(df.index[posicao]),
                "id_cliente": (
                    str(identificador)
                    if pd.notna(identificador)
                    else None
                ),
                "coluna": coluna,
                "valor": (
                    str(valor)
                    if pd.notna(valor)
                    else None
                ),
            })

        return registros

    # --------------------------------------------------------
    # 1. Colunas obrigatórias
    # --------------------------------------------------------

    for coluna in regras["colunas_obrigatorias"]:

        if coluna not in df.columns:

            registrar(
                regra="coluna_obrigatoria",
                coluna=coluna,
                severidade="CRITICA",
                registros=[],
                descricao=(
                    f"A coluna obrigatória '{coluna}' não existe."
                ),
            )

    colunas_existentes = set(df.columns)

    # --------------------------------------------------------
    # 2. Campos obrigatórios
    # --------------------------------------------------------

    for coluna in regras["campos_obrigatorios"]:

        if coluna in colunas_existentes:

            mask = df[coluna].isnull()

            if mask.any():

                registros = identificar_registros(
                    mask,
                    coluna,
                )

                registrar(
                    regra="campo_obrigatorio",
                    coluna=coluna,
                    severidade="ALTA",
                    registros=registros,
                    descricao=(
                        f"Existem {len(registros)} valores "
                        f"ausentes em '{coluna}'."
                    ),
                )

    # --------------------------------------------------------
    # 3. Unicidade
    # --------------------------------------------------------

    for coluna in regras["colunas_unicas"]:

        if coluna in colunas_existentes:

            mask = (
                df[coluna].duplicated(keep=False)
                & df[coluna].notna()
            )

            if mask.any():

                registros = identificar_registros(
                    mask,
                    coluna,
                )

                registrar(
                    regra="valor_unico",
                    coluna=coluna,
                    severidade="ALTA",
                    registros=registros,
                    descricao=(
                        f"Existem {len(registros)} registros "
                        f"envolvidos em duplicidades "
                        f"na coluna '{coluna}'."
                    ),
                )

    # --------------------------------------------------------
    # 4. Formato de e-mail
    # --------------------------------------------------------

    if regras["validar_email"]:

        coluna = regras["coluna_email"]

        if coluna in colunas_existentes:

            emails = df[coluna].astype("string")

            mask = (
                emails.notna()
                & ~emails.str.match(
                    r"^[^@\s]+@[^@\s]+\.[^@\s]+$",
                    na=False,
                )
            )

            if mask.any():

                registros = identificar_registros(
                    mask,
                    coluna,
                )

                registrar(
                    regra="formato_email",
                    coluna=coluna,
                    severidade="MEDIA",
                    registros=registros,
                    descricao=(
                        f"Existem {len(registros)} e-mails "
                        "com formato potencialmente inválido."
                    ),
                )

    # --------------------------------------------------------
    # 5. Intervalo de idade
    # --------------------------------------------------------

    if regras["validar_idade"]:

        coluna = regras["coluna_idade"]

        if coluna in colunas_existentes:

            idade = pd.to_numeric(
                df[coluna],
                errors="coerce",
            )

            mask = (
                (idade < regras["idade_minima"])
                | (idade > regras["idade_maxima"])
            )

            if mask.any():

                registros = identificar_registros(
                    mask,
                    coluna,
                )

                registrar(
                    regra="intervalo_idade",
                    coluna=coluna,
                    severidade="MEDIA",
                    registros=registros,
                    descricao=(
                        f"Existem {len(registros)} valores "
                        "fora do intervalo permitido."
                    ),
                )

    # --------------------------------------------------------
    # 6. Resultado consolidado
    # --------------------------------------------------------

    return {
        "total_regras_violadas": len(resultados),

        "total_ocorrencias": sum(
            item["quantidade"]
            for item in resultados
        ),

        "regras_violadas": resultados,
    }
