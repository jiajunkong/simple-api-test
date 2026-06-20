import sqlite3


def get_connection(db_path="test.db"):
    """获取数据库连接"""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path="test.db"):
    """初始化数据库，创建表"""
    conn = get_connection(db_path)
    cursor = conn.cursor()

    # 创建用户表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def clean_db(db_path="test.db"):
    """清空数据库（测试前清理用）"""
    conn = get_connection(db_path)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM users")

    conn.commit()
    conn.close()