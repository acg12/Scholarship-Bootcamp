from bs4 import BeautifulSoup
import requests
import pandas as pd

url = 'http://books.toscrape.com/catalogue/category/books/romance_8/index.html'


def findBooks(soup, n_books):
    items = soup.find_all('li', {'class': 'col-xs-6 col-sm-4 col-md-3 col-lg-3'})
    return items[:n_books]

def findLinks(items):
    links = []
    catalogue_url = 'http://books.toscrape.com/catalogue/'
    for i in items:
        tags_a = i.find('a', href=True)
        link = tags_a.get('href')
        link = link.replace('../../../', '')
        links.append(catalogue_url + '/' + link)
    return links

def findTitle(book):
    title = book.find('h1').getText()
    return title

def findPrice(book):
    price_text = book.find('div', {'class': 'col-sm-6 product_main'}).find('p').getText()
    price = float(price_text[2:])
    return price

def findRating(book):
    rating_p = book.find('p', {'class': 'star-rating'})
    rating = None
    if rating_p.has_attr('class'):
        rating_text = rating_p['class'][1]
        if rating_text == 'Five':
            rating = 5
        elif rating_text == 'Four':
            rating = 4
        elif rating_text == 'Three':
            rating = 3
        elif rating_text == 'Two':
            rating = 2
        else:
            rating = 1
    return rating

def findStock(book):
    stock_text = book.find('p', {'class': 'instock availability'}).text
    stock_text = stock_text.strip().replace('(', '').split(' ')
    stock = int(stock_text[2])
    return stock

def findDetails(links):
    data = {
        'Title': [],
        'Price': [],
        'Rating': [],
        'Stock': []
    }
    
    for i in range(len(links)):
        book_html = requests.get(links[i]).text
        book = BeautifulSoup(book_html, 'html.parser')  
        
        data['Title'].append(findTitle(book))
        data['Price'].append(findPrice(book))
        data['Rating'].append(findRating(book))
        data['Stock'].append(findStock(book))
    return data

def saveToCsv(data):
    df = pd.DataFrame(data)
    df.to_csv('romance_books.csv', index=True)

def scrapeRomanceBooks(url, n_books):
    index_html = requests.get(url).text
    soup = BeautifulSoup(index_html, 'html.parser')
    items = findBooks(soup, n_books)
    links = findLinks(items)
    data = findDetails(links)
    saveToCsv(data)
    
scrapeRomanceBooks(url, 10)
print('All done! :D')
