#!/usr/bin/env python
import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)

message = "{\n    \"files\": [{\n        \"filename\": \"HelloWorld.java\",\n        \"contents\": \"import java.util.Scanner; \\npublic class HelloWorld { \\n\\n    public static void main(String[] args) { \\n\\t// Prints Hello, World to the terminal window.\\n        Scanner in = new Scanner(System.in); \\n        String s = in.nextLine(); \\n        System.out.println(s); \\n    }\\n\\n}\"\n    }],\n    \"run_file\": \"HelloWorld\",\n    \"tests\": [{\n            \"input\": \"Test String 1\",\n            \"expected_output\": \"Test String 1\"\n        },\n        {\n            \"input\": \"Test String 2\",\n            \"expected_output\": \"Test String 2\"\n        },\n        {\n            \"input\": \"Test String 3\",\n            \"expected_output\": \"Test String 3\"\n        },\n        {\n            \"input\": \"Test String 4\",\n            \"expected_output\": \"Test String 5\"\n        }\n    ],\n    \"language\": \"java\",\n    \"callback_address\": \"\",\n    \"compile_timeout\": 5,\n    \"run_timeout\": 5,\n    \"other\": {\n        \"user_id\": 1,\n        \"job_guid\": \"abcdefg\"\n    }\n}"

channel.basic_publish(exchange='',
                      routing_key="java",
                      body=message,
                      properties=pika.BasicProperties(
                         delivery_mode = 2, # make message persistent
                      ))
print("Job Dispatched")

connection.close()