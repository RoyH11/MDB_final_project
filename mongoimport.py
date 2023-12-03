import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["test"]
mycol = mydb["test"]

query = {"name": "Smith"}
result = mycol.find_one(query)
print(result)
