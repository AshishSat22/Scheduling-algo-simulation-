#include <stdio.h>
#include <string.h>
#include "../include/memory_manager.h"
#include "../include/file_handler.h"

#define MAX_ADDRESSES 2000

int main(int argc, char* argv[]) {
    if (argc < 2) {
        printf("Usage: %s <FIFO|LRU|OPT>\n", argv[0]);
        return 1;
    }

    AlgorithmType algo;
    if (strcmp(argv[1], "FIFO") == 0) algo = ALGO_FIFO;
    else if (strcmp(argv[1], "OPT") == 0) algo = ALGO_OPTIMAL;
    else {
        printf("Invalid algorithm. Use FIFO or OPT.\n");
        return 1;
    }

    FILE* address_file = fopen("data/addresses.txt", "r");
    if (!address_file) {
        perror("Error opening addresses.txt");
        return 1;
    }

    int addresses[MAX_ADDRESSES];
    int pages[MAX_ADDRESSES];
    int count = 0;
    while (count < MAX_ADDRESSES && fscanf(address_file, "%d", &addresses[count]) == 1) {
        pages[count] = (addresses[count] >> 8) & 0xFF;
        count++;
    }
    fclose(address_file);

    open_files("data/backing_store.bin");
    memory_manager_init(algo);

    if (algo == ALGO_OPTIMAL) {
        init_optimal_algorithm(pages, count);
    }

    printf("Logical Address | Physical Address | Value | Type\n");
    printf("--------------------------------------------------\n");

    for (int i = 0; i < count; i++) {
        TranslationStatus status;
        int physical_address = translate_address(addresses[i], &status);
        signed char value = read_memory(physical_address);

        const char* type_str;
        switch(status) {
            case TLB_HIT: type_str = "TLB Hit"; break;
            case PAGE_TABLE_HIT: type_str = "PT Hit "; break;
            case PAGE_FAULT: type_str = "Fault  "; break;
        }

        printf("%15d | %16d | %5d | %s\n", addresses[i], physical_address, value, type_str);
    }

    int faults, hits;
    get_metrics(&faults, &hits);

    printf("\n--- Performance Metrics ---\n");
    printf("Total Addresses: %d\n", count);
    printf("Page Faults:     %d (%.2f%%)\n", faults, (float)faults/count * 100);
    printf("TLB Hits:        %d (%.2f%%)\n", hits, (float)hits/count * 100);

    close_files();
    return 0;
}
