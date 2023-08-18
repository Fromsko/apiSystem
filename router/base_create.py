# -*- encoding: utf-8 -*-
from pathlib import Path

from jinja2 import Template

tmpl = """\
from fastapi import APIRouter

router = APIRouter(prefix="/api/v1")  # 创建一个带有前缀的路由器对象


@router.get('/{{ api_local }}')
async def {{ name }}():
    \"\"\"
    {{ description }}
    \"\"\"
    # 实现你的接口逻辑
    return {'message': 'Hello, {{ name }}!'}

"""

init_tmpl = """\
from router.base_router import base_api

# 导入路由信息
{import_statements}


# 创建路由
{include_router_statements}
"""


def create_api_files(data):
    template = Template(tmpl)

    existing_names = []
    api_list = []
    api_name_list = []
    existing_files = Path(__file__).parents[1].joinpath('api')
    for name in existing_files.iterdir():
        skip_pycache = existing_files.joinpath("__pycache__")
        skip_init = existing_files.joinpath("__init__.py")
        if skip_pycache == name or skip_init == name:
            continue
        existing_names.append(name)

    for item in data['data']['items']:
        name = item['name']
        api_local = item['apiLocal']
        if "/api/v1/" in api_local:
            api_local = api_local.split("/api/v1/")[1]
        # 接口昵称列表
        api_name_list.append(name)
        # 接口描述
        description = item['description']
        create_file_path = existing_files.joinpath(f"{name}.py")

        api_list.append(create_file_path)

        if create_file_path in existing_names:
            print(f"Skipping file: {name}.py (already exists)")
            continue

        # 渲染模板
        content = template.render(
            name=name, api_local=api_local, description=description)

        # 创建文件
        with open(str(create_file_path), 'w', encoding="utf-8") as f:
            f.write(content)

        print(f"Created API file: api/{name}.py")

    # 删除不存在的接口文件
    for item in set(existing_names) - set(api_list):
        if item.is_dir():
            continue
        item.unlink()
        print(f"删除接口 api/{item}")
    else:
        import_statements = ""
        include_router_statements = ""

        for index, api_name in enumerate(api_name_list):
            # 将 {{ api_local }} 替换为 api_local
            import_statement = f"from .{api_name} import router as router_{index}\n"
            include_router_statement = f"base_api.include_router(router_{index})\n"

            import_statements += import_statement
            include_router_statements += include_router_statement

        code = init_tmpl.format(
            import_statements=import_statements,
            include_router_statements=include_router_statements
        )

        with open(existing_files.joinpath("__init__.py"), "w", encoding="utf-8") as file:
            file.write(code)
