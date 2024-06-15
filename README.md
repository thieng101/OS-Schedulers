# Process Scheduler Simulation

## Team Member
- Hong Thy Nguyen
- Diego Aguirre
- Kota Ramsey
## Description
This project simulates different process scheduling algorithms including First-Come First-Served (FCFS), Preemptive Shortest Job First (SJF), and Round Robin (RR). The results are displayed in a Tkinter-based GUI, showing the events and process metrics for each scheduler.

## Features
- Simulate FCFS, SJF, and RR scheduling algorithms.
- Display scheduling events and process metrics in a user-friendly GUI.
- Easily select input files through a file dialog.

## Requirements
- Python 3.x
- Tkinter (usually included with Python on most systems)

## Installation

### Ensure Python and Tkinter are installed
- **On macOS**:
  Tkinter is included with Python on macOS by default. If you encounter any issues, you can install Tkinter via Homebrew:
  ```bash
  brew install python-tk

- **On Windows**:
  Tkinter is included with the standard Python distribution. If you encounter any issues, make sure you have Python installed correctly from python.org.

## Usage

1. Clone the repository:
    ```bash
    git clone https://github.com/thieng101/OS-Schedulers.git
    cd OS-scheduler
    ```

2. Run the scheduler script:
    ```bash
    python3 scheduler-gpt.py inputFile.in
    ```
    Replace `inputFile.in` with the correct input file. The output will be written in a file with the same name as the input file but with an ending `.out` extension.

3. Run the UI script (the file creating UI for the schedulers):
    ```bash
    python3 ui_os.py
    ```
    Select the input file:
    A file dialog will appear. Select the input file with the `.in` extension.

   ###NOTE
   Running the ui_os.py won't generate an output file, only displaying in the window.

5. View the results:
    The scheduling results will be displayed in a tabbed interface. Each tab corresponds to a scheduler and shows the events and process metrics.





