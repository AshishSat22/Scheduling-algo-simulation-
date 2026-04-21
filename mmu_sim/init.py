import os
import subprocess
import sys

def setup_project():
    print("=== MMU Simulation Setup & Launcher ===")
    
    # 1. Ensure directories exist
    dirs = ["bin", "data", "src", "include"]
    for d in dirs:
        if not os.path.exists(d):
            os.makedirs(d)
            print(f"Created directory: {d}")

    # 2. Generate Data if missing
    if not os.path.exists("data/backing_store.bin") or not os.path.exists("data/addresses.txt"):
        print("Generating simulation data (backing_store.bin and addresses.txt)...")
        import generate_data
        generate_data.generate_binary_store()
        generate_data.generate_addresses()
    else:
        print("Simulation data already exists.")

    # 3. Check for compiler and compile C backend
    try:
        print("Attempting to compile C backend...")
        # Try running the batch file or direct gcc
        if os.name == 'nt': # Windows
            result = subprocess.run(["cmd", "/c", "compile.bat"], capture_output=True, text=True)
        else:
            result = subprocess.run(["gcc", "-Iinclude", "src/main.c", "src/tlb.c", "src/page_table.c", 
                                   "src/memory_manager.c", "src/algorithms.c", "src/file_handler.c", 
                                   "-o", "bin/mmu_sim"], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("C Backend compiled successfully.")
        else:
            print("Warning: Compilation failed. Ensure GCC is in your PATH.")
            print(result.stderr)
    except FileNotFoundError:
        print("Error: GCC compiler not found. Please install MinGW/GCC to run the C backend.")

    print("\nInitialization Complete!")
    print("---------------------------------------")
    print("1. Launch Visual Dashboard (Python GUI)")
    print("2. Run FIFO Simulation (C CLI)")
    print("3. Run LRU Simulation (C CLI)")
    print("4. Run Optimal Simulation (C CLI)")
    print("q. Exit")
    
    choice = input("\nSelect an option: ").lower()
    
    executable = "bin/mmu_sim.exe" if os.name == 'nt' else "bin/mmu_sim"
    
    if choice == '1':
        print("Launching Visualizer...")
        subprocess.Popen([sys.executable, "visualizer.py"])
    elif choice == '2':
        subprocess.run([executable, "FIFO"])
    elif choice == '3':
        subprocess.run([executable, "LRU"])
    elif choice == '4':
        subprocess.run([executable, "OPT"])
    elif choice == 'q':
        sys.exit()

if __name__ == "__main__":
    setup_project()
