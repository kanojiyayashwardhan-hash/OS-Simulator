"""OS Simulator: interactive desktop visualization of core OS algorithms."""
import tkinter as tk
from tkinter import ttk, messagebox
from os_simulator.algorithms import cpu_schedule, bankers_algorithm, page_replacement

APP_TITLE = "OS Simulator | Operating Systems Mini Project"

class OSSimulator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("1120x760")
        self.minsize(900, 620)
        self.configure(bg="#f4f6fb")
        self._style()
        header = ttk.Frame(self, padding=(18, 14))
        header.pack(fill="x")
        ttk.Label(header, text="OS SIMULATOR", style="Title.TLabel").pack(anchor="w")
        ttk.Label(header, text="Visual learning lab for CPU scheduling, deadlock avoidance, and memory management", style="Subtitle.TLabel").pack(anchor="w", pady=(4, 0))
        self.tabs = ttk.Notebook(self)
        self.tabs.pack(fill="both", expand=True, padx=16, pady=(0, 16))
        self._build_cpu_tab()
        self._build_banker_tab()
        self._build_page_tab()
        footer = ttk.Label(self, text="B.Tech CSE | Yashwardhan Rajesh Kanojiya | Roll No. 42 | Academic Year 2026–2027", style="Footer.TLabel", anchor="center")
        footer.pack(fill="x", padx=10, pady=(0, 8))

    def _style(self):
        s = ttk.Style(self)
        try: s.theme_use("clam")
        except tk.TclError: pass
        s.configure("TFrame", background="#ffffff")
        s.configure("TLabel", background="#ffffff", foreground="#1f2937", font=("Segoe UI", 10))
        s.configure("Title.TLabel", background="#f4f6fb", foreground="#16213e", font=("Segoe UI", 22, "bold"))
        s.configure("Subtitle.TLabel", background="#f4f6fb", foreground="#596579", font=("Segoe UI", 10))
        s.configure("Footer.TLabel", background="#f4f6fb", foreground="#667085", font=("Segoe UI", 9))
        s.configure("TLabelframe", background="#ffffff", bordercolor="#dce2ed")
        s.configure("TLabelframe.Label", background="#ffffff", foreground="#23345d", font=("Segoe UI", 10, "bold"))
        s.configure("TButton", font=("Segoe UI", 10), padding=(10, 6))
        s.configure("Accent.TButton", background="#284b9b", foreground="#ffffff")
        s.map("Accent.TButton", background=[("active", "#1f3d80")])
        s.configure("Treeview", font=("Segoe UI", 10), rowheight=26)
        s.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
        s.configure("TNotebook.Tab", padding=(14, 8), font=("Segoe UI", 10, "bold"))

    def _tab(self, name):
        f = ttk.Frame(self.tabs, padding=14)
        self.tabs.add(f, text=name)
        return f

    def _build_cpu_tab(self):
        tab = self._tab("CPU Scheduling")
        top = ttk.Frame(tab); top.pack(fill="x")
        form = ttk.LabelFrame(top, text="Process Input", padding=10); form.pack(side="left", fill="y", padx=(0, 12))
        self.cpu_text = tk.Text(form, width=34, height=9, font=("Consolas", 10), relief="solid", borderwidth=1)
        self.cpu_text.pack(fill="both", expand=True)
        self.cpu_text.insert("1.0", "PID Arrival Burst Priority\nP1 0 5 2\nP2 1 3 1\nP3 2 8 3\nP4 3 6 2")
        ttk.Label(form, text="One process per line: ID Arrival Burst Priority").pack(anchor="w", pady=(6, 0))
        opts = ttk.LabelFrame(top, text="Run Settings", padding=10); opts.pack(side="left", fill="both", expand=True)
        ttk.Label(opts, text="Algorithm").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.cpu_algo = ttk.Combobox(opts, values=["FCFS", "SJF", "Priority", "Round Robin"], state="readonly", width=18)
        self.cpu_algo.set("FCFS"); self.cpu_algo.grid(row=0, column=1, sticky="w", padx=5, pady=5)
        ttk.Label(opts, text="Time quantum (Round Robin)").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.quantum = ttk.Spinbox(opts, from_=1, to=99, width=8); self.quantum.set("2"); self.quantum.grid(row=1, column=1, sticky="w", padx=5, pady=5)
        ttk.Button(opts, text="Run Scheduling", style="Accent.TButton", command=self.run_cpu).grid(row=2, column=0, columnspan=2, sticky="w", padx=5, pady=12)
        self.cpu_summary = ttk.Label(opts, text="Enter processes and run an algorithm.", wraplength=390)
        self.cpu_summary.grid(row=3, column=0, columnspan=2, sticky="w", padx=5, pady=5)
        result = ttk.LabelFrame(tab, text="Execution Timeline and Metrics", padding=10); result.pack(fill="both", expand=True, pady=(12, 0))
        self.gantt = tk.Canvas(result, height=105, bg="#fbfcff", highlightthickness=1, highlightbackground="#dce2ed")
        self.gantt.pack(fill="x", pady=(0, 10))
        cols = ("pid", "arrival", "burst", "priority", "completion", "turnaround", "waiting")
        self.cpu_table = ttk.Treeview(result, columns=cols, show="headings", height=8)
        for c, label, width in zip(cols, ["Process", "Arrival", "Burst", "Priority", "Completion", "Turnaround", "Waiting"], [90, 90, 90, 90, 110, 110, 100]):
            self.cpu_table.heading(c, text=label); self.cpu_table.column(c, width=width, anchor="center")
        self.cpu_table.pack(fill="both", expand=True)

    def _parse_processes(self):
        lines = [x.strip() for x in self.cpu_text.get("1.0", "end").splitlines() if x.strip()]
        if lines and lines[0].lower().startswith("pid"): lines = lines[1:]
        out = []
        for line in lines:
            parts = line.replace(",", " ").split()
            if len(parts) not in (3, 4): raise ValueError(f"Invalid process line: {line}\nUse: ID Arrival Burst [Priority]")
            out.append({"pid": parts[0], "arrival": int(parts[1]), "burst": int(parts[2]), "priority": int(parts[3]) if len(parts) == 4 else 0})
        return out

    def run_cpu(self):
        try:
            result = cpu_schedule(self._parse_processes(), self.cpu_algo.get(), int(self.quantum.get()))
            for row in self.cpu_table.get_children(): self.cpu_table.delete(row)
            for p in result["metrics"]: self.cpu_table.insert("", "end", values=(p["pid"], p["arrival"], p["burst"], p["priority"], p["completion"], p["turnaround"], p["waiting"]))
            self.cpu_summary.config(text=f"Algorithm: {result['algorithm']}    |    Average waiting time: {result['average_waiting']:.2f}    |    Average turnaround time: {result['average_turnaround']:.2f}")
            self._draw_gantt(result["segments"])
        except Exception as e: messagebox.showerror("Scheduling input error", str(e))

    def _draw_gantt(self, segments):
        c = self.gantt; c.delete("all")
        if not segments: return
        total = max(s["end"] for s in segments); total = max(total, 1)
        left, right = 18, max(c.winfo_width() - 18, 400)
        width = right - left; y1, y2 = 22, 65
        palette = ["#d8e5ff", "#d8f3e8", "#ffe8c7", "#eadfff", "#ffdce5", "#e5edb7"]
        for i, s in enumerate(segments):
            x1 = left + width * s["start"] / total; x2 = left + width * s["end"] / total
            color = "#edf0f5" if s["pid"] == "IDLE" else palette[i % len(palette)]
            c.create_rectangle(x1, y1, x2, y2, fill=color, outline="#8795aa")
            if x2-x1 > 18: c.create_text((x1+x2)/2, (y1+y2)/2, text=s["pid"], font=("Segoe UI", 9, "bold"))
            c.create_text(x1, y2+15, text=str(s["start"]), anchor="n", font=("Segoe UI", 8))
        c.create_text(right, y2+15, text=str(total), anchor="n", font=("Segoe UI", 8))

    def _build_banker_tab(self):
        tab = self._tab("Banker's Algorithm")
        ttk.Label(tab, text="Enter one row per process and one column per resource. Use spaces or commas between numbers.").pack(anchor="w", pady=(0, 10))
        body = ttk.Frame(tab); body.pack(fill="both", expand=True)
        self.alloc_text = self._matrix_box(body, "Allocation Matrix", "0 1 0\n2 0 0\n3 0 2\n2 1 1\n0 0 2")
        self.max_text = self._matrix_box(body, "Maximum Demand Matrix", "7 5 3\n3 2 2\n9 0 2\n2 2 2\n4 3 3")
        self.avail_text = self._matrix_box(body, "Available Resources", "3 3 2", height=3)
        ttk.Button(tab, text="Check Safe State", style="Accent.TButton", command=self.run_banker).pack(anchor="w", pady=12)
        self.banker_result = tk.Text(tab, height=10, font=("Consolas", 10), wrap="word", relief="solid", borderwidth=1)
        self.banker_result.pack(fill="both", expand=True)
        self.banker_result.insert("1.0", "Result will appear here. Example values are prefilled.")

    def _matrix_box(self, parent, title, value, height=9):
        box = ttk.LabelFrame(parent, text=title, padding=8); box.pack(side="left", fill="both", expand=True, padx=(0, 8))
        t = tk.Text(box, height=height, width=24, font=("Consolas", 10), relief="solid", borderwidth=1); t.pack(fill="both", expand=True); t.insert("1.0", value)
        return t

    @staticmethod
    def _parse_matrix(widget):
        rows = []
        for line in widget.get("1.0", "end").splitlines():
            line = line.strip()
            if line: rows.append([int(x) for x in line.replace(",", " ").split()])
        return rows

    def run_banker(self):
        try:
            allocation = self._parse_matrix(self.alloc_text); maximum = self._parse_matrix(self.max_text)
            available_lines = self._parse_matrix(self.avail_text)
            if len(available_lines) != 1: raise ValueError("Available Resources must be a single row.")
            result = bankers_algorithm(allocation, maximum, available_lines[0])
            need_text = "\n".join(f"P{i}: {row}" for i, row in enumerate(result["need"]))
            if result["safe"]:
                status = "SAFE STATE CONFIRMED\nSafe sequence: " + " → ".join(result["sequence"])
            else:
                status = "UNSAFE STATE\nNo complete safe sequence exists. Unfinished processes: " + ", ".join(result["unfinished"])
            self.banker_result.delete("1.0", "end")
            self.banker_result.insert("1.0", status + "\n\nNeed Matrix (Maximum − Allocation):\n" + need_text)
        except Exception as e: messagebox.showerror("Banker's Algorithm input error", str(e))

    def _build_page_tab(self):
        tab = self._tab("Page Replacement")
        form = ttk.LabelFrame(tab, text="Simulation Input", padding=12); form.pack(fill="x")
        ttk.Label(form, text="Page reference string").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.page_refs = ttk.Entry(form, width=60); self.page_refs.insert(0, "7 0 1 2 0 3 0 4 2 3 0 3 2"); self.page_refs.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        ttk.Label(form, text="Number of frames").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.frame_count = ttk.Spinbox(form, from_=1, to=20, width=8); self.frame_count.set("3"); self.frame_count.grid(row=1, column=1, sticky="w", padx=5, pady=5)
        ttk.Label(form, text="Algorithm").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.page_algo = ttk.Combobox(form, values=["FIFO", "LRU", "Optimal"], state="readonly", width=16); self.page_algo.set("FIFO"); self.page_algo.grid(row=2, column=1, sticky="w", padx=5, pady=5)
        form.columnconfigure(1, weight=1)
        ttk.Button(form, text="Run Page Replacement", style="Accent.TButton", command=self.run_pages).grid(row=3, column=1, sticky="w", padx=5, pady=10)
        self.page_summary = ttk.Label(tab, text="Run the simulation to count hits and page faults."); self.page_summary.pack(anchor="w", pady=10)
        box = ttk.LabelFrame(tab, text="Frame Trace", padding=10); box.pack(fill="both", expand=True)
        cols = ("step", "page", "f1", "f2", "f3", "f4", "f5", "status", "replaced")
        self.page_table = ttk.Treeview(box, columns=cols, show="headings", height=15)
        labels = ["Step", "Page", "Frame 1", "Frame 2", "Frame 3", "Frame 4", "Frame 5", "Result", "Replaced"]
        for c, label in zip(cols, labels): self.page_table.heading(c, text=label); self.page_table.column(c, width=82, anchor="center")
        self.page_table.pack(fill="both", expand=True)

    def run_pages(self):
        try:
            refs = self.page_refs.get().replace(",", " ").split()
            result = page_replacement(refs, int(self.frame_count.get()), self.page_algo.get())
            for row in self.page_table.get_children(): self.page_table.delete(row)
            for i, r in enumerate(result["rows"], 1):
                frames = r["frames"] + [None] * (5-len(r["frames"]))
                self.page_table.insert("", "end", values=(i, r["page"], *["—" if x is None else x for x in frames[:5]], r["status"], "—" if r["replaced"] is None else r["replaced"]))
            self.page_summary.config(text=f"{result['algorithm']} | Hits: {result['hits']} | Faults: {result['faults']} | Hit ratio: {result['hit_ratio']:.1%} | Fault ratio: {result['fault_ratio']:.1%}")
        except Exception as e: messagebox.showerror("Page replacement input error", str(e))

if __name__ == "__main__":
    OSSimulator().mainloop()
