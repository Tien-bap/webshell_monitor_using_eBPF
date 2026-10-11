import json

FILE = "../data/filter.json"


class FilterController:

    def __init__(self):
        self.file = FILE
        self.ignored_pids = set()
        self.load()

    def load(self):
        try:
            with open(self.file, "r") as f:
                data = json.load(f)

            self.ignored_pids = set(data.get("ignored_pids", []))

        except Exception:
            self.ignored_pids = set()

    def save(self):
        with open(self.file, "w") as f:
            json.dump(
                {
                    "ignored_pids": sorted(self.ignored_pids)
                },
                f,
                indent=4
            )

    def add_pid(self, pid):
        if pid not in self.ignored_pids:
            self.ignored_pids.add(pid)
            self.save()

    def remove_pid(self, pid):
        if pid in self.ignored_pids:
            self.ignored_pids.remove(pid)
            self.save()

    def reset(self):
        self.ignored_pids.clear()
        self.save()

    def show(self):
        print(sorted(self.ignored_pids))

    def get_ignored_pids(self):
        return self.ignored_pids

    def run(self):
        while True:

            self.show()

            payload = input("PID filter> ").strip()

            if not payload:
                continue

            op = payload[0]

            if op == "e":
                break

            elif op == "r":
                self.reset()
                continue

            try:
                pid = int(payload[1:])
            except ValueError:
                print("Invalid PID")
                continue

            if op == "a":
                self.add_pid(pid)

            elif op == "d":
                self.remove_pid(pid)