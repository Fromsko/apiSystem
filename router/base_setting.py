import json
from pathlib import Path
from collections import defaultdict
from datetime import datetime

import plotly.graph_objects as go

from api import base_api
from router.base_router import Request

# 使用字典来存储API调用次数
api_call_counts = defaultdict(int)


def init_counts():
    # 获取API调用统计数据
    with open(
        str(Path(__file__).parents[1] / "res" / "count.ini"),
        "r",
        encoding="utf-8"
    ) as file:
        lines = file.readlines()

    api_stats = {}
    for line in lines:
        time_point, call_number = line.strip().split(": ")
        api_stats.update({time_point: int(call_number)})
    return api_stats


call_info = init_counts()


# 定义统计中间件
@base_api.middleware("http")
async def count_api_calls(request: Request, call_next):
    """ 调用统计 """

    # 获取请求的路径
    path = request.url.path

    # 判断路径是否在指定范围内
    if path.startswith("/api/v1"):
        # 统计API调用次数
        current_time = datetime.now().strftime("%H:00")
        api_call_counts[path] += 1
        call_info.update({
            current_time: api_call_counts[path]
        })

    # 继续处理请求
    response = await call_next(request)

    return response


@base_api.get("/api/call_number")
async def get_call_numbers():
    """ 获取调用次数 """

    global call_info
    time_range = ["00:00", "01:00", "02:00", "03:00", "04:00", "05:00", "06:00", "07:00", "08:00",
                  "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00",
                  "18:00", "19:00", "20:00", "21:00", "22:00", "23:00"]

    call_counts = 0  # 总调用次数
    sert_time_data = 0  # 时段调用次数
    call_numbers = []
    call_sert_time = datetime.now().strftime("%H:00")

    for time_point in time_range:
        call_number = call_info.get(time_point, 0)
        # 统计不为 0 的调用次数
        if call_number != 0:
            call_counts += call_number
        # 统计时间
        if call_sert_time == time_point:
            sert_time_data += call_number
        # 数据追加
        call_numbers.append((time_point, call_number))

    # 将信息写入文件
    with open(
        str(Path(__file__).parents[1] / "res" / "count.ini"),
        "w",
        encoding="utf-8"
    ) as file:
        for time_point, call_number in call_numbers:
            file.write(f"{time_point}: {call_number}\n")

    return {"data": [call_counts, sert_time_data]}


@base_api.get("/api/chart")
async def get_api_chart() -> dict:
    """ 获取 API 图表 """
    dates = []
    call_numbers = []

    # 提取日期和调用次数数据
    for k, v in enumerate(list(call_info.items())):
        dates.append(k)  # 使用索引作为日期
        call_numbers.append(v)

    # 创建图表
    fig = go.Figure(data=go.Scatter(x=dates, y=call_numbers, mode='lines'))

    # 设置图表布局
    fig.update_layout(
        title='API调用统计',
        xaxis_title='日期',
        yaxis_title='调用次数'
    )

    return fig.to_plotly_json()
