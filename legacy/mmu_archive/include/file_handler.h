#ifndef FILE_HANDLER_H
#define FILE_HANDLER_H

#include <stdio.h>

void open_files(const char* backing_store_path);
void close_files();
void read_page_from_disk(int page_number, signed char* buffer);

#endif
