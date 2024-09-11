import re

# 定义字符串
s = "GIn_京A8NH00_181322716.jpg"

# 定义正则表达式模式
pattern = r'_([^_]+)_'

# 使用正则表达式匹配两个下划线之间的内容
match = re.search(pattern, s)

# 判断是否匹配成功
if match:
    content = match.group(1)
    print(f"截取到的内容: {content}")
else:
    print("未找到匹配的内容")
