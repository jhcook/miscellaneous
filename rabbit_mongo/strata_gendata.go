/*
This code generates a 0 or 1 within probability restraints (0: 90%, 1: 10%)
and creates a MongoDB entry with an ISO timestamp and that value. The doc
id is left to MongoDB to insert:

[
  {
    "_id": ObjectId("54764c888516986244deabf3"),
    "value": 0,
    "dt": ISODate("2014-11-26T21:56:23.430Z")
  }
]

Tested on Ubuntu Server 14.10 with MongoDB 2.6.3

TODO: - config file and/or command-line options
      - more error handling

Author: Justin Cook <jhcook@gmail.com>
*/

package main

import (
	"labix.org/v2/mgo"
	"log"
	"math/rand"
	"os"
	"strconv"
	"time"
)

type msg struct {
	Value int       `bson:"value"`
	Dt    time.Time `bson:"dt"`
}

var MAX_ITERS int = 1000
var num_zero int
var num_ones int

func calcPerc() {
	log.Println("percentage of ones: ", strconv.FormatFloat(
		((float64(num_ones)/float64(MAX_ITERS))*100), 'f', 2, 64))
	log.Println("percentage of zero: ", strconv.FormatFloat(
		((float64(num_zero)/float64(MAX_ITERS))*100), 'f', 2, 64))

}

/*
An integer of `1` needs to be produced 10% of the time with random
distribution. This function generates a number 0 < 100 with 1 being the
remainder when divided by 10, 10% of the time. Therefore, return 1 when this is
the case or 0 otherwise. Since it is evenly disributed randomly, this will
give 1 10% of the time and 0 90%.
*/
func GenZeroOrOne() int {
	if num := rand.Intn(100); num%10 == 1 {
		num_ones++
		return 1
	}
	num_zero++
	return 0
}

func main() {
	// Create a session to the MongoDB
	session, err := mgo.Dial("localhost")
	if err != nil {
		log.Fatal("Unable to create MongoDB session")
		os.Exit(1)
	}
	defer session.Close()

	// Connect to the named database and collection.
	c := session.DB("localdb").C("test_data")

	// Seed the random generator as usual with epoch timestamp.
	rand.Seed(time.Now().UnixNano())

	//Loop 1000 times, create a `msg` structure and insert a document in
	//the Mongo database/collection.
	for i := 0; i < MAX_ITERS; i++ {
		doc := msg{Value: GenZeroOrOne(), Dt: time.Now()}
		log.Println(doc)
		c.Insert(doc)
	}

	calcPerc()
}
