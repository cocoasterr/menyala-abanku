import pandas as pd
from datetime import date
from fastapi import APIRouter, Depends, Request, Query
from app.schemas.schemasTransaction import TransactionTabung, TransactionTarik, TransactionTransfer
from app.database import get_db
from sqlalchemy.orm import Session
from app.service.transaction import serviceTabung, serviceTarik, servicetransfer, serviceSaldo, serviceMutation
from app.oauth import require_user
from app.models.mutation import Mutation
from app.models.users import Users
from app.serializers.transactionSerializers import transactionEntity
from app.serializers.mutationSerializers import mutationListEntity
from app.serializers.userSerializers import userEntity, userSaldoEntity
from app.repository.userRepository import userRepo
from app.repository.mutationRepo import mutationRepo
from fastapi.responses import StreamingResponse
from io import BytesIO
from app.database import db

router = APIRouter()


@router.put('/tabung')
async def tabung(payload:TransactionTabung,
                session: Session = Depends(get_db),
                 user_id: str = Depends(require_user)) -> dict:
    return await serviceTabung(user_id, Users, userRepo, session, payload, transactionEntity)

@router.put('/tarik')
async def tarik(payload:TransactionTarik,
                session: Session = Depends(get_db),
                user_id: str = Depends(require_user)) -> dict:
    return await serviceTarik(user_id, Users, userRepo, session, payload, transactionEntity)

@router.put('/transfer')
async def transfer(payload:TransactionTransfer,
                session: Session = Depends(get_db),
                user_id: str = Depends(require_user)) -> dict:
    return await servicetransfer(user_id, Users, userRepo, session, payload, transactionEntity)

@router.get('/saldo')
async def get_saldo(session: Session = Depends(get_db),
                   user_id: str=Depends(require_user)) -> dict:
    return await serviceSaldo(user_id, Users, userRepo, userSaldoEntity)

@router.get('/mutation')
async def mutation(request: Request,
                   searchByTitle: str = '',
                   page: int = Query(default=1, gt=0),
                   limit: int = Query(default=10, gt=0),
                   session: Session = Depends(get_db),
                   user_id: str = Depends(require_user)):
    return await serviceMutation(Mutation, mutationRepo, mutationListEntity, searchByTitle,
                                    page, limit, user_id, Users, userRepo, userEntity)

@router.get('/download-excel')
async def download_excel(request: Request, session: Session = Depends(get_db),
                         user_id: str = Depends(require_user)):
    def to_excel(data: list, filename: str):
        df = pd.DataFrame(data)
        excel_file_path = f'{filename}.xlsx'
        df.to_excel(excel_file_path, index=False)
        return excel_file_path  

    date_now = date.today()
    query = f"""
    SELECT
        COUNT(id) AS total_transaksi,
        SUM(CASE WHEN transaction_code = 'D' THEN CAST(nominal AS integer) ELSE 0 END) AS total_nominal_tarik,
        SUM(CASE WHEN transaction_code = 'C' THEN CAST(nominal AS integer) ELSE 0 END) AS total_nominal_setor,
        SUM(CASE WHEN transaction_code = 'T' THEN CAST(nominal AS integer) ELSE 0 END) AS total_nominal_transfer
    FROM mutation
    WHERE time BETWEEN '{date_now} 00:00:00' AND '{date_now} 23:59:59'
    """
    DB = await db.conn()
    data = DB.exec_driver_sql(query).all()

    excel_file_path = to_excel(data, "data")
    excel_data = BytesIO()

    with open(excel_file_path, "rb") as file:
        excel_data.write(file.read())

    excel_data.seek(0)

    return StreamingResponse(content=excel_data, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", 
                             headers={"Content-Disposition": "attachment; filename=data.xlsx"})
