# -*- coding: utf-8 -*-
"""
    @File  : models.py
    @Date  : 2023-07-02 00:15:16
    @notes : 数据库模型
"""
from typing import Optional
from sqlmodel import SQLModel
from fastapi_amis_admin.models.fields import Field


# 参数模型
class Category(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True, nullable=False)
    name: str = Field(title='CategoryName')
    description: str = Field(default='', title='Description')


# API接口模型
class APIModel(SQLModel, table=True):
    # 设置唯一标识
    id: int = Field(default=None, primary_key=True, nullable=False)
    # 设置字段昵称
    name: str = Field(title='接口名称')
    # 设置地址 [可选类型为 str]
    apiLocal: Optional[str] = Field(default='', title='接口地址')
    # 设置字段描述
    description: str = Field(default='', title='接口描述')
