import hashlib

def getMd5(url):
    # 判断url如果为unicode编码，则转换为utf-8
    if isinstance(url, str):
        url  = url.encode('utf-8')
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()

if __name__ == "__main__":
    print(getMd5("https://www.baidu.com".encode('utf-8')))