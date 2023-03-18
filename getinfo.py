import requests
import json

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

if __name__ == '__main__':
    datafile = open('foundapidata.json', 'a')
    datafilecheckyear = open('checkyearapidata.json', 'a')
    txtfile = 'allbooks.txt'
    datadict = {}
    datadictcheckyear = {}
    notfound = []

    with open(txtfile) as f:
        for book_name in f:
            book_name = book_name.strip()
            isbn = get_isbn(book_name)
            data = get_data(isbn)
            try:
                if book_name[:4] == data['year'] and book_name[5:15].lower() == data['title'][:10].lower():
                    #print("OK: Pobieram:" + book_name.upper() + "do bazy danych")
                    datadict[book_name] = data
                elif book_name[5:15].lower() == data['title'][:10].lower() and int(book_name[:4]) == int(data['year']) or int(book_name[:4]) == int(data['year'])+1 or int(book_name[:4]) == int(data['year'])-1:
                    #print("WARNING: Different year: Pobieram:" + book_name.upper() + "do bazy danych")
                    datadictcheckyear[book_name] = data
                else:
                    get_isbn(book_name, start=1)
                    get_data(isbn)
                    if book_name[:4] == data['year'] and book_name[5:15].lower == data['title'][:10].lower():
                        #print("OK: Pobieram:" + book_name.upper() + "do bazy danych")
                        #print(data)
                        datadict[book_name] = data
                    elif book_name[5:15].lower() == data['title'][:10].lower() and int(book_name[:4]) == int(data['year']) or int(book_name[:4]) == int(data['year'])+1 or int(book_name[:4]) == int(data['year'])-1:
                        #print("WARNING: Different year: Pobieram:" + book_name.upper() + "do bazy danych")
                        datadictcheckyear[book_name] = data
                    else:
                        print('ERROR:' + book_name.upper() + ' dodane do listy brakujących')
                        notfound.append(book_name)

            except:
                print('NOT INT: ' + book_name)
                notfound.append(book_name)

    datafile.write(json.dumps(datadict))
    datafile.close()
    datafilecheckyear.write(json.dumps(datadictcheckyear))
    datafilecheckyear.close()

    with open('notfound.txt', 'w') as f:
        for book in notfound:
            f.write(book)