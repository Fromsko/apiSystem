from fastapi import APIRouter, Request, Response, Query
from api.one_say import one_say_spider as spider

router = APIRouter(prefix="/api/v1")  # 创建一个带有前缀的路由器对象


@router.get('/onesay')
async def get_onesay(
    request: Request,
    limit: str = Query("1", description="查询数量")
):
    """
    本地化每日一言
    """
    # 获取请求者地址
    client_ip: str = request.client.host
    json_return = {}

    if int(limit) > 1:
        # 格式化返回
        for limit_cont in range(1, int(limit)+1):
            json_return[limit_cont] = await spider.one_say_api(
                client_ip=client_ip
            )

        return json_return
    return (await spider.one_say_api(client_ip))
