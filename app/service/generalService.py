from datetime import datetime
from typing import Collection, Type
from uuid import uuid4
from fastapi import HTTPException, status
from app.utils.general import exception_message, general_response, general_search


async def general_index(collection_db:Collection, repo:Type, entity: dict, 
                        searchByTitle:str="" ,page:int = 0, limit:int = 0, condition:str=''):
    table_name = collection_db.__tablename__
    search = ""
    if searchByTitle:
        searchTitle = {"filter[title]" : searchByTitle}
        search = general_search(searchTitle)
    try:
        res, total = await repo.getAll(table_name, page, limit, search, condition)
        res = entity(res)
        return await general_response("success", res, total, page)
    except Exception as e:
        return exception_message(e)


async def general_get_by_id(id:str,collection_db:Collection, repo:Type, entity:dict):
    try:
        tb_name = collection_db.__tablename__
        res = await repo.getById(id, tb_name)
        if not res:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Data not found!")
        res = entity(res)
        return await general_response("success", res)
    except Exception as e:
        return exception_message(e)

async def general_delete(id:str, collection_db:Collection, repo:Type):
    try:
        tb_name = collection_db.__tablename__
        get_by_id = await repo.getById(id, tb_name)
        if not get_by_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Data not found!")
        res = await repo.delete(id, tb_name)
        return await general_response(res)
    except Exception as e:
        return exception_message(e)
    
async def general_update(id:str, collection_db:Collection,repo:type, session:Type, 
                         payload:Type):
    tb_name = collection_db.__tablename__
    get_by_id = await repo.getById(id, tb_name)
    if not get_by_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Data not found!")
    try:
        new_data = payload.dict(exclude_unset=True)
    except:
        new_data = payload
        pass
    if 'nominal' in new_data:
        new_data['saldo'] = new_data['nominal']
        del new_data["nominal"]
    # dt_now_mills = int(round(datetime.utcnow().timestamp() * 1000))
    # payload.updated_at =  dt_now_mills

    res = await repo.update(session, get_by_id.id, new_data)
    return await general_response(res, current_page=0)

# async def general_bulk_update(ids: list, collection_db: Collection, repo: type,
#                               session: AsyncSession, payload: Type):
#     tb_name = collection_db.__tablename__

#     entities = await repo.get_entities_by_ids(ids, tb_name)
    
#     if not entities:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"Data not found!")
#     try:
#         new_data = payload.dict(exclude_unset=True)
#     except:
#         new_data = payload
#         pass
    
#     if 'nominal' in new_data:
#         new_data['saldo'] = new_data['nominal']
#         del new_data["nominal"]
    
#     stmt = (
#         update(collection_db)
#         .where(collection_db.c.id.in_(ids))
#         .values(new_data)
#     )

#     await session.execute(stmt)

#     await session.commit()
#     return await general_response("Bulk update successful", current_page=0)

async def general_create(collection_db:Type, repo:Type, user_id:str,
                          session:Type, payloads:Type, is_user:bool=False, 
                          user_db:Type=None):
    try:
        _create_id = str(uuid4())
        dt_now_mills = int(round(datetime.utcnow().timestamp() * 1000))
        new_data_obj = []
        for payload in payloads:
            if is_user:
                tb_name = user_db.__tablename__
                user = await repo.getById(user_id, tb_name)
                payload.username = user.username
                payload.user_id = user_id
            payload.id = _create_id
            payload.created_at = dt_now_mills
            payload.updated_at = dt_now_mills
            new_data_obj.append(collection_db(**payload.dict()))
        res = await repo.bulkCreate(session, new_data_obj)
        return await general_response(res, current_page=0)
    except Exception as e:
        return exception_message(e)