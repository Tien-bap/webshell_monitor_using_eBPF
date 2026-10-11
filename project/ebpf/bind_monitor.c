#include <uapi/linux/ptrace.h>
#include <linux/sched.h>
#include <uapi/linux/in.h>
#include <uapi/linux/socket.h>

#define AF_INET 2

struct data_t {
    u32 pid;
    u32 ppid;
    u32 tgid;
    u64 cgroup;
    char comm[16];

    u32 addr;
    u16 port;
};

BPF_PERF_OUTPUT(events);

TRACEPOINT_PROBE(syscalls, sys_enter_bind) {
    struct data_t data = {};

    u64 id = bpf_get_current_pid_tgid();
    data.pid = id & 0xFFFFFFFF;
    data.tgid = id >> 32;

    struct task_struct *task = (struct task_struct *)bpf_get_current_task();
    data.ppid = task->real_parent->tgid;
    data.cgroup = bpf_get_current_cgroup_id();
    bpf_get_current_comm(&data.comm, sizeof(data.comm));

    struct sockaddr_in sin = {};

    bpf_probe_read_user(&sin, sizeof(sin), args->umyaddr);

    if (sin.sin_family != AF_INET)
        return 0;

    data.addr = sin.sin_addr.s_addr;
    data.port = sin.sin_port;

    events.perf_submit(args, &data, sizeof(data));

    return 0;
}