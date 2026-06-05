import os
from graphviz import Digraph

def ensure_assets_folder():
    """Creates the assets folder if it doesn't exist."""
    if not os.path.exists('assets'):
        os.makedirs('assets')

def generate_email_dfa_graph() -> str:
    """Generates the static Email DFA diagram and returns the file path."""
    ensure_assets_folder()
    
    dot = Digraph(comment='Email DFA', format='png')
    dot.attr(rankdir='LR', size='8,5') # Left to Right layout
    
    # Define States (q5 is the double-circle accepted state)
    dot.node('q0', 'q0\n(Start)', shape='circle')
    dot.node('q1', 'q1', shape='circle')
    dot.node('q2', 'q2', shape='circle')
    dot.node('q3', 'q3', shape='circle')
    dot.node('q4', 'q4', shape='circle')
    dot.node('q5', 'q5\n(Accept)', shape='doublecircle', style='filled', fillcolor='lightgreen')
    dot.node('Dead', 'Dead State', shape='circle', style='filled', fillcolor='lightcoral')
    
    # Define Transitions
    dot.edge('q0', 'q1', label=' letter/num ')
    dot.edge('q1', 'q1', label=' letter/num ')
    dot.edge('q1', 'q2', label=' @ ')
    dot.edge('q2', 'q3', label=' letter/num ')
    dot.edge('q3', 'q3', label=' letter/num ')
    dot.edge('q3', 'q4', label=' . ')
    dot.edge('q4', 'q5', label=' letter/num ')
    dot.edge('q5', 'q5', label=' letter/num ')
    
    # Invalid transitions leading to dead state
    dot.edge('q1', 'Dead', label=' . / @ ')
    dot.edge('q2', 'Dead', label=' @ / . ')
    
    output_path = 'assets/email_dfa'
    dot.render(output_path, cleanup=True)
    return f"{output_path}.png"

def generate_password_dfa_graph() -> str:
    """Generates the static Password DFA diagram and returns the file path."""
    ensure_assets_folder()
    
    dot = Digraph(comment='Password DFA', format='png')
    dot.attr(rankdir='LR', size='10,6')
    
    # Define States based on combinations of U (Upper), L (Lower), D (Digit)
    states = ['q0', 'q_U', 'q_L', 'q_D', 'q_UL', 'q_UD', 'q_LD']
    for state in states:
        dot.node(state, state, shape='circle')
        
    dot.node('q_ULD', 'q_ULD\n(Accept)', shape='doublecircle', style='filled', fillcolor='lightgreen')
    
    # Define Core Transitions (simplified to prevent visual clutter)
    dot.edge('q0', 'q_U', label=' U ')
    dot.edge('q0', 'q_L', label=' L ')
    dot.edge('q0', 'q_D', label=' D ')
    
    dot.edge('q_U', 'q_UL', label=' L ')
    dot.edge('q_U', 'q_UD', label=' D ')
    
    dot.edge('q_L', 'q_UL', label=' U ')
    dot.edge('q_L', 'q_LD', label=' D ')
    
    dot.edge('q_D', 'q_UD', label=' U ')
    dot.edge('q_D', 'q_LD', label=' L ')
    
    dot.edge('q_UL', 'q_ULD', label=' D ')
    dot.edge('q_UD', 'q_ULD', label=' L ')
    dot.edge('q_LD', 'q_ULD', label=' U ')
    
    # Self loops for characters already found or 'Other' characters
    for state in states + ['q_ULD']:
        dot.edge(state, state, label=' (Self) ')
    
    output_path = 'assets/password_dfa'
    dot.render(output_path, cleanup=True)
    return f"{output_path}.png"


# --- TESTING BLOCK ---
if __name__ == "__main__":
    print("Generating Email DFA...")
    email_img = generate_email_dfa_graph()
    print(f"Success! Saved to {email_img}")
    
    print("Generating Password DFA...")
    pass_img = generate_password_dfa_graph()
    print(f"Success! Saved to {pass_img}")