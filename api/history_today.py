import datetime
import json
import re
from pathlib import Path

import requests
import pandas as pd
from fastapi import APIRouter

router = APIRouter(prefix="/api/v1")  # 创建一个带有前缀的路由器对象


class TodayHistory(object):
    """ 获取历史上的今天数据 """

    def _fetch(self):
        """ 数据请求模块 """
        try:
            url = "https://www.bjsoubang.com/api/getHistoryDaily"
            r = requests.get(url=url)
            res_list = json.loads(r.text)['info']
            df = pd.DataFrame(res_list)
            df = df.drop(['cover', 'festival', 'recommend'], axis=1)
            return df
        except:
            return None

    def _parser(self, df_index: dict):
        """ 数据解析 """
        title = df_index['title']
        cl_title = []
        cl_year = []

        for x in title:
            # 正则表达式去掉<a>标签
            result = re.split('</a>', x)
            m = result[0]
            m = re.split('<a.*>', m)
            outstr = ""
            for n in m:
                outstr += n
            outstr += result[1]
            cl_title.append(outstr)

        for y in df_index['year']:
            # 处理年份数字
            if y[0] == '-':
                daystr = "公元前" + y[1:] + "年"
            else:
                daystr = y + "年"
            cl_year.append(daystr)
        return cl_year, cl_title

    def history(self):
        """ 历史上的今天 """
        today_history = {}

        try:
            df_index = self._fetch()
        except Exception as err:
            raise err

        if df_index is not None:
            path_ = Path(__file__).parent / "history"
            date_ = datetime.datetime.now().strftime('%m月%d日')

            if not path_.exists():
                path_.mkdir()

            file_name = path_ / f"histroy_today-{date_}.json"

            with open(file_name, "w", encoding='utf-8') as file_obj:

                cl_year, cl_title = self._parser(df_index)

                for index in range(len(df_index['year'])):
                    content = f"{cl_year[index]}{date_},{cl_title[index]}"
                    today_history.update({index + 1: content})

                today_history['len'] = (today_history.__len__())

                file_obj.write(json.dumps(
                    today_history,
                    ensure_ascii=False,
                ))
            return today_history
        return None


@router.get('/history_today')
async def history_today():
    """
    今日历史数据
    """
    json_return: dict = {
        "code": 200,
        "data": None,
        "error": None,
    }

    spider = TodayHistory()
    try:
        if (result := spider.history()) is not None:
            json_return['data'] = result
            return result
    except Exception as err:
        json_return['code'] = 500
        json_return['error'] = err.__str__()
    return json_return
