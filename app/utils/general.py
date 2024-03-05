from passlib.context import CryptContext
from fastapi import (HTTPException, status)


async def general_response(
        status: str,
        data: list = [],
        total: int = 0,
        current_page: int = 1) -> dict:
    """
    helping all function response

    Args:
        status (str): status code
        data (list): data
        total (int, optional): total data from database. Defaults to 0.
        current_page (int, optional): page pagination. Defaults to 1.
        message (str, optional): response message. Defaults to None.

    Returns:
        dict: dict {status, data, message, total, and current_pag}
    """
    res = {
        "status": status,
    }
    if data:
        res['data'] = data
    if total:
        res['total'] = total
    if current_page:
        res['current_page'] = current_page
    return res

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def hash_password(password: str) -> str:
    """Helper function to hashing the password

    Args:
        password (str): Actuall password from user

    Returns:
        str: Hashed password
    """
    return pwd_context.hash(password)


def exception_message(e):
    message = e
    if isinstance(e, HTTPException):
        message = e.detail
    raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                        detail=f'Failed! {message}')

async def verify_password(password: str, hashed_password: str) -> bool:
    """Check if password from user is match with hashed password or not

    Args:
        password (str): Actual password from user
        hashed_password (str): Hashed password

    Returns:
        bool: True/False
    """
    return pwd_context.verify(password, hashed_password)


def general_search(params):
    query_search = []
    for k, v in params.items():
        search_field = str(k).replace('filter[', '').replace(']', '')
        if search_field in ['page', 'limit']:
            continue
        if search_field in ["start_date", "end_date"]:
            if search_field == 'start_date':
                date_start = int(v)
            elif search_field == 'end_date':
                date_end = int(v)
            if date_start and date_end:
                statement_query = f" created_on >= {date_start} AND created_on <= {date_end} "
        else:
            statement_query = f" LOWER({search_field}) LIKE '%%{str(v).lower()}%%' "
        query_search.append(statement_query)
    final_query_statement = ''
    if query_search:
        final_query_statement = f" WHERE {'AND'.join(query_search)} "
    return final_query_statement