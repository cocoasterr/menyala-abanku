from pydantic import BaseModel, constr

class UserBaseSchema(BaseModel):
    nomor_rekening: str

    class Config:
        orm_mode = True


class CreateUserSchema(BaseModel):
    nik: constr(min_length=16)
    pin: constr(min_length=6)
    phone_number: str


    class Config:
        schema_extra = {
            "example": {
                "nik": "3672829393888885",
                "phone_number": "+6281232142168741",
                "pin": "123412"
            }
        }

class LoginUserSchema(UserBaseSchema, BaseModel):
    pin: str

    class Config:
        schema_extra = {
            "example": {
                "nomor_rekening": "123123123",
                "pin": "123412"
            }
        }
