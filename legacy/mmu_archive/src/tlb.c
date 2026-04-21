#include "../include/tlb.h"
#include <string.h>

static TLBEntry tlb[TLB_SIZE];
static int next_tlb_index = 0;
static unsigned int timer = 0;

void tlb_init() {
    for (int i = 0; i < TLB_SIZE; i++) {
        tlb[i].page_number = -1;
        tlb[i].frame_number = -1;
        tlb[i].last_used = 0;
    }
    next_tlb_index = 0;
    timer = 0;
}

int tlb_lookup(int page_number) {
    timer++;
    for (int i = 0; i < TLB_SIZE; i++) {
        if (tlb[i].page_number == page_number) {
            tlb[i].last_used = timer;
            return tlb[i].frame_number;
        }
    }
    return -1;
}

void tlb_update(int page_number, int frame_number) {
    timer++;
    // Check if entry already exists (update it)
    for (int i = 0; i < TLB_SIZE; i++) {
        if (tlb[i].page_number == page_number) {
            tlb[i].frame_number = frame_number;
            tlb[i].last_used = timer;
            return;
        }
    }

    // Find a slot: either empty or least recently used
    int lru_index = 0;
    unsigned int min_time = tlb[0].last_used;
    
    for (int i = 0; i < TLB_SIZE; i++) {
        if (tlb[i].page_number == -1) {
            lru_index = i;
            break;
        }
        if (tlb[i].last_used < min_time) {
            min_time = tlb[i].last_used;
            lru_index = i;
        }
    }

    tlb[lru_index].page_number = page_number;
    tlb[lru_index].frame_number = frame_number;
    tlb[lru_index].last_used = timer;
}
