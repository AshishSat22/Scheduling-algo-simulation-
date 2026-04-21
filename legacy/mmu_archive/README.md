# MMU Virtual Memory Simulation

A high-fidelity Modular Virtual Memory Manager simulation implementing a 16-bit logical address space, TLB, Page Table, and demand paging from a binary backing store.

## 🚀 Features
- **Strictly Modular C Backend**: Clear separation of TLB, Page Table, and Memory Logic.
- **Replacement Algorithms**: 
  - **FIFO** (First-In, First-Out)
  - **LRU** (Least Recently Used)
  - **Optimal** (Look-ahead future reference scanning)
- **Academic Dashboard**: A Python/Tkinter GUI to visualize step-by-step translation and frame replacement.
- **Demand Paging**: Loads 256-byte pages from `backing_store.bin` only when needed.

## 📁 Project Structure
- `src/`: C source files (main, tlb, page_table, algorithms, etc.)
- `include/`: Header files defining constants and interfaces.
- `data/`: Simulation data (addresses.txt, backing_store.bin).
- `bin/`: Compiled executable location.
- `visualizer.py`: The Python visualization dashboard.

## 🛠️ Compilation & Setup

### 1. Prerequisites
- **GCC** (MinGW for Windows)
- **Python 3.x** with Tkinter (usually included)

### 2. Generate Data Files
Run the utility script to create the binary backing store and random addresses:
```bash
python generate_data.py
```

### 3. Compile C Backend
Use the provided batch script:
```bash
compile.bat
```

### 4. Run Simulation (C CLI)
Pass the algorithm type as an argument:
```bash
bin/mmu_sim.exe FIFO
bin/mmu_sim.exe LRU
bin/mmu_sim.exe OPT
```

### 5. Run Visualizer (Python GUI)
```bash
python visualizer.py
```

## 📊 Performance Metrics
The simulation reports:
- Total page faults and fault rate.
- TLB hits and hit ratio.
- Physical address translations and byte values read from disk.
