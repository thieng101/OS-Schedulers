#Team Member: Hong Thy Nguyen, Diego Aguirre, Kota Ramsey
import heapq
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
                continue  # Ignore comments and the end marker

            parts = line.split()
            if not parts:
                continue

            directive = parts[0]
            if directive == 'processcount':
                # Expected to read a certain number of processes, could be stored if needed
                pass
            elif directive == 'runfor':
                total_run_time = int(parts[1])
            elif directive == 'use':
                algorithm = parts[1]
            elif directive == 'quantum':
                quantum = int(parts[1])
            elif directive == 'process':
                # Parsing each process detail
                _, _, name, _, arrival, _, burst = parts
                processes.append(Process(name, int(arrival), int(burst)))            
    
    return processes, algorithm, quantum, total_run_time

def fifo_scheduler(processes, total_run_time):
    processes.sort(key=lambda x: x.arrival)
    current_time = 0
    events = []

    for process in processes:
        if current_time < process.arrival:
            # Log idle until the process arrives if there is a gap
            while current_time < process.arrival:
                events.append(f"Time {current_time} : Idle")
                current_time += 1

        # Log arrival and selection
        events.append(f"Time {process.arrival} : {process.name} arrived")
        events.append(f"Time {current_time} : {process.name} selected (burst {process.burst})")
        process.start_time = current_time
        process.response_time = current_time - process.arrival
        
        # Update current time after the process finishes
        current_time += process.burst
        if current_time > total_run_time:
            process.finish_time = None  # Process did not finish within the total run time
            events.append(f"Time {total_run_time} : {process.name} did not finish")
            break
        else:
            process.finish_time = current_time
            process.turnaround_time = process.finish_time - process.arrival
            process.waiting_time = process.start_time - process.arrival
            # Log process completion
            events.append(f"Time {process.finish_time} : {process.name} finished")
    
    # Log final idle time if necessary
    while current_time < total_run_time:
        events.append(f"Time {current_time} : Idle")
        current_time += 1
    events.append(f"Finished at time {current_time}")
    
    return events

def sjf_preemptive_scheduler(processes, total_run_time):
    # Implement Preemptive SJF scheduling
    #import heapq

    current_time = 0
    events = []
    ready_queue = []
    current_process = None
    process_index = 0
    processes.sort(key=lambda x: (x.arrival, x.burst))  # Sort primarily by arrival, secondarily by burst time

    while current_time < total_run_time:
        # Check for new arriving processes and add them to the queue
        while process_index < len(processes) and processes[process_index].arrival <= current_time:
            process = processes[process_index]
            heapq.heappush(ready_queue, (process.remaining_burst, process.arrival, process))
            events.append(f"Time {current_time} : {process.name} arrived")
            process_index += 1

        # If current process finishes
        if current_process and current_process.remaining_burst <= 0:
            events.append(f"Time {current_time} : {current_process.name} finished")
            current_process.finish_time = current_time
            current_process = None

        # If no current process or preemption is needed
        if not current_process or (ready_queue and ready_queue[0][0] < current_process.remaining_burst):
            if current_process:
                heapq.heappush(ready_queue, (current_process.remaining_burst, current_process.arrival, current_process))
            if ready_queue:
                _, _, current_process = heapq.heappop(ready_queue)
                if current_process.start_time is None or current_process.start_time > current_time:
                    current_process.start_time = current_time
                    current_process.response_time = current_time - current_process.arrival
                events.append(f"Time {current_time} : {current_process.name} selected (remaining {current_process.remaining_burst})")

        # Increment time if there is a current process
        if current_process:
            current_process.remaining_burst -= 1

        # Idle if no current process and no pending process in the queue
        if not current_process and not ready_queue:
            events.append(f"Time {current_time} : Idle")

        current_time += 1

    # Ensure to log finishing time at the end of the simulation
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
        # Add new processes to the ready queue as they arrive
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

            # Check for arriving processes during time slice
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

    # Append any remaining idle time till the total run time
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


def output_results(processes, algorithm, events, output_filename, quantum):
    len_processes = len(processes)
    
    with open(output_filename, 'w') as f:
        f.write(f"{len_processes} processes\n")
        #human code:
        print(f"{len_processes} processes")
        type_scheduler = print_type_schedulers(algorithm)
        print(f"{type_scheduler}")
        ####
        f.write(f"{type_scheduler}\n")
        
        
        if quantum:
            f.write(f"Quantum {quantum}\n")
            #Human Code:
            print(f"Quantum {quantum}\n")
            
        # Sort events by time before printing if needed
        def extract_time(event):
            try:
                return int(event.split()[1])
            except (IndexError, ValueError):
                # Handle unexpected format
                print(f"Unexpected event format: {event}")
                return float('inf')  # Push unexpected formats to the end
        
        sorted_events = sorted(events, key=extract_time)
        for event in sorted_events:
            f.write(event + '\n')
        
        f.write("\n")
        #Sort the process in order
        processes = sorted(processes, key=lambda processes: processes.name)
        # Print metrics after events
        for process in processes:
            if process.finish_time == None:
                f.write(f"{process.name} did not finish\n")
            else: 
                f.write(f"{process.name} wait {process.waiting_time} turnaround {process.turnaround_time} response {process.response_time}\n")


def print_type_schedulers(algorithm):
    if algorithm == 'fcfs':
        return("Using First-Come First-Served (FCFS)")
    elif algorithm == 'sjf':
        return("Using Preemptive Shortest Job First")
    elif algorithm == 'rr':
        return("Using Round Robin (RR)")
    else:
        return("Unknown algorithm")
    

def main(input_filename):
    processes, algorithm, quantum, total_run_time = parse_input(input_filename)
    
    if algorithm == 'fcfs':
        events = fifo_scheduler(processes, total_run_time)
    elif algorithm == 'sjf':
        events = sjf_preemptive_scheduler(processes, total_run_time)
    elif algorithm == 'rr':
        if quantum is None:
            print("Error: Missing quantum parameter when use is 'rr'")
            return
        events = round_robin_scheduler(processes, quantum, total_run_time)
    calculate_metrics(processes)
    
    #change to out2 for testing
    output_filename = input_filename.replace('.in', '.out')
    
    output_results(processes, algorithm, events, output_filename, quantum)
    

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print("Usage: scheduler-gpt.py <input file>")
    else:
        main(sys.argv[1])
