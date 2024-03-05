from pydantic import BaseModel, constr

class TransactionBaseSchema(BaseModel):
    nomor_rekening: str

    class Config:
        orm_mode = True


class TransactionTabung(BaseModel):
    nomor_rekening: constr(min_length=10)
    nominal: int
    pin: str


    class Config:
        schema_extra = {
            "example": {
                "nomor_rekening": "5664677696",
                "nominal": 1_000_000,
                "pin": "123412"
            }
        }

class TransactionTarik(TransactionTabung, BaseModel):

    class Config:
        schema_extra = {
            "example": {
                "nomor_rekening": "5664677696",
                "nominal": 1_000_000,
                "pin": "123412"
            }
        }

class TransactionTransfer(BaseModel):
    nomor_rekening_from: constr(min_length=10)
    nomor_rekening_dest: constr(min_length=10)
    nominal: int
    pin: str

    class Config:
        schema_extra = {
            "example": {
                "nomor_rekening_from": "5664677696",
                "nomor_rekening_dest": "5345440602",
                "nominal": 1_000_000,
                "pin": "123412"
            }
        }
