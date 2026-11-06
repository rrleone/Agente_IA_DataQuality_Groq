
import pandas as pd

from src.regras_qualidade import validar_regras


def test_identifica_id_cliente_duplicado():

    df = pd.DataFrame({
        "id_cliente": [1, 2, 2, 3],
        "nome": ["Ana", "Bruno", "Bruno", "Carlos"],
        "idade": [28, 35, 35, 40],
        "email": [
            "ana@email.com",
            "bruno@email.com",
            "bruno@email.com",
            "carlos@email.com",
        ],
    })

    resultado = validar_regras(df)

    regras = resultado["regras_violadas"]

    regra_id = [
        regra
        for regra in regras
        if regra["regra"] == "valor_unico"
    ]

    assert len(regra_id) == 1
    assert regra_id[0]["coluna"] == "id_cliente"
    assert regra_id[0]["quantidade"] == 2


def test_identifica_email_invalido():

    df = pd.DataFrame({
        "id_cliente": [1, 2],
        "nome": ["Ana", "Bruno"],
        "idade": [28, 35],
        "email": ["ana@email.com", "email_invalido"],
    })

    resultado = validar_regras(df)

    regras = resultado["regras_violadas"]

    regra_email = [
        regra
        for regra in regras
        if regra["regra"] == "formato_email"
    ]

    assert len(regra_email) == 1
    assert regra_email[0]["quantidade"] == 1


def test_identifica_idade_fora_do_intervalo():

    df = pd.DataFrame({
        "id_cliente": [1, 2],
        "nome": ["Ana", "Bruno"],
        "idade": [-5, 35],
        "email": ["ana@email.com", "bruno@email.com"],
    })

    resultado = validar_regras(df)

    regras = resultado["regras_violadas"]

    regra_idade = [
        regra
        for regra in regras
        if regra["regra"] == "intervalo_idade"
    ]

    assert len(regra_idade) == 1
    assert regra_idade[0]["quantidade"] == 1


def test_base_sem_violacoes():

    df = pd.DataFrame({
        "id_cliente": [1, 2],
        "nome": ["Ana", "Bruno"],
        "idade": [28, 35],
        "email": ["ana@email.com", "bruno@email.com"],
    })

    resultado = validar_regras(df)

    assert resultado["total_regras_violadas"] == 0
    assert resultado["total_ocorrencias"] == 0
