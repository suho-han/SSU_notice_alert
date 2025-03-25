import requests
from bs4 import BeautifulSoup

'''Function to get posts from a given URL and class name'''
def get_posts(url, class_name):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    posts = soup.find_all('div', class_=class_name)

    new_posts = []
    for post in posts:
        title_span = post.find('span')
        title = title_span.text if title_span else None
        link = post.find_parent('a')['href'] if post.find_parent('a') else ""
        if link.startswith('/'):
            full_link = 'http://infocom.ssu.ac.kr' + link
        elif link != "":
            full_link = link
        else:
            full_link = url
        new_posts.append({'title': title, 'link': full_link})
    return new_posts


'''URLs and classes for undergraduate and graduate'''
url_origin_undergrad = 'http://infocom.ssu.ac.kr/kor/notice/undergraduate.php'
url_origin_grad = 'http://infocom.ssu.ac.kr/kor/notice/graduateSchool.php'

new_posts_infocom = get_posts(url_origin_undergrad, 'subject on')
new_posts_infocom_grad = get_posts(url_origin_grad, 'subject on')


'''Function to get posts from SCATCH'''
def get_scatch_posts(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    posts = soup.find_all('div', class_='notice_col3')
    new_posts_scatch = []
    for post in posts:
        title_span = post.find('span', class_='d-inline-blcok m-pt-5')
        title = title_span.text.strip() if title_span else ""
        link = post.find('a')['href'] if post.find('a') else ""
        if link.startswith('http'):
            full_link = link
        elif link != "":
            full_link = 'https://scatch.ssu.ac.kr' + link
        else:
            full_link = url
        new_posts_scatch.append({'title': title, 'link': full_link})
    return new_posts_scatch


url_scatch = 'https://scatch.ssu.ac.kr/%ea%b3%b5%ec%a7%80%ec%82%ac%ed%95%ad/'
new_posts_scatch = get_scatch_posts(url_scatch)

'''Function to get posts from DISU'''
def get_disu_posts(urls):
    new_posts_disu = []
    for url in urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        posts = soup.select('#zcmsprogram > div > table > tbody > tr')
        for post in posts:
            title_td = post.select_one('td.title.noti-tit')
            if title_td:
                category = title_td.select_one('span.hidden-md-up')
                a_tag = title_td.find('a')
                if a_tag:
                    title = '{} {}'.format(category.text.strip(), a_tag.text.strip())
                    link = a_tag['href']
                    if link.startswith('http'):
                        full_link = link
                    else:
                        full_link = 'https://www.disu.ac.kr' + link
                    new_posts_disu.append({'title': title, 'link': full_link})
    return new_posts_disu


base_urls_disu = [
    'https://www.disu.ac.kr/community/notice?cidx=38',
    'https://www.disu.ac.kr/community/notice?cidx=42'
]

new_posts_disu = get_disu_posts(base_urls_disu)

results = {
    'infocom': new_posts_infocom,
    'infocom_grad': new_posts_infocom_grad,
    'scatch': new_posts_scatch,
    'disu': new_posts_disu
}
