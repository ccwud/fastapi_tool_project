def calculate_starrocks_varchar_length(text: str, is_enterprise=False) -> int:
    """计算字符串在 StarRocks 中的 VARCHAR 所需长度"""
    max_length = 1048576 if is_enterprise else 65533  # 根据版本选择上限
    return min(len(text), max_length)

# 示例
sample_texts = [
    "Hello, World!"       # 超长字符串
]

for text in sample_texts:
    length = calculate_starrocks_varchar_length(text, is_enterprise=True)
    print(f"文本: '{text[:20]}...' → 长度: {len(text)} 字符 → StarRocks VARCHAR 需: {length} 字符")