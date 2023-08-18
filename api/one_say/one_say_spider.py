# -*- coding: utf-8 -*-
import time

from .config import random_choice


async def one_say_api(client_ip: str):
    request_time = time.strftime(
        '%Y-%m-%d %H:%M:%S',
        time.localtime(time.time())
    )

    content = {
        "code": 200,
        "data": None,
        "error": None,
        "date": request_time,
        "client_ip": client_ip,
    }

    try:
        data = random_choice()
    except Exception as err:
        content['error'] = err.__str__()
        return content
    else:
        content['data'] = {
            "type": data[0],
            "content": data[1]
        }
        return content
