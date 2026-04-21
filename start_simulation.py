import os
import subprocess
import sys

# Change directory to the simulation folder
sim_dir = "mmu_sim"

if not os.path.exists(sim_dir):
    print(f"Error: {sim_dir} directory not found.")
    sys.exit(1)

os.chdir(sim_dir)

# Run the project's init script
subprocess.run([sys.executable, "init.py"])
