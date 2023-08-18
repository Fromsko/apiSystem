# -*- coding: utf-8 -*-
"""
    @File  : demo.py
    @Date  : 2023-03-17 21:32:46
    @notes : 全校课表信息解析 && 存储
"""
import json
from re import findall
from pathlib import Path

import pandas as pd
from loguru import logger

from ._xls_xlsx import open_xls_as_xlsx

__all__ = ("parser_excel", )

logger = logger.bind(name="TestPath")
load: Path = Path(__file__).parent.parent / "resource" / "data.xlsx"


def _save_json_file(filename="all_class_info.json", data_info=None) -> Path:
    save_file_load: Path = load.parent / "result"
    if not save_file_load.exists():
        logger.debug(
            f"Not find filedir [{save_file_load.exists()}] => will create!"
        )
        save_file_load.mkdir()
    with open(save_file_load / filename, 'a+', encoding='utf-8') as file_obj:
        file_obj.write(json.dumps(data_info or "{}", ensure_ascii=False))
    logger.info("Parser data and save finised!")
    return save_file_load / "all_class_info.json"


def _access_path() -> Path:
    """
    检测文件是否存在
    """
    source_load: Path = load.parent / '2022年下学期全校总课表10.20.xls'
    save_load: Path = load.parent / 'data.xlsx'

    if load.exists():
        logger.info("data.xlsx is exists")
    else:
        save_load: Path = open_xls_as_xlsx(
            xls_path=source_load,
            xlsx_path=save_load
        )
        logger.debug("Source file is not exists, Created!")
        logger.info(f"SaveLoad: {save_load}")
    return save_load


def parser_excel():
    """
    全校班级统计: |截取全校自全校课表|
    """
    cname_info = {
        '2020': {},
        '2021': {},
        '2022': {}
    }

    parser_file: Path = _access_path()
    raw_data = pd.read_excel(
        parser_file,
        header=0
    )

    for cname in raw_data.values[4: 80, 0: 1].tolist():
        enroll, name, people_num = findall(
            r"(.*?)级(.*?)\((.*?)\)",
            string=cname[0]
        )[0]
        cname_info[enroll].update({
            name: {
                "people_num": people_num,
                "data": "data",
                "source_name": cname[0]
            }
        })

    save_load = _save_json_file(data_info=cname_info)
    return cname_info, save_load


if __name__ == "__main__":
    parser_excel()
