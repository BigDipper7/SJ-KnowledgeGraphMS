from pymongo import MongoClient

MDB_URL = 'mongodb://127.0.0.1:27017'
MDB_NAME = 'cayley'

client =  MongoClient(MDB_URL)
db = client[MDB_NAME]

collection = db.collection

if __name__ == '__main__':
    main()
