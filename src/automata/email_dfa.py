def get_input_type(char: str) -> str:
    """Classifies the character for the DFA transition table."""
    if char.isalnum() or char in ['_', '-']:
        return 'letter'
    elif char == '@':
        return '@'
    elif char == '.':
        return '.'
    else:
        return 'invalid'

def simulate_email_dfa(email_string: str) -> tuple[bool, list]:
    """
    Simulates the Email DFA character by character.
    Returns a tuple: (is_accepted_boolean, transition_history_list)
    """
    # This directly represents your TOA Transition Table
    transitions = {
        'q0': {'letter': 'q1'},                   # Start state expects a letter/number
        'q1': {'letter': 'q1', '@': 'q2'},        # Reading username, waiting for @
        'q2': {'letter': 'q3'},                   # Read @, expects domain letter
        'q3': {'letter': 'q3', '.': 'q4'},        # Reading domain, waiting for dot
        'q4': {'letter': 'q5'},                   # Read dot, expects extension letter
        'q5': {'letter': 'q5'}                    # Final Accept state (e.g., "com")
    }
    
    current_state = 'q0'
    accept_state = 'q5'
    transition_log = []
    
    for char in email_string:
        char_type = get_input_type(char)
        
        # If there is no valid path forward (e.g., two @ symbols) -> Dead State
        if char_type not in transitions.get(current_state, {}):
            transition_log.append({
                'char': char,
                'from_state': current_state,
                'to_state': 'Dead State / Error',
                'status': 'REJECTED'
            })
            return False, transition_log
            
        next_state = transitions[current_state][char_type]
        
        # Record the step so the GUI can animate it later
        transition_log.append({
            'char': char,
            'from_state': current_state,
            'to_state': next_state,
            'status': 'PROCESSING'
        })
        
        current_state = next_state
        
    is_accepted = (current_state == accept_state)
    return is_accepted, transition_log


# --- TESTING BLOCK ---
if __name__ == "__main__":
    test_email = "abc@gmail.com"
    print(f"Simulating DFA for: {test_email}\n")
    
    accepted, log = simulate_email_dfa(test_email)
    
    for step in log:
        print(f"Read '{step['char']}' | {step['from_state']} ---> {step['to_state']}")
        
    print("\n---------------------------------")
    if accepted:
        print("FINAL RESULT: EMAIL ACCEPTED (Final State Reached)")
    else:
        print("FINAL RESULT: EMAIL REJECTED")
    print("---------------------------------")