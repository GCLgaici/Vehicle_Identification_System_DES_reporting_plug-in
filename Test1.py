import os
import time

# 定义要监控的目录
directory = 'D:/新建文件夹/'

# 获取初始文件夹内容
initial_contents = set(os.listdir(directory))

while True:
    time.sleep(4)  # 每隔10秒检查一次
    current_contents = set(os.listdir(directory))
    # print(current_contents)

    # 检查新增的内容
    new_contents = current_contents - initial_contents
    print(new_contents)
    if new_contents:
        for item in new_contents:
            print(f"新增内容: {item}")

    # 更新内容列表
    initial_contents = current_contents
