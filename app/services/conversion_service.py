import opencc
import translators as ts
from markdownify import markdownify as md
import asyncio
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
        result = await loop.run_in_executor(
            None,  # 使用默认的线程池执行器
            ts.translate_text, # 要执行的阻塞函数
            text, # 传递给函数的参数
            'bing', # translator 参数
            target_lang # to_language 参数
        )
        return result
    except Exception as e:
        return f"Translation failed: {e}"


# HTML 转 Markdown
def convert_html_to_markdown(html_content: str) -> str:
    return md(html_content)