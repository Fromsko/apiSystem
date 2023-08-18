# -*- coding: utf-8 -*-
"""
    @File  : base_router.py
    @Date  : 2023-07-02 02:38:15
    @notes : 路由基础信息
"""
from pathlib import Path

from fastapi import FastAPI, Request, Response
from fastapi.responses import RedirectResponse
from fastapi_amis_admin.admin.settings import Settings
from fastapi_user_auth.site import AuthAdminSite
from sqlmodel import SQLModel
from starlette.requests import Request

work_dir = Path(__file__).parents[1]
base_api = FastAPI(redoc_url='/')

db_local = work_dir.joinpath("db", "amisadmin.db")
config = Settings(
    database_url_async=f'sqlite+aiosqlite:///{db_local}',
)
config.site_title = "接口服务平台"
config.site_icon = work_dir / "res" / "logo.png"
site = AuthAdminSite(settings=config)

auth = site.auth


@base_api.on_event("startup")
async def startup():
    await site.db.async_run_sync(
        SQLModel.metadata.create_all,
        is_session=False
    )
    await auth.create_role_user('admin')
    await auth.create_role_user('vip')


@base_api.get("/auth/get_user", include_in_schema=False)
@auth.requires()
def get_user(request: Request):
    return request.user


@base_api.exception_handler(404)
async def redirect_to_login(request: Request, exc: Exception):
    # 重定向到主页面
    return RedirectResponse(url="/admin")
