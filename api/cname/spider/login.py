# -*- coding: utf-8 -*-
"""
    @File  : login.py
    @Date :  2023-03-13 01:12:41
"""
import re
from lxml import etree
from bs4 import BeautifulSoup
from cn2an import cn2an
from ddddocr import DdddOcr
from requests import Session

__all__ = ("SchoolLogin", "ParserData")


class SchoolLogin(Session):
    """
        流程:
            1.获取cookies  get_cookie()
            2.获取验证码   get_verify_code(session)
            3.获取解码数据 get_code(__username, __password, session)
        =>登录(encoded, verify_code, session)
    """

    def __init__(self, username: str, password: str):
        super().__init__()
        self.__username = username
        self.__password = password
        self.__img_url = "http://61.186.94.104:8090/verifycode.servlet"
        self.__str_url = "http://61.186.94.104:8090/Logon.do?method=logon&flag=sess"
        self.__login_url = "http://61.186.94.104:8090/Logon.do?method=logon"
        self.__logout_url = "http://61.186.94.104:8090/jsxsd/xk/LoginToXk"
        self.__status = self.keep_alive()
        assert self.__status == 200, "访问失败"

    @property
    def login_info(self) -> tuple:
        """设置登录用户信息"""
        return self.__username, self.__password, self.__status

    @login_info.setter
    def login_info(self, info):
        if info[0] and info[1]:
            self.__username, self.__password = info
        else:
            print("设置失败")

    def keep_alive(self):
        """保持会话"""
        return self.get(url="http://61.186.94.104:8090", headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
                (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
        }).status_code

    def _get_verify_code(self):
        """获取验证码"""
        headers = {
            'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Host': '61.186.94.104:8090',
            'Referer': 'http://61.186.94.104:8090',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
                AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
        }
        # 获取验证码图片
        safe_resp = self.get(self.__img_url, headers=headers)
        text = DdddOcr(show_ad=False).classification(safe_resp.content)
        return text

    def _get_encode(self) -> str:
        """获取加密码"""
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;\
                q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': '61.186.94.104:8090',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
                AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
        }
        data_str = self.get(self.__str_url, headers=headers).text
        encode = ""
        scode = data_str.split("#")[0]
        sxh = data_str.split("#")[1]

        # 计算encoded字符串
        code = self.__username + "%%%" + self.__password
        for i in range(len(code)):
            if i < 20:
                encode += code[i:i + 1]
                encode += scode[0:int(sxh[i:i + 1])]
                scode = scode[int(sxh[i:i + 1]):]
            else:
                encode += code[i:]
        encode = encode[: -15]  # 陷阱(需要去除) | 防止模拟登录 | "501190119119199"
        return encode

    def _login(self):
        """模拟登录"""
        verify_code = self._get_verify_code()
        encoded = self._get_encode()

        data = {
            'userAccount': self.__username,
            'user__Password': "",
            'RANDOMCODE': verify_code,
            'encoded': encoded,
        }
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;\
                q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Content-Length': '101',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': '61.186.94.104:8090',
            'Origin': 'http://61.186.94.104:8090',
            'Referer': 'http://61.186.94.104:8090/',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
                AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
        }
        resp = self.post(self.__login_url, headers=headers, data=data)
        resp.raise_for_status()
        return resp

    def exit_login(self):
        """退出登录"""
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;\
                q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Origin': 'http://61.186.94.104:8090',
            'Proxy-Connection': 'keep-alive',
            'Referer': 'http://61.186.94.104:8090/jsxsd/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
                AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
            'Host': '61.186.94.104:8090',
            'Connection': 'keep-alive'
        }
        resp = self.get(
            url=self.__logout_url,
            data={'method': 'exit'},
            headers=headers
        )
        assert resp.status_code == 200, "退出失败"
        self.close()


class ParserData(SchoolLogin):
    """页面解析|课表查询"""

    def __init__(self, username: str, password: str):
        super().__init__(username=username, password=password)
        self._xnxqh = None
        self._now_week = None
        self._assert_parser_xnxqh()

    def _parser_xnxqh(self):
        """获取当前 学年|周数"""
        headers = {
            'Accept': 'text/html, */*; q=0.01',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Connection': 'keep-alive',
            'Referer': 'http://61.186.94.104:8090/Logon.do?method=logon',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
                (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.69',
            'X-Requested-With': 'XMLHttpRequest',
        }

        resp = self.get(
            "http://61.186.94.104:8090/jsxsd/framework/xsMain_new.jsp",
            headers=headers
        ).text
        html = etree.HTML(resp)

        try:
            self._xnxqh = (re.findall(
                r'<option value="">(.*?)</option>',
                string=resp
            ) or ("2022-2023-2", ))[0]

            self._now_week = cn2an(re.findall(
                "第(.*?)周",
                html.xpath('//*[@id="week"]/option[@selected="selected"]')
                [0].text)[0]
            )
        except IndexError as err:
            raise IndexError("获取当前 学年|周数异常") from err

        print(f"当前学年: {self._xnxqh} 当前周期: {self._now_week}")

    def _assert_parser_xnxqh(self):
        """
        捕获 学年信息的 索引异常
        """
        resp = self._login().text
        soup = BeautifulSoup(resp, 'html.parser')
        if soup.title.string == "首页":
            try:
                self._parser_xnxqh()
            except IndexError as err:
                print(f"捕获到了异常信息: {err}")
                self._parser_xnxqh()
        else:  # 登陆失败则重试
            self._login()

    def search_table(self, cname, week=None, weekly=''):
        """查询课表"""
        if not week:
            week = str(self._now_week)
        class_table_url = "http://61.186.94.104:8090/jsxsd/kbcx/kbxx_xzb_ifr"
        data = {
            'xnxqh': self._xnxqh,
            'kbjcmsid': '043280346FD24641BAC2EB4A79D1CFF9',
            'skyx': '',
            'sknj': '',
            'skzy': '',
            'skbjid': '',
            'skbj': cname,
            'zc1': week,
            'zc2': week,
            'skxq1': weekly,
            'skxq2': weekly,
            'jc1': '',
            'jc2': ''
        }

        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;\
                q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Origin': 'http://61.186.94.104:8090',
            'Proxy-Connection': 'keep-alive',
            'Referer': 'http://61.186.94.104:8090/jsxsd/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
                AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
            'Host': '61.186.94.104:8090',
            'Connection': 'keep-alive'
        }

        resp = self.post(
            url=class_table_url,
            headers=headers,
            data=data
        )

        return week, resp

    def get_base_table(self):
        """获取当周课表数据 | 写入文件"""
        headers = {
            'Accept': 'text/html, */*; q=0.01',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Connection': 'keep-alive',
            'Referer': 'http://61.186.94.104:8090/jsxsd/framework/xsMain_new.jsp?t1=1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
                (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.69',
            'X-Requested-With': 'XMLHttpRequest',
        }

        params = {
            'rq': '2023-03-13',  # 从 parser_xnxqh 获取(本周)
            'sjmsValue': '',
        }

        response = self.get(
            'http://61.186.94.104:8090/jsxsd/framework/main_index_loadkb.jsp',
            params=params,
            headers=headers
        )

        return response


if __name__ == "__main__":
    app = ParserData()

    # 登陆信息
    print(app.login_info)

    # 基础课表
    app.get_base_table()

    # 退出
    app.exit_login()
