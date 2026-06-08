=============================================================================
CSC205 – Theory of Automata: Course Project
Interactive DFA-Based Email & Password Validation System
=============================================================================
Group Member Name: 
	1. Muhammad Fahaz Khan (24SP-047-CS)
	2. Hassan (24SP-010-CS)
	3. Fawwad (24SP-035-CS)
	4. Saim (24SP-006-CS)
University: UIT University

PROJECT OVERVIEW
-----------------------------------------------------------------------------
This project is a Python-based visual simulator that implements Deterministic 
Finite Automata (DFA) to strictly validate strings for Email and Password 
structures. It demonstrates formal language theory using a mathematical 
state machine, complete with a Turing-style input tape and interactive 
graphical state transitions.

PREREQUISITES
-----------------------------------------------------------------------------
1. Python 3.10 or higher installed on your system.
2. Graphviz Software (Crucial for rendering the Automata graphs):
   - You MUST download and install the Graphviz executable from: 
     https://graphviz.org/download/
   - Ensure you check the box that says "Add Graphviz to the system PATH 
     for all users" during installation.

SETUP INSTRUCTIONS
-----------------------------------------------------------------------------
1. Extract the provided .zip folder to your local machine.
2. Open your Command Prompt (CMD) or Terminal.
3. Navigate to the root directory of the extracted folder:
   cd path/to/Muhammad_Fahaz_Khan_Course_Project
4. (Optional but recommended) Create and activate a virtual environment:
   python -m venv venv
   venv\Scripts\activate   (On Windows)
   source venv/bin/activate (On Mac/Linux)
5. Install the required Python libraries using the provided requirements file:
   pip install -r requirements.txt

HOW TO RUN THE SIMULATION
-----------------------------------------------------------------------------
1. From the root folder, navigate into the "src" directory:
   cd src
2. Execute the main Python script:
   python main.py
3. The PyQt6 graphical interface will launch.
4. From the main menu, select either the "Email DFA" or "Password DFA" 
   simulator.
5. Enter a test string into the input field and click "Start Automata".
6. Use the playback controls (Next Step, Pause, Back Step) to visually trace 
   the state transitions on the screen and view the live log execution matrix.
7. Click "Export Report" to save the simulation trace log. You can select the 
   provided "output" folder to save your logs for easy reviewing.

=============================================================================