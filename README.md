# Simple API Test

基于 Flask + Pytest + Requests 的接口自动化测试项目。

## 项目简介

本项目实现了一个简单的用户管理接口服务，并基于 Pytest 搭建接口自动化测试框架，覆盖用户注册、登录、查询用户、Token 鉴权等测试场景。

项目主要用于练习和展示接口自动化测试的完整流程，包括接口封装、请求封装、测试数据管理、日志输出、测试报告生成等内容。

## 技术栈

- Python 3.13
- Flask
- Pytest
- Requests
- pytest-html

## 项目结构

```text
simple-api-test/
├── api/                 # 接口封装
│   └── user_api.py
├── cases/               # 测试用例
│   └── test_user.py
├── config/              # 配置文件
│   └── config.py
├── data/                # 测试数据
│   └── test_data.json
├── report/              # 测试报告
├── utils/               # 工具类
│   └── request_util.py
├── server.py            # Flask 后端服务
├── requirements.txt     # 项目依赖
├── pytest.ini           # Pytest 配置
└── README.md
```