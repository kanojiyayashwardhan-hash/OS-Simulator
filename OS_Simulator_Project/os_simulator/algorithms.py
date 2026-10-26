"""Core algorithms for the OS Simulator educational project."""
from collections import deque


def _validate_processes(processes):
    if not processes:
        raise ValueError("Enter at least one process.")
    seen = set()
    for p in processes:
        pid = str(p.get("pid", "")).strip()
        if not pid:
            raise ValueError("Every process must have an ID.")
        if pid in seen:
            raise ValueError(f"Duplicate process ID: {pid}")
        seen.add(pid)
        if int(p.get("arrival", 0)) < 0 or int(p.get("burst", 0)) <= 0:
            raise ValueError("Arrival time must be >= 0 and burst time must be > 0.")
    return [dict(pid=str(p["pid"]), arrival=int(p.get("arrival", 0)), burst=int(p["burst"]), priority=int(p.get("priority", 0))) for p in processes]


def cpu_schedule(processes, algorithm="FCFS", quantum=2):
    """Return schedule segments, per-process metrics, and averages.

    Supported algorithms: FCFS, SJF, Priority, Round Robin.
    Lower numeric priority means higher priority.
    """
    ps = _validate_processes(processes)
    algorithm = algorithm.strip().upper()
    if algorithm not in {"FCFS", "SJF", "PRIORITY", "ROUND ROBIN", "RR"}:
        raise ValueError("Unsupported CPU scheduling algorithm.")
    if algorithm in {"ROUND ROBIN", "RR"} and int(quantum) <= 0:
        raise ValueError("Round Robin quantum must be greater than zero.")

    remaining = {p["pid"]: p["burst"] for p in ps}
    by_id = {p["pid"]: p for p in ps}
    complete = {}
    segments = []
    time = min(p["arrival"] for p in ps)
    ready = []

    if algorithm in {"FCFS", "SJF", "PRIORITY"}:
        pending = sorted(ps, key=lambda p: (p["arrival"], p["pid"]))
        while pending:
            available = [p for p in pending if p["arrival"] <= time]
            if not available:
                next_time = pending[0]["arrival"]
                if next_time > time:
                    segments.append({"pid": "IDLE", "start": time, "end": next_time})
                time = next_time
                available = [p for p in pending if p["arrival"] <= time]
            if algorithm == "FCFS":
                chosen = min(available, key=lambda p: (p["arrival"], p["pid"]))
            elif algorithm == "SJF":
                chosen = min(available, key=lambda p: (p["burst"], p["arrival"], p["pid"]))
            else:
                chosen = min(available, key=lambda p: (p["priority"], p["arrival"], p["pid"]))
            pending.remove(chosen)
            start = time
            time += chosen["burst"]
            segments.append({"pid": chosen["pid"], "start": start, "end": time})
            complete[chosen["pid"]] = time
    else:
        pending = sorted(ps, key=lambda p: (p["arrival"], p["pid"]))
        i = 0
        q = int(quantum)
        while i < len(pending) or ready:
            if not ready and i < len(pending) and time < pending[i]["arrival"]:
                segments.append({"pid": "IDLE", "start": time, "end": pending[i]["arrival"]})
                time = pending[i]["arrival"]
            while i < len(pending) and pending[i]["arrival"] <= time:
                ready.append(pending[i]["pid"])
                i += 1
            if not ready:
                continue
            pid = ready.pop(0)
            run_for = min(q, remaining[pid])
            start = time
            time += run_for
            remaining[pid] -= run_for
            segments.append({"pid": pid, "start": start, "end": time})
            while i < len(pending) and pending[i]["arrival"] <= time:
                ready.append(pending[i]["pid"])
                i += 1
            if remaining[pid] > 0:
                ready.append(pid)
            else:
                complete[pid] = time

    metrics = []
    for p in sorted(ps, key=lambda x: x["pid"]):
        ct = complete[p["pid"]]
        tat = ct - p["arrival"]
        wt = tat - p["burst"]
        metrics.append({"pid": p["pid"], "arrival": p["arrival"], "burst": p["burst"], "priority": p["priority"], "completion": ct, "turnaround": tat, "waiting": wt})
    n = len(metrics)
    return {"algorithm": algorithm, "segments": segments, "metrics": metrics,
            "average_waiting": sum(x["waiting"] for x in metrics) / n,
            "average_turnaround": sum(x["turnaround"] for x in metrics) / n}


def bankers_algorithm(allocation, maximum, available):
    """Run Banker's safety check. Matrices are lists of integer rows."""
    if not allocation or len(allocation) != len(maximum):
        raise ValueError("Allocation and Maximum must have the same non-zero number of processes.")
    resources = len(available)
    if resources == 0 or any(len(row) != resources for row in allocation + maximum):
        raise ValueError("All matrix rows must match the number of resources.")
    if any(len(a) != resources for a in allocation) or any(len(m) != resources for m in maximum):
        raise ValueError("Invalid matrix dimensions.")
    if any(v < 0 for row in allocation + maximum for v in row) or any(v < 0 for v in available):
        raise ValueError("Resource values cannot be negative.")
    if any(allocation[i][j] > maximum[i][j] for i in range(len(allocation)) for j in range(resources)):
        raise ValueError("Allocation cannot exceed maximum demand.")
    need = [[maximum[i][j] - allocation[i][j] for j in range(resources)] for i in range(len(allocation))]
    work = list(available)
    finish = [False] * len(allocation)
    sequence = []
    progress = True
    while progress:
        progress = False
        for i in range(len(allocation)):
            if not finish[i] and all(need[i][j] <= work[j] for j in range(resources)):
                work = [work[j] + allocation[i][j] for j in range(resources)]
                finish[i] = True
                sequence.append(f"P{i}")
                progress = True
    return {"safe": all(finish), "need": need, "sequence": sequence if all(finish) else sequence,
            "unfinished": [f"P{i}" for i, done in enumerate(finish) if not done]}


def page_replacement(reference_string, frame_count, algorithm="FIFO"):
    """Simulate FIFO, LRU, or Optimal page replacement."""
    refs = [int(x) for x in reference_string]
    frame_count = int(frame_count)
    algorithm = algorithm.upper()
    if not refs:
        raise ValueError("Enter a page reference string.")
    if frame_count <= 0:
        raise ValueError("Frame count must be greater than zero.")
    if algorithm not in {"FIFO", "LRU", "OPTIMAL", "OPT"}:
        raise ValueError("Unsupported page replacement algorithm.")
    algorithm = "OPTIMAL" if algorithm == "OPT" else algorithm
    frames = []
    queue = deque()
    last_used = {}
    rows = []
    faults = hits = 0
    for idx, page in enumerate(refs):
        hit = page in frames
        replaced = None
        if hit:
            hits += 1
        else:
            faults += 1
            if len(frames) < frame_count:
                frames.append(page)
                queue.append(page)
            else:
                if algorithm == "FIFO":
                    victim = queue.popleft()
                elif algorithm == "LRU":
                    victim = min(frames, key=lambda x: last_used.get(x, -1))
                else:
                    future = refs[idx + 1:]
                    victim = max(frames, key=lambda x: future.index(x) if x in future else float("inf"))
                replaced = victim
                frames[frames.index(victim)] = page
                if algorithm == "FIFO":
                    queue.append(page)
                elif algorithm == "OPTIMAL":
                    pass
        last_used[page] = idx
        rows.append({"page": page, "frames": list(frames) + [None] * (frame_count - len(frames)), "status": "HIT" if hit else "FAULT", "replaced": replaced})
    return {"algorithm": algorithm, "rows": rows, "hits": hits, "faults": faults,
            "hit_ratio": hits / len(refs), "fault_ratio": faults / len(refs)}
