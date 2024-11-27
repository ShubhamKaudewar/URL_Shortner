from pydantic import BaseModel


class ShortURL(BaseModel):
    shortUrl: str
    longUrl: str
    createTime: int
    expiry: int
    expired: bool
    counter: int

