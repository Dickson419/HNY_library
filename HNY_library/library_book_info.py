import csv
import datetime
import os.path

book_status = "data/student_books_in_out.csv"

def get_status(row):
    """Helper function to check for a true or false entry for books which are checked out"""
    if row["Check Out"] == "True":
        return "Out"
    else:
        return "In"

def all_books_status():
    """Function to get all books"""
    books = []

    with open(book_status, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        for row in reader:
            #key = (row["Title"], row["Student"])
            status = get_status(row)
            books.append({
                "title":row["Title"],
                "author": row["Author"],
                "student": row["Student"],
                "dtg": row["DTG"],
                "status": status
            })
    return [book for book in books if book["status"] == "Out"]


def log_book_returns(student, title, author, take_out=False, return_book=False):
    """
    Keeps track of whether a book is returned.
    IF return_book is True the checkout should be removed
    """
    student = student.title().strip()
    title = title.title().strip()
    author = author.title().strip()

    file_exists = os.path.isfile(book_status)

    #read existing rows
    rows = []
    if file_exists:
        #open and read the file
        with open(book_status, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            rows = list(reader)

    updated_rows = [] #list for updated information
    #if returning check all rows
    for item in rows:
        #check if this row matches the student and book
        if item["Title"] == title and item["Student"] == student:
            #skip this as it is being returned...
            continue
        updated_rows.append(item)

    if take_out:
        updated_rows.append({
            "DTG":datetime.datetime.now().strftime("%m/%d/%Y/%H%M"),
            "Student": student,
            "Title": title,
            "Author":author,
            "Check Out": str(take_out),
            "Return": str(return_book)
        })

    #write back all updated rows
    with open(book_status, "w", newline="",encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["DTG","Student","Title","Author","Check Out","Return"])
        writer.writeheader()
        writer.writerows(updated_rows)

