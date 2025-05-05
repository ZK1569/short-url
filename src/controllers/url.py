from typing import Dict

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

from ..errors.error import NotFound, UrlAlreadyShortened
from ..services.service import UrlServiceAbs
from ..services.url import get_url_service

router = APIRouter(prefix="/url", tags=["url"])


class NewUrlBody(BaseModel):
    long_url: str


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Dict[str, str])
async def create_url(
    body: NewUrlBody,
    url_service: UrlServiceAbs = Depends(get_url_service),
) -> Dict[str, str]:
    try:
        shortened = url_service.generate_url(body.long_url)
    except UrlAlreadyShortened as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        )
    return {"shortened_url": shortened}


@router.get("/{short_url}", response_class=RedirectResponse)
async def get_long_url(
    short_url: str,
    url_service: UrlServiceAbs = Depends(get_url_service),
) -> dict[str, str]:
    try:
        long_url = url_service.get_long_url_and_increment(short_url)
    except NotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    return RedirectResponse(url=long_url)
