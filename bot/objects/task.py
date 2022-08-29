class Task:
    def __init__(self, data: dict):
        self.task_id = data.get("command_ID")  # an inner ID for the target
        self.task_type = data.get("command_name")  # which function should run?
        self.target = data.get("targets")  # attack target
        self.target_type = data.get("target_type")  # ip or URL?
        self.bots = data.get("command_bot_names")
        self.start_time = data.get("start_time")
        self.end_time = data.get("end_time")

    def convert_to_dict(self):
        return {
            "task_id": self.task_id,
            "task_type": self.task_type,
            "target": self.target,
            "target_type": self.target_type,
            "start_time": self.start_time,
            "end_time": self.end_time,
        }


class TaskResult:
    def __init__(self, data: dict) -> None:
        self.task_id = data.get("task_id")  # task_id of the task
        self.status = data.get("status")  # successful or failed
        self.end_time = data.get("end_time")  # when did the task finished
        self.result = data.get("result")  # result of the task or error

    def convert_to_dict(self):
        return {
            "task_id": self.task_id,
            "status": self.status,
            "end_time": self.end_time,
            "result": self.result
        }
