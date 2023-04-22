from typing import Optional, Mapping, Any

from pydantic import BaseSettings, PostgresDsn, validator


class Backend(BaseSettings):
    DB_USER: str = 'postgres'
    DB_PASSWORD: str = 'postgres'
    DB_HOST: str = '127.0.0.1'
    DB_DATABASE: str = 'market'

    DB_URL: PostgresDsn = None



    SECRET_KEY = "ASFAFDSsdfsagdsgdagdf"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 1 #в минутах


    @validator("DB_URL", pre=True)
    def assemble_postgres_url(cls, v: Optional[str], values: Mapping[str, Any]) -> str:
        if v is not None and isinstance(v, str):
            return v
        return str(
            PostgresDsn.build(
                scheme="postgresql",
                user=values['DB_USER'],
                password=values['DB_PASSWORD'],
                host=values['DB_HOST'],
                port="5432",
                path=f'/{values["DB_DATABASE"]}'
            )
        )


settings = Backend()
