RabbitMQ and MongoDB
==============

Deploy Ubuntu server, login, and issue the following commands in succession (most require root such for installing software):

# Update everything
apt-get update
reboot

# Main development/operational packages
apt-get install golang-go mongodb rabbitmq-server python-pip

# For `go get …`
apt-get install git bzr

# For Python.h in some `pip install …`
apt-get install python-dev

pip install pika
pip install pymongo

# In the development user’s environment
mkdir -p ~/go/{bin,src,pkg}
export GOPATH=~/go
go get labix.org/v2/mgo
go get github.com/streadway/amqp

Copy the two Go files to a directory in $GOPATH/src/… and then execute `go build $filename`.

The code that creates the random data and populates Mongo is “strata_gendata.go” and finishes by calculating and showing the percentage of 0s and 1s was generated:

$ ./strata_gendata

...

2015/01/25 18:02:00 {1 2015-01-25 18:02:00.914340023 +0000 GMT}
2015/01/25 18:02:00 {1 2015-01-25 18:02:00.914495897 +0000 GMT}
2015/01/25 18:02:00 {1 2015-01-25 18:02:00.915398275 +0000 GMT}
2015/01/25 18:02:00 percentage of ones: 10.70
2015/01/25 18:02:00 percentage of zero: 89.30

After creating the random data, Mongo shows the following:

MongoDB shell version: 2.6.3
connecting to: test

> use localdb

switched to db localdb

> show collections

system.indexes
test_data

> db.test_data.find().pretty()

...

{
"_id" : ObjectId("54c52f98648407740c9aa880"),
"value" : 0,
"dt" : ISODate("2015-01-25T18:02:00.574Z")
}
{
"_id" : ObjectId("54c52f98648407740c9aa881"),
"value" : 1,
"dt" : ISODate("2015-01-25T18:02:00.574Z")
}
{
"_id" : ObjectId("54c52f98648407740c9aa882"),
"value" : 0,
"dt" : ISODate("2015-01-25T18:02:00.574Z")
}

…

Then, you execute the listener/filter that writes the alerts:

$ ./strata_filterdata
2015/01/25 18:02:38 [*] Waiting for messages. To exit press CTRL+C

If you want, you can place this in the background by ^Z and then `bg` (or in another terminal) execute the Python code that gets the data from Mongo and populates a RabbitMQ queue with one publish per second. By default, Ubuntu uses Python 2.7.8, which I used:

$ chmod u+x mongo2rabbit.py
$ ./mongo2rabbit.py
{"dt": "2015-01-25 18:02:00.553000", "_id": "54c52f98648407740c9aa86c", "value": "0"}
{"dt": "2015-01-25 18:02:00.564000", "_id": "54c52f98648407740c9aa86d", "value": "0"}
{"dt": "2015-01-25 18:02:00.565000", "_id": "54c52f98648407740c9aa86e", "value": "0"}

...

Any of the messages with a “value” of 1 will cause `strata_filterdata` to log to /tmp/stratagem_golang_output.txt:

strataRec: 2015/01/25 18:03:34 strata_filterdata.go:97: Got a 1!
strataRec: 2015/01/25 18:03:58 strata_filterdata.go:97: Got a 1!
strataRec: 2015/01/25 18:04:05 strata_filterdata.go:97: Got a 1!

...

If you allow it to run the entire data set, the Python code will exit normally, but `strata_filterdata` will continue subscribing to the queue. You will need to bring it back to the foreground if you’ve placed it in the background with `fg` in the same terminal and then ^C.
