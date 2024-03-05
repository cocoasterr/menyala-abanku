def transactionEntity(transaction: dict) -> dict:
    """maping value from database

    Args:
        transaction (dict): entity schema

    Returns:
        dict: get field database
    """
    return {
        "id": transaction.id,
        "nomor_rekening": transaction.nomor_rekening,
        "saldo": transaction.saldo
    }


def transactionResponseEntity(transaction: dict) -> dict:
    """this function used for response entity

    Args:
        transaction (dict): entity schema


    Returns:
        dict: field database
    """
    return {
        "id": transaction.id,
        "nomor_rekening": transaction.nomor_rekening,
        "phone_number": transaction.phone_number,
        "nik": transaction.nik,
        "pin": transaction.pin,
        "saldo": transaction.saldo,
    }

def transactionListEntity(transactions: list) -> list:
    """response when data need to mapping is morethan one

    Args:
        transactions (list): list entities schema

    Returns:
        list: get list field from database
    """
    return [transactionEntity(transaction) for transaction in transactions]
