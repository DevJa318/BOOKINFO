import requests
import json
import os


search1 = '2017 Python Testing with pytest'
APISEARCH = 'https://api.itbook.store/1.0/search/'
APIBYISBN = 'https://api.itbook.store/1.0/books/'

def get_json(link,search):
    url = link + search
    res = requests.get(url)
    api = json.loads(res.text)
    return api

def get_isbn(search, start=0):
    api = get_json(APISEARCH, search)
    isbn = api['books'][start]['isbn13']
    return isbn

def get_data(isbn):
    api = get_json(APIBYISBN, isbn)
    return api

def first_check(book_name, data):
    if book_name[:4] == data['year'] and book_name[5:15].lower() == data['title'][:10].lower():
        return True
    else:
        return False
    
def second_check(book_name, data):
    if book_name[5:15].lower() == data['title'][:10].lower() \
            and int(book_name[:4]) == int(data['year']) \
                or int(book_name[:4]) == int(data['year'])+1 \
                or int(book_name[:4]) == int(data['year'])-1:
        return True
    else:
        return False

if __name__ == '__main__':
    datafile = open('foundapidata.json', 'w')
    datafilecheckyear = open('checkyearapidata.json', 'w')
    txtfile = 'allbooksuniq.txt'
    datadict = {}
    datadictcheckyear = {}
    notfound = []

    with open(txtfile) as f:
        for book_name in f:
            try:
                book_name = os.path.basename(book_name).strip()
                isbn = get_isbn(book_name)
                data = get_data(isbn)
                if first_check(book_name, data):
                    datadict[book_name.strip()] = data
                elif second_check(book_name, data):
                    datadictcheckyear[book_name.strip()] = data
                else:
                    get_isbn(book_name, start=1)
                    get_data(isbn)
                    if first_check(book_name, data):
                        datadict[book_name.strip()] = data
                    elif second_check(book_name, data):
                        #print("WARNING: Different year: Pobieram:" + book_name.upper() + "do bazy danych")
                        datadictcheckyear[book_name.strip()] = data
                    else:
                        print('ERROR:' + book_name.upper() + ' dodane do listy brakujących')
                        notfound.append(book_name)
            except:
                print(book_name)

    datafile.write(json.dumps(datadict))
    datafile.close()
    datafilecheckyear.write(json.dumps(datadictcheckyear))
    datafilecheckyear.close()

    with open('notfound.txt', 'w') as f:
        for book in notfound:
            f.write(book)
            f.write('')
