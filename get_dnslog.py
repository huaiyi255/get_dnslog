# 通过dnslog平台获取dsnlog地址，以及获得刷新结果
# 通过两个函数，一个函数 中的 xmlhttp.open("GET","/getrecords.php?t="+Math.random(),true); 随机生成一个标志 生成dnslog地址
# 另一个函数通过这个dnslog地址对应的随机数 以及返回的cookie 来获取结果
import time
import requests
import random
import subprocess
import os
import json
from tabulate import tabulate


# 国内网才能请求到这个的dnslog地址，不然返回的状态码就是503
def dnslog_request():
    flag = '.php?t=0.' + str(random.randint(1000000000000000, 9999999999999999))  # 生成一个随机数
    url = "http://www.dnslog.cn/getdomain" + flag
    response = requests.get(url=url, verify=True, timeout=30, proxies=None)
    headers = response.headers  # 获得响应头
    aaa = str(headers['Set-Cookie'])[:-8]
    # print(f"dnslog地址：{response.text},{headers['Set-Cookie']}")
    return {"dnslog_url": response.text, "flag": flag, "cookie": aaa}


# 获得结果需要请求时返回的 Set-Cookie
def dnslog_result(flag1):
    try:
        while True:
            url = "http://www.dnslog.cn/getrecords" + flag1["flag"]
            headers = {'Cookie': flag1['cookie']}
            response = requests.get(url=url, headers=headers, verify=True, timeout=30, proxies=None)
            print(
                f"[+] 当前dnslog地址：{flag1['dnslog_url']}   dnsflag：{flag1['flag'][7:]}   cookie：{flag1['cookie']}\n[+] 缓存如下：\n")
            # print(f"[+] 当前dnslog地址的请求结果为：{response.text}")
            my_list = json.loads(response.text)
            print(tabulate(my_list, headers=["request url", "源ip", "请求时间"]))  # 使用 tabulate 库格式化输出二维数组的元素
            print("\n[=] 3秒后将刷新缓存，按Ctrl+C退出")
            time.sleep(3)
            os.system('cls' if os.name == 'nt' else 'clear')  # 清屏
            print("\n")
    except KeyboardInterrupt:
        pass
        # print("退出")


def main():
    dnslog = dnslog_request()
    print(f"[+] 获取的dnslog地址为：{dnslog['dnslog_url']}")
    print(f"[+] 将对dnslog地址进行ping测试")
    result = subprocess.run(['ping', dnslog["dnslog_url"]], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    print(result.stdout)
    print(f"[+] 开始刷新dnslog地址]")
    dnslog_result(dnslog)
    time.sleep(5)

main()
