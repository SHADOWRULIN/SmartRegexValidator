# Interactive DFA-Based Email & Password Validation System

A professional Python desktop application designed to validate strings using Regular Expressions and provide a live, interactive visual simulation of Deterministic Finite Automata (DFA) state transitions. 

Developed as a comprehensive visual implementation of Theory of Automata concepts.

## Features

* **Regex Validation Engine**: Evaluates standard email structures and strict password policies (minimum 8 characters, requiring uppercase, lowercase, and numeric digits).
* **Interactive DFA Simulation**: Features an animated "flipbook" transition engine with a live Turing-style Input Tape.
* **Automata Laboratory Tools**: 
  * Dynamic mathematical Transition Tables generated for each language.
  * Manual Playback Controls (Pause, Resume, Step Forward, Step Backward).
  * Adjustable simulation execution speeds.
* **High-Definition Diagrams**: Integrates Graphviz to dynamically generate 300 DPI state machines, embedded within a native PyQt6 canvas supporting zoom and pan.
* **Export Capabilities**: Generate and save detailed simulation statistics and transition logs to local text files.

## Technology Stack

* **Language**: Python 3.x
* **GUI Framework**: PyQt6
* **Automata Engine**: Custom Python logic mapping state transition tables
* **Visualization**: Graphviz, NetworkX

## Prerequisites & Setup

To run this application locally, you must have Python installed, along with the Graphviz system executable.

### 1. Install Graphviz (System Level)
The application requires the underlying Graphviz software to be installed on your operating system to render the DFA states.
* **Windows**: Download the 64-bit EXE installer from graphviz.org or run `winget install Graphviz.Graphviz` in PowerShell. **Crucial:** You must check "Add Graphviz to the system PATH" during the installation process.
* **Linux (Ubuntu/Mint)**: Run `sudo apt install graphviz` in your terminal.

### 2. Local Installation
Clone the repository and set up the Python virtual environment:

```bash
# Clone the repository
git clone https://github.com/SHADOWRULIN/SmartRegexValidator.git
cd SmartRegexValidator

# Create and activate a virtual environment
python -m venv venv

# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

```

### 3. Generate Assets & Run

Before running the simulator for the first time, you must generate the high-resolution animation frames:

```bash
python diagrams/graph_generator.py

```

Launch the application:

```bash
python main.py

```

## Author
**Muhammad Fahaz Khan**  
- **GitHub:** [@SHADOWRULIN](https://github.com/SHADOWRULIN)  
- **LinkedIn:** [Fahaz Khan](https://www.linkedin.com/in/muhammadfahazkhan/)
