import os
import subprocess
import sys

def setup_project():
    # Return to root if inside a subfolder
    if os.path.basename(os.getcwd()) in ["mmu_sim", "cpu_scheduler", "process_sim"]:
        os.chdir("..")

    print("\n" + "═"*60)
    print("        OPERATING SYSTEM ARCHITECTURE SIMULATOR              ")
    print("═"*60)
    print("1. Process State Lifecycle Simulation (New, Ready, Run...)")
    print("2. CPU Scheduling Algorithms (FCFS, SJF, RR...)")
    print("q. Exit")
    
    choice = input("\nSelect Module (1-2): ").lower()
    if choice == '1':
        run_process_module()
    elif choice == '2':
        run_cpu_module()
    elif choice == 'q':
        sys.exit()

def run_process_module():
    if not os.path.exists("process_sim"):
        print("Error: process_sim directory missing.")
        return
    os.chdir("process_sim")
    
    print("\n[Module 1: Process State Simulation]")
    print("Opening Interactive Dashboard...")
    subprocess.Popen([sys.executable, "visualizer.py"])
    
    input("\nPress Enter to return to main menu...")
    setup_project()

def run_cpu_module():
    if not os.path.exists("cpu_scheduler"):
        print("Error: cpu_scheduler directory missing.")
        return
    os.chdir("cpu_scheduler")
    
    if not os.path.exists("bin"): os.makedirs("bin")
    if not os.path.exists("bin/scheduler.exe") and os.name == 'nt':
        print("Compiling CPU module...")
        subprocess.run(["gcc", "-Iinclude", "src/main.c", "src/scheduler_algos.c", "-o", "bin/scheduler.exe"])

    print("\n[Module 2: CPU Scheduler]")
    print("1. Visual Dashboard (Gantt Chart)\n2. Run FCFS (CLI)\n3. Run SJF (CLI)\n4. Run SRTF (CLI)\n5. Run Round Robin (CLI)\nb. Back")
    c = input("\nSelect: ").lower()
    
    executable = "bin/scheduler.exe" if os.name == 'nt' else "bin/scheduler"
    if c == '1': subprocess.Popen([sys.executable, "cpu_visualizer.py"])
    elif c == '2': subprocess.run([executable, "FCFS"])
    elif c == '3': subprocess.run([executable, "SJF"])
    elif c == '4': subprocess.run([executable, "SRTF"])
    elif c == '5': 
        q = input("Enter Time Quantum (default 2): ") or "2"
        subprocess.run([executable, "RR", q])
    elif c == 'b': setup_project()

if __name__ == "__main__":
    setup_project()
