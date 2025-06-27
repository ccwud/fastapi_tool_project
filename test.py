# main.py (Self-hosted OpenRouter + Local ChromaDB version)

# --- 1. 安装依赖 ---
# 确保你已经安装了所有必要的库:
# pip install vanna[mysql,openai,chromadb]

import vanna as vn
import pandas as pd
from openai import OpenAI  # 我们仍然使用这个库，因为它非常灵活
from vanna.openai import OpenAI_Chat
from vanna.chromadb import ChromaDB_VectorStore


# --- 2. 定义自定义 Vanna 类 ---
# 这个类完全不需要改动，它能很好地与我们即将配置的 OpenRouter 客户端配合工作。
class MyVanna(ChromaDB_VectorStore, OpenAI_Chat):
    def __init__(self, client, config=None):
        ChromaDB_VectorStore.__init__(self, config=config)
        OpenAI_Chat.__init__(self, client=client, config=config)


def main():
    print("--- Vanna.ai Demo: Self-Hosted OpenRouter + Local ChromaDB ---")

    # --- 3. 配置 OpenRouter 客户端 ---
    # 在这里填入你的 OpenRouter API 密钥和希望使用的模型。
    OPENROUTER_API_KEY = "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"  # <--- 在这里替换成你的 OpenRouter API Key

    # 关键改动：指定 OpenRouter 上的模型名称
    # 格式通常是 '供应商/模型名称'，例如 'google/gemini-pro', 'anthropic/claude-3-opus' 等
    # 你可以在 OpenRouter 网站上找到所有可用模型的列表：https://openrouter.ai/models
    OPENROUTER_MODEL = "openai/gpt-4o-mini"

    # 创建一个 OpenAI 客户端实例，但将其配置为指向 OpenRouter
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",  # <--- 关键改动：指定 OpenRouter 的端点
        api_key=OPENROUTER_API_KEY,  # <--- 使用 OpenRouter 的密钥
        default_headers={  # (推荐) OpenRouter 建议添加这些头信息用于日志和识别
            "HTTP-Referer": "YOUR_APP_NAME",  # <--- 替换成你的应用名称或URL
            "X-Title": "Vanna Demo Project",  # <--- 替换成你的项目标题
        },
    )

    print("\n[STEP 1/5] OpenRouter 客户端已配置。")

    # --- 4. 实例化自定义的 Vanna 类 ---
    # 我们将上面创建的客户端和模型名称传递给我们的 MyVanna 类。
    vn = MyVanna(
        client=client,
        config={'model': OPENROUTER_MODEL}
    )
    print("[STEP 2/5] 自定义 Vanna 实例已创建。")

    # --- 5. 连接到你的 MySQL 数据库 ---
    # 这一步和之前完全一样
    print("\n[STEP 3/5] 正在连接到 MySQL 数据库...")
    try:
        vn.connect_to_mysql(
            host='192.168.8.197',  # <--- 替换成你的数据库主机地址
            user='root',  # <--- 替换成你的数据库用户名
            password='123456',  # <--- 替换成你的数据库密码
            dbname='sys',# <--- 替换成你的数据库名称
            port=3306
        )
        print("✅ 数据库连接成功！")
    except Exception as e:
        print(f"❌ 数据库连接失败: {e}")
        return

    # --- 6. 训练模型 ---
    # 这一步和之前完全一样
    print("\n[STEP 4/5] 正在使用 DDL 训练模型...")

    ddl_statement = """
    CREATE TABLE IF NOT EXISTS Customers (
        customer_id INT PRIMARY KEY,
        name VARCHAR(255),
        email VARCHAR(255),
        join_date DATE
    );

    CREATE TABLE IF NOT EXISTS Orders (
        order_id INT PRIMARY KEY,
        customer_id INT,
        order_date DATE,
        total_amount DECIMAL(10, 2),
        FOREIGN KEY (customer_id) REFERENCES Customers(customer_id)
    );
    """

    vn.train(ddl=ddl_statement)
    print("✅ 模型训练完成！训练数据已保存在本地 ChromaDB 中。")

    # --- 7. 提问 ---
    # 这一步和之前完全一样
    print("\n[STEP 5/5] 准备开始提问...")

    question = "Who are the top 3 customers with the highest total order amount?"
    print(f"\n> 你的问题: {question}")

    df_result = vn.ask(question)

    print("\n查询结果 (DataFrame):")
    if df_result is not None and not df_result.empty:
        print(df_result)
    else:
        print("未能获取查询结果或结果为空。")

    print("\n--- 演示完成！ ---")


if __name__ == '__main__':
    main()