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
    # Sort processes based on their arrival time
    processes.sort(key=lambda x: x.arrival)
    
    current_time = 0
    events = []

    for process in processes:
        if current_time < process.arrival:
            # CPU is idle until the next process arrives
            events.append(f"Time {current_time} : Idle")
            current_time = process.arrival

        # Start the process if it arrives
        if current_time >= process.arrival:
            process.start_time = current_time
            process.response_time = current_time - process.arrival
            events.append(f"Time {process.arrival} : {process.name} arrived")
            events.append(f"Time {current_time} : {process.name} selected (burst {process.burst})")
            
            # Update current time after the process finishes
            current_time += process.burst
            process.finish_time = current_time
            
            # Process has finished execution
            events.append(f"Time {process.finish_time} : {process.name} finished")
    
    # Calculate waiting, response, and turnaround times
    for process in processes:
        process.turnaround_time = process.finish_time - process.arrival
        process.waiting_time = process.start_time - process.arrival
    
    # Append final time
    while current_time < total_run_time:
        events.append(f"Time {current_time} : Idle")
        current_time += 1
    events.append(f"Finished at time {current_time}")
    
    return events

def sjf_preemptive_scheduler(processes):
    # Implement Preemptive SJF scheduling
    pass

def round_robin_scheduler(processes, quantum):
    # Implement Round Robin scheduling
    pass

def calculate_metrics(processes):
    # Calculate metrics for all processes
    pass

#
#TODO: change output. For now it just printed the input file for testing purpose
def output_results(processes, algorithm, events, output_filename):
    len_processes = len(processes)
    print(f"{len_processes} processes")
    print_type_schedulers(algorithm)
    for event in events:
        print(event)

def print_type_schedulers(algorithm):
    if algorithm == 'fcfs':
        print("Using First-Come First-Served (FCFS)")
    elif algorithm == 'sjf':
        print("Using Shortest Job First (SJF)")
    elif algorithm == 'rr':
        print("Using Round Robin (RR)")
    else:
        print("Unknown algorithm")
    

def main(input_filename):
    processes, algorithm, quantum, total_run_time = parse_input(input_filename)
 
    if algorithm == 'fcfs':
        events = fifo_scheduler(processes, total_run_time)
    elif algorithm == 'sjf':
        sjf_preemptive_scheduler(processes)
    elif algorithm == 'rr':
        if quantum is None:
            print("Error: Missing quantum parameter when use is 'rr'")
            return
        round_robin_scheduler(processes, quantum)
    calculate_metrics(processes)
    
    #do we need to change the input file to become output file or we need to create a new output file? 
    #TODO: check assignment requirement
    output_filename = input_filename.replace('.in', '.out')
    
    output_results(processes, algorithm, events, output_filename)
    

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print("Usage: scheduler-gpt.py <input file>")
    else:
        main(sys.argv[1])
