from cs50 import SQL
from flask import Flask, redirect, request, render_template

app = Flask(__name__)

# set database
db = SQL("sqlite:///layoffHK.db")

# home page
@app.route("/")
def index():
    # select the most recent entry for each company and order the rows by date in descending order
    rows = db.execute("SELECT company, status, paycut, date, source, note, MAX(date) FROM layoffStatus GROUP BY UPPER(company) ORDER BY date DESC")
    return render_template("index.html", rows=rows)

# contribute page that accepts datas
@app.route("/add", methods=["GET", "POST"])
def add():
    # default method is rendering the page
    if request.method == "GET":
        return render_template("add.html")
    # when user submits form, add the data to the database
    else:
        company = request.form.get("company")
        status = request.form.get("status")
        paycut=request.form.get("paycut")
        date = request.form.get("date")
        source = request.form.get("source")
        note = request.form.get("note")
        db.execute("INSERT INTO layoffStatus (company, status, paycut, date, source, note) VALUES (:company, :status, :paycut, :date, :source, :note)", company=company, status=status, paycut=paycut, date=date, source=source, note=note)
        # redirect back to home with updated info
        return redirect("/")

# about page
@app.route("/about")
def about():
    return render_template("about.html")