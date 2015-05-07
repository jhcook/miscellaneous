/*
This code subscribes to a RabbitMQ queue and spawns two Goroutines to watch
the queue, filter messages and then log to a file when the filter matches.

The write to file is registered as a separate Goroutine so the filtering
routine can continue filtering in constant time and queue logs if need be.

TODO: - much more error detection/correction needs to be implemented
      - config file implementation
      - command line arguments
      - should work fine with systemd, but if you want init will need standard
        files handled

Tested on Ubuntu Server 14.10 with RabbitMQ RabbitMQ 3.3.5.

Author: Justin Cook <jhcook@gmail.com>
    Name Unknown https://github.com/mandolyte
*/

package main

import (
	"encoding/json"
	"fmt"
	"github.com/streadway/amqp"
	"log"
	"os"
	"strconv"
)

var strataLog *log.Logger

func failOnError(err error, msg string) {
	if err != nil {
		log.Fatalf("%s: %s", msg, err)
		panic(fmt.Sprintf("%s: %s", msg, err))
	}
}

func initLogger(logfn string) *log.Logger {
	logf, err := os.OpenFile(logfn, os.O_RDWR|os.O_CREATE|os.O_APPEND,
		0755)
	if err != nil {
		failOnError(err, "Failed to open logfile for writing")
	}
	our_logger := log.New(logf, "strataRec: ",
		log.Ldate|log.Ltime|log.Lshortfile)
	return our_logger
}

func main() {
	// This map is used to JSON.Unmarshal messages.
	var rmsg map[string]interface{}
	// This map is used to pass messages to a routine that writes to disk.
	write_to_disk := make(chan map[string]interface{})
	// This channel simply blocks waiting on an input that will never be
	// received. So, ^C will be instructed to interrupt.
	forever := make(chan bool)

	// This should be a config file or command line option.
	logfn := "/tmp/stratagem_golang_output.txt"
	strataLog = initLogger(logfn)

	// Connect to the code listening for AMQP on localhost
	conn, err := amqp.Dial("amqp://localhost:5672/")
	failOnError(err, "Failed to connect to RabbitMQ")
	defer conn.Close()

	ch, err := conn.Channel()
	failOnError(err, "Failed to open a channel")
	defer ch.Close()

	q, err := ch.QueueDeclare(
		"test_queue", // name
		false,        // durable
		false,        // delete when usused
		false,        // exclusive
		false,        // no-wait
		nil,          // arguments
	)

	msgs, err := ch.Consume(
		q.Name, // queue
		"",     // consumer
		true,   // auto-ack
		false,  // exclusive
		false,  // no-local
		false,  // no-wait
		nil,    // args
	)
	failOnError(err, "Failed to register a consumer")

	go func() {
		for {
			wtd_msg := <-write_to_disk
			strataLog.Println(fmt.Sprintf("Got a %s!",
				wtd_msg["value"].(string)))
		}
	}()

	go func() {
		for d := range msgs {
			if err := json.Unmarshal(d.Body, &rmsg); err == nil {
				if i, _ := strconv.Atoi(rmsg["value"].(string)); i == 1 {
					write_to_disk <- rmsg
				}
			}
		}
	}()

	log.Println(" [*] Waiting for messages. To exit press CTRL+C")
	<-forever
}
