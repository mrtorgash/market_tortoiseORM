from typing import Optional

import tortoise.validators
from pydantic import validator
from tortoise.exceptions import ValidationError
from tortoise.models import Model
from tortoise import fields , models
from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator
from tortoise.validators import MinValueValidator

class Products(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    price = fields.IntField(validators=[MinValueValidator(0)])
    count = fields.IntField(validators=[MinValueValidator(0)],null=True)
    foto_loc = fields.CharField(max_length=255,null=True)
    followed_by: fields.ManyToManyRelation["Users"]
    class Meta:
        ordering = ["name"]
    class PydanticMeta:
        exclude = ["foto_loc"]

class Users(models.Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=255,unique=True)
    password = fields.CharField(max_length=255)
    follow: fields.ManyToManyRelation[Products] = fields.ManyToManyField("models.Products")


User_Pydantic = pydantic_model_creator(Users, name ='user')
UserIn_Pydantic = pydantic_model_creator(Users, name="UserIn", exclude_readonly=True)
Prod_Pydantic = pydantic_model_creator(Products, name ='prod')
ProdIn_Pydantic = pydantic_model_creator(Products,name = "ProdIn",exclude_readonly=True)



