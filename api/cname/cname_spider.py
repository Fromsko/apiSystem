# -*- coding: utf-8 -*-
"""
    @File  : main.py
    @notes : 获取本周课表图片
"""
from .spider import init_config
from .spider.create import create_photo
from .spider.login import ParserData
from .spider.parser import parser_response


def search_kb_info(cname="2022级学前教育12班", week=None, weekly=''):
    json_return = {
        "code": 200,
        "data": None,
        "error": None,
    }

    if (config := init_config()) is not None:
        app = ParserData(**config)

        week, table_resp = app.search_table(
            cname,
            week,
            weekly,
        )
        cname, data_info, spec = parser_response(
            table_resp,
            save=True
        )
        app.exit_login()
        result = create_photo(cname + week, data_info)
        json_return['data'] = result[1]
        return json_return
    else:
        json_return['code'] = 500
        json_return["error"] = "账号配置失败"
        return json_return


if __name__ == '__main__':
    print(search_kb_info())
