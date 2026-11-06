"""
Validador determinístico da interpretação produzida pela IA.

Compara fatos selecionados da interpretação com o relatório técnico e,
quando disponível, com o DataFrame original.
"""

import re
import unicodedata
from typing import Any

import pandas as pd


SECOES_OBRIGATORIAS = [
    "Resumo Executivo",
    "Indicadores Gerais de Qualidade",
    "Problemas Identificados",
    "Violações das Regras de Negócio",
    "Registros Afetados",
    "Riscos para o Negócio",
    "Recomendações",
    "Priorização das Ações",
    "Conclusão",
]


def _normalizar(texto: str) -> str:
    texto = str(texto).lower()
    texto = texto.replace("e-mail", "email").replace("e‑mail", "email")
    texto = unicodedata.normalize("NFD", texto)
    return "".join(
        caractere
        for caractere in texto
        if unicodedata.category(caractere) != "Mn"
    )


def _adicionar_alerta(
    alertas: list[dict[str, str]],
    tipo: str,
    mensagem: str,
) -> None:
    alertas.append({"tipo": tipo, "mensagem": mensagem})


def _obter_linhas_com_ausencias(df: pd.DataFrame) -> dict[str, list[int]]:
    """Retorna linhas CSV (cabeçalho = linha 1)."""
    ausencias: dict[str, list[int]] = {}

    for coluna in df.columns:
        indices = df.index[df[coluna].isna()].tolist()
        if indices:
            ausencias[str(coluna)] = [int(indice) + 2 for indice in indices]

    return ausencias


def _verificar_severidade(
    texto: str,
    relatorio_tecnico: dict[str, Any],
    alertas: list[dict[str, str]],
) -> None:
    texto_norm = _normalizar(texto)
    regras = relatorio_tecnico.get("regras_qualidade", {})
    violacoes = regras.get("violacoes", []) if isinstance(regras, dict) else []

    for violacao in violacoes:
        if not isinstance(violacao, dict):
            continue

        severidade = str(violacao.get("severidade", "")).upper()
        regra = str(violacao.get("regra", ""))
        coluna = str(violacao.get("coluna", ""))

        if severidade == "ALTA" and re.search(r"\bcritica\b|\bcritico\b", texto_norm):
            _adicionar_alerta(
                alertas,
                "SEVERIDADE",
                f"A interpretação usa classificação crítica, mas o relatório técnico "
                f"registra ALTA para a regra '{regra}' na coluna '{coluna}'.",
            )
            break


def _verificar_afirmacoes_de_correcao(
    texto: str,
    alertas: list[dict[str, str]],
) -> None:
    texto_norm = _normalizar(texto)

    afirmacoes_proibidas = [
        "dados foram corrigidos",
        "dados corrigidos automaticamente",
        "correcao automatica realizada",
        "registros foram corrigidos",
        "a limpeza foi executada",
        "os dados foram tratados automaticamente",
    ]

    if any(afirmacao in texto_norm for afirmacao in afirmacoes_proibidas):
        _adicionar_alerta(
            alertas,
            "CORREÇÃO NÃO AUTORIZADA",
            "A interpretação afirma que houve correção/tratamento dos dados, "
            "mas o agente apenas recomenda ações e exige aprovação humana.",
        )


def _extrair_numeros_de_linha(texto: str) -> set[int]:
    texto_norm = _normalizar(texto)
    numeros: set[int] = set()

    padrao = re.compile(
        r"\blinhas?\s*(?:csv|no arquivo|do arquivo)?\s*[:#]?\s*"
        r"(\d+(?:\s*(?:,|e|and)\s*\d+)*)"
    )

    for match in padrao.finditer(texto_norm):
        numeros.update(int(n) for n in re.findall(r"\d+", match.group(1)))

    return numeros


def _linhas_associadas_a_coluna(texto: str, coluna: str) -> set[int]:
    """
    Procura números de linha apenas em linhas de texto que também mencionam
    a coluna. Isso evita considerar a linha de uma coluna como evidência
    para outra coluna.
    """
    coluna_norm = _normalizar(coluna)
    linhas_associadas: set[int] = set()

    for linha_texto in texto.splitlines():
        linha_norm = _normalizar(linha_texto)

        if coluna_norm not in linha_norm:
            continue

        linhas_associadas.update(_extrair_numeros_de_linha(linha_texto))

    return linhas_associadas


def _verificar_ausencias(
    texto: str,
    df: pd.DataFrame,
    alertas: list[dict[str, str]],
) -> None:
    """Valida menção, contagem e localização de ausências por coluna.

    Em bases pequenas, valida as linhas CSV mencionadas pela IA. Em bases
    volumosas, não exige a enumeração de todas as linhas, pois isso tornaria
    a interpretação excessivamente extensa. A contagem por coluna continua
    sendo verificada em ambos os casos.
    """
    texto_norm = _normalizar(texto)
    ausencias = _obter_linhas_com_ausencias(df)
    total_celulas_ausentes = int(df.isna().sum().sum())

    # Limite para validar a localização individual de linhas.
    # Bases maiores continuam sujeitas à validação de coluna e contagem.
    validar_localizacao = total_celulas_ausentes <= 20

    for coluna, linhas_esperadas in ausencias.items():
        coluna_norm = _normalizar(coluna)
        quantidade_real = len(linhas_esperadas)

        if coluna_norm not in texto_norm:
            _adicionar_alerta(
                alertas,
                "VALORES AUSENTES",
                f"A interpretação não menciona a coluna '{coluna}', que possui "
                f"{quantidade_real} valor(es) ausente(s).",
            )
            continue

        quantidade_mencionada = _extrair_contagem_por_coluna(texto, coluna)

        if (
            quantidade_mencionada is not None
            and quantidade_mencionada != quantidade_real
        ):
            _adicionar_alerta(
                alertas,
                "CONTAGEM DE AUSÊNCIAS POR COLUNA",
                f"Contagem divergente para '{coluna}'. Esperada: "
                f"{quantidade_real}; mencionada: {quantidade_mencionada}.",
            )

        if not validar_localizacao:
            continue

        linhas_mencionadas = _linhas_associadas_a_coluna(texto, coluna)

        if linhas_mencionadas != set(linhas_esperadas):
            _adicionar_alerta(
                alertas,
                "LOCALIZAÇÃO DE AUSÊNCIAS",
                f"Linhas CSV divergentes para '{coluna}'. "
                f"Esperadas: {linhas_esperadas}; "
                f"mencionadas: {sorted(linhas_mencionadas)}.",
            )


def _extrair_contagem_por_coluna(texto: str, coluna: str) -> int | None:
    """Extrai contagem de ausência por coluna, incluindo tabelas Markdown."""
    coluna_norm = _normalizar(coluna)

    # Formato do relatório atual: | **Ausências – idade** | 50 | 0,5% |
    # Captura o primeiro valor inteiro após o nome da coluna, evitando
    # interpretar a porcentagem seguinte (ex.: 0,5%) como a contagem.
    for linha in texto.splitlines():
        linha_norm = _normalizar(linha)
        if coluna_norm not in linha_norm:
            continue
        if not re.search(r"ausencias?", linha_norm):
            continue

        partes = linha.split("|")
        for parte in partes:
            parte_norm = _normalizar(parte).strip(" *`_:-–—")
            if coluna_norm in parte_norm or "ausencia" in parte_norm:
                continue
            match = re.fullmatch(r"\s*(\d+)\s*", parte)
            if match:
                return int(match.group(1))

    texto_norm = _normalizar(texto)
    coluna_norm_regex = re.escape(coluna_norm)

    padroes = [
        rf"valores?\s+ausentes?\s*\(\s*{coluna_norm_regex}\s*\)\s*[:|=]\s*(\d+)",
        rf"{coluna_norm_regex}\s*[:|=]\s*(\d+)\s*(?:\([^)]*\))?",
        rf"{coluna_norm_regex}\s*[:|=]\s*(\d+)\s+valores?\s+ausentes?",
        rf"(\d+)\s+valores?\s+ausentes?\s+(?:em|na coluna)\s+{coluna_norm_regex}",
    ]

    for padrao in padroes:
        match = re.search(padrao, texto_norm)
        if match:
            return int(match.group(1))

    return None


def _interpretacao_informa_total_ausencias(
    texto: str,
    df: pd.DataFrame,
) -> bool:
    total_real = int(df.isna().sum().sum())
    texto_norm = _normalizar(texto)

    padroes_globais = [
        rf"\b{total_real}\s+valores?\s+ausentes?\b",
        rf"\bvalores?\s+ausentes?\s*[:=]\s*{total_real}\b",
        rf"\bvalores?\s+ausentes?\s*\|\s*{total_real}\b",
        rf"\b{total_real}\s*\(\s*[^)]*(?:idade|email)",
    ]

    if any(re.search(padrao, texto_norm) for padrao in padroes_globais):
        return True

    contagens = []
    for coluna in df.columns:
        if int(df[coluna].isna().sum()) > 0:
            valor = _extrair_contagem_por_coluna(texto, str(coluna))
            if valor is None:
                return False
            contagens.append(valor)

    return bool(contagens) and sum(contagens) == total_real


def _verificar_contagem_ausencias(
    texto: str,
    df: pd.DataFrame,
    alertas: list[dict[str, str]],
) -> None:
    total_real = int(df.isna().sum().sum())

    if total_real == 0:
        return

    texto_norm = _normalizar(texto)
    menciona_ausencia = any(
        termo in texto_norm
        for termo in ["valor ausente", "valores ausentes", "missing", "nulo", "null"]
    )

    if menciona_ausencia and not _interpretacao_informa_total_ausencias(texto, df):
        _adicionar_alerta(
            alertas,
            "CONTAGEM DE AUSÊNCIAS",
            f"O DataFrame contém {total_real} célula(s) ausente(s), "
            "mas a interpretação não informa corretamente a contagem total.",
        )



def _obter_duplicidades_dataframe(
    df: pd.DataFrame,
) -> dict[str, dict[str, dict[str, Any]]]:
    """Mapeia valores duplicados por coluna, com quantidade e linhas CSV."""
    resultado: dict[str, dict[str, dict[str, Any]]] = {}

    for coluna in df.columns:
        mascara = df[coluna].notna() & df[coluna].duplicated(keep=False)
        if not mascara.any():
            continue

        grupos = df.loc[mascara].groupby(coluna, dropna=True, sort=False)
        duplicados_coluna: dict[str, dict[str, Any]] = {}

        for valor, grupo in grupos:
            chave = str(valor)
            duplicados_coluna[chave] = {
                "valor": valor,
                "quantidade": int(len(grupo)),
                "linhas_csv": [int(indice) + 2 for indice in grupo.index],
            }

        resultado[str(coluna)] = duplicados_coluna

    return resultado


def _extrair_ids_duplicados_mencionados(
    texto: str,
    coluna: str,
) -> set[str]:
    """
    Extrai somente IDs numéricos explicitamente escritos como 'ID 5'
    em um trecho relacionado à coluna duplicada.
    """
    texto_norm = _normalizar(texto)
    coluna_norm = _normalizar(coluna)
    ids: set[str] = set()

    for match_coluna in re.finditer(re.escape(coluna_norm), texto_norm):
        inicio = max(0, match_coluna.start() - 120)
        fim = min(len(texto_norm), match_coluna.end() + 250)
        trecho = texto_norm[inicio:fim]

        if not re.search(r"duplic|repetid|ocorrenc", trecho):
            continue

        # "ID 5", "ID: 5", "ID = 5". Não captura palavras
        # posteriores nem números das linhas CSV.
        ids.update(
            re.findall(r"\bid\b\s*[:=#]?\s*(\d+)\b", trecho)
        )

    return ids


def _extrair_linhas_duplicidade(texto: str, coluna: str) -> set[int]:
    texto_norm = _normalizar(texto)
    coluna_norm = _normalizar(coluna)
    linhas: set[int] = set()

    for match in re.finditer(re.escape(coluna_norm), texto_norm):
        # Considera somente o texto posterior à coluna para não capturar
        # linhas de outras verificações (ex.: ausências de idade/email).
        inicio = match.end()
        fim = min(len(texto_norm), inicio + 350)
        trecho = texto_norm[inicio:fim]

        if not re.search(r"duplic|repetid|ocorrenc", texto_norm[max(0, match.start()-50):fim]):
            continue

        for numeros in re.findall(
            r"\blinhas?\s*(?:csv|no arquivo|do arquivo)?\s*[:#]?\s*"
            r"(\d+(?:\s*(?:,|e|and)\s*\d+)*)",
            trecho,
        ):
            linhas.update(int(n) for n in re.findall(r"\d+", numeros))

    return linhas


def _extrair_quantidade_duplicidade(texto: str, coluna: str) -> int | None:
    texto_norm = _normalizar(texto)
    coluna_norm = _normalizar(coluna)

    for match in re.finditer(re.escape(coluna_norm), texto_norm):
        inicio = max(0, match.start() - 100)
        fim = min(len(texto_norm), match.end() + 350)
        trecho = texto_norm[inicio:fim]

        if not re.search(r"duplic|repetid|ocorrenc", trecho):
            continue

        padroes = [
            r"\b(?:aparece|consta|ocorre)\s+em\s+(\d+)\s+ocorrenc",
            r"\b(\d+)\s+ocorrenc",
            r"\b(\d+)\s+registros?\b",
        ]
        for padrao in padroes:
            match_qtd = re.search(padrao, trecho)
            if match_qtd:
                return int(match_qtd.group(1))

    return None


def _verificar_duplicidades(
    texto: str,
    df: pd.DataFrame,
    relatorio_tecnico: dict[str, Any],
    alertas: list[dict[str, str]],
) -> None:
    duplicidades = _obter_duplicidades_dataframe(df)
    if not duplicidades:
        return

    # Valida duplicidades somente nas colunas declaradas como únicas nas
    # regras determinísticas. Repetições em nome/email, por exemplo, podem
    # ser legítimas e não devem ser tratadas como violação automaticamente.
    regras = relatorio_tecnico.get("regras_qualidade", {})
    violacoes = regras.get("violacoes", []) if isinstance(regras, dict) else []
    colunas_unicas = {
        str(item.get("coluna"))
        for item in violacoes
        if isinstance(item, dict)
        and str(item.get("regra", "")).lower() in {
            "valor_unico", "unicidade", "coluna_unica", "unique"
        }
        and item.get("coluna")
    }

    if colunas_unicas:
        duplicidades = {
            coluna: valores
            for coluna, valores in duplicidades.items()
            if coluna in colunas_unicas
        }
    else:
        # Sem regra explícita de unicidade, não presumimos que qualquer
        # repetição de valor seja um erro de qualidade.
        return

    if not duplicidades:
        return

    texto_norm = _normalizar(texto)

    for coluna, valores_reais in duplicidades.items():
        coluna_norm = _normalizar(coluna)

        # Não valida menções genéricas sem referência à coluna.
        if coluna_norm not in texto_norm:
            _adicionar_alerta(
                alertas,
                "DUPLICIDADES",
                f"A interpretação não menciona a coluna '{coluna}', "
                "que possui valores duplicados.",
            )
            continue

        ids_mencionados = _extrair_ids_duplicados_mencionados(texto, coluna)
        ids_reais = {str(info["valor"]).lower() for info in valores_reais.values()}

        ids_incorretos = ids_mencionados - ids_reais
        ids_omitidos = ids_reais - ids_mencionados

        if ids_incorretos or ids_omitidos:
            _adicionar_alerta(
                alertas,
                "DUPLICIDADES",
                f"Divergência de valores duplicados na coluna '{coluna}'. "
                f"Valores reais: {sorted(ids_reais)}. "
                f"Valores mencionados: {sorted(ids_mencionados)}. "
                f"Valores inventados: {sorted(ids_incorretos)}; "
                f"valores reais não confirmados: {sorted(ids_omitidos)}.",
            )

        linhas_reais = {
            linha
            for info in valores_reais.values()
            for linha in info["linhas_csv"]
        }
        linhas_mencionadas = _extrair_linhas_duplicidade(texto, coluna)

        if linhas_mencionadas and linhas_mencionadas != linhas_reais:
            _adicionar_alerta(
                alertas,
                "DUPLICIDADES",
                f"Linhas CSV incorretas para duplicidades em '{coluna}'. "
                f"Esperadas: {sorted(linhas_reais)}; "
                f"mencionadas: {sorted(linhas_mencionadas)}.",
            )

        quantidade_mencionada = _extrair_quantidade_duplicidade(texto, coluna)
        quantidade_real = sum(
            info["quantidade"] for info in valores_reais.values()
        )

        if (
            quantidade_mencionada is not None
            and quantidade_mencionada != quantidade_real
        ):
            _adicionar_alerta(
                alertas,
                "DUPLICIDADES",
                f"Quantidade de ocorrências divergente na coluna '{coluna}'. "
                f"Esperada: {quantidade_real}; "
                f"mencionada: {quantidade_mencionada}.",
            )

def validar_interpretacao_ia(
    interpretacao: str,
    relatorio_tecnico: dict[str, Any],
    df: pd.DataFrame | None = None,
) -> dict[str, Any]:
    """Valida a interpretação da IA contra fatos determinísticos."""

    alertas: list[dict[str, str]] = []

    if not interpretacao or not interpretacao.strip():
        _adicionar_alerta(
            alertas,
            "INTERPRETAÇÃO VAZIA",
            "A IA não retornou uma interpretação.",
        )
    else:
        texto_norm = _normalizar(interpretacao)

        secoes_ausentes = [
            secao
            for secao in SECOES_OBRIGATORIAS
            if _normalizar(secao) not in texto_norm
        ]

        if secoes_ausentes:
            _adicionar_alerta(
                alertas,
                "ESTRUTURA",
                "Seções obrigatórias ausentes: " + ", ".join(secoes_ausentes),
            )

        _verificar_severidade(interpretacao, relatorio_tecnico, alertas)
        _verificar_afirmacoes_de_correcao(interpretacao, alertas)

        if df is not None:
            _verificar_ausencias(interpretacao, df, alertas)
            _verificar_contagem_ausencias(interpretacao, df, alertas)
            _verificar_duplicidades(interpretacao, df, relatorio_tecnico, alertas)

    return {
        "status": "VALIDAÇÃO INICIAL APROVADA" if not alertas else "REVISÃO NECESSÁRIA",
        "total_alertas": len(alertas),
        "alertas": alertas,
        "observacao": (
            "A validação automatizada cobre verificações determinísticas "
            "limitadas e não substitui revisão humana."
        ),
    }


validar_interpretacao = validar_interpretacao_ia
