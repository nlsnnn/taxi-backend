from pydantic import BaseModel
from typing import List, Optional, Type, TypeVar

from sqlalchemy import func, update as alchemy_update, delete as alchemy_delete
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import Base


T = TypeVar("T", bound=Base)


class BaseCRUD:
    model: Type[T] = None

    @classmethod
    async def find_all(cls, session: AsyncSession, filters: Optional[BaseModel] = None):
        stmt = select(cls.model).filter_by(**cls._get_model_dict(filters))
        result = await session.execute(stmt)
        return result.scalars().all()

    @classmethod
    async def get_paginated(
        cls,
        session: AsyncSession,
        filters: Optional[BaseModel] = None,
        skip: int = 0,
        limit: int = 50,
    ):
        stmt = (
            select(cls.model)
            .filter_by(**cls._get_model_dict(filters))
            .offset(skip)
            .limit(limit)
        )
        result = await session.execute(stmt)

        items = result.scalars().all()
        total = await session.scalar(select(func.count()).select_from(cls.model))
        return items, total

    @classmethod
    async def find_one_or_none(
        cls, session: AsyncSession, filters: Optional[BaseModel] = None
    ):
        stmt = select(cls.model).filter_by(**cls._get_model_dict(filters))
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    @classmethod
    async def find_one_or_none_by_id(cls, session: AsyncSession, data_id: int):
        stmt = select(cls.model).filter_by(id=data_id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    @classmethod
    async def add(cls, session: AsyncSession, values: BaseModel):
        instance = cls.model(**cls._get_model_dict(values, True))
        session.add(instance)
        await session.commit()
        await session.refresh(instance)
        return instance

    @classmethod
    async def add_many(cls, session: AsyncSession, instances: List[BaseModel]):
        values_list = [item.model_dump(exclude_unset=True) for item in instances]
        new_instances = [cls.model(**values) for values in values_list]
        session.add_all(new_instances)
        await session.commit()
        return new_instances

    @classmethod
    async def update(cls, session: AsyncSession, filters: BaseModel, values: BaseModel):
        filter_values = cls._get_model_dict(filters, True)
        values_list = cls._get_model_dict(values, True)
        query = (
            alchemy_update(cls.model)
            .where(*[getattr(cls.model, k) == v for k, v in filter_values.items()])
            .values(**values_list)
        )
        result = await session.execute(query)
        await session.commit()
        return result.rowcount

    @classmethod
    async def delete(cls, session: AsyncSession, filters: BaseModel):
        filter_values = cls._get_model_dict(filters, True)
        query = alchemy_delete(cls.model).filter_by(**filter_values)
        result = await session.execute(query)
        await session.commit()
        return result.rowcount

    @staticmethod
    def _get_model_dict(schema: Optional[BaseModel] = None, required=False):
        if required:
            return schema.model_dump(exclude_unset=True)

        return schema.model_dump(exclude_unset=True) if schema else {}
