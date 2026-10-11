from queue import Queue
import threading
import time

from core.container_manager import ContainerManager
from monitors.exec_monitor import ExecMonitor
from monitors.open_monitor import OpenMonitor
from core.filter_manager import FilterManager
from monitors.connect_monitor import ConnectMonitor
from monitors.bind_monitor import BindMonitor
from monitors.listen_monitor import ListenMonitor
from core.logger import Logger
from core.process_cache import ProcessCache
from dashboard.main_dashboard import MainDashboard
from core.alert_manager import AlertManager
from rule.rule_manager import RuleManager
from core.action_manager import ActionManager
from web_log_analyzer.web_log_analyzer_main import WebLogAnalyzerMain

WEB_LOG_PATH = "../reverse_proxy/logs/access.log"

action_mgr = ActionManager("data/filter.json")

container_mgr = ContainerManager()
container_mgr.refresh()

process_cache = ProcessCache()

filter_mgr = FilterManager("data/filter.json")
filter_mgr.start()

dashboard_queue = Queue()
alert_queue = Queue()

rule_manager = RuleManager()
alert_mgr = AlertManager(alert_queue, rule_manager)



logger = Logger("data/events.jsonl", dashboard_queue, alert_mgr, process_cache)
logger.start()

web_log_analyzer = WebLogAnalyzerMain(WEB_LOG_PATH)

print(container_mgr.container_map)

exec_monitor = ExecMonitor(container_mgr, filter_mgr, logger)
open_monitor = OpenMonitor(container_mgr, filter_mgr, logger)
connect_monitor = ConnectMonitor(container_mgr, filter_mgr, logger)
bind_monitor = BindMonitor(container_mgr, filter_mgr, logger)
listen_monitor = ListenMonitor(container_mgr, filter_mgr, logger)


exec_monitor.start()
open_monitor.start()
connect_monitor.start()
bind_monitor.start()
listen_monitor.start()


threading.Thread(target=container_mgr.auto_refresh, daemon=True).start()
threading.Thread(target=exec_monitor.poll, daemon=True).start()
threading.Thread(target=open_monitor.poll, daemon=True).start()
threading.Thread(target=connect_monitor.poll, daemon=True).start()
threading.Thread(target=bind_monitor.poll, daemon=True).start()
threading.Thread(target=listen_monitor.poll, daemon=True).start()

main_dashboard = MainDashboard(dashboard_queue, alert_queue, filter_mgr, action_mgr, process_cache, web_log_analyzer)
main_dashboard.start()

while True:
    time.sleep(60)