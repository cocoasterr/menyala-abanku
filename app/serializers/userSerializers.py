def userEntity(user: dict) -> dict:
    """maping value from database

    Args:
        user (dict): entity schema

    Returns:
        dict: get field database
    """
    return {
        "id": user.id,
        "nomor_rekening": user.nomor_rekening,
    }
def userSaldoEntity(user: dict) -> dict:
    """maping value from database

    Args:
        user (dict): entity schema

    Returns:
        dict: get field database
    """
    return {
        "id": user.id,
        "nomor_rekening": user.nomor_rekening,
        "saldo": user.saldo,
    }


def getMeResponseEntity(user:dict) ->dict:
    return {
        "id": user['id'],
        "nomor_rekening": user['nomor_rekening'],
        "pin": user['pin'],
        "saldo": user['saldo'],
    }


def userResponseEntity(user: dict) -> dict:
    """this function used for response entity

    Args:
        user (dict): entity schema


    Returns:
        dict: field database
    """
    return {
        "id": user.id,
        "nomor_rekening": user.nomor_rekening,
        "phone_number": user.phone_number,
        "nik": user.nik,
        "pin": user.pin,
        "saldo": user.saldo,
    }

def userCreateResponseEntity(user: dict) -> dict:
    """this function used for response entity

    Args:
        user (dict): entity schema


    Returns:
        dict: field database
    """
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
    }


def userListEntity(users: list) -> list:
    """response when data need to mapping is morethan one

    Args:
        users (list): list entities schema

    Returns:
        list: get list field from database
    """
    return [userEntity(user) for user in users]
