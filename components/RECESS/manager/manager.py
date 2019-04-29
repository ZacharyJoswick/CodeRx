#!/usr/bin/env python
import time
import docker
import etcd3
import threading
import argparse
import logging
import coloredlogs
import signal

class manager:

    def __init__(self,
                 etcdHost="etcd",
                 etcdPort=2379,
                 nodeName="node1",
                 logLevel="DEBUG"
                 ):

        self.etcdHost = etcdHost
        self.etcdPort = etcdPort
        self.nodeName = nodeName

        #Setting up logging and signal handlers
        self.initialSetup(logLevel)
        
        #Setup docker connection
        self.setupDocker()

        #Setup ETCD connection
        self.setupEtcd()

        #Start workers
        self.start_workers()

        #Start docker event handling thread
        self.startBackgroundthread()

        #Infinite loop
        self.spin()

    # setup of logger and signal handler
    def initialSetup(self, logLevel):
        self.logger = logging.getLogger(__name__)
        coloredlogs.install(level=logLevel, logger=self.logger)
        signal.signal(signal.SIGTERM, self.signal_received)
        signal.signal(signal.SIGINT, self.signal_received)

    def signal_received(self, signum, frame):
        self.logger.warning('Signal Received, exiting')

    def setupDocker(self):
        self.client = docker.from_env()

    def setupEtcd(self):
        self.etcd = etcd3.client(host=self.etcdHost, port=self.etcdPort)
        self.etcd.put("/start", 'false')
        self.etcd.put("/" + self.nodeName + "/java_workers", '3')
        self.etcd.add_watch_callback("/start", self.start_workers_event)
        #self.etcd.add_watch_callback("/" + self.nodeName + "/java_workers", test)

    def startWorker(self, language):
        if language == "java":
            self.client.containers.run(
                "coderx_worker", detach=True, auto_remove=True, network="coderx_default")
        else:
            self.logger.info(f"Havent implemented {language} yet ;)")

    def stopWorker(self, id):
        result = self.client.containers.stop(id)

    def getNumWorkersCurrently(self):
        workers = self.client.containers.list(filters={"ancestor": "coderx_worker"})
        self.logger.info(f"Current number of workers: {len(workers)}")
        return len(workers)

    def getDesiredWorkers(self):
        return int(self.etcd.get("/" + self.nodeName + "/java_workers")[0])

    def start_workers_event(self, event):
        self.start_workers()

    def start_workers(self):
        desired_workers = self.getDesiredWorkers()
        current_workers = self.getNumWorkersCurrently()
        delta = desired_workers - current_workers

        if delta < 0:
            self.logger.info(f"Too many workers, stopping {delta}")

        if delta > 0:
            self.logger.info(f"Not enough workers, starting {delta}")
            for i in range(0,delta):
                self.logger.info("Starting Worker")
                self.startWorker("java")

    def spin(self):
        try:
            while True:
                time.sleep(.1)
        except KeyboardInterrupt:
            pass
    
    def startBackgroundthread(self):
        self.dockerEventThread = threading.Thread(
            target=self.handleEvents, name="dockerEvents")
        self.dockerEventThread.start()

    def handleEvents(self):
        self.logger.info("Listening for events")
        events = self.client.events(decode=True)
        for event in events:
            # self.logger.info(event)
            try:
                if event['status'] == "die":
                    self.logger.info(event)
                    language = event['Actor']['Attributes']['language']
                    self.logger.info(f"Event language: {language}")
                    self.startWorker(language)
                    
            except Exception as e:
                self.logger.warn(f"Exception in handle events: {e}")
                pass
            
def parse_arguments():
    parser = argparse.ArgumentParser(description='Optional app description')

    parser.add_argument("-u", "--etcdHost", dest="etcdHost", nargs='?', const="etcd", default="etcd",
                        help="Etcd address", metavar="host")
    parser.add_argument("-p", "--etcdPort", dest="etcdPort", nargs='?', const=2379, default=2379,
                        help="Etcd port", metavar="port")
    parser.add_argument("-n", "--nodeName", dest="nodeName", nargs='?', const="node1", default="node1",
                        help="Name of node manager is running on", metavar="Name")
    parser.add_argument("-l", "--logLevel", dest="logLevel", nargs='?', const="DEBUG", default="DEBUG",
                        help="Log Level", metavar="level")

    args = parser.parse_args()

    worker = manager(etcdHost=args.etcdHost,
                     etcdPort=args.etcdPort,
                     nodeName=args.nodeName,
                     logLevel=args.logLevel
                     )


if __name__ == "__main__":
    parse_arguments()
