#include "../include/algorithms.h"
#include <limits.h>

static int fifo_counter = 0;
static unsigned int frame_last_used[NUM_FRAMES];
static int frames_to_page[NUM_FRAMES];
static unsigned int global_timer = 0;

// For Optimal
static int* future_references = NULL;
static int future_index = 0;
static int sequence_len = 0;

void init_optimal_algorithm(int* address_sequence, int sequence_length) {
    future_references = address_sequence;
    sequence_len = sequence_length;
    future_index = 0;
}

int select_victim_frame(AlgorithmType type) {
    static int next_free_frame = 0;
    
    // First, use empty frames
    if (next_free_frame < NUM_FRAMES) {
        return next_free_frame++;
    }

    // If no empty frames, use replacement algorithm
    if (type == ALGO_FIFO) {
        int victim = fifo_counter;
        fifo_counter = (fifo_counter + 1) % NUM_FRAMES;
        return victim;
    } 
    else if (type == ALGO_OPTIMAL) {
        int victim = -1;
        int farthest_future = -1;

        for (int i = 0; i < NUM_FRAMES; i++) {
            int current_page_in_frame = frames_to_page[i];
            int found_at = INT_MAX;

            // Search for next occurrence of this page in the future
            for (int j = future_index; j < sequence_len; j++) {
                if (future_references[j] == current_page_in_frame) {
                    found_at = j;
                    break;
                }
            }

            if (found_at == INT_MAX) { // Page never used again
                return i;
            }

            if (found_at > farthest_future) {
                farthest_future = found_at;
                victim = i;
            }
        }
        return victim;
    }

    return 0; // Default
}

void update_algorithm_state(int frame_number, int page_number) {
    global_timer++;
    frame_last_used[frame_number] = global_timer;
    frames_to_page[frame_number] = page_number;
    future_index++; // Advance future pointer for Optimal
}
