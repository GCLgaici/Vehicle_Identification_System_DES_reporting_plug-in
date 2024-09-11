"""
纳米车辆进出汇报检测系统
"""
from datetime import datetime
import time
import requests
import json
import os



# 从测试号信息获取
appID = "wxfe87182bd1371294"
appSecret = "7a6e5a3f118f1f3317f57fb065e7c06a"
#收信人ID即 用户列表中的微信号，见上文
openId = "ogur66Me6Rpbfg6vx7RvUKgGO8AY"
# 车辆报送模板ID
Vehicle_Submission_id = "oi0HXl_BiIvIjW8SP6DUYhnoXD5Z3bqwti2zySLGgY0"

# 检测目录
detect_path = "D:/新建文件夹/"



class Detect_new_files:
    def __init__(self, num_path):
        # 检测目录
        self.detect_path = num_path

        # 获取初始文件夹内容
        self.initial_contents = set(os.listdir(num_path))

        ...
    def jc(self):
        current_contents = set(os.listdir(self.detect_path))

        # 检查新增的内容
        new_contents = current_contents - self.initial_contents

        # 更新内容列表
        self.initial_contents = current_contents

        if new_contents:
            for item in new_contents:
                # print(f"新增内容: {item}")
                ...
            return new_contents
        else:
            return None



def get_access_token():
    # 获取access token的url
    url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}' \
        .format(appID.strip(), appSecret.strip())
    response = requests.get(url).json()
    print(response)
    access_token = response.get('access_token')
    return access_token
def send_Vehicle_Submission(access_token, message):
    body = {
        "touser": openId,
        "template_id": Vehicle_Submission_id.strip(),
        "url": "https://weixin.qq.com",
        "data": {
            "message": {
                "value": message
            },
        }
    }
    url = 'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={}'.format(access_token)
    print(requests.post(url, json.dumps(body)).text)
    ...
def Vehicle_Submission(message):
    # 1.获取access_token
    access_token = get_access_token()
    # 3. 发送消息
    send_Vehicle_Submission(access_token, message)

def wjj_sf_cz(num_path):
    # 判断文件夹是否存在
    if os.path.exists(num_path):
        # print("数据文件夹存在")
        return True
    else:
        # print("数据文件夹不存在")
        return False

def get_date():
    # 获取当前日期和时间
    now = datetime.now()

    # 格式化日期为 YYMMDD 格式
    formatted_date = now.strftime("%y%m%d")

    # 打印格式化后的日期
    # print("格式化后的日期:", formatted_date)
    return formatted_date

# 领导车列表
leadership_car_list = [
    "CBF416",
    "H00",
    "KHE368",
    "057",
    "517",

    "G86"
]
F416 = 'C'
H00 = 'C'
E368 = 'C'
g_057 = 'C'
g_517 = 'C'

if __name__ == '__main__':
    dq_path = detect_path + get_date()
    jc_wj = Detect_new_files(dq_path)
    while True:
        dq_path = detect_path+get_date()
        if wjj_sf_cz(dq_path):      # 判断数据文件夹是否存在
            jc_wj.detect_path = dq_path
            new_cl = jc_wj.jc()     # 判断有没有新识别车辆
            if new_cl:
                for cp_cl in new_cl:
                    # 开始检测是不是领导车
                    for ldc in leadership_car_list:
                        if ldc in cp_cl:
                            print("领导车过", cp_cl)
                            if '416' in cp_cl:
                                if F416 == 'C':
                                    Vehicle_Submission(cp_cl + "车辆进园区")
                                    F416 = 'J'
                                else:
                                    Vehicle_Submission(cp_cl + "车辆出园区")
                                    F416 = 'C'
                            else:
                                Vehicle_Submission(cp_cl + "车辆过大门岗")

        else:
            print("检测不到数据文件夹")


        time.sleep(5)
    # Vehicle_Submission("517")

