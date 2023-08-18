import time

from config.config import file_load, random_choice

request_time = time.strftime(
    '%Y-%m-%d %H:%M:%S',
    time.localtime(time.time())
)


def test_file_load() -> dict:
    """基础请求测试"""
    data: dict = file_load('version')["sentences"]
    content = {
        "Message": {
            "code": 200,
            "data": {
                "type": "lv",
                "content": data
            }
        },
        "date": request_time
    }
    return content


def test_random_choice() -> dict:
    """测试随机获取"""
    data: dict = random_choice()
    content = {
        "Message": {
            "code": 200,
            "data": data
        },
        "date": request_time
    }
    return content


if __name__ == '__main__':
    print(test_random_choice())
    print(test_file_load())
