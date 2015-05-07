#!/usr/bin/env python
"""This is a proof of concept that establishes a connection to a MongoDB
and a RabbitMQ broker. The code reads all documents in a specific 
collection of a local database, iterates through them and places one
each second on a specific RabbitMQ queue.

Please note, there is very little to nonexistent error detection and 
handling. This very well could explode, but should create no damage.

Tested on Ubuntu Server 14.10 with MongoDB 2.6.3 and RabbitMQ 3.3.5.

Author: Justin Cook <jhcook@gmail.com>
"""

from sys import stderr, exit
from pymongo import MongoClient, errors as mongoops
from time import sleep
import pika

TESTHOST = "localhost"
MONGO_DB = "localdb"
MONGO_CO = "test_data"
R_MQUEUE = "test_data"

try:
    mongo_conn = MongoClient(TESTHOST)
except mongoops.ConnectionFailure:
    stderr.write("Unable to connect to db\n")
    exit(1)

rabbit_conn = pika.BlockingConnection(
    pika.ConnectionParameters(host=TESTHOST))

channel = rabbit_conn.channel()
channel.queue_declare(queue=R_MQUEUE)

# TODO: test if database and collection exist 
db = eval("mongo_conn.{}.{}".format(MONGO_DB, MONGO_CO))

# TODO: this finds everyting in the collection. It needs to be more graceful
# and check for a range so data can be handled in chunks and kept track of.
results = db.find()

try:
    for doc in results:
        # Since this is simply a bridge from Mongo to Rabbit, take everything in
        # each document and make it a comma delimited JSON string. 
        # Note: this does not take nested structures to account.
        try:
            sdoc = '{'+', '.join(['"{0[0]}": "{0[1]}"'.format(b) for b in 
                [(x, doc[x]) for x in doc.keys()]])+'}'
        except Exception:
            continue
        print(sdoc)
        channel.basic_publish(exchange='', routing_key='test_queue', body=sdoc)
        sleep(1)
except KeyboardInterrupt:
    print("Exiting on interrupt")

mongo_conn.close()
rabbit_conn.close()
