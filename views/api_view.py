# -*- coding: utf-8 -*-
"""
    @File  : view.py
    @Date  : 2023-07-02 20:31:06
    @notes : 视图函数
"""
import typing
import re

from fastapi_amis_admin.admin import admin
from fastapi_amis_admin.amis.components import PageSchema, Form, Iframe
from fastapi_amis_admin.crud import CrudEnum
from httpx import HTTPStatusError
from starlette.requests import Request

from models.model import APIModel
from router.base_create import create_api_files as create_api


class APISettings(admin.ModelAdmin):
    """ 接口管理页面 """
    page_schema = PageSchema(label='接口管理', icon='far fa-edit')
    model = APIModel

    async def get_update_form(self, request: Request, bulk: bool = False) -> Form:
        extra = {}
        if not bulk:
            api = f"put:{self.router_path}/item/${self.pk_name}"
            fields = self.schema_update.__fields__.values()
            if self.schema_read:
                extra["initApi"] = f"get:{self.router_path}/item/${self.pk_name}"
        else:
            api = f"put:{self.router_path}/item/" + "${ids|raw}"
            fields = self.bulk_update_fields

        try:
            await self.auto_api_services()  # 自动创建 API 接口
        except HTTPStatusError as _:
            pass

        return Form(
            api=api,
            name=CrudEnum.update,
            body=await self._conv_modelfields_to_formitems(request, fields, CrudEnum.update),
            submitText=None,
            trimValues=True,
            **extra,
        )

    @staticmethod
    async def auto_api_services():
        import httpx
        import json

        url = "http://localhost:8000/admin/APISettings/list?page=1&perPage=10&orderBy=&orderDir="

        payload: typing.Optional[str] = json.dumps({
            "_replace": "1",
            "page": 1,
            "perPage": 10
        })

        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Connection': 'keep-alive',
            'Origin': 'http://localhost:8000',
            'Referer': 'http://localhost:8000/admin/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.58',
            'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Microsoft Edge";v="114"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'Cookie': 'Authorization="bearer Kol99ABQDTP18rjS9s8vBGcmyayXhsWr7lfZa6OhJ0w"',
            'Content-Type': 'application/json',
            'Host': 'localhost:8000'
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, headers=headers, data=payload)
                response.raise_for_status()
                # 已有接口列表
                data = response.json()
                # 动态创建路由
                print("即将创建路由")
                create_api(data)
                return data
        except httpx.RequestError as e:
            print(f"Error fetching list data: {e}")
            return {}


class APIDocAdmin(admin.IframeAdmin):
    """ 接口测试页面 """
    page_schema = PageSchema(label='接口测试', icon='fab fa-medapps')

    @property
    def src(self):
        return self.app.site.settings.site_url + '/docs'

    def get_page_schema(self) -> typing.Optional[PageSchema]:
        if super().get_page_schema():
            # 判断跳转地址是否为空
            assert self.src, "src is None"
            iframe = self.iframe or Iframe(src=self.src)
            if self.site.settings.site_url and iframe.src.startswith(self.site.settings.site_url):
                self.page_schema.url = iframe.src
            else:
                self.page_schema.url = re.sub(r"^https?:", "", iframe.src)
            # 内嵌页面载入
            self.page_schema.schema_ = iframe
        return self.page_schema
