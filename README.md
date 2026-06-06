# Smart Regex-Based Email & Password Validator ⚙️

A modern Python desktop application designed to validate strings using Regular Expressions and provide a live, step-by-step visual simulation of Deterministic Finite Automata (DFA) state transitions. 

Developed as a comprehensive visual implementation of **Theory of Automata** concepts.

## 🚀 Features
- [x] **Regex Validation Engine**: Evaluates standard email structures and strict password policies (minimum 8 characters, requiring uppercase, lowercase, and numeric digits).
- [x] **Live DFA Simulation**: Features an animated "flipbook" transition engine that highlights the exact path of the string through the automaton in real-time without UI lag.
- [x] **High-Definition Diagrams**: Integrates Graphviz to dynamically generate 300 DPI state machines, embedded within a native PyQt6 canvas supporting zoom and pan.
- [x] **Professional UI/UX**: Built with a fully responsive PyQt6 interface, featuring custom typography, dynamic drop shadows, and modern component states.

## 🛠️ Technology Stack
* **Language:** Python 3.x
* **GUI Framework:** PyQt6
* **Automata Engine:** Custom Python logic mapping state transition tables
* **Visualization:** Graphviz, NetworkX

## ⚙️ Prerequisites & Setup
To run this application locally, you must have Python installed, along with the Graphviz system executable.

### 1. Install Graphviz (System Level)
The application requires the underlying Graphviz software to be installed on your operating system to render the DFA states.
* **Windows**: Download the 64-bit EXE installer from [graphviz.org](https://graphviz.org/download/) or run `winget install Graphviz.Graphviz` in PowerShell. **Crucial:** You must check "Add Graphviz to the system PATH" during the installation process.
* **Linux (Ubuntu/Mint)**: Run `sudo apt install graphviz` in your terminal.

### 2. Local Installation
Clone the repository and set up the environment:

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

Before running the simulator for the first time, generate the high-resolution animation frames:

```bash
python diagrams/graph_generator.py

```

Launch the application:

```bash
python main.py

```

## 👤 Author
**Muhammad Fahaz Khan**  
- **GitHub:** [@SHADOWRULIN](https://github.com/SHADOWRULIN)  
- **LinkedIn:** [Fahaz Khan](https://www.linkedin.com/in/muhammadfahazkhan/)
