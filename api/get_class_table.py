from fastapi import APIRouter, Form, Request, Response
from fastapi.responses import FileResponse
from api.cname import cname_spider, cname_search

router = APIRouter(prefix="/api/v1")  # 创建一个带有前缀的路由器对象


@router.post('/classTable')
async def get_class_table(
    request: Request,
    cname: str = Form(...),
    week: str = Form(default=None),
    weekly: str = Form(default='')
):
    """
    获取课表数据
    """
    # 实现你的接口逻辑

    config_ = cname_spider.search_kb_info(
        cname=cname, week=week, weekly=weekly
    )

    if config_['error'] is not None:
        config_['client_ip'] = request.client.host
        return config_

    img_path = config_['data']

    return FileResponse(img_path, media_type="image/jpeg")


@router.post('/search_cname')
async def search_cname(
    request: Request,
    cname: str = Form(default='学前教育4班'),
    year: str = Form(default='2022'),
):
    if (result := cname_search.search(cname, year)) is not None:
        return {"code": 200, "result": result}
    return {"code": 302, "result": None}
