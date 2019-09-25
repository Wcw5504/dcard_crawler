from bs4 import BeautifulSoup
import requests
import json
import os

# 取得json並轉換為dict
def get_json(url):
    r = requests.get(url).text
    return json.loads(r)

api = "https://www.dcard.tw/_api"

# 從文章列表取得文章ID(依時間排序))
def get_article(board, last):
    source = f"{api}/forums/{board}/posts?popular=false&limit=30"
    
    # 換頁時，於網址尾端加上前頁ID
    if last:
        source += "&before=" + last
    return get_json(source)

# 取得文章內文
def get_post(id):
    source = f"{api}/posts/{id}"
    return get_json(source)

# 取得文章回應
def get_comment(id):
    source = f"{api}/posts/{id}/comments?popular=false&limit=30"
    return get_json(source)

board = input("請輸入看板英文名: ")
last = 0
k = 1

if not(os.path.exists(f"./{board}/")):
    os.mkdir(board)

for i in range(5):
    a_list = get_article(board, last)

    # 取得尾篇文章的ID
    last = str(a_list[-1]["id"])

    for j in a_list:
        article = {"post": get_post(j["id"]), "comment": get_comment(j["id"])}
        
        with open(f"./{board}/{k:03d}.json", "w+", encoding="UTF-8") as f:
            f.write(json.dumps(article, ensure_ascii=False, indent=2))
        k += 1
