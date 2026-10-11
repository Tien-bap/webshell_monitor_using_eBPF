#include <uapi/linux/ptrace.h>
#include <linux/sched.h>

struct data_t{
    u32 pid;
    u32 ppid;
    u32 tgid;
    u64 cgroup;
    char comm[16];
    char filename[256];
};

BPF_PERCPU_ARRAY(data_heap, struct data_t, 1);

static int starts_with(const char *s, const char *prefix){
    for(int i = 0; prefix[i] != '\0'; i++){
        if(s[i] != prefix[i]) return 0;
    }
    return 1;
}

static int str_equal(const char *a, const char *b)
{
    int i;
    for (i = 0; i < 255; i++) {
        if (a[i] != b[i])
            return 0;
        if (a[i] == '\0')
            return 1;
    }
    return 0;
}

static int file_filter(char *f)
{
    if (f[0] == '\0') return 0;

    if (starts_with(f, "/proc")) return 0;
    if (starts_with(f, "/sys")) return 0;
    if (starts_with(f, "/usr/lib")) return 0;
    if (starts_with(f, "/usr/local/lib")) return 0;
    if (starts_with(f, "/lib")) return 0;
    if (starts_with(f, "/usr/share/locale")) return 0;
    if (starts_with(f, "/etc/localtime")) return 0;
    if (starts_with(f, "/usr/share/zoneinfo")) return 0;
    if (starts_with(f, "/var/cache")) return 0;
    if (starts_with(f, "/root/.cache")) return 0;
    if (starts_with(f, "/app/app/static")) return 0;
    if (starts_with(f, "/app/app/__pycache__")) return 0;
    if (starts_with(f, "/app/app/templates")) return 0;
    if (starts_with(f, "/etc/ld.so.cache")) return 0;

    return 1;
}

BPF_PERF_OUTPUT(events);

TRACEPOINT_PROBE(syscalls, sys_enter_openat){
    int zero = 0;
    struct data_t *data = data_heap.lookup(&zero);
    if (!data) return 0;

    __builtin_memset(data, 0, sizeof(*data));

    u64 id = bpf_get_current_pid_tgid();
    data->tgid = id >> 32;
    data->pid = id & 0xFFFFFFFF;

    struct task_struct *task = (struct task_struct *)bpf_get_current_task();
    data->ppid = task->real_parent->tgid;
    data->cgroup = bpf_get_current_cgroup_id();

    bpf_get_current_comm(&data->comm, sizeof(data->comm));
    bpf_probe_read_user_str(
        data->filename,
        sizeof(data->filename),
        args->filename
    );

    if(file_filter(data->filename) == 0) return 0;
    events.perf_submit(args, data, sizeof(*data));

    return 0;
}