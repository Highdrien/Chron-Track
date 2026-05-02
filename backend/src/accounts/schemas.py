import uuid

from ninja import Schema


class RegisterIn(Schema):
    username: str
    password: str
    email: str = ""


class TokenPairOut(Schema):
    access: str
    refresh: str


class UserOut(Schema):
    id: uuid.UUID
    username: str
    email: str


class ErrorOut(Schema):
    detail: str
