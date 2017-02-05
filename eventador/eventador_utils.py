import threading
from time import sleep


def start_eventador(target, target_args):
    thread = threading.Thread(target=target, args=target_args)
    thread.start()
    return thread


def start_publishers(client, publisher_configs, publish_args=()):
    eventador_publishers = [client.get_publisher(config) for config in publisher_configs]
    eventador_threads = [start_eventador(publisher.publish, publish_args) for publisher in eventador_publishers]
    sleep(2) # UGLY SLEEP
    return eventador_threads


def wait_for_publishers(threads):
    [thread.join() for thread in threads]