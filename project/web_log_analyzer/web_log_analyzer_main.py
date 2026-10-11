
from web_log_analyzer.web_log_analyzer_window import WebLogAnalyzerWindow
from web_log_analyzer.load_log import LoadLog
from datetime import datetime, timedelta, timezone

class WebLogAnalyzerMain:
    def __init__(self, PATH):
        self.window = WebLogAnalyzerWindow()
        self.load_log = LoadLog(PATH)

    def start(self, event):
        event_time = self.normalize_time(event["timestamp"])
        start_time = event_time + timedelta(seconds=10)
        end_time = event_time - timedelta(seconds=10)

        logs = self.load_log.search_logs(start_time, end_time)
        self.window.start(logs)

    def normalize_time(self, timestamp):
        dt = datetime.fromisoformat(timestamp)

        # nếu timestamp không có timezone
        if dt.tzinfo is None:
            dt = dt.replace(
                tzinfo=timezone(timedelta(hours=7))
            )

        # convert về UTC
        return dt.astimezone(timezone.utc)