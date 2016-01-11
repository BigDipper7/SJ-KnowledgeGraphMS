from pymongo import MongoClient

MDB_URL = 'mongodb://127.0.0.1:27017'
MDB_NAME = 'cayley'
MDB_COLLECTION_LOG = 'log'
MDB_COLLECTION_QUADS = 'quads'
MDB_COLLECTION_NODES = 'nodes'

#get mongo client, guess same as mongo
client =  MongoClient(MDB_URL)
#get specified db, just like use cayley
db = client[MDB_NAME]

# collection = db.collection

def main():
    #get three main collections through name and db
    collecion_quads = db[MDB_COLLECTION_QUADS]
    collecion_nodes = db[MDB_COLLECTION_NODES]
    collecion_log = db[MDB_COLLECTION_LOG]

    return

if __name__ == '__main__':
    main()
