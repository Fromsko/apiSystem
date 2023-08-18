from fastapi import APIRouter

router = APIRouter(prefix="/api/v1")  # 创建一个带有前缀的路由器对象


@router.get('/api_test')
async def api_test_demo():
    """
    测试接口增加
    """
    # 实现你的接口逻辑
    return {'message': 'Hello, api_test_demo!'}
