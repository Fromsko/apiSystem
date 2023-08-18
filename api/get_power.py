from fastapi import APIRouter, Query, Request

router = APIRouter(prefix="/api/v1")  # 创建一个带有前缀的路由器对象


@router.post('/search')
async def get_power(
        request: Request,
        house: str = Query(..., description="宿舍号"),
):
    """
    获取房间电费
    """
    host = request.client.host
    print(host)
    return {
        'message': 'Hello, get_power!',
        "house": house,
        "host": host,
    }
