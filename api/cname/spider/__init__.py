# -*- encoding: utf-8 -*-

import json
from pathlib import Path


def init_config():
    config_path = Path(__file__).parents[1] / "res" / "config.json"
    config = {
        "username": "",
        "password": "",
    }

    if not config_path.exists():
        with open(config_path, encoding="utf-8", mode="w") as file_obj:
            file_obj.write(json.dumps(config, ensure_ascii=False))
        return None

    with open(config_path, encoding="utf-8", mode="r") as file_obj:
        content = file_obj.read()
        config = json.loads(content)
    return config