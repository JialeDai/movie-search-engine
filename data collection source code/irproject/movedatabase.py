import pymongo
from bson.objectid import ObjectId
client = pymongo.MongoClient("mongodb://DJL:Djl123456@cluster0-shard-00-00-ywxjv.azure.mongodb.net:27017,cluster0-shard-00-01-ywxjv.azure.mongodb.net:27017,cluster0-shard-00-02-ywxjv.azure.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority")
db = client['film_web']
new_db = client['movie_web']
catalog_films=db['catalog_films']
result=list(catalog_films.find(no_cursor_timeout=True,batch_size=5))
catalog_movies = new_db['catalog_movies']
testlist = []
# resultlist = list(result)
i = 0

for each in result:
    newdic = {}
    if '_id' in each.keys():
        newdic["_id"]= each['_id']

    if 'title' in each.keys():
        newdic['title'] = each['title']

    if 'plot' in each.keys():
        newdic['plot'] = each['plot']
    
    if 'genres' in each.keys():
        newdic['genres'] = each['genres']
    
    if 'runtime' in each.keys():
        newdic['runtime'] = each['runtime']
    
    if 'cast' in each.keys():
        newdic['cast'] = each['cast']
    
    if 'poster' in each.keys():
        newdic['poster'] = each['poster']
  
    if 'fullplot' in each.keys():
        newdic['fullplot'] = each['fullplot']
    
    if 'countries' in each.keys():
        newdic['countries'] = each['countries']

    if "released" in each.keys():
        newdic['released'] = each['released']
    
    if 'language' in each.keys():
        newdic['language'] = each['language']
   
    if 'directors' in each.keys():
        newdic['directors'] = each['directors']
    
    if 'writers' in each.keys():
        newdic['writers'] = each['writers']
    
    if 'year' in each.keys():
        newdic['year'] = each['year']
    
    if 'imdb' in each.keys():
        newdic['imdb'] = each['imdb']
    
    if 'tomatoes' in each.keys():
        newdic['tomatoes'] = each['tomatoes']
    
    if 'Douban' in each.keys():
        newdic['Douban'] = each['Douban']

    testlist.append(newdic)
# print(testlist)
for each in testlist:
    print(each['_id'])
    print(each['title'])

# print(testlist)

catalog_movies.insert(testlist)


