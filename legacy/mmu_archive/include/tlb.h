#ifndef TLB_H
#define TLB_H

#include "common.h"

void tlb_init();
int tlb_lookup(int page_number);
void tlb_update(int page_number, int frame_number);

#endif
