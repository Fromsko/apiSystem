# apiSystem
一个简易版的接口管理平台

实现如下功能: 
1. 后台管理系统
2. 教务系统爬虫
3. 自动接口生成
4. 本地化一言
5. 今日历史

## 目录结构
> 整体目录
```markdown
apiSystem
    - api       接口逻辑
    - db        数据存储
    - models    视图模型
    - res       资源相关
    - router    路由相关
    - views     页面视图
    - main.py   程序入口
```
> 部分目录
```markdown
- api
    - cname             教务系统-课表
    - history           历史上的今天
    - one_say           本地化一言

- router
    - base_create.py    自动注册新接口
    - base_router.py    路由相关逻辑
    - base_setting.py   基础设置
```

## 使用

```bash
# Install
python -m pip install -r requirement.txt
# run application
python main.py
```

## 运行截图
`教务系统爬虫`
![教务系统爬虫](./api/cname/img/2022级婴幼儿托育与服务1班4.png)


## 注意
> 项目通过修改第三方依赖库, 而非打补丁实现对页面的渲染
> 
> 如需自定义修改 | 展示 | 请遵循项目的协议 自行修改
## 鸣谢
+ [fastapi_amis_admin](https://github.com/amisadmin/fastapi-amis-admin) - FastAPI管理框架
+ [fastapi-user-auth](https://github.com/amisadmin/fastapi-user-auth) - 权限控制
+ [fastapi](https://github.com/tiangolo/fastapi) - 超级厉害的web框架
+ [ddddocr](https://github.com/sml2h3/ddddocr) - 验证码识别
## 支持项目
> 作者能力有限, 如果项目能够帮助到你 |=> 可以助力本项目
> 
> 接定制 Go | Python | Lua for android 相关的机器人

<div align="center">
   <img src="./res/money.jpg"  height=160>
   <img src="./res/wx.jpg" height=160>
</div>

<p align="center">
注：备注来意
</p>