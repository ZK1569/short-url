from fastapi import APIRouter, Depends

from ..services.url import UrlService, get_url_service

router = APIRouter(prefix="/admin", tags=["health"])


@router.get("/")
def get_all_url(
    url_service: UrlService = Depends(get_url_service),
):
    urls = url_service.get_all_urls()
    return {"data": urls}
