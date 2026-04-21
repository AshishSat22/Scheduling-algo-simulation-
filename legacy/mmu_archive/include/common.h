#ifndef COMMON_H
#define COMMON_H

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

#define PAGE_SIZE 256
#define NUM_PAGES 256
#define TLB_SIZE 16
#define NUM_FRAMES 128
#define PHYSICAL_MEMORY_SIZE (NUM_FRAMES * PAGE_SIZE)

// Result status for translation
typedef enum {
    TLB_HIT,
    PAGE_TABLE_HIT,
    PAGE_FAULT
} TranslationStatus;

// Data structure for TLB entry
typedef struct {
    int page_number;
    int frame_number;
    unsigned int last_used; // For LRU
} TLBEntry;

// Data structure for Page Table entry
typedef struct {
    int frame_number;
    bool valid;
} PageTableEntry;

#endif
