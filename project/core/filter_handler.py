from watchdog.events import FileSystemEventHandler


class FilterHandler(FileSystemEventHandler):

    def __init__(self, manager):
        self.manager = manager

    def on_modified(self, event):

        if event.src_path == self.manager.filter_file:
            self.manager.load()