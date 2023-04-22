from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse
from tortoise.contrib.fastapi import register_tortoise

from app.exceptions import APIexception
from app.routes.auth import auth_router
from app.routes.add_prod import prod_router
from app.servecise.database import DB
from app.routes.follow import follow_router
from fastapi.staticfiles import StaticFiles

app = FastAPI(title='Login playground')
app.mount("/static", StaticFiles(directory="static_directory"), name="static")

@app.on_event('startup')
async def fastapi_startup():
    print('Hello')
    await DB.connect_db()


@app.on_event('shutdown')
async def fastapi_shutdown():
    await DB.disconnect_db()


@app.exception_handler(APIexception)
async def handle_exception(request: Request, exc: APIexception):
    print(exc.debug)
    return JSONResponse(
        status_code= exc.status_code,
        content= {
            "status_code": exc.status_code,
            "message": exc.message
        }
    )

app.include_router(auth_router)
app.include_router(prod_router)
app.include_router(follow_router)


register_tortoise(
    app,
    db_url="postgres://postgres:postgres@localhost:5432/market_new",
    modules={"models": ["app.views.tortoise_model"]},
    generate_schemas=True,
    add_exception_handlers=True,
)


#идея как сделать фото товара