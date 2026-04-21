#ifndef ALGORITHMS_H
#define ALGORITHMS_H

#include "common.h"

typedef enum {
    ALGO_FIFO,
    ALGO_OPTIMAL
} AlgorithmType;

int select_victim_frame(AlgorithmType type);
void update_algorithm_state(int frame_number, int page_number);
void init_optimal_algorithm(int* address_sequence, int sequence_length);

#endif
