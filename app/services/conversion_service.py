import opencc
import translators as ts
from markdownify import markdownify as md
import asyncio
import sqlparse
import re
# 简繁转换
# 修正后的代码
s2t_converter = opencc.OpenCC('s2t')  # 简体到繁体
t2s_converter = opencc.OpenCC('t2s')  # 繁体到简体


def convert_to_traditional(text: str) -> str:
    return s2t_converter.convert(text)


def convert_to_simplified(text: str) -> str:
    return t2s_converter.convert(text)


# 中英文翻译
async def translate_text_async(text: str, target_lang: str) -> str:
    loop = asyncio.get_running_loop()
    try:
        # 使用 run_in_executor 将阻塞的IO操作放入线程池执行
        # 完整传递所有必要参数，包括from_language
        result = await loop.run_in_executor(
            None,  # 使用默认的线程池执行器
            lambda: ts.translate_text(
                text,  # 要翻译的文本
                translator='google',  # 使用更稳定的Google翻译
                from_language='auto',  # 自动检测源语言
                to_language=target_lang,  # 目标语言
                timeout=10  # 设置超时时间
            )
        )
        return result
    except Exception as e:
        return f"翻译失败: {str(e)}"


# HTML 转 Markdown
def convert_html_to_markdown(html_content: str) -> str:
    return md(html_content)


# ... (all your other service functions like translate_text_async, etc.)

def compress_sql(sql_query: str) -> str:
    """
    Compresses a formatted SQL query into a single line.
    - Strips comments.
    - Replaces newlines and multiple spaces with a single space.
    """
    # Use sqlparse to safely strip comments and handle basic formatting.
    # This is much more robust than simple string manipulation.
    formatted_sql = sqlparse.format(sql_query, strip_comments=True)

    # Replace newlines with a single space.
    one_line_sql = formatted_sql.replace('\n', ' ')

    # Use a regular expression to replace any sequence of multiple whitespace
    # characters with a single space.
    compressed_sql = re.sub(r'\s+', ' ', one_line_sql).strip()

    return compressed_sql