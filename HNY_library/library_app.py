import csv, os, datetime
import threading
from flask import Flask, render_template, request
from library_book_info import all_books_status, log_book_returns
from usb_backup import run_backups
#gill sans MT
app = Flask(__name__)

book_data = "data/student_books_in_out.csv"

threading.Thread(target=run_backups, daemon=True).start()

def ensure_csv():
    """Make sure the csv is created before the rest of the application runs"""
    os.makedirs(os.path.dirname(book_data), exist_ok=True)
    if not os.path.isfile(book_data):
        with open(book_data, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            #csv file headings
            writer.writerow(["DTG", "Student", "Title", "Author", "Check Out", "Return"])


#render the template to view the content page - see the index.html!
@app.route("/")
def home():
    ensure_csv()
    books = all_books_status()
    return render_template("index.html", books=books)



@app.route("/submit", methods=["POST"])
def submit():
    """What happens when the submit button is pressed on the font-end"""
    ensure_csv()

    student = request.form.get("Student")
    title = request.form.get("Book-title")
    author = request.form.get("Book-author")
    take_out = request.form.get("Take-out")
    return_book = request.form.get("Return")

    #convert the on/off from checkboxes to be boolean values
    #take_out = bool(request.form.get("Take-out"))
    #return_book = bool(request.form.get("Return"))

    #check if file exists
    file_exists = os.path.isfile(book_data)

    log_book_returns(student,title,author,take_out=take_out,return_book=return_book)

    #write this information to a csv file - the book status function needs to be called after each write/form submission!
    with open(book_data, 'a', newline="") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["DTG", "Student", "Title", "Author", "Check Out", "Return"])

        writer.writerow([datetime.datetime.now().strftime("%m/%d/%Y/%H%M"), student.title(), title.title(), author.title(), bool(take_out), bool(return_book)])

    #call the book status function after using the form
    books = all_books_status()

    return render_template("index.html", message="Entry Saved!", books=books)



if __name__ == "__main__":
    app.run(debug=True)

