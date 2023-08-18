from router.base_router import base_api

# 导入路由信息
from .get_power import router as router_0
from .history_today import router as router_1
from .get_class_table import router as router_2
from .get_onesay import router as router_3
from .api_test_demo import router as router_4



# 创建路由
base_api.include_router(router_0)
base_api.include_router(router_1)
base_api.include_router(router_2)
base_api.include_router(router_3)
base_api.include_router(router_4)

