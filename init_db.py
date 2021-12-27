import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbsparta_hj

# DB에 저장할 영화들의 출처 url을 가져옵니다.
def get_urls():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get('https://movie.naver.com/movie/sdb/rank/rmovie.naver', headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    trs = soup.select('#old_content > table > tbody > tr')

    urls = []
    for tr in trs:
        a = tr.select_one('td.title > div > a')
        if a is not None:
            base_url = 'https://movie.naver.com/'
            url = base_url + a['href']
            urls.append(url)

    return urls


# 출처 url로부터 영화들의 이미지, 이름, url, 평점순(나중에 좋아요 순위로 바꿀것)을 가져오고 toymovies 콜렉션에 저장합니다.
def insert_movies(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url, headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    image = soup.select_one('meta[property="og:image"]')['content']
    title = soup.select_one('meta[property="og:title"]')['content']
    url = soup.select_one('meta[property="og:url"]')['content']
    # star = soup.select_one('#old_content > table > tbody > tr:nth-child(2) > td.point')

    doc = {
        'image': image,
        'title': title,
        'url': url,
        # 'star': star  //print에 star 추후 추가
    }
    db.toymovies.insert_one(doc)
    print('완료!', image, title, url)


# 기존 mymovies 콜렉션을 삭제하고, 출처 url들을 가져온 후, 크롤링하여 DB에 저장합니다.
def insert_all():
    db.mystar.drop()  # toymovies 콜렉션을 모두 지워줍니다.
    urls = get_urls()
    for url in urls:
        insert_movies(url)


### 실행하기
insert_all()