# -*- coding: utf-8 -*-
"""
    @File  : parser.py
    @Date  : 2023-03-14 09:38:41
    @notes : 响应数据处理
"""
import json
from pathlib import Path

from bs4 import BeautifulSoup

__all__ = ("parser_response", )


def _write_json(save_load: Path, filename: str, data: json):
    """Write the data to file."""
    with open(save_load / f"{filename}.json", 'w', encoding='utf-8') as fp:
        fp.write(json.dumps(data, ensure_ascii=False))


def _data_parser(soup_data):
    """
    二次解析,并通过生成器返回(加快解析速度)
    :param soup_data: BeautifulSoup 文本对象
    :return: 生成器返回 每周数据
    """
    week_data_info = {}
    week_data = [1, 2, 3, 4, 5, 6, 7]
    try:
        for index, week in zip(range(1, 35, 5), week_data):  # 取出七天数据
            jc_info = {'first': None, 'second': None,
                       'third': None, 'fourth': None, 'fifth': None}
            for jc_data, jc in zip(soup_data[index: index + 5], jc_info):
                if jc_data.find("div") is None:
                    jc_info[jc] = {
                        "lesson_name": "",
                        "teacher": "",
                        "week": "",
                        "rank": "",
                        "place": ""
                    }
                else:
                    divs = jc_data.div.get_text('#').split('#')
                    # 有课的数据填充
                    divs = [i.strip('\n') for i in divs]
                    for index_, i in enumerate(divs):
                        if '\n' in i:
                            divs.pop(index_)
                            for new_index, j in enumerate(i.split('\n')):
                                divs.insert(index_ + new_index, j)
                    divs.pop(1)
                    jc_info[jc] = {
                        "lesson_name": divs[0],
                        "teacher": divs[1],
                        "week": divs[2],
                        "rank": jc,
                        "place": divs[3]
                    }
            week_data_info.update({week: jc_info})
        return week_data_info
    except IndexError as exc:
        raise IndexError("Could not find Data.") from exc


def parser_response(resp, save: bool = False):
    """解析课表
    Args:
        resp (Response): 课表响应
        save (bool, optional): 是否开启存储. Defaults to True.

    Raises:
        IndexError: 初次解析失败

    Returns:
        cname: 班级名
        data_info: 数据源
        spec: 特殊信息
    """
    spec: str = ""
    cname: str = ""
    data_info: dict = {}
    try:
        soup = BeautifulSoup(resp.text, "lxml")
        soup_td = soup.find_all("tr")[2].find_all("td")
        cname = soup_td[0].text.strip()  # 班级昵称
        spec = soup_td[-1].text  # 特殊信息(备注)
    except IndexError as _:
        print('本周没有课')
        return cname, None, spec

    data_info = _data_parser(soup_td)

    if bool(save):
        _write_json(  # 存储为json文件
            save_load=Path(__file__).parent.parent / "res",
            filename=cname,
            data=data_info
        )

    return cname, data_info, spec


if __name__ == '__main__':
    # 获取课表(登陆-> 获取-> 退出)
    from spider.login import ParserData
    login = ParserData()

    response = login.search_table(
        cname="2022级学前教育12班"
    )

    login.exit_login()

    parser_response(response)
