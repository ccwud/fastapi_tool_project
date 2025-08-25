# main.py (Self-hosted OpenRouter + Local ChromaDB version)

# --- 1. 安装依赖 ---
# 确保你已经安装了所有必要的库:
# pip install vanna[mysql,openai,chromadb]

import vanna as vn
import pandas as pd
from openai import OpenAI
from vanna.openai import OpenAI_Chat
from vanna.chromadb import ChromaDB_VectorStore
import config  # <--- 关键改动：导入我们的配置文件


# --- 2. 定义自定义 Vanna 类 ---
# 这个类完全不需要改动。
class MyVanna(ChromaDB_VectorStore, OpenAI_Chat):
    def __init__(self, client, config=None):
        ChromaDB_VectorStore.__init__(self, config=config)
        OpenAI_Chat.__init__(self, client=client, config=config)


def main():
    print("--- Vanna.ai Demo: Self-Hosted OpenRouter + Local ChromaDB ---")

    # --- 3. 从 config.py 加载配置 ---
    # 我们现在直接从导入的 config 模块中获取变量。
    print("\n[STEP 1/5] 正在从 config.py 加载配置...")
    try:
        # 检查关键配置是否存在
        _ = config.OPENROUTER_API_KEY
        _ = config.DB_HOST
        _ = config.DB_USER
        _ = config.DB_PASSWORD
        _ = config.DB_NAME
    except AttributeError as e:
        print(f"❌ 错误：配置文件 'config.py' 中缺少必要的配置项: {e}")
        print("请确保 'config.py' 文件存在且包含所有必需的变量。")
        return

    print("✅ 配置加载成功。正在配置 OpenRouter 客户端...")

    # --- 4. 配置 OpenRouter 客户端 ---
    OPENROUTER_MODEL = "openai/gpt-4o-mini"

    # 使用从 config.py 中加载的密钥
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=config.OPENROUTER_API_KEY,  # <--- 关键改动
        default_headers={
            "HTTP-Referer": "YOUR_APP_NAME",
            "X-Title": "Vanna Demo Project",
        },
    )

    print("✅ OpenRouter 客户端已配置。")

    # --- 5. 实例化自定义的 Vanna 类 ---
    vn = MyVanna(
        client=client,
        config={'model': OPENROUTER_MODEL}
    )
    print("[STEP 2/5] 自定义 Vanna 实例已创建。")

    # --- 6. 连接到你的 MySQL 数据库 ---
    # 使用从 config.py 中加载的数据库信息
    print("\n[STEP 3/5] 正在连接到 MySQL 数据库...")
    try:
        vn.connect_to_mysql(
            host=config.DB_HOST,  # <--- 关键改动
            user=config.DB_USER,  # <--- 关键改动
            password=config.DB_PASSWORD,  # <--- 关键改动
            dbname=config.DB_NAME,  # <--- 关键改动
            port=config.DB_PORT  # <--- 关键改动
        )
        print("✅ 数据库连接成功！")
    except Exception as e:
        print(f"❌ 数据库连接失败: {e}")
        return

    # --- 7. 训练模型 ---
    print("\n[STEP 4/5] 正在使用 DDL 训练模型...")

    ddl_statement = """
                    CREATE TABLE `aio-db`.data_examination_menu (
    id VARCHAR(20) NOT NULL PRIMARY KEY,
    menuName VARCHAR(100) NULL,
    menuName_CN VARCHAR(100) NULL,
    menuName_TW VARCHAR(100) NULL,
    menuCode VARCHAR(100) NULL,
    parentId VARCHAR(20) NULL,
    menuStatus BIGINT NULL COMMENT '菜单状态',
    menuType VARCHAR(20) NULL,
    menuSource VARCHAR(20) NULL,
    imgUrl VARCHAR(255) NULL,
    menuOrder INT NULL COMMENT '菜单排序',
    appCode VARCHAR(20) NULL,
    eid BIGINT NULL,
    isPage BIT NULL,
    sid BIGINT NULL,
    createDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updateDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL ON UPDATE CURRENT_TIMESTAMP,
    moudleAuth BIT DEFAULT b'0' NOT NULL,
    CONSTRAINT data_examination_menu_menuCode_unique UNIQUE (sid, eid, appCode, menuSource, menuStatus, menuCode, parentId),
    CONSTRAINT data_examination_menu_menuName_unique UNIQUE (sid, eid, appCode, menuSource, menuStatus, menuName, parentId)
) COMMENT '数据体检中心 菜单表';

                    """
    doc = """
    表名: data_examination_menu
该表用于存储“数据体检中心”应用的菜单结构。表中的每一行代表一个菜单项。
id: 菜单项的唯一主键ID。
menuName: 菜单的显示名称。
menuName_CN: 菜单的简体中文名称。
menuName_TW: 菜单的繁体中文名称。
menuCode: 菜单的唯一编码，通常用于程序内部识别和调用。
parentId: 父级菜单的id。如果这个字段为NULL，表示这是一个顶级菜单。
menuStatus: 菜单状态，用于控制菜单是否可用（例如：1表示启用，0表示禁用）。
menuType: 菜单类型（例如：链接、子菜单目录等）。
menuSource: 菜单数据的来源系统或模块。
imgUrl: 菜单图标的URL地址。
menuOrder: 菜单排序值，用于决定同级菜单的显示顺序，数值越小越靠前。
appCode: 该菜单所属的应用编码。
eid: 企业或实体ID。
isPage: 是否是一个页面，布尔值。
sid: 站点或系统ID。
createDate: 记录创建时间。
updateDate: 记录最后更新时间。
moudleAuth: 是否需要模块认证，布尔值。
Java代码逻辑 (test方法) 说明:
这段Java代码的核心功能是：在指定的父菜单下批量创建新的子菜单。
输入参数: 方法接收parentCode（父菜单编码）、menuCode（新菜单编码）、menuName（新菜单名称）和menuSource（菜单来源）作为输入。
查找父菜单: 代码首先通过parentCode查询到所有符合条件的父菜单。
分组处理: 将查询到的父菜单按menuSource进行分组。
创建子菜单:
遍历每个父菜单，并将其id设置为新菜单的parentId，从而建立层级关系。
代码会自动处理中英繁转换：根据输入的menuName，使用ZhConverterUtil工具类自动生成简体 (menuName_CN) 和繁体 (menuName_TW) 名称。
排序值(menuOrder)的确定: 代码会查找当前父菜单下的所有子菜单，获取其中最大的menuOrder值，并将这个最大值赋给新创建的菜单。注意：这里的逻辑是让新菜单的排序值与当前最大的排序值相同，而不是 最大值 + 1。
ID生成与插入: 为新菜单生成业务主键(getBusKey())作为其id，然后调用insertMenu方法将其插入数据库。
返回结果: 方法最终返回一个包含了所有被成功创建的新菜单对象的列表。
    """
    sql = """
    SELECT id, menuName, menuCode FROM `aio-db`.data_examination_menu WHERE parentId IS NULL;
        SELECT id, menuName, parentId, menuOrder FROM `aio-db`.data_examination_menu WHERE appCode = 'AIO_APP' ORDER BY menuOrder;
        SELECT id, menuName, menuCode, menuOrder FROM `aio-db`.data_examination_menu WHERE parentId = 'parent_01' ORDER BY menuOrder;
        SELECT COUNT(*) FROM `aio-db`.data_examination_menu;
        SELECT menuSource, COUNT(id) AS menu_count FROM `aio-db`.data_examination_menu GROUP BY menuSource;
        SELECT id, menuName, menuName_CN, menuName_TW FROM `aio-db`.data_examination_menu WHERE menuName LIKE '%仪表盘%';
        SELECT id, menuName, appCode FROM `aio-db`.data_examination_menu WHERE menuStatus = 0;
        SELECT id, menuName, menuOrder FROM `aio-db`.data_examination_menu WHERE parentId = 'parent_02' ORDER BY menuOrder DESC LIMIT 1;
SELECT COUNT(*) FROM `aio-db`.data_examination_menu WHERE moudleAuth = 1;
        SELECT
    child.menuName AS menu_name,
    parent.menuName AS parent_menu_name
FROM
    `aio-db`.data_examination_menu AS child
LEFT JOIN
    `aio-db`.data_examination_menu AS parent
ON
    child.parentId = parent.id;
    """
    vn.train(ddl=ddl_statement)
    vn.train(documentation=doc)
    vn.train(sql=sql)
    print("✅ 模型训练完成！训练数据已保存在本地 ChromaDB 中。")

    # --- 8. 提问 ---
    print("\n[STEP 5/5] 准备开始提问...")

    question = """
    请你根据 {
          name: '资产变更',
          nameI18n: 'menu.aio-asset-mgr-change',
          key: 'change',
          children: [
            {
              name: '资产变更申请单',
              nameI18n: 'menu.aio-asset-mgr-change-requests-list',
              path: '/aio-asset-mgr/change/requests-list',
              key: 'requests-list'
            },
            {
              name: '资产变更申请单报告',
              nameI18n: 'menu.aio-asset-mgr-change-requests-report',
              path: '/aio-asset-mgr/change/requests-report',
              key: 'requests-report',
       
            }
          ]
        } 
        这个json，帮我写一个insert 到菜单表得语句
    """
    print(f"\n> 你的问题: {question}")

    df_result = vn.ask(question=question, visualize=False)

    print("\n查询结果 (DataFrame):")
    if df_result is not None:
        print(df_result)
    else:
        print("未能获取查询结果或结果为空。")

    print("\n--- 演示完成！ ---")


if __name__ == '__main__':
    main()