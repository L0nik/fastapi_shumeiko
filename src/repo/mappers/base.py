from typing import TypeVar
from src.database import BaseModel as ModelORM
from pydantic import BaseModel

SchemaType = TypeVar("SchemaType", bound=BaseModel)
DBModelType = TypeVar("DBModelType", bound=ModelORM)

class DataMapper:

    db_model: type[DBModelType] = None
    schema: type[SchemaType] = None

    @classmethod
    def map_to_domain_entity(cls, data):
        return cls.schema.model_validate(data, from_attributes=True)

    @classmethod
    def map_to_persistance_entity(cls, data):
        return cls.db_model(**data.model_dump())