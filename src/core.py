from dotenv import load_dotenv
import platform
import os
from datetime import datetime, date, timedelta
import glob


class Log:

    level: str

    def __init__(self, origin: str = "any") -> None:
        load_dotenv()
        self.origin = origin
        self.level = os.getenv("LOG_LEVEL")

        self.path = "/tmp/logs/"
        if platform.system() == "Windows":
            self.path = "\\tmp\\logs\\"
        self.path_log = self.path + "log_"

        self.clean_old_logs()

    def register(self, level: str, msg: str) -> None:
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        with open(
                os.path.dirname(os.path.realpath(__file__)) + self.path_log + str(date.today()) + '.log', 'a',
                encoding='utf-8'
        ) as log_file:
            log_file.write("[{}] {}: {} \n".format(str(datetime.now()), level, msg))

    def error(self, msg: str) -> None:
        self.register('ERROR', self.origin + " - " + msg)

    def info(self, msg: str) -> None:
        if self.level != "error":
            self.register('INFO', self.origin + " - " + msg)

    def debug(self, msg: str) -> None:
        if self.level == "debug":
            self.register('DEBUG', self.origin + " - " + msg)

    def clean_old_logs(self):
        now = datetime.now()
        retention_days = 3
        cutoff = now - timedelta(days=retention_days)

        files = glob.glob(os.path.dirname(os.path.realpath(__file__)) + self.path_log + "*.log")
        for file in files:
            file_date_str = file.split('_')[-1].split('.')[0]
            file_date = datetime.strptime(file_date_str, '%Y-%m-%d').date()
            if datetime.combine(file_date, datetime.min.time()) < cutoff:
                os.remove(file)
                self.info(f"Log file {file} removed.")


class Core:
    log: Log
    origin: str

    def __init__(self, origin: str):
        load_dotenv()
        self.origin = origin
        self.log = self.get_logger()

    def get_logger(self) -> Log:
        return Log(self.origin)
