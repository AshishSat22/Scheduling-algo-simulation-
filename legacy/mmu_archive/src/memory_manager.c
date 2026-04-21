#include "../include/memory_manager.h"
#include "../include/tlb.h"
#include "../include/page_table.h"
#include "../include/file_handler.h"
#include "../include/algorithms.h"

static signed char physical_memory[PHYSICAL_MEMORY_SIZE];
static int page_faults = 0;
static int tlb_hits = 0;
static AlgorithmType current_algo;

void memory_manager_init(AlgorithmType algo) {
    tlb_init();
    page_table_init();
    current_algo = algo;
    page_faults = 0;
    tlb_hits = 0;
}

int translate_address(int logical_address, TranslationStatus* status) {
    int page_number = (logical_address >> 8) & 0xFF;
    int offset = logical_address & 0xFF;

    // 1. Try TLB
    int frame_number = tlb_lookup(page_number);
    if (frame_number != -1) {
        *status = TLB_HIT;
        tlb_hits++;
    } else {
        // 2. Try Page Table
        frame_number = page_table_lookup(page_number);
        if (frame_number != -1) {
            *status = PAGE_TABLE_HIT;
            tlb_update(page_number, frame_number);
        } else {
            // 3. Page Fault
            *status = PAGE_FAULT;
            page_faults++;

            // Select a frame using replacement algorithm
            frame_number = select_victim_frame(current_algo);

            // Read from disk into the frame
            read_page_from_disk(page_number, &physical_memory[frame_number * PAGE_SIZE]);

            // Update structures
            page_table_update(page_number, frame_number, true);
            tlb_update(page_number, frame_number);
        }
    }

    update_algorithm_state(frame_number, page_number);
    return (frame_number * PAGE_SIZE) + offset;
}

signed char read_memory(int physical_address) {
    if (physical_address >= 0 && physical_address < PHYSICAL_MEMORY_SIZE) {
        return physical_memory[physical_address];
    }
    return 0;
}

void get_metrics(int* faults, int* hits) {
    *faults = page_faults;
    *hits = tlb_hits;
}
