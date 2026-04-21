import tkinter as tk
from tkinter import messagebox

class ProcessStateVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("OS Process State Simulator")
        self.root.geometry("1000x750")
        self.root.configure(bg="#1e1e1e")

        self.current_state = "NEW"
        self.history_index = 0
        # Realistic OS Sequence for the math task
        self.state_sequence = ["NEW", "READY", "RUNNING", "WAITING", "READY", "RUNNING", "TERMINATED"]
        self.problem = ""
        self.result = None
        self.pcb = {"PID": 1024, "State": "NEW", "Registers": "None", "Task": "IDLE"}

        self.coords = {
            "NEW": (60, 150),
            "READY": (210, 150),
            "RUNNING": (360, 150),
            "TERMINATED": (510, 150),
            "WAITING": (285, 380)
        }

        self.setup_ui()
        self.update_visuals()

    def setup_ui(self):
        tk.Label(self.root, text="Process State Transition Flow", font=("Helvetica", 20, "bold"), bg="#1e1e1e", fg="white").pack(pady=10)

        main_frame = tk.Frame(self.root, bg="#1e1e1e")
        main_frame.pack(fill="both", expand=True, padx=20)

        self.canvas = tk.Canvas(main_frame, width=700, height=500, bg="#2d2d2d", highlightthickness=0)
        self.canvas.pack(side="left")

        log_frame = tk.LabelFrame(main_frame, text="Transition Log", bg="#2d2d2d", fg="white")
        log_frame.pack(side="right", fill="both", expand=True, padx=10)
        self.log_box = tk.Text(log_frame, width=30, bg="#1e1e1e", fg="#abb2bf", font=("Consolas", 9))
        self.log_box.pack(fill="both", expand=True)

        math_frame = tk.Frame(self.root, bg="#1e1e1e")
        math_frame.pack(fill="x", padx=20, pady=5)
        self.math_entry = tk.Entry(math_frame, width=20, font=("Helvetica", 11))
        self.math_entry.pack(side="left", padx=10)
        tk.Button(math_frame, text="✅ Load Math Task", command=self.start_math_task, bg="#28a745", fg="white", font=("Helvetica", 10, "bold")).pack(side="left")
        
        nav_frame = tk.Frame(self.root, bg="#1e1e1e")
        nav_frame.pack(fill="x", padx=20, pady=5)
        tk.Button(nav_frame, text="⏪ Previous State", command=self.step_backward, bg="#636e72", fg="white").pack(side="left", padx=10)
        tk.Button(nav_frame, text="⏩ Next State", command=self.step_forward, bg="#2980b9", fg="white").pack(side="left", padx=10)
        tk.Button(nav_frame, text="⚠️ Trigger Interrupt", command=self.trigger_interrupt, bg="#c0392b", fg="white").pack(side="left", padx=20)

        self.pcb_lbl = tk.Label(self.root, text=self.get_pcb_text(), bg="#1e1e1e", fg="#98c379", font=("Consolas", 11))
        self.pcb_lbl.pack(pady=10)

    def draw_graph_base(self):
        self.canvas.delete("all")
        # NEW -> READY
        self.create_arrow(60, 150, 210, 150, "Admitted", "NEW_READY")
        # READY -> RUNNING
        self.create_arrow(210, 130, 360, 130, "Dispatch", "READY_RUNNING")
        # RUNNING -> READY
        self.create_arrow(360, 170, 210, 170, "Interrupt", "RUNNING_READY")
        # RUNNING -> TERMINATED
        self.create_arrow(360, 150, 510, 150, "Exit", "RUNNING_TERMINATED")
        # RUNNING -> WAITING
        self.create_arrow(360, 150, 285, 380, "I/O Wait", "RUNNING_WAITING")
        # WAITING -> READY
        self.create_arrow(285, 380, 210, 150, "I/O Done", "WAITING_READY")

    def create_arrow(self, x1, y1, x2, y2, label, tag):
        dx, dy = x2-x1, y2-y1
        dist = (dx**2 + dy**2)**0.5
        x1_adj, y1_adj = x1 + (dx/dist)*50, y1 + (dy/dist)*30
        x2_adj, y2_adj = x2 - (dx/dist)*50, y2 - (dy/dist)*30
        self.canvas.create_line(x1_adj, y1_adj, x2_adj, y2_adj, arrow=tk.LAST, fill="gray", width=2, tags=tag)
        self.canvas.create_text((x1+x2)/2, (y1+y2)/2 - 15, text=label, fill="gray", font=("Helvetica", 8), tags=tag)

    def update_visuals(self, skip_base=False):
        if not skip_base: self.draw_graph_base()
        if self.history_index > 0:
            prev = self.state_sequence[self.history_index-1]
            curr = self.state_sequence[self.history_index]
            tag = f"{prev}_{curr}"
            self.canvas.itemconfig(tag, fill="#f1c40f", width=4)

        for state, (x, y) in self.coords.items():
            color = "#61afef" if state == self.current_state else "#333"
            self.canvas.create_oval(x-50, y-30, x+50, y+30, fill=color, outline="white", width=2)
            self.canvas.create_text(x, y, text=state, fill="white", font=("Helvetica", 10, "bold"))
        self.pcb_lbl.config(text=self.get_pcb_text())

    def get_pcb_text(self):
        return f"PCB Info: [ PID: 1024 | State: {self.current_state} | Task: {self.pcb.get('Task','-')} | Reg: {self.pcb.get('Registers','-')} ]"

    def log(self, message):
        self.log_box.insert(tk.END, f"> {message}\n")
        self.log_box.see(tk.END)

    def start_math_task(self):
        expr = self.math_entry.get().strip()
        if not expr: return
        self.problem = expr
        self.history_index = 0
        try: self.result = eval(expr, {"__builtins__": None}, {})
        except: self.result = "Error"
        self.pcb = {"PID": 1024, "State": "NEW", "Registers": "0x00", "Task": f"Solving {expr}"}
        self.log(f"NEW TASK: '{expr}' created.")
        self.update_to_index(0)

    def trigger_interrupt(self):
        if self.current_state == "RUNNING":
            self.log("INTERRUPT: Process forced back to READY queue.")
            for i in range(self.history_index - 1, -1, -1):
                if self.state_sequence[i] == "READY":
                    self.history_index = i
                    break
            self.update_to_index(self.history_index, interrupted=True)
        else: messagebox.showinfo("Interrupt", "Only a RUNNING process can be interrupted.")

    def step_forward(self):
        if self.history_index < len(self.state_sequence) - 1:
            self.history_index += 1
            self.update_to_index(self.history_index)

    def step_backward(self):
        if self.history_index > 0:
            self.history_index -= 1
            self.update_to_index(self.history_index)

    def update_to_index(self, idx, interrupted=False):
        self.current_state = self.state_sequence[idx]
        self.canvas.delete("result_ui")
        self.update_visuals()
        
        if interrupted:
            self.canvas.itemconfig("RUNNING_READY", fill="#c0392b", width=4)

        if idx == 2 or idx == 5: self.pcb["Registers"] = "ALU Working..."
        elif idx == 3: self.pcb["Registers"] = "Waiting on Port 80"
        elif idx == len(self.state_sequence)-1: 
            self.pcb["Registers"] = f"Res: {self.result}"
            tx, ty = self.coords["TERMINATED"]
            self.canvas.create_rectangle(tx-80, ty+40, tx+80, ty+100, fill="#1e1e1e", outline="#98c379", tags="result_ui")
            self.canvas.create_text(tx, ty+60, text="COMPLETED", fill="#98c379", font=("Helvetica", 10, "bold"), tags="result_ui")
            self.canvas.create_text(tx, ty+85, text=f"{self.result}", fill="white", font=("Helvetica", 16, "bold"), tags="result_ui")

        self.log(f"TRANSITION: Now in {self.current_state}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ProcessStateVisualizer(root)
    root.mainloop()
