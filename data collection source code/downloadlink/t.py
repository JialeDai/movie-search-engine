import requests
import requests_cache

requests_cache.install_cache('demo_cache') # 为 requests 建立缓存，避免每次执行都去请求一次网页，造成时间浪费

# 把我们的爬虫伪装成浏览器，否则服务器会拒绝你的请求
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
}

response = requests.get("http://www.dy2018.com/html/gndy/dyzz/index.html", headers=headers)
html_doc = response.content.decode('gbk') # 由于此网页是 gb2312 编码的，需要转码成 utf8，但 python 貌似不支持 gb2312，所以用 gbk
print(html_doc)