# -*- coding: utf-8 -*-
"""
    @File  : main.py
    @Date  : 2023-07-02 02:42:30
    @notes : 菜单页面挂载
"""
from router.base_router import site as engine
from router.base_setting import base_api
from views.api_view import APISettings, APIDocAdmin
from views.home_view import HomeAdmin

# 注册页面
engine.register_admin(
    HomeAdmin,    # 主页面
    APISettings,  # API 管理
    APIDocAdmin,  # API 测试
)

# 挂载路由
engine.mount_app(base_api)

if __name__ == '__main__':
    import uvicorn

    uvicorn.run("main:base_api", host="localhost", port=8000, reload=True)
