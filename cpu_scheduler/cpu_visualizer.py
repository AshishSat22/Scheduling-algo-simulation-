import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class CPUSchedulerVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("OS CPU Scheduling Visualizer")
        self.root.geometry("1000x800")
        self.root.configure(bg="#1e1e1e")

        self.processes = []
        self.setup_ui()

    def setup_ui(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview", background="#2d2d2d", foreground="white", fieldbackground="#2d2d2d", rowheight=25)
        style.configure("Treeview.Heading", background="#4a4a4a", foreground="white", font=("Helvetica", 10, "bold"))
        style.map("Treeview", background=[('selected', '#007acc')])

        entry_frame = tk.LabelFrame(self.root, text="Input Processes", bg="#2d2d2d", fg="white", font=("Helvetica", 12))
        entry_frame.pack(fill="x", padx=10, pady=10)

        tk.Label(entry_frame, text="Arrival Time:", bg="#2d2d2d", fg="white").grid(row=0, column=0, padx=5, pady=5)
        self.arrival_entry = tk.Entry(entry_frame, width=10)
        self.arrival_entry.grid(row=0, column=1)

        tk.Label(entry_frame, text="Burst Time:", bg="#2d2d2d", fg="white").grid(row=0, column=2, padx=5, pady=5)
        self.burst_entry = tk.Entry(entry_frame, width=10)
        self.burst_entry.grid(row=0, column=3)

        tk.Button(entry_frame, text="Add Process", command=self.add_process, bg="#28a745", fg="white").grid(row=0, column=4, padx=10)
        
        self.tree = ttk.Treeview(self.root, columns=("PID", "Arr", "Burst", "Comp", "Turn", "Wait"), show="headings", height=8)
        for col in ("PID", "Arr", "Burst", "Comp", "Turn", "Wait"):
            self.tree.heading(col, text=col, anchor="center")
            self.tree.column(col, width=100, anchor="center")
        self.tree.pack(fill="x", padx=10, pady=10)
        
        # Add a subtle border around the tree
        self.tree.configure(style="Treeview")

        ctrl_frame = tk.Frame(self.root, bg="#1e1e1e")
        ctrl_frame.pack(fill="x", padx=10)

        self.algo_var = tk.StringVar(value="FCFS")
        ttk.Combobox(ctrl_frame, textvariable=self.algo_var, values=["FCFS", "SJF", "SRTF", "Round Robin"]).pack(side="left", padx=5)
        
        tk.Label(ctrl_frame, text="Quantum:", bg="#1e1e1e", fg="white").pack(side="left", padx=5)
        self.quantum_entry = tk.Entry(ctrl_frame, width=5)
        self.quantum_entry.insert(0, "2")
        self.quantum_entry.pack(side="left")

        tk.Button(ctrl_frame, text="Simulate (All)", command=self.run_full_sim, bg="#007acc", fg="white", font=("Helvetica", 10, "bold")).pack(side="left", padx=5)
        tk.Button(ctrl_frame, text="Next Step", command=self.next_step, bg="#f39c12", fg="white", font=("Helvetica", 10, "bold")).pack(side="left", padx=5)
        tk.Button(ctrl_frame, text="How it Works?", command=self.show_help, bg="#e67e22", fg="white", font=("Helvetica", 10, "bold")).pack(side="right", padx=5)
        tk.Button(ctrl_frame, text="Clear Results", command=self.reset, bg="#dc3545", fg="white", width=12).pack(side="right", padx=5)
        tk.Button(ctrl_frame, text="Delete All", command=self.clear_all, bg="#636e72", fg="white", width=12).pack(side="right", padx=5)

        self.chart_frame = tk.Frame(self.root, bg="#2d2d2d")
        self.chart_frame.pack(fill="both", expand=True, padx=10, pady=10)

    def add_process(self):
        try:
            arr = int(self.arrival_entry.get())
            burst = int(self.burst_entry.get())
            pid = len(self.processes) + 1
            self.processes.append({'pid': pid, 'arrival': arr, 'burst': burst})
            self.tree.insert("", "end", values=(pid, arr, burst, "-", "-", "-"))
            self.arrival_entry.delete(0, tk.END)
            self.burst_entry.delete(0, tk.END)
        except ValueError: messagebox.showerror("Error", "Enter valid integers")

    def show_help(self):
        help_text = "DOCTOR'S CLINIC ANALOGY:\n- Patients = Processes\n- Doctor = CPU\n- Waiting Room = Ready Queue\n\nFCFS: First patient in line.\nSJF: Shortest treatment first.\nSRTF: Switches to shorter patient immediately.\nRound Robin: Everyone gets 2 mins."
        messagebox.showinfo("Help", help_text)

    def run_full_sim(self):
        if not self.processes: return
        algo = self.algo_var.get()
        proc_list = [dict(p) for p in self.processes]
        proc_list.sort(key=lambda x: x['arrival'])
        
        gantt = []
        time = 0
        completed = 0
        for p in proc_list: p['rem'] = p['burst']

        while completed < len(proc_list):
            available = [p for p in proc_list if p['arrival'] <= time and p['rem'] > 0]
            if not available:
                time += 1
                continue
            
            if algo == "FCFS": p = min(available, key=lambda x: x['arrival'])
            elif algo == "SJF": p = min(available, key=lambda x: x['burst'])
            elif algo == "SRTF": p = min(available, key=lambda x: x['rem'])
            elif algo == "Round Robin": p = available[0] # Simplified block logic

            execute = 1
            if algo == "FCFS" or algo == "SJF": execute = p['rem']
            elif algo == "Round Robin": execute = min(p['rem'], int(self.quantum_entry.get()))

            gantt.append((p['pid'], time, time + execute))
            time += execute
            p['rem'] -= execute
            if p['rem'] == 0:
                p['comp'] = time
                completed += 1
                for orig in self.processes:
                    if orig['pid'] == p['pid']: orig['comp'] = time

        self.update_table(self.processes)
        self.draw_gantt(gantt)

    def next_step(self):
        if not self.processes: return
        if not hasattr(self, 'state'):
            self.state = {'time': 0, 'gantt': [], 'completed': 0, 'procs': [dict(p) for p in self.processes]}
            for p in self.state['procs']: p['rem'] = p['burst']
        
        s = self.state
        if s['completed'] >= len(self.processes): return

        avail = [p for p in s['procs'] if p['arrival'] <= s['time'] and p['rem'] > 0]
        if avail:
            algo = self.algo_var.get()
            if algo == "FCFS": p = min(avail, key=lambda x: x['arrival'])
            elif algo == "SJF": p = min(avail, key=lambda x: x['burst'])
            else: p = min(avail, key=lambda x: x['rem']) # SRTF/RR simplified step
            
            p['rem'] -= 1
            s['gantt'].append((p['pid'], s['time'], s['time'] + 1))
            s['time'] += 1
            if p['rem'] == 0:
                s['completed'] += 1
                for orig in self.processes:
                    if orig['pid'] == p['pid']: orig['comp'] = s['time']
        else: s['time'] += 1

        self.update_table(self.processes)
        self.draw_gantt(s['gantt'])

    def update_table(self, data):
        for item in self.tree.get_children(): self.tree.delete(item)
        for p in data:
            comp = p.get('comp', '-')
            turn = comp - p['arrival'] if comp != '-' else '-'
            wait = turn - p['burst'] if turn != '-' else '-'
            self.tree.insert("", "end", values=(p['pid'], p['arrival'], p['burst'], comp, turn, wait))

    def draw_gantt(self, data):
        for w in self.chart_frame.winfo_children(): w.destroy()
        if not data: return
        fig, ax = plt.subplots(figsize=(8, 2))
        ax.set_yticks([])
        for pid, start, end in data:
            ax.broken_barh([(start, end-start)], (0, 10), facecolors=plt.cm.tab10(pid%10), edgecolors="black")
            ax.text(start+(end-start)/2, 5, f"P{pid}", ha='center', va='center', fontweight='bold', color='white')
        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both")

    def reset(self):
        # Clear only the simulation state, KEEP the processes
        if hasattr(self, 'state'): del self.state
        for p in self.processes:
            if 'comp' in p: del p['comp']
        self.update_table(self.processes)
        for w in self.chart_frame.winfo_children(): w.destroy()
        messagebox.showinfo("Reset", "Simulation cleared. You can now choose a new algorithm!")

    def clear_all(self):
        # Separate method if they want to start completely fresh
        self.processes = []
        self.reset()

if __name__ == "__main__":
    root = tk.Tk()
    app = CPUSchedulerVisualizer(root)
    root.mainloop()
