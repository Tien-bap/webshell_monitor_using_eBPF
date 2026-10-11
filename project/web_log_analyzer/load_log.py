from datetime import datetime
import re

LOG_PATTERN = re.compile(
    r'(?P<ip>\S+) '
    r'\[(?P<time>.*?)\] '
    r'"(?P<method>\S+) (?P<url>\S+) (?P<protocol>.*?)" '
    r'(?P<status>\d+) '
    r'(?P<size>\d+) '
    r'"(?P<referer>.*?)" '
    r'"(?P<user_agent>.*?)"'
    r'(?: "(?P<host>.*?)")?'
    r'(?: "(?P<request_uri>.*?)")?'
    r'(?: "(?P<query_string>.*?)")?'
    r'(?: "(?P<request_time>.*?)")?'
    r'(?: "(?P<remote_user>.*?)")?'
)

MONTH_MAP = {
    "Jan": "01",
    "Feb": "02",
    "Mar": "03",
    "Apr": "04",
    "May": "05",
    "Jun": "06",
    "Jul": "07",
    "Aug": "08",
    "Sep": "09",
    "Oct": "10",
    "Nov": "11",
    "Dec": "12"
}


class LoadLog: 
    def __init__(self, PATH):
        self.path = PATH

    def load(self):
        logs = []

        with open(self.path, "r", encoding="utf-8") as f:
            for line in f: 
                log = self.parse(line)
                if log:
                    logs.append(log)
        return logs
    


    def parse(self, line):

        m = LOG_PATTERN.match(line)

        if not m:
            return None

        data = m.groupdict()

        data["time"] = self.normalize_time(
            data["time"]
        )

        data["status"] = int(data["status"])
        data["size"] = int(data["size"])

        return data
    


    def search_logs(self, start, end):
        results = []
        print("start = ", start)
        print("end = ", end)

        for line in self.read_log_reverse(self.path):
            line = line.strip()
            if not line:
                continue

            log = self.parse(line)
            print("log: ", log)
            if log is None:
                print("PARSE FAIL:", repr(line))
                continue

            log_time = log["time"] 

            # log mới hơn khoảng cần tìm
            if log_time > start:
                continue

            # nằm trong khoảng cần tìm
            if end <= log_time <= start:
                results.append(log)
                continue

            # đã đi qua vùng cần tìm
            if log_time < end:
                break
        return results[::-1]



    def read_log_reverse(self, path):
        with open(path, "rb") as f:

            f.seek(0, 2)
            position = f.tell()
            buffer = b""
            while position > 0:
                position -= 1
                f.seek(position)
                char = f.read(1)

                if char == b"\n":
                    yield buffer[::-1].decode()
                    buffer = b""
                else:
                    buffer += char

            if buffer:
                yield buffer[::-1].decode()


    def normalize_time(self, time):

        day = time[:2]
        month = MONTH_MAP[time[3:6]]
        year = time[7:11]
        hour = time[12:14]
        minute = time[15:17]
        second = time[18:20]
        timezone = time[21:]

        new_time = (
            f"{day}/{month}/{year} "
            f"{hour}:{minute}:{second} "
            f"{timezone}"
        )

        return datetime.strptime(
            new_time,
            "%d/%m/%Y %H:%M:%S %z"
        )
    