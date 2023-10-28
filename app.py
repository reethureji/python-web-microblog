from flask import Flask, render_template, request
import datetime
from pymongo import MongoClient


def create_app():
    app = Flask(__name__)
    client = MongoClient("mongodb+srv://admin:admin@microblog-application.aspiekk.mongodb.net/")
    app.db = client.microblog
    @app.route("/", methods=["GET", "POST"]) #Keyword argument methods --> Get and post
    def home():
        if request.method == "POST":
            entry_content = request.form.get("content")  #content is the name of the field defined in html
            formated_date = datetime.datetime.today().strftime("%Y-%m-%d")
            # entries.append((entry_content, formated_date))
            app.db.entries.insert_one({"content": entry_content, "date": formated_date})
        entries_with_date = [
            (
                entry["content"],
                entry["date"],
                datetime.datetime.strptime(entry["date"], "%Y-%m-%d").strftime("%b %d")
            )
        for entry in app.db.entries.find({}) #Removed list and get directly using db key
        ]
        
        return render_template("home.html", entries=entries_with_date)
    return app