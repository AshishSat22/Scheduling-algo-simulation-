#include "../include/file_handler.h"
#include "../include/common.h"

static FILE* backing_store = NULL;

void open_files(const char* backing_store_path) {
    backing_store = fopen(backing_store_path, "rb");
    if (!backing_store) {
        fprintf(stderr, "Error: Could not open backing store %s\n", backing_store_path);
        exit(1);
    }
}

void close_files() {
    if (backing_store) {
        fclose(backing_store);
    }
}

void read_page_from_disk(int page_number, signed char* buffer) {
    if (fseek(backing_store, page_number * PAGE_SIZE, SEEK_SET) != 0) {
        fprintf(stderr, "Error seeking in backing store\n");
        return;
    }
    if (fread(buffer, sizeof(signed char), PAGE_SIZE, backing_store) != PAGE_SIZE) {
        fprintf(stderr, "Error reading from backing store\n");
    }
}
