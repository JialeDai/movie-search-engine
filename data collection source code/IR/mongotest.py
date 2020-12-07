import pymongo
import datetime
client = pymongo.MongoClient("mongodb+srv://DJL:Djl123456@cluster0-ywxjv.azure.mongodb.net/test?retryWrites=true&w=majority")
db = client['sample_mflix']
collection = db['test']
post = {"author": "Maxsu",
         "text": "My first blog post!",
         "tags": ["mongodb", "python", "pymongo"],
         "date": datetime.datetime.utcnow()}
db.test.insert_one(post)
x = list(collection.find())


print(x)