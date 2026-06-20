# Simple API Test

基于 Flask + Pytest + Requests + SQLite 的接口自动化测试项目。

## 项目简介

本项目实现了一个物联网设备管理平台的后端接口服务，并基于 Pytest 搭建接口自动化测试框架，覆盖用户注册、设备注册、设备登录、状态上报、传感器数据上报、告警生成等测试场景。使用 SQLite 做数据持久化，在测试中加入数据库校验，验证接口返回数据与数据库数据的一致性。
## 技术栈

- Python 3.13
- Flask
- Pytest
- Requests
- SQLite
- pytest-html

## 项目结构

```
simple-api-test/
├── api/                # 接口封装
│   ├── user_api.py
│   └── device_api.py
├── cases/              # 测试用例
│   ├── test_user.py
│   └── test_device.py
├── config/             # 配置文件
│   └── config.py
├── data/               # 测试数据
│   └── test_data.json
├── db/                 # 数据库操作
│   └── db_init.py
├── utils/              # 工具类
│   └── request_util.py
├── server.py           # Flask 后端服务
├── requirements.txt    # 项目依赖
├── pytest.ini          # Pytest 配置
└── README.md

```
## 已实现功能

- 用户注册接口
- 用户登录接口
- 用户查询接口
- 当前用户信息接口
- Token 鉴权
- SQLite 数据持久化
- 数据库校验测试
- 接口请求封装
- 测试数据 JSON 管理
- 请求与响应日志输出
- HTML 测试报告生成

## 测试场景

- 注册成功
- 重复注册
- 登录成功
- 密码错误
- 登录后查询用户成功
- 登录后查询不存在用户
- 未登录访问受保护接口
- 登录后获取当前用户信息
- 注册后数据库校验
- 注册返回ID与数据库一致性校验

## 安装依赖

```
pip install -r requirements.txt
```
## 启动服务

```
python server.py
```

启动成功后服务地址：

```
 http://127.0.0.1:5000
```

## 运行测试

打开新的终端，执行：

```
pytest
```

## 测试报告

运行完成后，打开：

```

report/report.html

```
即可查看 HTML 测试报告。

## 项目亮点

- 对 Requests 进行二次封装，统一管理请求发送逻辑
- 使用 Pytest 组织测试用例，支持自动化回归测试
- 使用 JSON 文件管理测试数据，降低用例和数据耦合
- 支持请求与响应日志输出，便于定位接口问题
- 使用 SQLite 做数据持久化，更接近真实业务场景
- 在测试中加入数据库校验，验证接口返回与数据库数据一致性
- 实现 Token 鉴权测试，模拟真实接口鉴权流程
