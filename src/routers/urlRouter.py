from fastapi import FastAPI, APIRouter, Body, Request, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import HttpUrl
from .rateLimiter import limiter
from src.service import URLService
from src.utils.validationUtil import validate_url
app = FastAPI()
router = APIRouter(prefix="")

@router.post("/shorten")
@limiter.limit("10/second")
async def get_short_link(request: Request, url: HttpUrl = Body(..., embed=True)) -> dict:
    url_str = str(url)
    if not validate_url(url_str):
        raise HTTPException(status_code=404, detail="URL is not valid")
    print(f'url received: {url_str}')
    data = URLService().generate_short_link(url_str)
    response = {"status": "success", "data": data}
    return response

@router.get("/{short_link}")
async def redirect(request: Request, short_link: str):
    from src.dao.urlDao import UrlDao
    obj = UrlDao().get_long_url_by_shorten_value(short_link)
    if obj is None:
        raise HTTPException(status_code=404, detail="The link does not exist, could not redirect.")
    elif obj.expired:
        raise HTTPException(status_code=404, detail="The link expired")
    return RedirectResponse(url=obj.longUrl)
