# -*- coding: utf-8 -*-
"""
    @File  : test_config.py
    @Date  : 2023-03-17 22:00:23
    @notes : Test results
"""
# try:
#     from util.config_info import parser_excel
# except ImportError or parser_excel as error:
#     from re import search
#     from os import system
#     from sys import executable

#     system('{} -m pip install {}'.format(
#         executable, search("'(.*?)'", str(error))[1])
#     )

from util.config_info import parser_excel

if __name__ == "__main__":
    _, save_load = parser_excel()
    print(
        save_load
    )
