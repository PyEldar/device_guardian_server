from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class PairingCode(BaseModel):
    pairing_code: str


class TokenPayload(BaseModel):
    sub: str
