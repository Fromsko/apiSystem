# -*- coding: utf-8 -*-
"""
    @notes : 获取班级昵称
"""
import json
from pathlib import Path

class_dict = None

def load_data():
    global class_dict
    jsonFile = Path(__file__).parent / "all_class_info.json"
    with open(str(jsonFile), "r", encoding="utf-8") as file_obj:
        content = file_obj.read()
        class_dict = json.loads(content)

def search(cname: str, year: str):
    global class_dict
    if class_dict is None:
        load_data()

    if year in class_dict and cname in class_dict[year]:
        class_info = class_dict[year][cname]
        source_name = class_info["source_name"].split('(')[0]
        return {
            "source_name": source_name,
            "people_num": class_info["people_num"],
        }
    
    return None
