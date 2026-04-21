#ifndef MEMORY_MANAGER_H
#define MEMORY_MANAGER_H

#include "common.h"
#include "algorithms.h"

void memory_manager_init(AlgorithmType algo);
int translate_address(int logical_address, TranslationStatus* status);
signed char read_memory(int physical_address);
void get_metrics(int* faults, int* hits);

#endif
