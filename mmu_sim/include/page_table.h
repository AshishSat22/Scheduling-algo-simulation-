#ifndef PAGE_TABLE_H
#define PAGE_TABLE_H

#include "common.h"

void page_table_init();
int page_table_lookup(int page_number);
void page_table_update(int page_number, int frame_number, bool valid);

#endif
