import os
import subprocess
import sys

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main_menu():
    clear_screen()
    print("\n" + "═"*60)
    print("        OPERATING SYSTEM ARCHITECTURE SIMULATOR              ")
    print("═"*60)
    print(" 1. Process State Lifecycle Simulator")
    print("    [Interactive math, manual transitions, interrupts]")
    print("\n 2. CPU Scheduling Algorithms")
    print("    [FCFS, SJF, SRTF, Round Robin with Gantt Charts]")
    print("\n q. Exit Simulator")
    print("═"*60)
    
    choice = input("\n[Main] Select Module (1 or 2): ").lower()
    if choice == '1':
        launch_module("modules/process_sim")
    elif choice == '2':
        # Handles both cases: if it moved to modules or stayed in root
        if os.path.exists("modules/cpu_scheduler"):
            launch_module("modules/cpu_scheduler")
        else:
            launch_module("cpu_scheduler")
    elif choice == 'q':
        print("\nExiting. Have a great session!")
        sys.exit()
    else:
        main_menu()

def launch_module(path):
    clear_screen()
    if not os.path.exists(path):
        print(f"Error: Module directory '{path}' not found.")
        input("\nPress Enter to return...")
        main_menu()
        return

    os.chdir(path)
    
    # Identify the correct visualizer to launch
    if "process_sim" in path:
        print(f"\n🚀 Launching Process State Simulator...")
        subprocess.Popen([sys.executable, "visualizer.py"])
    elif "cpu_scheduler" in path:
        print(f"\n🚀 Launching CPU Scheduler Dashboard...")
        # Compile C backend if needed
        if not os.path.exists("bin/scheduler.exe") and os.name == 'nt':
            print("  - Compiling C logic...")
            if not os.path.exists("bin"): os.makedirs("bin")
            subprocess.run(["gcc", "-Iinclude", "src/main.c", "src/scheduler_algos.c", "-o", "bin/scheduler.exe"])
        subprocess.Popen([sys.executable, "cpu_visualizer.py"])
    
    input("\n✅ Module Running. Press Enter to close and return to Main Menu...")
    os.chdir("../..") if "modules" in path else os.chdir("..")
    main_menu()

if __name__ == "__main__":
    main_menu()
