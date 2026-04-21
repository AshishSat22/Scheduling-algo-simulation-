#ifndef SCHEDULER_H
#define SCHEDULER_H

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>

#define MAX_PROCESSES 10

typedef struct {
    int pid;
    int arrival_time;
    int burst_time;
    int remaining_time;
    int completion_time;
    int turnaround_time;
    int waiting_time;
    bool completed;
} Process;

typedef enum {
    ALGO_FCFS,
    ALGO_SJF,
    ALGO_SRTF,
    ALGO_RR
} SchedulerAlgo;

void run_fcfs(Process* p, int n);
void run_sjf(Process* p, int n);
void run_srtf(Process* p, int n);
void run_rr(Process* p, int n, int quantum);

// Helper for sorting
void sort_by_arrival(Process* p, int n);
void calculate_metrics(Process* p, int n);
void print_results(Process* p, int n);

#endif
