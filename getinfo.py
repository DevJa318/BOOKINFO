"""

GET INFO ABOUT BOOKS - title, subtitle, authors, publisher, language, isbn10, isbn13, 
	pages, rating, description, price, link to image, link to book on itbook.store site, pdf if there is.

input:
	txtfile variable - path to txtfile with year and title of books one by line.
	ie:
	2022 Learning DevOps.pdf
	2022 Learning Modern Linux.pdf
	2020 PYTHON ONE-LINERS.pdf

output:
	foundapidata.json file with info of found books.
	ie:
	{
	"2022 Learning DevOps.pdf": {"error": "0", "title": "Learning DevOps, 2nd Edition", "subtitle": "A comprehensive guide to accelerating DevOps culture adoption with Terraform, Azure DevOps, Kubernetes, and Jenkins", "authors": "Mikael Krief", "publisher": "Packt Publishing", "language": "English", "isbn10": "1801818967", "isbn13": "9781801818964", "pages": "560", "year": "2022", "rating": "0", "desc": "In the implementation of DevOps processes, the choice of tools is crucial to the sustainability of projects and collaboration between developers and ops. This book presents the different patterns and tools for provisioning and configuring an infrastructure in the cloud, covering mostly open source t...", "price": "$44.99", "image": "https://itbook.store/img/books/9781801818964.png", "url": "https://itbook.store/books/9781801818964"}, 
	"2022 Learning Modern Linux.pdf": {"error": "0", "title": "Learning Modern Linux", "subtitle": "A Handbook for the Cloud Native Practitioner", "authors": "Michael Hausenblas", "publisher": "O'Reilly Media", "language": "English", "isbn10": "1098108949", "isbn13": "9781098108946", "pages": "258", "year": "2022", "rating": "4", "desc": "If you use Linux in development or operations and need a structured approach to help you dive deeper, this book is for you. Author Michael Hausenblas also provides tips and tricks for improving your workflow with this open source operating system. Whether you&#039;re a developer, software architect,...", "price": "$44.71", "image": "https://itbook.store/img/books/9781098108946.png", "url": "https://itbook.store/books/9781098108946"},
	"2020 PYTHON ONE-LINERS.pdf": {"error": "0", "title": "Python One-Liners", "subtitle": "Write Concise, Eloquent Python Like a Professional", "authors": "Christian Mayer", "publisher": "No Starch Press", "language": "English", "isbn10": "1718500505", "isbn13": "9781718500501", "pages": "216", "year": "2020", "rating": "5", "desc": "Python One-Liners will teach you how to read and write &quot;one-liners&quot;: concise statements of useful functionality packed into a single line of code. You&#039;ll learn how to systematically unpack and understand any line of Python code, and write eloquent, powerfully compressed Python like an...", "price": "$39.95", "image": "https://itbook.store/img/books/9781718500501.png", "url": "https://itbook.store/books/9781718500501", "pdf": {"Chapter 2": "https://itbook.store/files/9781718500501/chapter2.pdf"}},
	}

	checkyearapidata.json file if there was correct title but with different name	
	notfound.txt file with year and titles of books that hasn't been found

"""

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

    txtfile = 'allbooksuniq.txt'

    datafile = open('foundapidata.json', 'w')
    datafilecheckyear = open('checkyearapidata.json', 'w')

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