#!/usr/bin/env python
import pika
import time
import sys
import json
import signal
import subprocess
import coloredlogs
import logging
import requests
from argparse import ArgumentParser

# Main worker class. Handles all java compilation parts


class javaWorker:

    # Initialization function.
    # All parameters are defaulted, but they can be customized
    # Intended to be customized by command line parameters
    def __init__(self,
                 queueHost="broker",
                 queuePort=5672,
                 queueName="java",
                 managerURL="manager",
                 managerPort=4582,
                 logLevel="DEBUG"
                 ):

        self.queueHost = queueHost
        self.queuePort = queuePort
        self.queueName = queueName
        self.managerURL = managerURL
        self.managerPort = managerPort
        self.language = queueName

        self.initialSetup(logLevel)
        self.connectToQueue()

    # setup of logger and signal handler
    def initialSetup(self, logLevel):
        self.logger = logging.getLogger(__name__)
        coloredlogs.install(level=logLevel, logger=self.logger)
        # coloredlogs.install(fmt='%(asctime)s,%(msecs)03d %(hostname)s %(name)s[%(process)d] %(levelname)s %(message)s', level=logLevel, logger=self.logger)
        signal.signal(signal.SIGTERM, self.signal_received)
        signal.signal(signal.SIGINT, self.signal_received)

    # Connect to RabbitMQ queue and start listening for connections
    def connectToQueue(self):
        # Some debug prints
        self.logger.debug(
            f"Queue Host: {self.queueHost} Queue Port: {self.queuePort}")

        # Setup connection using queue host and port
        self.wait_for_rabbitmq()
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.queueHost, port=self.queuePort))
        self.channel = self.connection.channel()

        # Make sure the queue exists if it doesent already
        # In  full RECESS installation this will likely do nothing, but it prevents errors when testing
        self.channel.queue_declare(queue=self.queueName, durable=True)

        # Only get one job at a time from the queue
        self.channel.basic_qos(prefetch_count=1)

        # Connect to the specified queue and specificy self.callback as callback function
        self.channel.basic_consume(
            queue=self.queueName, on_message_callback=self.callback)

        # Log message for users
        self.logger.info('Waiting for messages. To exit press CTRL+C')

        # Start listening for new jobs
        self.channel.start_consuming()

        self.logger.info("Stuff")

    def wait_for_rabbitmq(self):
        connected = False
        while not connected:
            try:
                connection = pika.BlockingConnection(
                    pika.ConnectionParameters(host=self.queueHost, port=self.queuePort))
                if connection.is_open:
                    self.logger.info("Connected to Rabbitmq")
                    connected = True
            except Exception as error:
                self.logger.info("Rabbitmq not ready, sleeping")
                time.sleep(1)
                pass

    # Writes out the code to the specified file
    def write_code_to_file(self, code, filename):
        with open(filename, "w") as text_file:
            self.logger.debug(f"Contents of file {filename} is {code}")
            text_file.write(code)

    # Compiles the specified file
    # Expects a filename and a timeout
    # Files should be in either the current running directory or should have a full path specified
    def compile_file(self, file, timeout):
        try:
            result = subprocess.run(
                ['javac', file], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
            return {
                "stdout": result.stdout.decode('utf-8'),
                "stderror": result.stderr.decode('utf-8')
            }
        except subprocess.TimeoutExpired as e:
            self.logger.error(str(e))
            pass

    # Handles sigterm and sigabort signals gracefully
    def signal_received(self, signum, frame):
        self.logger.warning('Sigterm Received, exiting')
        self.channel.stop_consuming()

    def testCode(self, file, tests, timeout):
        try:
            # result = subprocess.run(['java', file], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, timeout=timeout)
            results = []
            for test in tests:
                result = subprocess.run(['java', file], stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE, input=test["input"].encode() + b"\n", timeout=timeout)
                passTest = False
                result_string = result.stdout.decode().rstrip("\n\r")
                if result_string == test["expected_output"]:
                    passTest = True

                self.logger.debug(
                    f'Value from code: {result_string} Test Value: {test["expected_output"]}')

                results.append({"stdout": result.stdout.decode(
                ), "stderr": result.stderr.decode(), "pass_status": passTest})

            return results
        except subprocess.TimeoutExpired as e:
            self.logger.error(str(e))
            pass

    # def signal_manager_job_complete(self, job):
    #     try:
    #         # container id = basename "$(cat /proc/1/cpuset)"
    #         result = subprocess.run(['basename $(cat /proc/1/cpuset)'],
    #                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

    #         workerCompletedResponse = {
    #             "language": self.language, "container_id": result.stdout.decode('utf-8').replace("\n", "")}

    #         r = requests.post(url="http://" + self.managerURL + ":" + str(self.managerPort) + "/worker_completed",
    #                         json=workerCompletedResponse, timeout=0.5)
    #     except Exception as e:
    #         self.logger.error(str(e))

    # The callback that is executed when a new job is taken from the queue
    def callback(self, ch, method, properties, body):
        try:
            self.channel.stop_consuming()

            job = json.loads(body)
            self.logger.debug(f'Language of job is: {job["language"]}')

            if job["language"] == self.language:

                compileOutputs = []
                runOutputs = []

                for singleFile in job["files"]:
                    self.write_code_to_file(
                        singleFile["contents"], singleFile["filename"])

                    compileOutput = self.compile_file(
                        singleFile["filename"], job["compile_timeout"])
                    compileOutput["filename"] = singleFile["filename"]
                    self.logger.debug(f"Compile Output: {compileOutput}")
                    compileOutputs.append(compileOutput)

                runOutputs = self.testCode(
                    job["run_file"], job["tests"], job["run_timeout"])
                self.logger.debug(f"Run outputs: {runOutputs}")

                if job["callback_address"] != "":
                    jobResponse = {"error": "",
                                   "compile": compileOutputs,
                                   "run": runOutputs,
                                   "other": job["other"]
                                   }

                    self.logger.debug(
                        f'Sending response with message: {jobResponse} to address: {job["callback_address"]}')
                    r = requests.post(
                        url=job["callback_address"], json=jobResponse, timeout=0.5)
                    self.logger.debug(
                        f'Callback url resulted in a response code of: {r.status_code}')
                else:
                    self.logger.warning(
                        "No callback address specified, not sending the message")

                ch.basic_ack(delivery_tag=method.delivery_tag)

            else:
                errorMsg = f'ERROR: Language was {job["language"]} not java'
                self.logger.debug(errorMsg)
                if job["callback_address"] != "":
                    jobResponse = {"error": errorMsg}
                    self.logger.debug(
                        f'Sending response with message: {jobResponse} to address: {job["callback_address"]}')
                    r = requests.post(
                        url=job["callback_address"], json=jobResponse, timeout=0.5)
                    self.logger.debug(
                        f'Callback url resulted in a response code of: {r.status_code}')
                else:
                    self.logger.warning(
                        "No callback address specified, not sending the message")

                ch.basic_ack(delivery_tag=method.delivery_tag)

            # self.signal_manager_job_complete(job)
            self.connection.close()
            sys.exit()

        except Exception as e:
            self.logger.error(str(e))

            # Properly quit and exit, but dont send the acknowledgement message
            # will re queue on a different worker
            ch.basic_ack(delivery_tag=method.delivery_tag)
            self.channel.stop_consuming()
            self.connection.close()
            sys.exit()

# main argument parser function
# accepts arguments and runs the worker


def parse_arguments():
    parser = ArgumentParser(description='Optional app description')

    parser.add_argument("-u", "--queueHost", dest="queueHost", nargs='?', const="broker", default="broker",
                        help="RabbitMQ Queue host address", metavar="host")
    parser.add_argument("-p", "--queuePort", dest="queuePort", nargs='?', const=5672, default=5672,
                        help="RabbitMQ Queue port", metavar="port")
    parser.add_argument("-n", "--queueName", dest="queueName", nargs='?', const="java", default="java",
                        help="RabbitMQ Queue name", metavar="name")
    parser.add_argument("-m", "--managerURL", dest="managerURL", nargs='?', const="manager", default="manager",
                        help="RECESS Manager URL", metavar="URL")
    parser.add_argument("-t", "--managerPort", dest="managerPort", nargs='?', const=4582, default=4582,
                        help="RECESS Manager port", metavar="port")
    parser.add_argument("-l", "--logLevel", dest="logLevel", nargs='?', const="DEBUG", default="DEBUG",
                        help="Log Level", metavar="level")
    parser.add_argument("-v", "--validate", dest="validate", nargs='?', type=str2bool, const=False, default=True,
                        help="Print out command line arguments and exit", metavar="value")

    args = parser.parse_args()

    if args.validate:
        worker = javaWorker(queueHost=args.queueHost,
                            queuePort=args.queuePort,
                            queueName=args.queueName,
                            managerURL=args.managerURL,
                            managerPort=args.managerPort,
                            logLevel=args.logLevel
                            )
    else:
        print(args)

# parses values from the command line and represents as applicable boolean value


def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


if __name__ == "__main__":
    parse_arguments()
