#include <uapi/linux/ptrace.h>
#include <linux/sched.h>

struct data_container{
    u32 pid;
    u32 ppid;
    u32 tgid;
    u64 cgroup_id;
    char comm[TASK_COMM_LEN];
    char filename[128];

    char cmd_args1[16];
    char cmd_args2[16];
    char cmd_args3[16];
    char cmd_args4[16];
    char cmd_args5[16];
};

BPF_PERF_OUTPUT(events);

TRACEPOINT_PROBE(syscalls, sys_enter_execve){
    struct data_container data = {};

    u64 id = bpf_get_current_pid_tgid();
    data.pid = id & 0xFFFFFFFF;
    data.tgid = id >> 32;

    struct task_struct *task = (struct task_struct *)bpf_get_current_task();
    data.ppid = task->real_parent->tgid;
    data.cgroup_id = bpf_get_current_cgroup_id();

    bpf_get_current_comm(&data.comm, sizeof(data.comm));
    bpf_probe_read_user_str(
        data.filename,
        sizeof(data.filename),
        args->filename
    );

    // Read command-line arguments (limited to 5 arguments)
    char *arg1 = NULL;
    char *arg2 = NULL;
    char *arg3 = NULL;
    char *arg4 = NULL;
    char *arg5 = NULL;

    bpf_probe_read_user(&arg1, sizeof(arg1), &args->argv[1]);
    bpf_probe_read_user(&arg2, sizeof(arg2), &args->argv[2]);
    bpf_probe_read_user(&arg3, sizeof(arg3), &args->argv[3]);
    bpf_probe_read_user(&arg4, sizeof(arg4), &args->argv[4]);
    bpf_probe_read_user(&arg5, sizeof(arg5), &args->argv[5]);

    if (arg1)
    {
        bpf_probe_read_user_str(data.cmd_args1,sizeof(data.cmd_args1),arg1);
        if (arg2)
        {
            bpf_probe_read_user_str(data.cmd_args2,sizeof(data.cmd_args2),arg2);
            if (arg3)
            {
                bpf_probe_read_user_str(data.cmd_args3,sizeof(data.cmd_args3),arg3);
                if (arg4)
                {
                    bpf_probe_read_user_str(data.cmd_args4,sizeof(data.cmd_args4),arg4);
                    if (arg5)
                    {
                        bpf_probe_read_user_str(data.cmd_args5,sizeof(data.cmd_args5),arg5);
                    }
                }
            }
        }
    }


    events.perf_submit(args, &data, sizeof(data));
    return 0;
}