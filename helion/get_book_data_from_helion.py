import requests
import bs4
import json

def get_soup(url):
    res = requests.get(url) 
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    return soup

def get_author(soup):
    author = soup.select('div .author')
    authorstring=author[0].get_text().strip()
    return authorstring[8:].strip()

def get_description(soup):
    description = []
    for line in soup.select('.center-body-center'):
        description. append(line.get_text())
        return description

def get_author_info(soup):
    authorinfo = soup.select('.author-description-book-page-full')
    return authorinfo[0].get_text()


if __name__ == '__main__':

    file = 'my_helion_books.txt'    
    all_books_info = {}

    with open(file, 'r') as f:
        for url in f:
            info = dict()
            soup = get_soup(url.strip())
            meta = soup.findAll('meta')
            # tytuł należy podzielić na tytuł podtytuł oraz nr wydania jeśli jest
            info['title'] = meta[3]['content']
            info['img'] = meta[4]['content']
            info['isbn'] = meta[11]['content']
            info['author'] = get_author(soup)
            try:
                info['author_info'] = get_author_info(soup)
            except:
                info['author_info'] = ''
            info['description'] = get_description(soup)
            info['year'] = soup.find("dt", string="Data wydania książki drukowanej:").findNext('dd').string.strip()[:4]
            info['publisher'] = soup.find("dt", string="Wydawnictwo:").findNext('dd').get_text().strip()
            info['pages'] = soup.find("dt", string="Stron:").findNext('dd').get_text().strip()
            try:
                info['oryginal_title'] = soup.find("dt", string="Tytuł oryginału:").findNext('dd').get_text().strip()
            except:
                info['oryginal_title'] = ''
            try:
                info['amazon_link'] = soup.find("dt", string="Tytuł oryginału:").findNext('dd').a['href']
            except:
                info['amazon_link'] = ''
            try:
                info['translation_by'] = soup.find("dt", string="Tłumaczenie:").findNext('dd').get_text().strip()
            except:
                info['translation_by'] = ''
            info['link_helion'] = meta[22]['content']
            try:
                info['code'] = soup.find("dt", string="Przykłady na ftp").a['href']
            except:
                info['code'] = ''
            all_books_info[url.strip()] = info
    

    with open('helionbooksinfo.json', 'w') as f:
        f.write(json.dumps(all_books_info))