def get_char_type(char: str) -> str:
    """Classifies the character for the Password DFA transition table."""
    if char.isupper():
        return 'U'
    elif char.islower():
        return 'L'
    elif char.isdigit():
        return 'D'
    else:
        return 'O'  # Other (special characters are allowed, but don't change core state)

def get_next_state(current_state: str, char_type: str) -> str:
    """
    Determines the next state based on what character types have been seen.
    States represent the combination of met requirements (U=Upper, L=Lower, D=Digit).
    """
    # If we are already in the state where all requirements are met, we stay there.
    if current_state == 'q_ULD':
        return 'q_ULD'

    # Extract what we already have from the state name (e.g., 'q_U' -> ['U'])
    # 'q0' means we have nothing yet.
    has_u = 'U' in current_state and current_state != 'q0'
    has_l = 'L' in current_state and current_state != 'q0'
    has_d = 'D' in current_state and current_state != 'q0'

    # Update what we have based on the new character
    if char_type == 'U': has_u = True
    if char_type == 'L': has_l = True
    if char_type == 'D': has_d = True

    # Reconstruct the state name based on the updated booleans
    new_state = 'q_'
    if has_u: new_state += 'U'
    if has_l: new_state += 'L'
    if has_d: new_state += 'D'

    # If it's still just 'q_', it means only 'Other' characters were entered
    if new_state == 'q_':
        return 'q0'

    return new_state

def simulate_password_dfa(password_string: str) -> tuple[bool, list]:
    """
    Simulates the Password DFA character by character.
    Returns a tuple: (is_accepted_boolean, transition_history_list)
    """
    current_state = 'q0'
    accept_state_requirement = 'q_ULD'
    transition_log = []
    
    length_count = 0

    for char in password_string:
        char_type = get_char_type(char)
        next_state = get_next_state(current_state, char_type)
        length_count += 1
        
        transition_log.append({
            'char': char,
            'from_state': current_state,
            'to_state': next_state,
            'status': 'PROCESSING'
        })
        
        current_state = next_state
        
    # The password is only accepted if it has all character types AND is at least 8 chars long
    is_accepted = (current_state == accept_state_requirement) and (length_count >= 8)
    
    # If it fails at the end, append a final summary note to the log for the GUI
    if not is_accepted:
        reason = []
        if current_state != accept_state_requirement:
            reason.append("Missing character types")
        if length_count < 8:
            reason.append("Too short")
        
        transition_log.append({
            'char': 'END',
            'from_state': current_state,
            'to_state': 'Rejected',
            'status': f"FAILED: {' and '.join(reason)}"
        })

    return is_accepted, transition_log


# --- TESTING BLOCK ---
if __name__ == "__main__":
    test_passwords = ["Abc12345", "weakpass", "Short1!"]
    
    for pwd in test_passwords:
        print(f"\nSimulating DFA for: {pwd}")
        accepted, log = simulate_password_dfa(pwd)
        
        for step in log:
            if step['char'] != 'END':
                print(f"Read '{step['char']}' | {step['from_state']} ---> {step['to_state']}")
            else:
                print(f"[{step['status']}]")
            
        print("-" * 33)
        if accepted:
            print("FINAL RESULT: PASSWORD ACCEPTED")
        else:
            print("FINAL RESULT: PASSWORD REJECTED")
        print("-" * 33)