from uuid import uuid4
from fastapi import HTTPException, status
from app.utils.general import exception_message, general_response
from typing import Collection, Type
from app.service.generalService import general_update
from datetime import datetime
from app.repository.mutationRepo import mutationRepo
from app.database import db


async def insert_mutation(session:type, code_transaction:str, nomor_rekening:str, nominal:int):
    try:
        _id = str(uuid4())

        mutation = {
            'id': _id,
            'nomor_rekening': nomor_rekening,
            'transaction_code': code_transaction,
            'time':f'{datetime.now()}',
            'nominal': f'{nominal}'
        }
        await mutationRepo.create(session, **mutation)
    except Exception as e:
        return exception_message(e)



async def serviceTarik(id: str, collection_db: Collection, repo: type, 
                       session: Type, payload: Type, entity:dict):

    try:
        new_data = payload.dict(exclude_unset=True)
        if new_data['nominal'] < 50_000:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='nominal must more than Rp.50000!')
        tb_name = collection_db.__tablename__

        user = await repo.getById(id, tb_name)
        res_user = entity(user)
        if not res_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='User not found!')
        nominal = new_data['nominal']

        if res_user['saldo'] < nominal:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='Your balance is insufficient!')
        payload.nominal = res_user['saldo'] - nominal

        await insert_mutation(session, 'D', res_user['nomor_rekening'], nominal)

        return await general_update(id, collection_db, repo, session, payload)

    except Exception as e:
        return exception_message(e)
    
async def serviceTabung(id: str, collection_db: Collection, repo: type, 
                       session: Type, payload: Type, entity:dict):

    try:
        new_data = payload.dict(exclude_unset=True)
        if new_data['nominal'] < 25_000:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='nominal must more than Rp.25000!')

        tb_name = collection_db.__tablename__

        user = await repo.getById(id, tb_name)
        res_user = entity(user)
        if not res_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='User not found!')
        
        payload.nominal = res_user['saldo'] + new_data['nominal']
        nominal = new_data['nominal']
        await insert_mutation(session, 'C', res_user['nomor_rekening'], nominal)

        return await general_update(id, collection_db, repo, session, payload)

    except Exception as e:
        return exception_message(e)
    
async def servicetransfer(id: str, collection_db: Collection, repo: type, 
                       session: Type, payload: Type, entity:dict):
    async def findUser(no_rek:str, ) -> dict:
        condition = f"WHERE nomor_rekening = '{no_rek}'"
        res = await repo.generalGetBy(tb_name, condition)
        if not res:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='User not found!')
        return entity(res)
    try:
        new_data = payload.dict(exclude_unset=True)
        if new_data['nominal'] < 1:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='nominal must more than 0!')
        rek_from = new_data['nomor_rekening_from']
        rek_dest = new_data['nomor_rekening_dest']

        tb_name = collection_db.__tablename__

        from_data = await findUser(rek_from)
        if from_data['saldo'] < new_data['nominal']:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                detail='Your balance is insufficient!')
        
        dest_data = await findUser(rek_dest)

        from_data['saldo'] = from_data['saldo'] - new_data['nominal']
        dest_data['saldo'] = dest_data['saldo'] + new_data['nominal']
        
        await repo.bulk_update(session,[from_data, dest_data])

        await insert_mutation(session, 'T', from_data['nomor_rekening'], new_data['nominal'])
        await insert_mutation(session, 'U', dest_data['nomor_rekening'], new_data['nominal'])
        
        return {'status': 'success!'}

    except Exception as e:
        return exception_message(e)

async def serviceSaldo(id: str,collection_db: Collection, repo: Type, entity: dict):
    tb_name = collection_db.__tablename__
    res = await repo.getById(id, tb_name)
    if not res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Data not found!")
    res = entity(res)
    msg = f"your balance is {res['saldo']}"
    return await general_response(msg, current_page=0)

async def serviceMutation(collection_db: Collection, repo: Type, entity: dict, searchByTitle: str = "",
                        page: int = 0, limit: int = 0, user_id:str = '', 
                        collection_user:Collection=None,repo_user:type=None, entity_user:dict={})->dict:
    tb_name = collection_user.__tablename__
    user = await repo_user.getById(user_id, tb_name)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Data not found!")
    user = entity_user(user)
    tb_name_mutation = collection_db.__tablename__
    offset = (page - 1) * limit
    condition = f"WHERE nomor_rekening = '{user['nomor_rekening']}'"
    query = f"SELECT * FROM {tb_name_mutation} {searchByTitle} {condition} ORDER BY time DESC LIMIT {limit} OFFSET {offset}"
    DB = await db.conn()

    res = DB.exec_driver_sql(query).all()
    
    query_total = f"SELECT COUNT(id) FROM {tb_name_mutation}"
    total = DB.exec_driver_sql(query_total).scalar()

    result_list_of_dicts = [{'id': item[0], 'nomor_rekening': item[1], 'transaction_type': item[2], 'time': item[3], 'nominal': item[4]} for item in res]

    return await general_response("success", result_list_of_dicts, total, page)
    