#include "../include/scheduler.h"

int main(int argc, char* argv[]) {
    if (argc < 2) {
        printf("Usage: %s <FCFS|SJF|SRTF|RR> [quantum]\n", argv[0]);
        return 1;
    }

    int n = 5;
    Process p[MAX_PROCESSES] = {
        {1, 0, 8, 0, 0, 0, 0, false},
        {2, 1, 4, 0, 0, 0, 0, false},
        {3, 2, 9, 0, 0, 0, 0, false},
        {4, 3, 5, 0, 0, 0, 0, false},
        {5, 4, 2, 0, 0, 0, 0, false}
    };

    char* algo = argv[1];
    if (strcmp(algo, "FCFS") == 0) run_fcfs(p, n);
    else if (strcmp(algo, "SJF") == 0) run_sjf(p, n);
    else if (strcmp(algo, "SRTF") == 0) run_srtf(p, n);
    else if (strcmp(algo, "RR") == 0) {
        int quantum = (argc > 2) ? atoi(argv[2]) : 2;
        run_rr(p, n, quantum);
    } else {
        printf("Invalid Algorithm.\n");
        return 1;
    }

    print_results(p, n);
    return 0;
}
