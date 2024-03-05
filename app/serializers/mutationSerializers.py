def mutationEntity(mutation: dict) -> dict:
    """maping value from database

    Args:
        mutation (dict): entity schema

    Returns:
        dict: get field database
    """
    return {
        "id": mutation.id,
        "transaction_code": mutation.transaction_code,
        "time": mutation.time,
        "nominal": mutation.nominal
    }


def mutationResponseEntity(mutation: dict) -> dict:
    """this function used for response entity

    Args:
        mutation (dict): entity schema


    Returns:
        dict: field database
    """
    return {
        "id": mutation.id,
        "transaction_code": mutation.transaction_code,
        "time": mutation.time,
        "nominal": mutation.nominal
    }

def mutationListEntity(mutations: list) -> list:
    """response when data need to mapping is morethan one

    Args:
        mutations (list): list entities schema

    Returns:
        list: get list field from database
    """
    return [mutationEntity(mutation) for mutation in mutations]
