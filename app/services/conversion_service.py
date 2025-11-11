import opencc
import translators as ts
from markdownify import markdownify as md
import asyncio
import sqlparse
import re
import json
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


def generate_api_markdown(postman_data: dict) -> str:
    """根据导出的接口文档 JSON 生成 Markdown 文本。

    期望的 JSON 结构示例：
    {
      "name": "项目接口",
      "requests": [
        {
          "name": "获取用户",
          "method": "GET",
          "endpoint": "/api/users",
          "params": [{"key": "id", "value": "1", "description": "用户ID", "active": true}],
          "headers": [{"key": "Authorization", "value": "Bearer xxx", "active": true}],
          "body": {"body": "{\n  \"name\": \"Tom\"\n}"}
        }
      ]
    }
    """

    markdown = f"# {postman_data.get('name', '接口文档')}\n\n"

    requests = postman_data.get('requests', []) or []
    for i, request in enumerate(requests):
        # 标题与编号
        markdown += f"## {i + 1}.{request.get('name', '未命名接口')}\n\n"

        # 方法
        markdown += f"**方法**: {request.get('method', '')}\n\n"

        # 端点
        markdown += f"**端点**: `{request.get('endpoint', '')}`\n\n"

        # 请求参数
        params = request.get('params') or []
        if isinstance(params, list) and len(params) > 0:
            markdown += "### 请求参数\n\n"
            params_table = []
            for param in params:
                try:
                    if param.get('active', False):
                        params_table.append(
                            f"| {param.get('key', '')} | {param.get('value', '')} | {param.get('description', '')} |")
                except AttributeError:
                    # 非字典项，跳过
                    continue

            if params_table:
                markdown += "| 参数名 | 值 | 描述 |\n"
                markdown += "| ------ | --- | ---- |\n"
                markdown += "\n".join(params_table) + "\n\n"

        # 请求头
        headers = request.get('headers') or []
        if isinstance(headers, list) and len(headers) > 0:
            markdown += "### 请求头\n\n"
            headers_table = []
            for header in headers:
                try:
                    if header.get('active', False):
                        headers_table.append(f"| {header.get('key', '')} | {header.get('value', '')} |")
                except AttributeError:
                    continue

            if headers_table:
                markdown += "| 键 | 值 |\n"
                markdown += "| --- | --- |\n"
                markdown += "\n".join(headers_table) + "\n\n"

        # 请求体
        body_obj = request.get('body') or {}
        body_content = None
        if isinstance(body_obj, dict):
            body_content = body_obj.get('body')

        if body_content:
            body_content_str = str(body_content)
            if body_content_str.strip():
                markdown += "### 请求体\n\n"
                try:
                    # 处理可能存在的转义字符，确保JSON正确解析
                    normalized = (
                        body_content_str.replace('\\n', '\n')
                        .replace('\\r', '\r')
                        .replace('\\t', '\t')
                    )
                    body_json = json.loads(normalized)
                    pretty_body = json.dumps(body_json, indent=2, ensure_ascii=False)
                    lines = pretty_body.split('\n')
                    numbered_lines = [f" {line}" for line in lines]
                    markdown += "```json\n" + "\n".join(numbered_lines) + "\n```\n\n"
                except json.JSONDecodeError:
                    # 如果不是有效的JSON，则原样显示
                    normalized = (
                        body_content_str.replace('\\n', '\n')
                        .replace('\\r', '\r')
                        .replace('\\t', '\t')
                    )
                    lines = normalized.split('\n')
                    numbered_lines = [f" {line}" for line in lines]
                    markdown += "```json\n" + "\n".join(numbered_lines) + "\n```\n\n"

        # 响应示例（支持从请求的 responses 中读取标题与示例体）
        responses = request.get('responses') or request.get('response') or []

        def _extract_response_title_and_body(resp_item):
            title = None
            body = None
            if isinstance(resp_item, dict):
                title = resp_item.get('name') or resp_item.get('title')
                # 直接字段
                body = resp_item.get('body') or resp_item.get('example')
                # examples 列表
                if not body:
                    examples = resp_item.get('examples')
                    if isinstance(examples, list) and len(examples) > 0:
                        first_ex = examples[0]
                        if isinstance(first_ex, dict):
                            body = first_ex.get('body') or first_ex.get('value')
                # OpenAPI 风格 content
                if not body:
                    content = resp_item.get('content')
                    if isinstance(content, dict):
                        for _, media in content.items():
                            if isinstance(media, dict):
                                body = media.get('example')
                                exs = media.get('examples')
                                if not body and isinstance(exs, dict):
                                    # 取第一个 examples 的 value
                                    for _, ex in exs.items():
                                        if isinstance(ex, dict):
                                            body = ex.get('value')
                                            if body:
                                                break
                            if body:
                                break
            return title, body

        heading = "### 响应"
        resp_title = None
        resp_body = None

        if isinstance(responses, list) and len(responses) > 0:
            # 优先选 active 的响应，否则取第一个
            active_resp = None
            for r in responses:
                try:
                    if isinstance(r, dict) and r.get('active', False):
                        active_resp = r
                        break
                except AttributeError:
                    continue
            candidate = active_resp or responses[0]
            resp_title, resp_body = _extract_response_title_and_body(candidate)
        elif isinstance(responses, dict) and len(responses) > 0:
            # 若为字典，取第一个项
            first_key = next(iter(responses.keys()))
            candidate = responses.get(first_key)
            # 若 key 更像标题，使用之
            resp_title = first_key
            extra_title, resp_body = _extract_response_title_and_body(candidate)
            if extra_title:
                resp_title = extra_title

        if resp_title:
            heading = f"### 响应：{resp_title}"

        markdown += heading + "\n\n"

        if resp_body:
            body_str = str(resp_body)
            try:
                normalized = (
                    body_str.replace('\\n', '\n')
                    .replace('\\r', '\r')
                    .replace('\\t', '\t')
                )
                body_json = json.loads(normalized)
                pretty_body = json.dumps(body_json, indent=2, ensure_ascii=False)
                lines = pretty_body.split('\n')
                numbered_lines = [f" {line}" for line in lines]
                markdown += "```json\n" + "\n".join(numbered_lines) + "\n```\n\n"
            except json.JSONDecodeError:
                normalized = (
                    body_str.replace('\\n', '\n')
                    .replace('\\r', '\r')
                    .replace('\\t', '\t')
                )
                lines = normalized.split('\n')
                numbered_lines = [f" {line}" for line in lines]
                markdown += "```\n" + "\n".join(numbered_lines) + "\n```\n\n"
        else:
            # 默认示例
            markdown += (
                "```json\n {\n     \"code\": \"0\",\n     \"errMsg\": \"success\",\n     \"data\": null\n }\n```\n\n"
            )

        # 分隔符
        markdown += "---\n\n"

    return markdown