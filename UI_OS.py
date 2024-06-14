import heapq
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class Process:
    def __init__(self, name, arrival, burst):
        self.name = name
        self.arrival = arrival
        self.burst = burst
        self.remaining_burst = burst
        self.start_time = None
        self.finish_time = None
        self.response_time = None
        self.waiting_time = None
        self.turnaround_time = None

def parse_input(filename):
    processes = []
    algorithm = ''
    quantum = None
    total_run_time = 0

    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith('#') or line == 'end':
                continue

            parts = line.split()
            if not parts:
                continue

            directive = parts[0]
            if directive == 'processcount':
                pass
            elif directive == 'runfor':
                total_run_time = int(parts[1])
            elif directive == 'use':
                algorithm = parts[1]
            elif directive == 'quantum':
                quantum = int(parts[1])
            elif directive == 'process':
                _, _, name, _, arrival, _, burst = parts
                processes.append(Process(name, int(arrival), int(burst)))

    return processes, algorithm, quantum, total_run_time

def fifo_scheduler(processes, total_run_time):
    processes.sort(key=lambda x: x.arrival)
    current_time = 0
    events = []

    for process in processes:
        if current_time < process.arrival:
            while current_time < process.arrival:
                events.append(f"Time {current_time} : Idle")
                current_time += 1

        events.append(f"Time {process.arrival} : {process.name} arrived")
        events.append(f"Time {current_time} : {process.name} selected (burst {process.burst})")
        process.start_time = current_time
        process.response_time = current_time - process.arrival

        current_time += process.burst
        process.finish_time = current_time
        process.turnaround_time = process.finish_time - process.arrival
        process.waiting_time = process.start_time - process.arrival

        events.append(f"Time {process.finish_time} : {process.name} finished")

    while current_time < total_run_time:
        events.append(f"Time {current_time} : Idle")
        current_time += 1
    events.append(f"Finished at time {current_time}")

    return events

def sjf_preemptive_scheduler(processes, total_run_time):
    current_time = 0
    events = []
    ready_queue = []
    current_process = None
    process_index = 0
    processes.sort(key=lambda x: (x.arrival, x.burst))

    while current_time < total_run_time:
        while process_index < len(processes) and processes[process_index].arrival <= current_time:
            process = processes[process_index]
            heapq.heappush(ready_queue, (process.remaining_burst, process.arrival, process))
            events.append(f"Time {current_time} : {process.name} arrived")
            process_index += 1

        if current_process and current_process.remaining_burst <= 0:
            events.append(f"Time {current_time} : {current_process.name} finished")
            current_process.finish_time = current_time
            current_process = None

        if not current_process or (ready_queue and ready_queue[0][0] < current_process.remaining_burst):
            if current_process:
                heapq.heappush(ready_queue, (current_process.remaining_burst, current_process.arrival, current_process))
            if ready_queue:
                _, _, current_process = heapq.heappop(ready_queue)
                if current_process.start_time is None or current_process.start_time > current_time:
                    current_process.start_time = current_time
                    current_process.response_time = current_time - current_process.arrival
                events.append(f"Time {current_time} : {current_process.name} selected (remaining {current_process.remaining_burst})")

        if current_process:
            current_process.remaining_burst -= 1

        if not current_process and not ready_queue:
            events.append(f"Time {current_time} : Idle")

        current_time += 1

    events.append(f"Finished at time {current_time}")

    return events

def round_robin_scheduler(processes, quantum, total_run_time):
    queue = []
    current_time = 0
    completed = 0
    n = len(processes)
    time_log = []

    processes.sort(key=lambda x: x.arrival)

    process_index = 0

    while completed < n and current_time < total_run_time:
        while process_index < len(processes) and processes[process_index].arrival <= current_time:
            process = processes[process_index]
            queue.append(process)
            time_log.append(f"Time {current_time} : {process.name} arrived")
            process_index += 1

        if not queue:
            if process_index < len(processes):
                next_process = processes[process_index]
                idle_time = next_process.arrival - current_time
                for _ in range(idle_time):
                    time_log.append(f"Time {current_time} : Idle")
                    current_time += 1
                continue
            else:
                break

        process = queue.pop(0)

        if process.start_time is None:
            process.start_time = current_time
            process.response_time = current_time - process.arrival

        time_slice = min(quantum, process.remaining_burst)
        time_log.append(f"Time {current_time} : {process.name} selected (burst {process.remaining_burst})")

        for _ in range(time_slice):
            current_time += 1
            process.remaining_burst -= 1

            while process_index < len(processes) and processes[process_index].arrival <= current_time:
                arrived_process = processes[process_index]
                queue.append(arrived_process)
                time_log.append(f"Time {current_time} : {arrived_process.name} arrived")
                process_index += 1

            if process.remaining_burst == 0:
                break

        if process.remaining_burst > 0:
            queue.append(process)
        else:
            completed += 1
            process.finish_time = current_time
            process.turnaround_time = process.finish_time - process.arrival
            process.waiting_time = process.turnaround_time - process.burst
            time_log.append(f"Time {current_time} : {process.name} finished")

    while current_time < total_run_time:
        time_log.append(f"Time {current_time} : Idle")
        current_time += 1

    time_log.append(f"Finished at time {current_time}")
    return time_log

def calculate_metrics(processes):
    for process in processes:
        if process.finish_time is None:
            process.turnaround_time = None
            process.waiting_time = None
            process.response_time = None
        else:
            process.turnaround_time = process.finish_time - process.arrival
            process.waiting_time = process.turnaround_time - process.burst
            if process.start_time is not None:
                process.response_time = process.start_time - process.arrival

def run_scheduler(input_filename):
    processes, algorithm, quantum, total_run_time = parse_input(input_filename)
    
    if algorithm == 'fcfs':
        events = fifo_scheduler(processes, total_run_time)
    elif algorithm == 'sjf':
        events = sjf_preemptive_scheduler(processes, total_run_time)
    elif algorithm == 'rr':
        if quantum is None:
            raise ValueError("Error: Missing quantum parameter when use is 'rr'")
        events = round_robin_scheduler(processes, quantum, total_run_time)
    calculate_metrics(processes)
    return algorithm, processes, events, quantum

def display_results_in_table(results):
    root = tk.Tk()
    root.title("Scheduling Results")
    root.geometry("1400x600")

    notebook = ttk.Notebook(root)
    notebook.pack(expand=1, fill="both")

    for scheduler, (processes, events, quantum) in results.items():
        frame = ttk.Frame(notebook)
        notebook.add(frame, text=scheduler)

        events_label = ttk.Label(frame, text="Events", font=('Arial', 12, 'bold'))
        events_label.pack(pady=10)

        events_tree = ttk.Treeview(frame, columns=("Event"), show='headings')
        events_tree.pack(side=tk.LEFT, expand=1, fill='both')
        events_tree.heading("Event", text="Event")

        for event in events:
            events_tree.insert('', 'end', values=(event,))

        process_label = ttk.Label(frame, text="Processes", font=('Arial', 12, 'bold'))
        process_label.pack(pady=10)

        process_tree = ttk.Treeview(frame, columns=("Name", "Arrival", "Burst", "Start", "Finish", "Response", "Waiting", "Turnaround"), show='headings')
        process_tree.pack(side=tk.RIGHT, expand=1, fill='both')
        process_tree.column("Name", width = 100);
        process_tree.column("Arrival", width = 100);
        process_tree.column("Burst", width = 100);
        process_tree.column("Start", width = 100);
        process_tree.column("Finish", width = 100);
        process_tree.column("Response", width = 100);
        process_tree.column("Waiting", width = 100);
        process_tree.column("Turnaround", width = 100);

        for col in process_tree['columns']:
            process_tree.heading(col, text=col)
            process_tree.column(col, anchor='center')

        for process in processes:
            process_tree.insert('', 'end', values=(process.name, process.arrival, process.burst, process.start_time, process.finish_time, process.response_time, process.waiting_time, process.turnaround_time))

    root.mainloop()

def main():
    input_filename = filedialog.askopenfilename(title="Select input file", filetypes=[("Text files", "*.in")])
    if not input_filename:
        messagebox.showerror("Error", "No file selected")
        return

    try:
        algorithm, processes, events, quantum = run_scheduler(input_filename)
    except ValueError as e:
        messagebox.showerror("Error", str(e))
        return
    
    results = {
        algorithm: (processes, events, quantum)
    }

    display_results_in_table(results)

if __name__ == "__main__":
    main()
