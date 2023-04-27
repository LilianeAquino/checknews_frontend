from django.shortcuts import render
from django.http import HttpResponse
import pymongo

client = pymongo.MongoClient('localhost:27017')
dbname = client['checknewsDB']
collection = dbname['checknews']


def index(request):
    return HttpResponse('<h1>Checknews</h1>')


# collection.insert_one({'name': 'Sammy', 'type' : 'Shark'})
# mascot_details = collection.find({})

# for r in mascot_details:
#     print(r['name'])
