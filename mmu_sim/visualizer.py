import tkinter as tk
from tkinter import ttk, messagebox
import random
import os
import generate_data

# Constants matching C implementation
PAGE_SIZE = 256
NUM_PAGES = 256
TLB_SIZE = 16
NUM_FRAMES = 128

class MMUVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("OS MMU Simulation Dashboard")
        self.root.geometry("1400x900")
        self.root.configure(bg="#1e1e1e")

        # Simulation State
        self.tlb = [] 
        self.page_table = [-1] * NUM_PAGES
        self.ram = [None] * NUM_FRAMES
        self.addresses = []
        self.current_index = 0
        self.timer = 0
        self.is_running = False  # Track if auto-run is active
        
        # Metrics
        self.total_faults = 0
        self.total_tlb_hits = 0
        self.total_pt_hits = 0

        self.ensure_data()
        self.setup_ui()
        self.load_data()

    def ensure_data(self):
        if not os.path.exists("data"):
            os.makedirs("data")
        if not os.path.exists("data/backing_store.bin") or not os.path.exists("data/addresses.txt"):
            generate_data.generate_binary_store()
            generate_data.generate_addresses()

    def setup_ui(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview", background="#2d2d2d", foreground="white", fieldbackground="#2d2d2d", rowheight=25)
        style.map("Treeview", background=[('selected', '#4a4a4a')])
        
        # Main Layout
        top_frame = tk.Frame(self.root, bg="#1e1e1e", pady=10)
        top_frame.pack(fill="x")

        title_label = tk.Label(top_frame, text="Memory Management Unit (MMU) Simulator", font=("Helvetica", 24, "bold"), fg="#ffffff", bg="#1e1e1e")
        title_label.pack()

        # Control Panel
        control_frame = tk.Frame(self.root, bg="#2d2d2d", padx=20, pady=10)
        control_frame.pack(fill="x", padx=20, pady=10)

        self.algo_var = tk.StringVar(value="FIFO")
        tk.Label(control_frame, text="Algorithm:", fg="white", bg="#2d2d2d", font=("Helvetica", 12)).pack(side="left")
        ttk.Combobox(control_frame, textvariable=self.algo_var, values=["FIFO"]).pack(side="left", padx=10)
        
        tk.Button(control_frame, text="Next Step", command=self.next_step, bg="#007acc", fg="white", font=("Helvetica", 12, "bold"), width=12).pack(side="left", padx=5)
        self.btn_run = tk.Button(control_frame, text="Auto Run", command=self.start_auto_run, bg="#28a745", fg="white", font=("Helvetica", 12, "bold"), width=12)
        self.btn_run.pack(side="left", padx=5)
        tk.Button(control_frame, text="Stop", command=self.stop_auto_run, bg="#f1c40f", fg="black", font=("Helvetica", 12, "bold"), width=12).pack(side="left", padx=5)
        tk.Button(control_frame, text="Reset", command=self.reset_sim, bg="#dc3545", fg="white", font=("Helvetica", 12, "bold"), width=12).pack(side="left", padx=5)
        tk.Button(control_frame, text="How it Works?", command=self.show_help, bg="#f39c12", fg="white", font=("Helvetica", 12, "bold"), width=15).pack(side="right", padx=5)

        # Dashboard Area
        dash_frame = tk.Frame(self.root, bg="#1e1e1e")
        dash_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Left Column: TLB and Page Table
        left_col = tk.Frame(dash_frame, bg="#1e1e1e")
        left_col.pack(side="left", fill="both", expand=True)

        tk.Label(left_col, text="TLB (Top 16 Entries)", fg="#61afef", bg="#1e1e1e", font=("Helvetica", 14, "bold")).pack()
        self.tlb_tree = ttk.Treeview(left_col, columns=("Page", "Frame"), show="headings", height=8)
        self.tlb_tree.heading("Page", text="Page Number")
        self.tlb_tree.heading("Frame", text="Frame Number")
        self.tlb_tree.pack(fill="x", pady=5)

        tk.Label(left_col, text="Recent Page Table Entries", fg="#e06c75", bg="#1e1e1e", font=("Helvetica", 14, "bold")).pack()
        self.pt_tree = ttk.Treeview(left_col, columns=("Page", "Frame", "Status"), show="headings", height=15)
        self.pt_tree.heading("Page", text="Page Number")
        self.pt_tree.heading("Frame", text="Frame Number")
        self.pt_tree.heading("Status", text="Status")
        self.pt_tree.pack(fill="x", pady=5)

        # Middle Column: RAM Frames
        mid_col = tk.Frame(dash_frame, bg="#1e1e1e")
        mid_col.pack(side="left", fill="both", expand=True, padx=20)

        tk.Label(mid_col, text="RAM Frames (Physical Memory)", fg="#98c379", bg="#1e1e1e", font=("Helvetica", 14, "bold")).pack()
        self.ram_tree = ttk.Treeview(mid_col, columns=("Frame", "Page"), show="headings", height=25)
        self.ram_tree.heading("Frame", text="Frame ID")
        self.ram_tree.heading("Page", text="Resident Page")
        self.ram_tree.pack(fill="both", expand=True, pady=5)

        # Right Column: Event Log & Metrics
        right_col = tk.Frame(dash_frame, bg="#1e1e1e", width=400)
        right_col.pack(side="right", fill="both")

        tk.Label(right_col, text="Real-Time Event Log", fg="#d19a66", bg="#1e1e1e", font=("Helvetica", 14, "bold")).pack()
        self.log_text = tk.Text(right_col, height=15, width=40, bg="#2d2d2d", fg="white", font=("Consolas", 10))
        self.log_text.pack(pady=5)

        # Metrics display
        metrics_frame = tk.LabelFrame(right_col, text="Live Metrics", bg="#2d2d2d", fg="white", font=("Helvetica", 12))
        metrics_frame.pack(fill="x", pady=20)

        self.lbl_faults = tk.Label(metrics_frame, text="Page Faults: 0", bg="#2d2d2d", fg="#e06c75", font=("Helvetica", 12))
        self.lbl_faults.pack(anchor="w", padx=10, pady=2)
        self.lbl_tlb = tk.Label(metrics_frame, text="TLB Hits: 0", bg="#2d2d2d", fg="#61afef", font=("Helvetica", 12))
        self.lbl_tlb.pack(anchor="w", padx=10, pady=2)
        self.lbl_hit_rate = tk.Label(metrics_frame, text="TLB Hit Rate: 0.00%", bg="#2d2d2d", fg="white", font=("Helvetica", 12))
        self.lbl_hit_rate.pack(anchor="w", padx=10, pady=2)

        # Stage Tracker Panel
        self.stage_frame = tk.LabelFrame(right_col, text="Instruction Execution Stages", bg="#2d2d2d", fg="white", font=("Helvetica", 12))
        self.stage_frame.pack(fill="x", pady=10)
        
        self.stages = []
        for i, text in enumerate(["1. Fetch Instruction", "2. Translate Address", "3. Retrieve Data", "4. Process Output"]):
            lbl = tk.Label(self.stage_frame, text=text, bg="#2d2d2d", fg="#5c6370", font=("Helvetica", 11, "bold"))
            lbl.pack(anchor="w", padx=10, pady=2)
            self.stages.append(lbl)

        # Legend (Bottom)
        legend_frame = tk.Frame(self.root, bg="#2d2d2d", pady=5)
        legend_frame.pack(side="bottom", fill="x")
        
        tk.Label(legend_frame, text="LEGEND: ", fg="white", bg="#2d2d2d", font=("Helvetica", 10, "bold")).pack(side="left", padx=10)
        tk.Label(legend_frame, text="● TLB HIT (Fast)", fg="#98c379", bg="#2d2d2d").pack(side="left", padx=5)
        tk.Label(legend_frame, text="● PT HIT (Found)", fg="#d19a66", bg="#2d2d2d").pack(side="left", padx=5)
        tk.Label(legend_frame, text="● PAGE FAULT (Slow Disk Read)", fg="#e06c75", bg="#2d2d2d").pack(side="left", padx=5)

    def load_data(self):
        try:
            with open("data/addresses.txt", "r") as f:
                self.addresses = [int(line.strip()) for line in f if line.strip()]
            self.log(f"Loaded {len(self.addresses)} addresses from file.")
        except FileNotFoundError:
            self.log("Error: data/addresses.txt not found!")

    def log(self, message, color="white"):
        self.log_text.insert(tk.END, f"> {message}\n")
        self.log_text.see(tk.END)

    def update_ui_colors(self, status):
        color_map = {
            "TLB HIT": "#98c379",     # Green
            "PT HIT": "#d19a66",      # Orange
            "PAGE FAULT": "#e06c75"   # Red
        }
        self.log_text.tag_config(status, foreground=color_map[status])
        self.log_text.insert(tk.END, f"STATUS: {status}\n", status)

    def show_help(self):
        help_text = (
            "THE LIBRARY ANALOGY\n\n"
            "1. DISK (Backing Store): A massive warehouse of books. Very slow to access.\n"
            "2. RAM (Physical Memory): Your desk. Fast but can only hold a few books.\n"
            "3. PAGE FAULT (Red): Trying to read a book that isn't on your desk. "
            "The Librarian must go to the warehouse to get it.\n"
            "4. TLB (Green): A small sticky note in your hand with the last 16 book locations.\n"
            "5. PAGE TABLE (Orange): An index card list showing which warehouse books are on the desk."
        )
        messagebox.showinfo("Simulated Memory Concepts", help_text)

    def next_step(self):
        if self.current_index >= len(self.addresses):
            messagebox.showinfo("Done", "Simulation complete!")
            return

        # Reset Stage Colors
        for s in self.stages: s.config(fg="#5c6370")
        
        addr = self.addresses[self.current_index]
        self.stages[0].config(fg="#61afef") # Blue for Fetch
        
        page_num = (addr >> 8) & 0xFF
        offset = addr & 0xFF
        self.timer += 1
        
        # Stage 2: Translate
        self.stages[1].config(fg="#d19a66") # Orange for Translate
        
        status = ""
        frame_num = -1
        # ... logic ...

        # 1. TLB Lookup
        tlb_hit = False
        for entry in self.tlb:
            if entry['page'] == page_num:
                frame_num = entry['frame']
                tlb_hit = True
                break
        
        if tlb_hit:
            status = "TLB HIT"
            self.total_tlb_hits += 1
        else:
            # 2. Page Table Lookup
            if self.page_table[page_num] != -1:
                status = "PT HIT"
                frame_num = self.page_table[page_num]
                self.total_pt_hits += 1
                # Update TLB
                self.update_tlb(page_num, frame_num)
            else:
                # 3. Page Fault
                status = "PAGE FAULT"
                self.total_faults += 1
                
                # Replacement Logic (Simplified for Visualizer)
                frame_num = self.find_replacement_frame(page_num)
                self.page_table[page_num] = frame_num
                self.update_tlb(page_num, frame_num)

        physical_addr = (frame_num * PAGE_SIZE) + offset
        
        # Stage 3: Retrieve 
        self.stages[2].config(fg="#98c379") # Green for Fetch
        
        # Stage 4: Output
        self.stages[3].config(fg="#ffffff")
        self.log(f"OUTPUT: Retrieved Value {random.randint(0, 255)} from Address {addr}")
        
        # Log event
        self.log(f"Addr: {addr} -> Page: {page_num}, Offset: {offset}")
        self.log(f"Phys Addr: {physical_addr} (Frame {frame_num})")
        self.update_ui_colors(status)
        self.log("-" * 30)

        # Refresh Trees
        self.refresh_trees()
        self.update_metrics()
        
        self.current_index += 1

    def update_tlb(self, page, frame):
        # Remove if exists
        self.tlb = [e for e in self.tlb if e['page'] != page]
        # FIFO behavior for visualizer TLB
        if len(self.tlb) >= TLB_SIZE:
            self.tlb.pop(0)
        self.tlb.append({'page': page, 'frame': frame})

    def find_replacement_frame(self, page_num):
        # First check for free frames
        for i in range(NUM_FRAMES):
            if self.ram[i] is None:
                self.ram[i] = {'page': page_num, 'time': self.timer}
                return i
        
        # Algorithm select
        algo = self.algo_var.get()
        if algo == "FIFO":
            # Simple circular for visualizer demo
            idx = (self.total_faults - 1) % NUM_FRAMES
        else: # LRU
            idx = min(range(NUM_FRAMES), key=lambda i: self.ram[i]['time'])
            
        # Invalidate old page in page table
        old_page = self.ram[idx]['page']
        self.page_table[old_page] = -1
        # Invalidate in TLB
        self.tlb = [e for e in self.tlb if e['page'] != old_page]
        
        # Load new
        self.ram[idx] = {'page': page_num, 'time': self.timer}
        return idx

    def refresh_trees(self):
        # Clear
        self.tlb_tree.delete(*self.tlb_tree.get_children())
        self.pt_tree.delete(*self.pt_tree.get_children())
        self.ram_tree.delete(*self.ram_tree.get_children())

        for entry in reversed(self.tlb):
            self.tlb_tree.insert("", "end", values=(entry['page'], entry['frame']))
        
        # Only show active pages in PT tree for visibility
        count = 0
        for p, f in enumerate(self.page_table):
            if f != -1:
                self.pt_tree.insert("", "end", values=(p, f, "Valid"))
                count += 1
                if count > 20: break # Keep it concise

        for i, val in enumerate(self.ram):
            p = val['page'] if val else "Empty"
            self.ram_tree.insert("", "end", values=(i, p))

    def update_metrics(self):
        self.lbl_faults.config(text=f"Page Faults: {self.total_faults}")
        self.lbl_tlb.config(text=f"TLB Hits: {self.total_tlb_hits}")
        total = self.total_tlb_hits + self.total_pt_hits + self.total_faults
        if total > 0:
            rate = (self.total_tlb_hits / total) * 100
            self.lbl_hit_rate.config(text=f"TLB Hit Rate: {rate:.2f}%")

    def start_auto_run(self):
        self.is_running = True
        self.btn_run.config(state="disabled")
        self.auto_run_loop()

    def stop_auto_run(self):
        self.is_running = False
        self.btn_run.config(state="normal")

    def auto_run_loop(self):
        if self.is_running and self.current_index < len(self.addresses):
            self.next_step()
            self.root.after(100, self.auto_run_loop)
        else:
            self.stop_auto_run()

    def reset_sim(self):
        self.stop_auto_run()
        self.current_index = 0
        self.total_faults = 0
        self.total_tlb_hits = 0
        self.total_pt_hits = 0
        self.tlb = []
        self.page_table = [-1] * NUM_PAGES
        self.ram = [None] * NUM_FRAMES
        self.log_text.delete(1.0, tk.END)
        self.refresh_trees()
        self.update_metrics()

if __name__ == "__main__":
    root = tk.Tk()
    app = MMUVisualizer(root)
    root.mainloop()
