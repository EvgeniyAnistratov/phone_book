from typing import Annotated

from fastapi import APIRouter, Query, status
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel, Field

from .redis_manager import RedisManager


phone_book_router = APIRouter(prefix="/phone-book", tags=["phone-book"])
PhoneQueryParam = Annotated[str, Query(pattern="^\\+?[1-9][0-9]{7,14}$", example="+79995554422")]


class Address(BaseModel):
    address: str


class PhoneAddress(Address):
    phone: str = Field(pattern="^\\+?[1-9][0-9]{7,14}$", examples=["+79995554422"])


class Message(BaseModel):
    message: str


@phone_book_router.get(
    "",
    responses={
        status.HTTP_200_OK: {"model": Address},
        status.HTTP_404_NOT_FOUND: {"model": None}
    },
)
async def read_row(phone: PhoneQueryParam):
    address = await RedisManager.get(phone)
    if address is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)

    return JSONResponse(content={"address": address.decode('utf-8')}, status_code=status.HTTP_200_OK)


@phone_book_router.post(
    "",
    responses={
        status.HTTP_201_CREATED: {"model": None},
        status.HTTP_409_CONFLICT: {"model": Message}
    },
)
async def create_row(phone_address: PhoneAddress):
    if await RedisManager.get(phone_address.phone):
        return JSONResponse(content={"message": "Such a phone already exists"}, status_code=status.HTTP_409_CONFLICT)

    await RedisManager.set(phone_address.phone, phone_address.address)
    return Response(status_code=status.HTTP_201_CREATED)


@phone_book_router.patch(
    "",
    responses={
        status.HTTP_200_OK: {"model": None},
        status.HTTP_404_NOT_FOUND: {"model": None}
    },
)
async def edit_row(phone: PhoneQueryParam, address: Address):
    if await RedisManager.get(phone) is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)

    await RedisManager.set(phone, address.address)
    return Response(status_code=status.HTTP_200_OK)


@phone_book_router.delete(
    "",
    responses={
        status.HTTP_204_NO_CONTENT: {"model": None},
        status.HTTP_404_NOT_FOUND: {"model": None}
    },
)
async def delete_row(phone: PhoneQueryParam):
    if await RedisManager.get(phone) is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)

    await RedisManager.delete(phone)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
