# OS Simulator — Operating Systems Mini Project

**Student:** Yashwardhan Rajesh Kanojiya  
**Programme:** B.Tech Computer Science and Engineering  
**Roll No.:** 42  
**Academic Year:** 2026–2027  
**Project Guide:** Prof. Krati Shrivastava  
**Department / HOD:** Dr. Sonali Patil

## Overview

OS Simulator is a Python desktop application built with Tkinter. It gives students an interactive way to explore three core operating-system topics:

1. **CPU scheduling:** First Come First Served (FCFS), non-preemptive Shortest Job First (SJF), non-preemptive Priority, and Round Robin.
2. **Deadlock avoidance:** Banker's safety algorithm, including the Need matrix and safe/unsafe state result.
3. **Memory management:** FIFO, Least Recently Used (LRU), and Optimal page replacement, including frame trace, hits, faults, and ratios.

The program is an educational simulator. It models algorithms; it does not control or modify the host operating system.

## Requirements

- Python 3.10 or newer recommended
- Tkinter (usually included with standard Python installations)
- No third-party Python packages are required

On some Linux distributions, Tkinter may need to be installed separately (for example, the package `python3-tk`).

## Run the project

### Windows 10 / 11

1. Extract the ZIP file to a normal folder.
2. Install Python from [python.org](https://www.python.org/downloads/) if it is not already installed. During setup, enable **Add Python to PATH**.
3. Open the extracted folder.
4. Double-click `run_windows.bat`, or open a terminal in this folder and run:

   ```powershell
   py -3 main.py
   ```

### Linux / macOS

From a terminal in the project directory:

```bash
python3 main.py
```

If Tkinter is missing on Linux, install the distribution's Tkinter package and run the command again.

## How to use

### CPU Scheduling tab

Each non-empty line is one process in the format:

```text
PID Arrival Burst Priority
P1 0 5 2
P2 1 3 1
```

Priority is optional; lower numeric values represent higher priority. Select an algorithm and click **Run Scheduling**. The app displays a Gantt-style timeline, completion time, turnaround time, waiting time, and averages. Round Robin also uses the time quantum field.

### Banker's Algorithm tab

Enter the Allocation matrix, Maximum matrix, and Available vector. Each process is a row and each resource is a column. The matrices must have matching dimensions, and allocation must not exceed maximum demand. Click **Check Safe State** to see the Need matrix and safety result.

### Page Replacement tab

Enter page numbers separated by spaces or commas, choose the frame count, select FIFO/LRU/Optimal, and click **Run Page Replacement**. Each row records the page, frame state, hit/fault result, and replaced page.

## Project structure

```text
OS_Simulator_Project/
├── main.py                         # Tkinter graphical interface
├── os_simulator/
│   ├── __init__.py
│   └── algorithms.py               # Scheduling, Banker's, page replacement
├── tests/
│   └── test_algorithms.py          # Basic algorithm tests
├── docs/
│   ├── Project_Report.docx         # Project documentation
│   └── Reference_Document.pdf      # Structure/reference document
├── assets/
│   └── system_flow.svg             # Application flowchart
├── run_windows.bat
├── run_linux_mac.sh
└── README.md
```

## Run tests

From the project root:

```bash
python -m unittest discover -s tests -v
```

## Algorithm notes and complexity

- **FCFS:** selects the earliest-arrived waiting process; sorting and selection are implemented with straightforward list operations, so worst-case scheduling overhead is O(n²).
- **SJF / Priority (non-preemptive):** selects the shortest burst / highest priority among arrived processes; straightforward selection gives O(n²) worst-case overhead.
- **Round Robin:** each process receives at most the configured quantum per turn. Runtime depends on the number of time slices; queue operations here use a Python list, so the simple implementation can incur O(k) removal overhead per slice.
- **Banker's safety check:** O(n²m) in the conventional bound, where n is the process count and m is the resource count.
- **Page replacement:** FIFO and LRU are implemented for clarity with list operations; Optimal scans future references. This educational version prioritizes traceability over large-input performance.

## Validation

The included unit tests check representative CPU scheduling metrics, Round Robin completion, a standard safe Banker's example, and page-fault counting. Run the test command above before demonstrating the project.

## References

1. Silberschatz, A., Galvin, P. B., and Gagne, G., *Operating System Concepts*, Wiley.
2. Tanenbaum, A. S. and Bos, H., *Modern Operating Systems*, Pearson.
3. Python documentation: https://docs.python.org/3/
4. Tkinter documentation: https://docs.python.org/3/library/tkinter.html
5. Reference project documentation supplied for the OS Simulator assignment (included in `docs/Reference_Document.pdf`).

---

**Prepared by Yashwardhan Rajesh Kanojiya | B.Tech CSE | Roll No. 42**
