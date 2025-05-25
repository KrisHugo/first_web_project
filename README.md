# 项目启动流程说明

## 1. 前端（Vue）

1. 进入前端目录：
    ```bash
    cd frontend
    ```
2. 安装依赖：
    ```bash
    npm install
    ```
3. 启动前端开发服务器：
    ```bash
    npm run dev
    ```

## 2. 后端（Python Flask）

1. 进入后端目录：
    ```bash
    cd backend
    ```
2. 建议使用虚拟环境（可选）：
    ```bash
    python -m venv venv
    source venv/bin/activate  # Windows: venv\Scripts\activate
    ```
3. 安装依赖：
    ```bash
    pip install -r requirements.txt
    ```
4. 启动后端服务：
    ```bash
    python app.py
    ```

## 3. 数据库（MySQL）

1. 手动启动MySQL服务（根据本地安装方式）：
    - Windows：在服务管理器中启动MySQL，或命令行输入：
      ```bash
      net start mysql
      ```
    - macOS/Linux（如使用Homebrew）：
      ```bash
      brew services start mysql
      ```
2. 确认数据库连接配置与后端一致。

---

**启动顺序建议**：先启动数据库，再启动后端，最后启动前端。


---
# 前端 Vue 项目

## 主要功能

1. 用户登录（基于 `flask_jwt`）

- **后端实现**：使用 Flask 框架结合 `flask_jwt` 扩展，实现用户注册、登录和身份验证接口。用户登录成功后，后端生成并返回 JWT（JSON Web Token）令牌。
- **前端流程**：
    1. 用户在前端页面输入用户名和密码，提交登录请求。
    2. 前端收到后端返回的 JWT 令牌后，将其保存在本地（如 `localStorage`）。
    3. 后续所有需要身份验证的请求，前端会在请求头中携带该 JWT 令牌，后端通过验证令牌判断用户身份。

2. 留言功能（MySQL 持久化存储）

- **后端实现**：留言数据存储在 MySQL 数据库中，后端提供留言的增、查接口。
- **前端流程**：
    1. 用户在前端页面输入留言内容，点击提交按钮。
    2. 前端将留言内容通过 API 发送到后端，后端将留言保存到 MySQL 数据库。
    3. 前端通过接口获取所有留言数据，并展示在页面上，实现留言的实时展示和持久化存储。

## 需要完成的其他工作
1. 需求档案梳理
2. git同步
3. 

## 预计开发功能

- 用户注册和用户持久化存储
- 留言编辑（暂时只允许管理员和作者自己删除留言的功能）
- 留言分页
- 留言搜索
- 留言点赞
- 用户头像
- 富文本编辑
- 暗黑模式
- 回复留言
- 消息通知