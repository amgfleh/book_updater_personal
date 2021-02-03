#! python3

# make every action into a function if possible
# try n exp with function attributes
# lists are mutanle, no need to return to change

import ezsheets as ez
import time
import bs4
import requests
import sys
import pprint
import pyinputplus as ppl
import os
print(os.getcwd())


# clearing screen
def clear():
    os.system('cls')


os.chdir('C:\\Users\\Amogh\\Desktop\\Scripts')
# access GoodReads
current_read_shelf = requests.get("https://www.goodreads.com/review/list/31212342-amogh-p?shelf=currently-reading")
try:
    current_read_shelf.raise_for_status()
except Exception as exp:
    print("There was a problem: ", exp)
# find currently reading book, isbn
cr_s = bs4.BeautifulSoup(current_read_shelf.text, "html.parser")
isbn, book_title = cr_s.select("td.field.isbn > div"), cr_s.select("td.field.title > div > a")
# print book name and isbn
for i in range(len(book_title)):
    print(f"Currently reading {len(isbn)} books:")
    current_book = {'ISBN - 10': isbn[i].text.strip(),
                    'Book Title': book_title[i].text.strip()}  # dictionary containing details of current book with keys ISBN - 10, Word Count, Book Titles
    if current_book['ISBN - 10'] == '' or current_book['Book Title'] == '':  # in case details are missing
        print('ISBN or Title not found. Skipping.')
        time.sleep(2)
        clear()
        continue
    # find the book on readinglength using isbn-10
    RL_res = requests.get("https://www.readinglength.com/book/isbn-" + current_book['ISBN - 10'])
    try:
        current_read_shelf.raise_for_status()
    except Exception as exp:
        print("There was a problem: ", exp)
    # access word count
    wl_s = bs4.BeautifulSoup(RL_res.text, 'html.parser')
    word_count = wl_s.select(
        "#__next > div > div.BookStyles-sc-7qtqdh-0.gFBanL > div.Inner__InnerStyles-vj740s-0.etlifP > div > div.book-info > div:nth-child(1) > div > "
        "div:nth-child(2) > p:nth-child(2)")
    word_count = word_count[0].text.strip(' words')
    current_book['Word Count'] = int(word_count.replace(',', ''))
    pprint.pprint(current_book)
    # access spreadsheet in drive
    # try adding verifying existence of spreadsheet named after goodreads id
    # if doesn't exist, create new sheet and save the sheet id for all future ref
    # helpful for app
    book_sheet = ez.Spreadsheet('1QTF4JokD_d6gbL4ky9tiiodmimbT6lC-BB0goDVkq3o')
    current_sheet = time.asctime()[-4:]
    if current_sheet not in book_sheet.sheetTitles:
        book_sheet.createSheet(current_sheet)
    cws = book_sheet[current_sheet]
    book_names = cws.getColumn(1)
    word_count = cws.getColumn(2)
    if current_book['Book Title'] not in book_names:
        if ppl.inputYesNo('Book not updated. Proceed with update?\n') is 'yes':
            # update after consent
            updated_book_names = [x for x in book_names if x != '']
            updated_word_count = word_count[:len(updated_book_names)]
            updated_book_names.insert(-1, current_book['Book Title'])
            updated_word_count.insert(-1, current_book['Word Count'])
            updated_word_count[-1] = f'=SUM(B1:B{len(updated_book_names) - 1})'
            cws.updateColumn(1, updated_book_names)
            cws.updateColumn(2, updated_word_count)
            print('Update finished.')
        else:
            print('Update skipped')
    else:
        print("Book is already updated")
    time.sleep(2)
    clear()

print("Program terminating.")
