
from datetime import datetime


# ============================================================
# PLANO DE TRATAMENTO DE DATA QUALITY
# ============================================================

def gerar_plano_tratamento(
    relatorio_regras: dict,
) -> dict:

    """
    Gera recomendações de tratamento para violações
    de Data Quality.

    Não modifica os dados originais.
    Não executa correções.
    """

    plano = []

    regras_violadas = relatorio_regras.get(
        "regras_violadas",
        [],
    )

    for regra in regras_violadas:

        nome_regra = regra["regra"]
        coluna = regra["coluna"]
        severidade = regra["severidade"]

        registros = regra.get(
            "registros_afetados",
            [],
        )

        # ----------------------------------------------------
        # Identificador duplicado
        # ----------------------------------------------------

        if nome_regra == "valor_unico":

            acao = (
                "Investigar os registros envolvidos e confirmar "
                "qual identificador deve ser mantido ou corrigido."
            )

            justificativa = (
                "A duplicidade viola a regra de unicidade "
                "configurada para a coluna."
            )

            aprovacao = True

        # ----------------------------------------------------
        # Campo obrigatório ausente
        # ----------------------------------------------------

        elif nome_regra == "campo_obrigatorio":

            acao = (
                "Consultar a fonte original para recuperar o valor. "
                "Se não for possível, avaliar uma política "
                "de tratamento de ausência."
            )

            justificativa = (
                "O campo foi definido como obrigatório "
                "nas regras de negócio."
            )

            aprovacao = True

        # ----------------------------------------------------
        # E-mail inválido
        # ----------------------------------------------------

        elif nome_regra == "formato_email":

            acao = (
                "Validar o endereço com a fonte responsável "
                "e corrigir somente após confirmação."
            )

            justificativa = (
                "O formato do e-mail não corresponde "
                "ao padrão esperado."
            )

            aprovacao = True

        # ----------------------------------------------------
        # Idade fora do intervalo
        # ----------------------------------------------------

        elif nome_regra == "intervalo_idade":

            acao = (
                "Verificar o valor na fonte original e confirmar "
                "se houve erro de entrada ou regra inadequada."
            )

            justificativa = (
                "A idade está fora do intervalo permitido "
                "pela regra configurada."
            )

            aprovacao = True

        # ----------------------------------------------------
        # Coluna obrigatória ausente
        # ----------------------------------------------------

        elif nome_regra == "coluna_obrigatoria":

            acao = (
                "Verificar o arquivo de origem e corrigir "
                "o esquema antes de prosseguir com o processamento."
            )

            justificativa = (
                "Uma coluna necessária para a análise "
                "não foi encontrada."
            )

            aprovacao = True

        # ----------------------------------------------------
        # Regra não reconhecida
        # ----------------------------------------------------

        else:

            acao = (
                "Investigar a violação e definir "
                "uma ação com o responsável pelos dados."
            )

            justificativa = (
                "A regra ainda não possui uma recomendação "
                "específica cadastrada."
            )

            aprovacao = True

        plano.append({

            "id_plano": len(plano) + 1,

            "regra": nome_regra,

            "coluna": coluna,

            "severidade": severidade,

            "quantidade_registros": regra["quantidade"],

            "registros_afetados": registros,

            "acao_recomendada": acao,

            "justificativa": justificativa,

            "requer_aprovacao_humana": aprovacao,

            "status": "PENDENTE",

        })

    return {

        "data_geracao": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),

        "total_acoes_recomendadas": len(plano),

        "acoes_pendentes": len(plano),

        "plano": plano,

    }
