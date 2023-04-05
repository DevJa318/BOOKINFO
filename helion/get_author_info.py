import requests
import bs4
import json

def get_soup(url):
    res = requests.get(url) 
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    return soup

def get_author_info(soup):
    author_info = []
    authorinfo = soup.select('.author-description-book-page-full')
    for author in authorinfo:
        author_info.append(author.getText())
    return author_info

if __name__ == '__main__':

    file = 'my_helion_books.txt'    
    all_books_info = {}

    with open(file, 'r') as f:
        for url in f:
            info = dict()
            soup = get_soup(url.strip())
            try:
                info['author_info'] = get_author_info(soup)
            except:
                info['author_info'] = ''
            all_books_info[url.strip()] = info
    
    with open('helionauthorinfo.json', 'w') as f:
        f.write(json.dumps(all_books_info))