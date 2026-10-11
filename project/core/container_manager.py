
import subprocess
import time


class ContainerManager():
    def __init__(self):
        self.container_map = {}

    def get_container_pid(self, container_name):
        try:
            result = subprocess.check_output(
                ["docker", "inspect", "--format={{.State.Pid}}", container_name],
                text=True
            )
            return int(result.strip())
        except Exception:
            return None
        

    def get_container_cgroup_path(self, pid):
        try:
            with open(f"/proc/{pid}/cgroup") as f:
                for line in f:
                    parts = line.strip().split(":")
                    if len(parts) == 3:
                        return parts[2]
                    
        except:
            pass

        return None
    

    def get_cgroup_inode(self, pid):
        path = self.get_container_cgroup_path(pid)

        if not path:
            return None
        
        cg_path = "/sys/fs/cgroup" + path

        try:
            st = subprocess.check_output(
                ["stat", "-Lc", "%i", cg_path],
                text=True
            )
            return int(st.strip())
        except:
            return None
        

    def refresh(self):
        new_map = {}
        try:
            result = subprocess.check_output(
                ["docker", "ps", "--format", "{{.Names}}"],
                text=True
            )
            containers = (result.strip().split("\n"))
            
            for name in containers:
                pid = self.get_container_pid(name)
                if not pid:
                    continue

                inode = self.get_cgroup_inode(pid)

                if inode:
                    new_map[inode] = name
        
        except Exception as e:
            print(e)

        self.container_map = new_map

    def auto_refresh(self):
        while True:
            self.refresh()
            time.sleep(60)


    
    def check_container(self, cgroup_id):
        return (cgroup_id in self.container_map)
    

    def get_name(self, cgroup_id):
        return self.container_map.get(cgroup_id, "Unknown")
