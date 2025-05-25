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