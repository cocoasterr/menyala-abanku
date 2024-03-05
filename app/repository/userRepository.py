from app.models.users import Users
from app.repository.BaseRepo import BaseRepo
from app.database import db

class userRepo(BaseRepo):
    model = Users

    @staticmethod
    async def findUser(phone_number:str = None, nik:str = None):
        query = f"SELECT * FROM users WHERE phone_number='{phone_number}'"
        if nik:
            query += f" OR nik = '{nik}' "
        DB = await db.conn()
        res = DB.exec_driver_sql(query).one_or_none()
        return res
    
    @staticmethod
    async def findUserLogin(nomor_rekening:str, pin:str):
        try:
            query = f"SELECT * FROM users WHERE nomor_rekening='{nomor_rekening}' AND Pin='{pin}'"
            DB = await db.conn()
            res = DB.exec_driver_sql(query).one_or_none()
            return res
        except Exception as e:
            query = f"SELECT * FROM users WHERE nomor_rekening='{nomor_rekening}' AND Pin='{pin}'"
            DB = await db.conn()
            res = DB.exec_driver_sql(query).one_or_none()
            return res

    