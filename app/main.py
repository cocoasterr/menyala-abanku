import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import db
from app.controllers import auth, transaction

origins= [
    "http://localhost:3000"
]
def init_app():

    app = FastAPI(
        title= "Menyala aBANKu",
        description= "tetap ilmu padi",
        version= "1"
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

    @app.on_event("startup")
    async def starup():
        db.init()
        await db.conn()
    

    app.include_router(auth.router,tags=['Auth'],prefix='/api/user')
    app.include_router(transaction.router,tags=['Transaction'],prefix='/api/transaction')

    return app

app = init_app()

def start():
    # """Launched with 'poetry run start' at root level"""
    uvicorn.run("app.main:app", host="localhost", port=8888, reload=True)



    # lala = ''''
    # https://www.ferizy.com/order/checkout

    # cart_id: f582c100-33ee-48a6-8e57-dfa5dc6c0330
    # customer_name: Ridho Maulana Prastian
    # phone: 082132443692
    # email: ridhompra@gmail.com
    # cc_email: ridhomp29@gmail.com
    # no_police: 
    # gender[adult][0]: 1
    # name[adult][0]: RIDHO
    # id_type[adult][0]: 1
    # nationality[adult][0]: 
    # id_number[adult][0]: 1233212345323453
    # age[adult][0]: 22
    # city[adult][0]: kab. aceh jaya
    
    # '''