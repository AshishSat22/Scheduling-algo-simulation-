#include "../include/scheduler.h"
#include <limits.h>

void sort_by_arrival(Process* p, int n) {
    for (int i = 0; i < n - 1; i++) {
        for (int j = 0; j < n - i - 1; j++) {
            if (p[j].arrival_time > p[j + 1].arrival_time) {
                Process temp = p[j];
                p[j] = p[j + 1];
                p[j + 1] = temp;
            }
        }
    }
}

void calculate_metrics(Process* p, int n) {
    for (int i = 0; i < n; i++) {
        p[i].turnaround_time = p[i].completion_time - p[i].arrival_time;
        p[i].waiting_time = p[i].turnaround_time - p[i].burst_time;
    }
}

void run_fcfs(Process* p, int n) {
    sort_by_arrival(p, n);
    int current_time = 0;
    for (int i = 0; i < n; i++) {
        if (current_time < p[i].arrival_time)
            current_time = p[i].arrival_time;
        p[i].completion_time = current_time + p[i].burst_time;
        current_time = p[i].completion_time;
    }
    calculate_metrics(p, n);
}

void run_sjf(Process* p, int n) {
    int current_time = 0;
    int completed_count = 0;
    while (completed_count < n) {
        int idx = -1;
        int min_burst = INT_MAX;
        for (int i = 0; i < n; i++) {
            if (!p[i].completed && p[i].arrival_time <= current_time) {
                if (p[i].burst_time < min_burst) {
                    min_burst = p[i].burst_time;
                    idx = i;
                }
            }
        }
        if (idx != -1) {
            p[idx].completion_time = current_time + p[idx].burst_time;
            current_time = p[idx].completion_time;
            p[idx].completed = true;
            completed_count++;
        } else {
            current_time++;
        }
    }
    calculate_metrics(p, n);
}

void run_srtf(Process* p, int n) {
    int current_time = 0;
    int completed_count = 0;
    for(int i=0; i<n; i++) p[i].remaining_time = p[i].burst_time;

    while (completed_count < n) {
        int idx = -1;
        int min_rem = INT_MAX;
        for (int i = 0; i < n; i++) {
            if (p[i].remaining_time > 0 && p[i].arrival_time <= current_time) {
                if (p[i].remaining_time < min_rem) {
                    min_rem = p[i].remaining_time;
                    idx = i;
                }
            }
        }
        if (idx != -1) {
            p[idx].remaining_time--;
            current_time++;
            if (p[idx].remaining_time == 0) {
                p[idx].completion_time = current_time;
                completed_count++;
            }
        } else {
            current_time++;
        }
    }
    calculate_metrics(p, n);
}

void run_rr(Process* p, int n, int quantum) {
    sort_by_arrival(p, n);
    for(int i=0; i<n; i++) p[i].remaining_time = p[i].burst_time;
    
    int current_time = 0;
    int completed_count = 0;
    while (completed_count < n) {
        bool idle = true;
        for (int i = 0; i < n; i++) {
            if (p[i].remaining_time > 0 && p[i].arrival_time <= current_time) {
                idle = false;
                int execute = (p[i].remaining_time > quantum) ? quantum : p[i].remaining_time;
                p[i].remaining_time -= execute;
                current_time += execute;
                if (p[i].remaining_time == 0) {
                    p[i].completion_time = current_time;
                    completed_count++;
                }
            }
        }
        if (idle) current_time++;
    }
    calculate_metrics(p, n);
}

void print_results(Process* p, int n) {
    printf("\nPID | Arr | Burst | Comp | Turn | Wait\n");
    printf("---------------------------------------\n");
    float avg_wait = 0, avg_turn = 0;
    for (int i = 0; i < n; i++) {
        printf("%3d | %3d | %5d | %4d | %4d | %4d\n", 
               p[i].pid, p[i].arrival_time, p[i].burst_time, 
               p[i].completion_time, p[i].turnaround_time, p[i].waiting_time);
        avg_wait += p[i].waiting_time;
        avg_turn += p[i].turnaround_time;
    }
    printf("\nAverage Waiting Time: %.2f\n", avg_wait / n);
    printf("Average Turnaround Time: %.2f\n", avg_turn / n);
}
