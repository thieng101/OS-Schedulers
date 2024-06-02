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
                processes.append(Process(name, arrival, burst))            
    
    return processes, algorithm, quantum, total_run_time

def fifo_scheduler(processes):
    # Implement FIFO scheduling
    pass

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
def output_results(processes, algorithm, quantum, total_run_time):
    # Format and output the results to a file
    processCounts = len(processes)
    print(f"{processCounts} processes")
    print(f"Algorithm: {algorithm}, Quantum: {quantum}, Total run time: {total_run_time}")
    for process in processes:
        print(f"Process {process.name}: Arrival {process.arrival}, Burst {process.burst}")    

def main(input_filename):
    processes, algorithm, quantum, total_run_time = parse_input(input_filename)
 
    if algorithm == 'fcfs':
        fifo_scheduler(processes)
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
    
    output_results(processes, algorithm, quantum, output_filename)

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print("Usage: scheduler-gpt.py <input file>")
    else:
        main(sys.argv[1])
