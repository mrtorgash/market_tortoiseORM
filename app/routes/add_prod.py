from fastapi import APIRouter, File, UploadFile, Depends
from app.queries.product import add_prod_to_db, search_prod_from_db,delete_prod_from_db
from app.exceptions import UnAuthorized, ForbiddenError, InternalServerError, NotFoundError
from app.views.auth import SuccessfulResponse, BadPriceResponse
from app.views.prod import ProdIn, ProdOut, ProdSearch, ProdId
from app.queries.product import viewing_prod
from typing import List
from app.views import from_list_to_pydantic
from app.views.auth import SuccessfulResponse
from typing import Optional
from uuid import uuid4
from app.views.tortoise_model import Prod_Pydantic, Products, User_Pydantic, ProdIn_Pydantic
from tortoise.exceptions import ValidationError

prod_router = APIRouter(tags=['Функционал продуктов'])


@prod_router.post('/add', response_model=SuccessfulResponse)
async def addprod(prod: ProdIn_Pydantic = Depends(), file: Optional[UploadFile] = File(None)):
    file_path: Optional[str] = None
    if file is not None:
        file_format = file.filename.split(".")[-1]
        data = await file.read()
        file_name = str(uuid4()) + "." + file_format
        file_path = "static_directory/" + file_name
        with open(file_path,"wb+") as newfile:
            newfile.write(data)

    try:
        prod_obj = await Products.create(**prod.dict(exclude_unset=True),foto_loc = file_path) #########1111111111111111111111111111
        await Prod_Pydantic.from_tortoise_orm(prod_obj)
    except ValidationError as e:
        return BadPriceResponse()
    return SuccessfulResponse()


@prod_router.post('/search', response_model=List[Prod_Pydantic])  # возможно get?
async def getprod(product: ProdSearch):
    if product.name is not None and product.price is not None:
        from tortoise.expressions import Q
        prod_obj = Products.filter(Q(Q(name__icontains = product.name),Q(price__range = (product.price.price_from,product.price.price_to)))).all()
    elif product.name is not None:
        prod_obj = Products.filter(name__icontains = product.name).all()
    else:
        prod_obj = Products.filter(price__range = (product.price.price_from,product.price.price_to)).all()
    return await Prod_Pydantic.from_queryset(prod_obj)
    # if product.price is None:
    #     product = await search_prod_from_db(product.name + "%", None, None)
    # else:
    #     product = await search_prod_from_db(pro.name + "%", product.price.price_from, product.price.price_to)
    # return from_list_to_pydantic(product, ProdOut)


@prod_router.get('/viewing_product', response_model=List[ProdOut])
async def view_product():
    print(await Prod_Pydantic.from_queryset(Products.all()))
    return await Prod_Pydantic.from_queryset(Products.all())

@prod_router.delete('/delete_prod') #проблема в том, что я могу удалить то чего нет(надо ли выводить
# вообще такое сообщение)
async def delete_prod(prod_id : ProdId):
    await Products.filter(id=prod_id.id).delete()
    return "SuccessfulDelete"