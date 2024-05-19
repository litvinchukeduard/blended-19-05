import requests
from bs4 import BeautifulSoup
from decimal import Decimal, getcontext

BASE_URL = 'https://books.toscrape.com/catalogue/category/books/travel_2/index.html'
response = requests.get(BASE_URL)
soup = BeautifulSoup(response.text, 'lxml')

prices = soup.select('.product_price .price_color')

getcontext().prec = 4

sum = Decimal(0)
sum_float = 0
for price in prices:
    current_price = price.text.replace('Â', '').replace('£', '')
    sum += Decimal(current_price)
    sum_float += float(current_price)

print(sum / Decimal(len(prices)))
print(sum_float / len(prices))
