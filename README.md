# Simple API Test

基于 Flask + Pytest + Requests + SQLite 的接口自动化测试项目，覆盖用户管理和物联网设备管理场景。

## 项目简介

本项目实现了一个物联网设备管理平台的后端接口服务，并基于 Pytest 搭建接口自动化测试框架。覆盖用户注册登录、设备注册登录、状态上报、传感器数据上报、告警生成等测试场景。使用 SQLite 做数据持久化，在测试中加入数据库校验验证接口返回与数据库数据的一致性。配置 GitHub Actions 实现代码推送自动运行测试。

## 技术栈

- Python 3.13
- Flask
- Pytest
- Requests
- SQLite
- pytest-html
- Allure
- GitHub Actions

## 项目结构

```text
simple-api-test/
├── .github/
│   └── workflows/
│       └── test.yml         # CI/CD 自动化测试
├── api/                     # 接口封装
│   ├── user_api.py          # 用户接口
│   └── device_api.py        # 设备接口
├── cases/                   # 测试用例
│   ├── test_user.py         # 用户模块测试
│   └── test_device.py       # 设备模块测试
├── config/                  # 配置文件
│   └── config.py
├── data/                    # 测试数据
│   └── test_data.json
├── db/                      # 数据库操作
│   └── db_init.py
├── utils/                   # 工具类
│   └── request_util.py      # 统一请求工具
├── server.py                # Flask 后端服务
├── requirements.txt         # 项目依赖
├── pytest.ini               # Pytest 配置
└── README.md
```

## 已实现功能

### 用户管理

- 用户注册
- 用户登录
- 用户查询
- 当前用户信息
- Token 鉴权

### 设备管理

- 设备注册
- 设备登录
- 设备状态上报（在线/离线）
- 传感器数据上报（温度、湿度、电量）
- 温度超限告警
- 电量过低告警
- 设备信息查询
- 设备告警查询

### 测试框架

- 接口请求封装（RequestUtil）
- 测试数据 JSON 管理
- 请求与响应日志输出
- HTML 测试报告（pytest-html）
- Allure 测试报告
- SQLite 数据持久化
- 数据库校验测试
- GitHub Actions CI/CD

## 测试场景

### 用户模块（10个）

- 注册成功
- 重复注册
- 登录成功
- 密码错误
- 登录后查询用户
- 登录后查询不存在用户
- 未登录访问受保护接口
- 登录后获取当前用户信息
- 注册后数据库校验
- 注册返回ID与数据库一致性校验

### 设备模块（11个）

- 设备注册成功
- 设备重复注册
- 设备登录成功
- 状态上报成功
- 未登录状态上报
- 数据上报成功
- 数据上报触发告警
- 查询设备信息
- 设备注册数据库校验
- 数据上报数据库校验
- 告警生成数据库校验

## 安装依赖

```bash
pip install -r requirements.txt
```

## 启动服务

```bash
python server.py
```

启动成功后服务地址：

```text
http://127.0.0.1:5000
```

## 运行测试

打开新的终端，执行：

```bash
pytest
```

## 测试报告

### HTML 报告

运行完成后，打开：

```text
report/report.html
```

### Allure 报告

运行完成后，执行：

```bash
allure generate report/allure-results -o report/allure-report --clean
```

然后打开：

```text
report/allure-report/index.html
```

## CI/CD

项目配置了 GitHub Actions，每次推送代码到 main 分支时自动运行测试。

查看测试结果：

```text
https://github.com/jiajunkong/simple-api-test/actions
```

## 项目亮点

- 对 Requests 进行二次封装，统一管理请求发送逻辑，支持日志输出
- 使用 Pytest 组织测试用例，使用 fixture 管理测试前后置操作
- 使用 JSON 文件管理测试数据，降低用例和数据耦合
- 实现 Token 鉴权测试，模拟真实接口鉴权流程
- 使用 SQLite 做数据持久化，在测试中加入数据库校验
- 结合物联网设备管理场景，覆盖状态上报、数据上报、告警生成等测试
- 配置 GitHub Actions CI/CD，实现代码推送自动运行测试
- 支持 pytest-html 和 Allure 两种测试报告格式