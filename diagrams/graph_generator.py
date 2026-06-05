import os
from graphviz import Digraph

def ensure_assets_folder():
    if not os.path.exists('assets'):
        os.makedirs('assets')

def build_email_graph(highlight_state=None, filename="email_dfa"):
    dot = Digraph(comment='Email DFA', format='png')
    
    # ADDED: dpi='300' to force High Definition rendering
    dot.attr(rankdir='LR', size='8,5', dpi='300') 
    
    states = ['q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'Dead State / Error']
    
    for s in states:
        shape = 'doublecircle' if s == 'q5' else 'circle'
        # Updated to use your exact Flag Red color for the dead state
        fillcolor = 'lightgreen' if s == 'q5' else '#C1292E' if s == 'Dead State / Error' else 'white'
        style = 'filled' if fillcolor != 'white' else ''
        
        if s == highlight_state:
            style = 'filled'
            fillcolor = '#F1D302' # Bright Gold
            
        node_id = 'Dead' if s == 'Dead State / Error' else s
        label = f"{s}\n(Accept)" if s == 'q5' else "Dead State" if node_id == 'Dead' else s
        if s == 'q0': label += "\n(Start)"
        
        dot.node(node_id, label, shape=shape, style=style, fillcolor=fillcolor)
        
    dot.edge('q0', 'q1', label=' letter/num ')
    dot.edge('q1', 'q1', label=' letter/num ')
    dot.edge('q1', 'q2', label=' @ ')
    dot.edge('q2', 'q3', label=' letter/num ')
    dot.edge('q3', 'q3', label=' letter/num ')
    dot.edge('q3', 'q4', label=' . ')
    dot.edge('q4', 'q5', label=' letter/num ')
    dot.edge('q5', 'q5', label=' letter/num ')
    dot.edge('q1', 'Dead', label=' . / @ ')
    dot.edge('q2', 'Dead', label=' @ / . ')
    
    dot.render(f'assets/{filename}', cleanup=True)

def build_password_graph(highlight_state=None, filename="password_dfa"):
    dot = Digraph(comment='Password DFA', format='png')
    
    # ADDED: dpi='300' to force High Definition rendering
    dot.attr(rankdir='LR', size='10,6', dpi='300')
    
    states = ['q0', 'q_U', 'q_L', 'q_D', 'q_UL', 'q_UD', 'q_LD', 'q_ULD', 'Rejected']
    
    for s in states:
        shape = 'doublecircle' if s == 'q_ULD' else 'circle'
        # Updated to use your exact Flag Red color for the rejected state
        fillcolor = 'lightgreen' if s == 'q_ULD' else '#C1292E' if s == 'Rejected' else 'white'
        style = 'filled' if fillcolor != 'white' else ''
        
        if s == highlight_state:
            style = 'filled'
            fillcolor = '#F1D302' # Bright Gold
            
        label = f"{s}\n(Accept)" if s == 'q_ULD' else s
        if s == 'q0': label += "\n(Start)"
        
        dot.node(s, label, shape=shape, style=style, fillcolor=fillcolor)
        
    # Standard Character Transitions
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
    
    for s in states:
        if s != 'Rejected':
            dot.edge(s, s, label=' (Self) ')
            
    # ADDED: Dashed lines to represent failing at the END of the string
    for s in ['q0', 'q_U', 'q_L', 'q_D', 'q_UL', 'q_UD', 'q_LD']:
        dot.edge(s, 'Rejected', label=' END\n(Missing Chars) ', style='dashed', color='#7f8c8d', fontcolor='#7f8c8d')
        
    # Even if they have all characters (q_ULD), it rejects if the string ends before 8 characters
    dot.edge('q_ULD', 'Rejected', label=' END\n(Len < 8) ', style='dashed', color='#7f8c8d', fontcolor='#7f8c8d')
            
    dot.render(f'assets/{filename}', cleanup=True)

if __name__ == "__main__":
    ensure_assets_folder()
    
    print("Generating High-Res Email DFA frames...")
    build_email_graph(filename="email_dfa_base")
    for state in ['q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'Dead State / Error']:
        safe_name = state.replace(" / ", "_").replace(" ", "_")
        build_email_graph(highlight_state=state, filename=f"email_dfa_{safe_name}")
        
    print("Generating High-Res Password DFA frames...")
    build_password_graph(filename="password_dfa_base")
    for state in ['q0', 'q_U', 'q_L', 'q_D', 'q_UL', 'q_UD', 'q_LD', 'q_ULD', 'Rejected']:
        build_password_graph(highlight_state=state, filename=f"password_dfa_{state}")
        
    print("Success! High resolution connected animation frames generated.")