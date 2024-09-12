"""
插件

2.21
    新增群汇报功能
"""

import requests
import time
import json
import os


class Function:
    def __init__(self):
        self.Number_of_executions = 0
        ...

    def get_date(self):
        from datetime import datetime
        # 获取当前日期和时间
        now = datetime.now()

        # 格式化日期为 YYMMDD 格式
        formatted_date = now.strftime("%y%m%d")

        self.Number_of_executions += 1
        return formatted_date

    def wjj_sf_cz(self, num_path):
        self.Number_of_executions += 1
        # 判断文件夹是否存在
        if os.path.exists(num_path):
            # print("数据文件夹存在")
            return True
        else:
            # print("数据文件夹不存在")
            return False

    def intercept_license_plate(self, num_str):
        self.Number_of_executions += 1
        import re

        # 定义字符串
        s = num_str

        # 定义正则表达式模式
        pattern = r'_([^_]+)_'

        # 使用正则表达式匹配两个下划线之间的内容
        match = re.search(pattern, s)

        # 判断是否匹配成功
        if match:
            content = match.group(1)
            # print(f"截取到的内容: {content}")
            return content
        else:
            # print("未找到匹配的内容")
            return None

    def w_log(self, num_jl):
        self.Number_of_executions += 1
        f = open("./logfile.log", 'a')
        f.write(num_jl)

class Detect_new_files:
    def __init__(self, num_path):
        self.detect_path = num_path     # 检测新文件路径

        # 获取初始文件夹内容
        self.initial_contents = set(os.listdir(num_path))

        ...
    def jc(self):
        current_contents = set(os.listdir(self.detect_path))    # 最新列表内容

        # 检查新增的内容
        new_contents = current_contents - self.initial_contents

        # 更新内容列表
        self.initial_contents = current_contents

        if new_contents:
            return new_contents
        else:
            return None
class WeChat_push:
    """
    微信测试号推送信息
    """
    def __init__(self):
        # 从测试号信息获取
        self.appID = ""
        self.appSecret = ""

        # 收信人ID即 用户列表中的微信号，
        self.openId = ""

        self.Mass_list = list()     # 群发openid列表

        # 车辆报送模板ID
        self.Vehicle_Submission_id = "oi0HXl_BiIvIjW8SP6DUYhnoXD5Z3bqwti2zySLGgY0"
    def get_access_token(self):
        # 获取access token的url
        url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}' \
            .format(self.appID.strip(), self.appSecret.strip())
        response = requests.get(url).json()
        # print(response)
        access_token = response.get('access_token')
        return access_token

    def send_Vehicle_Submission(self, access_token, message):
        body = {
            "touser": self.openId,
            "template_id": self.Vehicle_Submission_id.strip(),
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

    def Vehicle_Submission(self, message):
        # 1.获取access_token
        access_token = self.get_access_token()
        # 3. 发送消息
        self.send_Vehicle_Submission(access_token, message)

    def send_to_the_user(self, access_token, num_openid, message):
        body = {
            "touser": num_openid,
            "template_id": self.Vehicle_Submission_id.strip(),
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
    def Mass_all(self, message):
        # 1.获取access_token
        access_token = self.get_access_token()
        for zh in self.Mass_list:
            self.send_to_the_user(access_token, zh, message)
class Main:
    def __init__(self):
        # 实例类
        self.function = Function()
        self.dnf = None     # 检测新文件功能类
        self.wechat_push = WeChat_push()    # 发送信息功能类


        self.leadership_car_list = list()   # 汇报车牌
        self.Vehicle_date_path = r'D:/新建文件夹/'     # 检测的车辆日期路径
        self.Log_output_path = './logfile.log'       # 日志输出路径

        self.running = False
        ...
    def class_init(self):
        # 初始化配置
        self.wechat_push.appID = 'wxfe87182bd1371294'
        self.wechat_push.appSecret = '7a6e5a3f118f1f3317f57fb065e7c06a'
        self.wechat_push.openId = 'ogur66Me6Rpbfg6vx7RvUKgGO8AY'
        #   群发人员
        self.wechat_push.Mass_list.append('ogur66Me6Rpbfg6vx7RvUKgGO8AY')
        self.wechat_push.Mass_list.append('ogur66Io8YI85RejzPZUlqAhzYlY')
        #   汇报车
        self.leadership_car_list.append('F416')
        self.leadership_car_list.append('NH00')
        self.leadership_car_list.append('E368')
        self.leadership_car_list.append('7805')
        self.leadership_car_list.append('6351')
        self.leadership_car_list.append('XG86')

        #
        dq_path = self.Vehicle_date_path + self.function.get_date()
        if self.function.wjj_sf_cz(dq_path):
            self.running = True
            self.dnf = Detect_new_files(dq_path)
        else:
            self.running = False
            print("未检测到车辆数据文件")

        # 判断配置
        if not self.leadership_car_list:
            print("未添加汇报车辆将无法收到消息")

    def Run(self):
        while self.running:
            # 检测数据是否正常
            dq_path = self.Vehicle_date_path + self.function.get_date()     # 路径+当天日期
            if self.function.wjj_sf_cz(dq_path):      # 判断数据文件夹是否存在

                new_clb = self.dnf.jc()  # 判断有没有新识别车辆
                if new_clb:
                    for ctp_str in new_clb:

                        # 过滤一车多图片
                        if ctp_str[0] == 'G':
                            c_jtp = ctp_str[0:-4]
                            print(c_jtp)  # 打印来车
                            self.function.w_log(c_jtp+"\n")    # 日志
                            # 截取车牌
                            cp = self.function.intercept_license_plate(ctp_str)
                            # 检测是否是汇报车辆
                            for hbc_jb_str in self.leadership_car_list:
                                if hbc_jb_str in cp:
                                    print("汇报车辆：")

                                    # 优化发送数据
                                    jc_str = ctp_str[0:ctp_str.index('_')]
                                    if jc_str == 'GIn':
                                        jin_chu = '车进园区'
                                    elif jc_str == 'GOut':
                                        jin_chu = '车出园区'
                                    else:
                                        jin_chu = '车过，检测不到进出'
                                    print("    " + cp + jin_chu)
                                    try:
                                        self.wechat_push.Mass_all(cp+jin_chu)
                                    except Exception as bc_wb:
                                        print("数据发送失败\n", bc_wb)
                                else:
                                    ...
            else:
                print("无数据路径")

            time.sleep(5)
            ...



if __name__ == '__main__':
    main_sl = Main()
    main_sl.class_init()
    main_sl.Run()

