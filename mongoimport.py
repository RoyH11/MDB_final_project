import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["test"]
mycol = mydb["test"]

mydict = { "name": "John", "address": "Highway 37" }



query = {"name": "John"}
result = mycol.find_one(query)
print(result)
