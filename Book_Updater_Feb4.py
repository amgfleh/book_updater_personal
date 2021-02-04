import os
import pprint
import time
import bs4
import ezsheets as ez
import pyinputplus as ppl
import requests
import sys

# only thing to edit is at the very end

os.chdir(os.path.dirname(__file__))  # make sure your dir has the credentials-sheets.json, token-drive.pickle, token-sheets.pickle files


def clear():
    os.system('cls')


# fetch isbn of all current reading books
def fetch_isbn(current_read_url):
    # access current read
    current_read_shelf = requests.get(current_read_url)
    try:
        current_read_shelf.raise_for_status()
    except Exception as exp:
        print("There was a problem: ", exp)
    # find isbn of current reading books:
    cr_s = bs4.BeautifulSoup(current_read_shelf.text, "html.parser")
    isbn_list = []
    isbn, title = cr_s.select("td.field.isbn > div"), cr_s.select("td.field.title > div > a")
    for i, a in enumerate(isbn):
        if a.text.strip() == '':
            print("ISBN not found for ", book_title[i].text.strip())
        else:
            isbn_list.append(a.text.strip())
    books = []
    # fetch metadata
    for i, isbn in enumerate(isbn_list):
        word_count = fetch_metadata(isbn)
        if word_count != None:
            books.append({'Title': title[i].text.strip(), 'Word_Count': word_count, 'ISBN10': isbn})
    print(books)
    return books


# fetch word count from readinglength.com
def fetch_metadata(isbn):
    RL_res = requests.get("https://www.readinglength.com/book/isbn-" + isbn)
    try:
        RL_res.raise_for_status()
    except Exception as exp:
        print("There was a problem: ", exp)
        return None
    # access word count
    wl_s = bs4.BeautifulSoup(RL_res.text, 'html.parser')
    word_count = wl_s.select(
            "#__next > div > div.BookStyles-sc-7qtqdh-0.gFBanL > div.Inner__InnerStyles-vj740s-0.etlifP > div > div.book-info > div:nth-child(1) > div > "
            "div:nth-child(2) > p:nth-child(2)")
    return word_count[0].text.strip(' words')


def update_sheet(books, sheet_id):
    book_sheet = ez.Spreadsheet(sheet_id)
    current_sheet = str(time.gmtime().tm_year)
    if current_sheet not in book_sheet.sheetTitles:
        print("Creating new sheet: ", current_sheet)
        book_sheet.createSheet(current_sheet)
    for current_book in books:
        book_sheet.refresh()  # make sure upgrade is registered in case multiple books are there
        cws = book_sheet[current_sheet]
        book_names = cws.getColumn(1)
        word_count = cws.getColumn(2)
        pprint.pprint(current_book)
        if current_book['Title'] not in book_names:
            if ppl.inputYesNo('Book not updated. Proceed with update?\n') is 'yes':
                # update after consent
                updated_book_names = [x for x in book_names if x != '']
                updated_word_count = word_count[:len(updated_book_names)]
                num_of_books = len(updated_book_names)
                updated_book_names.insert(num_of_books, current_book['Title'])
                updated_word_count.insert(num_of_books, current_book['Word_Count'])
                updated_word_count.insert(num_of_books + 1, f'=SUM(B1:B{num_of_books + 1})') #add total of books read so far
                cws.updateColumn(1, updated_book_names)
                cws.updateColumn(2, updated_word_count)
                print('Update finished.')
            else:
                print('Update skipped')
        else:
            print("Book is already updated")
        time.sleep(2)
        clear()


books = fetch_isbn("https://www.goodreads.com/review/list/31212342-amogh-p?shelf=currently-reading")  # replace the link to your goodreads currently readying shelf
# that is set to public, or use mine to see what i am reading :)

update_sheet(books, '1QTF4JokD_d6gbL4ky9tiiodmimbT6lC-BB0goDVkq3o')  # replace the second argument with the sheet ID of your choice, where you want to save your Data
