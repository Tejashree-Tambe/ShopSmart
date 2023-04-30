from flask import Flask, request, render_template
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast
import pymongo

client = pymongo.MongoClient("mongodb+srv://admin:admin@cluster0.m6ymc.mongodb.net/?retryWrites=true&w=majority")
db = client["ShopSmart"]
col = db["rooms"]
collections = col.find({})

app = Flask(__name__)        

@app.route('/')
def trial_room():
    return render_template("trial_room.html", collection = collections)  
 
if __name__ == '__main__':
    app.run(debug=True)