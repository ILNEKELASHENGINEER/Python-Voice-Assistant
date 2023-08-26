import pymongo
client = pymongo.MongoClient("mongodb://localhost:27017")
mydb = client["mydatabase"]
print(client.list_database_names())

dblist = client.list_database_names()
if "mydatabse" in dblist:
    print("The database exists.")