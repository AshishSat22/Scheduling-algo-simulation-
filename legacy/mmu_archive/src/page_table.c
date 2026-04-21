#include "../include/page_table.h"

static PageTableEntry page_table[NUM_PAGES];

void page_table_init() {
    for (int i = 0; i < NUM_PAGES; i++) {
        page_table[i].frame_number = -1;
        page_table[i].valid = false;
    }
}

int page_table_lookup(int page_number) {
    if (page_number >= 0 && page_number < NUM_PAGES) {
        if (page_table[page_number].valid) {
            return page_table[page_number].frame_number;
        }
    }
    return -1;
}

void page_table_update(int page_number, int frame_number, bool valid) {
    if (page_number >= 0 && page_number < NUM_PAGES) {
        page_table[page_number].frame_number = frame_number;
        page_table[page_number].valid = valid;
    }
}
