# -*- coding: utf-8 -*-
"""
    @File  : Home_view.py
    @Date  : 2023-07-02 20:34:24
    @notes : 主页面视图
"""
import httpx
from fastapi_amis_admin import amis
from fastapi_amis_admin.admin import admin
from fastapi_amis_admin.amis.components import (
    Page,
    PageSchema,
    Property,
    Editor,
    Chart,
)
from fastapi_amis_admin.utils.translation import i18n as _
from starlette.requests import Request


class HomeAdmin(admin.PageAdmin):
    """ 主页面 """

    page_schema = PageSchema(
        label=_("Home"), icon="fa fa-home",
        url="/home", isDefaultPage=True, sort=100
    )

    page_path = "/home"

    async def get_page(self, request: Request) -> Page:
        page = await super().get_page(request)
        api_data, call_counts, sert_time_data = None, None, None

        try:
            # 获取调用次数
            async with httpx.AsyncClient() as client:
                show_resp = await client.get(
                    url="http://localhost:8000/api/call_number"
                )
                call_counts, sert_time_data = show_resp.json()['data']
        except Exception as _:
            print("调用次数获取失败")

        try:
            # 获取图标(渲染数据)
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    url="http://localhost:8000/api/chart"
                )
                api_data = response.json()['data'][0]['y']
        except Exception as _:
            print("绘图失败")

        page.body = [
            Property(
                title="接口调用统计",
                column=3,
                items=[
                    Property.Item(
                        label="今天调用次数",
                        content=call_counts or 0,
                    ),
                    Property.Item(
                        label="时段调用次数",
                        content=sert_time_data or 0,
                    )
                ],
            ),
            amis.Divider(),
            Chart(
                config={
                    "title": {
                        "text": "调用时间图谱",
                        "subtext": "监控频率: 自动更新"
                    },
                    "tooltip": {
                        "trigger": "axis"
                    },
                    "legend": {
                        "data": ["调用次数"]
                    },
                    "xAxis": {
                        "type": "category",
                        "data": ["00:00", "01:00", "02:00", "03:00", "04:00", "05:00", "06:00", "07:00", "08:00",
                                 "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00",
                                 "18:00", "19:00", "20:00", "21:00", "22:00", "23:00"]
                    },
                    "yAxis": {
                        "type": "value"
                    },
                    "series": [
                        {
                            "name": "次数",
                            "type": "line",
                            "data": api_data or [],
                        }
                    ],
                    "animation": False,
                    "dataZoom": [
                        {
                            "type": "inside",
                            "start": 0,
                            "end": 100
                        }
                    ],
                    "toolbox": {
                        "feature": {
                            "saveAsImage": {}
                        }
                    }
                },
            ),
            Editor(
                language="python",
                label="便捷调用代码",
                disabled=True,
                size='lg',
                value=_Call_code,
            ),
        ]
        return page


_Call_code = """\
import httpx


def get_api(fetch_url: str):
    resp = httpx.post(
        url=fetch_url,
        headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'},
    )
    if resp.status_code == 200:
        return resp.json()
    return 'API is not available.'


if __name__ == "__main__":
    api_local = "localhost"
    port = "8000"
    fetch_url = f"http://{api_local}:{port}/api/v1/search?house=xx-xxx"
    print(get_api(fetch_url))

"""
