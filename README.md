# web_cwk1
项目名称
Book Management API（图书管理接口服务）
项目目的 / 有什么用
这是一个轻量级的 Web API，用于管理图书数据（标题、作者、年份）。
它可以作为任何前端应用、管理后台或数据分析流程的后端数据接口，支持标准的增删改查操作，是典型的数据驱动服务原型。
目前实现的核心功能（基础版）
健康检查
GET /health
用于确认服务在线
图书 CRUD（数据库驱动）
POST /books：创建图书
GET /books：查询全部图书
GET /books/{id}：按 ID 查询图书
PUT /books/{id}：更新图书
DELETE /books/{id}：删除图书
输入校验
title、author 必填
year 必须是整数（若提供）
标准 HTTP 状态码与 JSON 响应
成功：200/201/204
错误：400/404
持久化存储
使用 SQLite（app.db）
服务重启后数据仍保留
