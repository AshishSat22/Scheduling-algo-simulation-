@echo off
echo Compiling MMU Simulation...
gcc -Iinclude src/main.c src/tlb.c src/page_table.c src/memory_manager.c src/algorithms.c src/file_handler.c -o bin/mmu_sim.exe
if %ERRORLEVEL% EQU 0 (
    echo Compilation successful! Binary located at bin/mmu_sim.exe
) else (
    echo Compilation failed.
)
