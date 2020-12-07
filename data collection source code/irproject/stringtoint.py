import pymongo

client = pymongo.MongoClient("mongodb+srv://DJL:Djl123456@cluster0-ywxjv.azure.mongodb.net/test?retryWrites=true&w=majority")
db = client['film_web']
catalog_films = db['catalog_films']
result = catalog_films.find(no_cursor_timeout=True, batch_size=5)

for each in result:
    if "Douban" in each.keys():
        if "no rating" in each["Douban"]["rating"]:
            each["Douban"]["rating"] = -1
        else:
            each["Douban"]["rating"] = float(each["Douban"]["rating"])
        db.catalog_films.update({'title':each['title']},{'$set':{"Douban":{"rating": each["Douban"]["rating"]}}})
    else:
        pass