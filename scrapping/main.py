import requests
from bs4 import BeautifulSoup

BASE_URL = 'https://books.toscrape.com/'
response = requests.get(BASE_URL)
soup = BeautifulSoup(response.text, 'lxml')

def make_normal_url(url):
    while not url[0].isalpha() and not url[0].isnumeric():
        url = url[1:]
    return url

def get_categories():
    response = requests.get(BASE_URL)
    soup = BeautifulSoup(response.text, 'lxml')
    categories = soup.select('ul ul li a')
    result = []
    for category in categories:
        link = category.attrs.get("href")
        if link is None:
            continue
        result.append(
            {
                'name': category.get_text(strip=True),
                'url': f'{BASE_URL}{link}'
            }
        )
    return result

def get_books_from_category(categories):
    result = {}
    for category in categories:
        url = category.get('url')
        if url is None:
            continue
        has_next_page = True
        book_links = []
        while has_next_page:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'lxml')
            articles = soup.find_all('article', class_='product_pod')
            for article in articles:
                article_url = article.find('a').attrs.get('href')
                if article_url is None:
                    continue
                article_url = make_normal_url(article_url)
                book_links.append(f'{BASE_URL}catalogue/{article_url}')

            next_page = soup.find('li', class_='next')
            has_next_page = next_page is not None
            if has_next_page:
                next_page = next_page.find('a').attrs.get('href')
                urls = url.split('/')
                urls = urls[:-1]
                urls.append(next_page)
                url = '/'.join(urls)
        result[category['name']] = book_links
        print(result)
    return result

# ul_list = soup.find_all('ul', class_=['nav'])
categories = get_categories()

print(get_books_from_category(categories))



