import requests
import hashlib
import json
import re
import os


#创建文件夹保存作品
os.chdir(os.path.dirname(os.path.abspath(__file__)))  #切换当前工作目录到程序所在文件夹
folder = 'like'
txt = 'like\\hash.txt'
if not os.path.exists(folder):  #创建我的喜欢文件夹
    os.makedirs(folder)
if not os.path.exists(txt):
    open(txt, 'w')


#创建集合储存txt中的哈希值
existing_hashes = set()
with open(txt, 'r') as f:
    for line in f:
        existing_hashes.add(line.strip())

#设置cookie
cookie = ''

#构建请求
header = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36 Edg/140.0.0.0",
    'Cookie':cookie,
    "referer":"https://www.lofter.com/like",
    "content-type": "text/plain",
}


#索引每次增加的值应等于单次获取的作品数量，默认值为 20 0.
amount = 10   #获取的作品数量
index = 0    #起始索引

#DWR请求数据
data = f"""callCount=1
scriptSessionId=${{scriptSessionId}}
c0-scriptName=PostBean
c0-methodName=getFavTrackItem
c0-id=0
c0-param0=number:{amount}
c0-param1=number:{index}
batchId=123456"""



response = requests.post('https://www.lofter.com/dwr/call/plaincall/PostBean.getFavTrackItem.dwr',headers=header,data=data)
print(response)

#解析DWR响应 
dwr = response.text
matches = re.findall(r'originPhotoLinks\s*=\s*"(.+?)";', dwr)

#处理结果获得图片url并下载图片
i = 0
for element in matches:
    fixed = element.replace('\\"', '"')
    data = json.loads(fixed)
    raw_links = [item["raw"] for item in data if "raw" in item]

    for link in raw_links:
        i += 1 
        
        if 'https://nos.netease.com' in link:
            link = link.replace('nos.netease.com/','')
            pop = 14
            link = link[:pop] + '.lf127.net' +link[pop:]

        image = requests.get(link) 
        hash_val = hashlib.md5(image.content).hexdigest()

        if hash_val in existing_hashes:
            continue
        
        else:
            with open(txt, 'a') as f:
                f.write(hash_val + '\n')

            path = os.path.join(folder,f'image{i}.jpg')
            open(path, 'wb').write(image.content)

print('complete')
