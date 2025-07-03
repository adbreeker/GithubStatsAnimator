"""
Character patterns for contribution square text animation
Each character is 5 squares high and 4 squares wide
"""

# Letter patterns - 5 rows × 4 columns each
LETTER_PATTERNS = {
    'A': [
        [0, 1, 1, 0],  # Row 0:  ██  
        [1, 0, 0, 1],  # Row 1: █  █
        [1, 1, 1, 1],  # Row 2: ████
        [1, 0, 0, 1],  # Row 3: █  █
        [1, 0, 0, 1]   # Row 4: █  █
    ],
    'B': [
        [1, 1, 1, 0],  # Row 0: ███ 
        [1, 0, 0, 1],  # Row 1: █  █
        [1, 1, 1, 0],  # Row 2: ███ 
        [1, 0, 0, 1],  # Row 3: █  █
        [1, 1, 1, 0]   # Row 4: ███ 
    ],
    'C': [
        [0, 1, 1, 1],  # Row 0:  ███
        [1, 0, 0, 0],  # Row 1: █   
        [1, 0, 0, 0],  # Row 2: █   
        [1, 0, 0, 0],  # Row 3: █   
        [0, 1, 1, 1]   # Row 4:  ███
    ],
    'D': [
        [1, 1, 1, 0],  # Row 0: ███ 
        [1, 0, 0, 1],  # Row 1: █  █
        [1, 0, 0, 1],  # Row 2: █  █
        [1, 0, 0, 1],  # Row 3: █  █
        [1, 1, 1, 0]   # Row 4: ███ 
    ],
    'E': [
        [1, 1, 1, 1],  # Row 0: ████
        [1, 0, 0, 0],  # Row 1: █   
        [1, 1, 1, 0],  # Row 2: ███ 
        [1, 0, 0, 0],  # Row 3: █   
        [1, 1, 1, 1]   # Row 4: ████
    ],
    'F': [
        [1, 1, 1, 1],  # Row 0: ████
        [1, 0, 0, 0],  # Row 1: █   
        [1, 1, 1, 0],  # Row 2: ███ 
        [1, 0, 0, 0],  # Row 3: █   
        [1, 0, 0, 0]   # Row 4: █   
    ],
    'G': [
        [0, 1, 1, 1],  # Row 0:  ███
        [1, 0, 0, 0],  # Row 1: █   
        [1, 0, 1, 1],  # Row 2: █ ██
        [1, 0, 0, 1],  # Row 3: █  █
        [0, 1, 1, 1]   # Row 4:  ███
    ],
    'H': [
        [1, 0, 0, 1],  # Row 0: █  █
        [1, 0, 0, 1],  # Row 1: █  █
        [1, 1, 1, 1],  # Row 2: ████
        [1, 0, 0, 1],  # Row 3: █  █
        [1, 0, 0, 1]   # Row 4: █  █
    ],
    'I': [
        [1, 1, 1, 1],  # Row 0: ████
        [0, 1, 1, 0],  # Row 1:  ██ 
        [0, 1, 1, 0],  # Row 2:  ██ 
        [0, 1, 1, 0],  # Row 3:  ██ 
        [1, 1, 1, 1]   # Row 4: ████
    ],
    'J': [
        [1, 1, 1, 1],  # Row 0: ████
        [0, 0, 1, 0],  # Row 1:   █ 
        [0, 0, 1, 0],  # Row 2:   █ 
        [1, 0, 1, 0],  # Row 3: █ █ 
        [0, 1, 0, 0]   # Row 4:  █  
    ],
    'K': [
        [1, 0, 0, 1],  # Row 0: █  █
        [1, 0, 1, 0],  # Row 1: █ █ 
        [1, 1, 0, 0],  # Row 2: ██  
        [1, 0, 1, 0],  # Row 3: █ █ 
        [1, 0, 0, 1]   # Row 4: █  █
    ],
    'L': [
        [1, 0, 0, 0],  # Row 0: █   
        [1, 0, 0, 0],  # Row 1: █   
        [1, 0, 0, 0],  # Row 2: █   
        [1, 0, 0, 0],  # Row 3: █   
        [1, 1, 1, 1]   # Row 4: ████
    ],
    'M': [
        [1, 0, 0, 1],  # Row 0: █  █
        [1, 1, 1, 1],  # Row 1: ████
        [1, 1, 1, 1],  # Row 2: ████
        [1, 0, 0, 1],  # Row 3: █  █
        [1, 0, 0, 1]   # Row 4: █  █
    ],
    'N': [
        [1, 0, 0, 1],  # Row 0: █  █
        [1, 1, 0, 1],  # Row 1: ██ █
        [1, 1, 1, 1],  # Row 2: ████
        [1, 0, 1, 1],  # Row 3: █ ██
        [1, 0, 0, 1]   # Row 4: █  █
    ],
    'O': [
        [0, 1, 1, 0],  # Row 0:  ██ 
        [1, 0, 0, 1],  # Row 1: █  █
        [1, 0, 0, 1],  # Row 2: █  █
        [1, 0, 0, 1],  # Row 3: █  █
        [0, 1, 1, 0]   # Row 4:  ██ 
    ],
    'P': [
        [1, 1, 1, 0],  # Row 0: ███ 
        [1, 0, 0, 1],  # Row 1: █  █
        [1, 1, 1, 0],  # Row 2: ███ 
        [1, 0, 0, 0],  # Row 3: █   
        [1, 0, 0, 0]   # Row 4: █   
    ],
    'Q': [
        [0, 1, 1, 0],  # Row 0:  ██ 
        [1, 0, 0, 1],  # Row 1: █  █
        [1, 0, 0, 1],  # Row 2: █  █
        [1, 0, 1, 1],  # Row 3: █ ██
        [0, 1, 1, 1]   # Row 4:  ███
    ],
    'R': [
        [1, 1, 1, 0],  # Row 0: ███ 
        [1, 0, 0, 1],  # Row 1: █  █
        [1, 1, 1, 0],  # Row 2: ███ 
        [1, 0, 1, 0],  # Row 3: █ █ 
        [1, 0, 0, 1]   # Row 4: █  █
    ],
    'S': [
        [0, 1, 1, 1],  # Row 0:  ███
        [1, 0, 0, 0],  # Row 1: █   
        [0, 1, 1, 0],  # Row 2:  ██ 
        [0, 0, 0, 1],  # Row 3:    █
        [1, 1, 1, 0]   # Row 4: ███ 
    ],
    'T': [
        [1, 1, 1, 1],  # Row 0: ████
        [0, 1, 1, 0],  # Row 1:  ██ 
        [0, 1, 1, 0],  # Row 2:  ██ 
        [0, 1, 1, 0],  # Row 3:  ██ 
        [0, 1, 1, 0]   # Row 4:  ██ 
    ],
    'U': [
        [1, 0, 0, 1],  # Row 0: █  █
        [1, 0, 0, 1],  # Row 1: █  █
        [1, 0, 0, 1],  # Row 2: █  █
        [1, 0, 0, 1],  # Row 3: █  █
        [0, 1, 1, 0]   # Row 4:  ██ 
    ],
    'V': [
        [1, 0, 0, 1],  # Row 0: █  █
        [1, 0, 0, 1],  # Row 1: █  █
        [1, 0, 0, 1],  # Row 2: █  █
        [0, 1, 1, 0],  # Row 3:  ██ 
        [0, 1, 1, 0]   # Row 4:  ██ 
    ],
    'W': [
        [1, 0, 0, 1],  # Row 0: █  █
        [1, 0, 0, 1],  # Row 1: █  █
        [1, 1, 1, 1],  # Row 2: ████
        [1, 1, 1, 1],  # Row 3: ████
        [1, 0, 0, 1]   # Row 4: █  █
    ],
    'X': [
        [1, 0, 0, 1],  # Row 0: █  █
        [0, 1, 1, 0],  # Row 1:  ██ 
        [0, 1, 1, 0],  # Row 2:  ██ 
        [0, 1, 1, 0],  # Row 3:  ██ 
        [1, 0, 0, 1]   # Row 4: █  █
    ],
    'Y': [
        [1, 0, 0, 1],  # Row 0: █  █
        [1, 0, 0, 1],  # Row 1: █  █
        [0, 1, 1, 0],  # Row 2:  ██ 
        [0, 1, 1, 0],  # Row 3:  ██ 
        [0, 1, 1, 0]   # Row 4:  ██ 
    ],
    'Z': [
        [1, 1, 1, 1],  # Row 0: ████
        [0, 0, 0, 1],  # Row 1:    █
        [0, 1, 1, 0],  # Row 2:  ██ 
        [1, 0, 0, 0],  # Row 3: █   
        [1, 1, 1, 1]   # Row 4: ████
    ]
}

# Number patterns - 5 rows × 4 columns each
NUMBER_PATTERNS = {
    '0': [
        [0, 1, 1, 0],  # Row 0:  ██ 
        [1, 0, 0, 1],  # Row 1: █  █
        [1, 0, 0, 1],  # Row 2: █  █
        [1, 0, 0, 1],  # Row 3: █  █
        [0, 1, 1, 0]   # Row 4:  ██ 
    ],
    '1': [
        [0, 1, 1, 0],  # Row 0:  ██ 
        [1, 1, 1, 0],  # Row 1: ███ 
        [0, 1, 1, 0],  # Row 2:  ██ 
        [0, 1, 1, 0],  # Row 3:  ██ 
        [1, 1, 1, 1]   # Row 4: ████
    ],
    '2': [
        [0, 1, 1, 0],  # Row 0:  ██ 
        [1, 0, 0, 1],  # Row 1: █  █
        [0, 0, 1, 0],  # Row 2:   █ 
        [0, 1, 0, 0],  # Row 3:  █  
        [1, 1, 1, 1]   # Row 4: ████
    ],
    '3': [
        [1, 1, 1, 0],  # Row 0: ███ 
        [0, 0, 0, 1],  # Row 1:    █
        [0, 1, 1, 0],  # Row 2:  ██ 
        [0, 0, 0, 1],  # Row 3:    █
        [1, 1, 1, 0]   # Row 4: ███ 
    ],
    '4': [
        [1, 0, 0, 1],  # Row 0: █  █
        [1, 0, 0, 1],  # Row 1: █  █
        [1, 1, 1, 1],  # Row 2: ████
        [0, 0, 0, 1],  # Row 3:    █
        [0, 0, 0, 1]   # Row 4:    █
    ],
    '5': [
        [1, 1, 1, 1],  # Row 0: ████
        [1, 0, 0, 0],  # Row 1: █   
        [1, 1, 1, 0],  # Row 2: ███ 
        [0, 0, 0, 1],  # Row 3:    █
        [1, 1, 1, 0]   # Row 4: ███ 
    ],
    '6': [
        [0, 1, 1, 0],  # Row 0:  ██ 
        [1, 0, 0, 0],  # Row 1: █   
        [1, 1, 1, 0],  # Row 2: ███ 
        [1, 0, 0, 1],  # Row 3: █  █
        [0, 1, 1, 0]   # Row 4:  ██ 
    ],
    '7': [
        [1, 1, 1, 1],  # Row 0: ████
        [0, 0, 0, 1],  # Row 1:    █
        [0, 0, 1, 0],  # Row 2:   █ 
        [0, 1, 0, 0],  # Row 3:  █  
        [1, 0, 0, 0]   # Row 4: █   
    ],
    '8': [
        [0, 1, 1, 0],  # Row 0:  ██ 
        [1, 0, 0, 1],  # Row 1: █  █
        [0, 1, 1, 0],  # Row 2:  ██ 
        [1, 0, 0, 1],  # Row 3: █  █
        [0, 1, 1, 0]   # Row 4:  ██ 
    ],
    '9': [
        [0, 1, 1, 0],  # Row 0:  ██ 
        [1, 0, 0, 1],  # Row 1: █  █
        [0, 1, 1, 1],  # Row 2:  ███
        [0, 0, 0, 1],  # Row 3:    █
        [0, 1, 1, 0]   # Row 4:  ██ 
    ]
}

# Special characters
SPECIAL_PATTERNS = {
    ' ': [
        [0, 0, 0, 0],  # Row 0:     
        [0, 0, 0, 0],  # Row 1:     
        [0, 0, 0, 0],  # Row 2:     
        [0, 0, 0, 0],  # Row 3:     
        [0, 0, 0, 0]   # Row 4:     
    ],
    '!': [
        [0, 1, 1, 0],  # Row 0:  ██ 
        [0, 1, 1, 0],  # Row 1:  ██ 
        [0, 1, 1, 0],  # Row 2:  ██ 
        [0, 0, 0, 0],  # Row 3:     
        [0, 1, 1, 0]   # Row 4:  ██ 
    ],
    '?': [
        [0, 1, 1, 0],  # Row 0:  ██ 
        [1, 0, 0, 1],  # Row 1: █  █
        [0, 0, 1, 0],  # Row 2:   █ 
        [0, 0, 0, 0],  # Row 3:     
        [0, 1, 0, 0]   # Row 4:  █  
    ],
    '.': [
        [0, 0, 0, 0],  # Row 0:     
        [0, 0, 0, 0],  # Row 1:     
        [0, 0, 0, 0],  # Row 2:     
        [0, 0, 0, 0],  # Row 3:     
        [0, 1, 1, 0]   # Row 4:  ██ 
    ],
    '-': [
        [0, 0, 0, 0],  # Row 0:     
        [0, 0, 0, 0],  # Row 1:     
        [1, 1, 1, 1],  # Row 2: ████
        [0, 0, 0, 0],  # Row 3:     
        [0, 0, 0, 0]   # Row 4:     
    ],
    '_': [
        [0, 0, 0, 0],  # Row 0:     
        [0, 0, 0, 0],  # Row 1:     
        [0, 0, 0, 0],  # Row 2:     
        [0, 0, 0, 0],  # Row 3:     
        [1, 1, 1, 1]   # Row 4: ████
    ]
}

# Combine all patterns
ALL_PATTERNS = {**LETTER_PATTERNS, **NUMBER_PATTERNS, **SPECIAL_PATTERNS}

def get_char_pattern(char: str):
    """Get the pattern for a character, returns space pattern if not found"""
    return ALL_PATTERNS.get(char.upper(), SPECIAL_PATTERNS[' '])

def generate_text_pattern(text: str):
    """Generate a 2D pattern for text display - returns dict with letter positions"""
    result = {}
    col_offset = 0
    
    for i, char in enumerate(text.upper()):
        pattern = get_char_pattern(char)
        result[col_offset] = pattern
        col_offset += 4  # Each character is 4 columns wide
        
        # Add 1 column space between characters (except after the last character)
        if i < len(text) - 1:
            col_offset += 1
    
    return result

def preview_text(text: str):
    """Preview how text will look as contribution squares"""
    patterns = generate_text_pattern(text)
    if not patterns:
        print("No text to preview")
        return
    
    # Get the maximum width
    max_col = max(patterns.keys()) + 4
    
    print(f"Preview of '{text}' ({max_col} columns wide):")
    print()
    
    # Print each row
    for row in range(5):
        line = ""
        for col in range(max_col):
            # Find which character this column belongs to
            char_found = False
            for start_col, pattern in patterns.items():
                if start_col <= col < start_col + 4:
                    pattern_col = col - start_col
                    if pattern[row][pattern_col] == 1:
                        line += "█"
                    else:
                        line += " "
                    char_found = True
                    break
            
            if not char_found:
                line += " "  # Space between characters
        
        print(line)
    
    print()
    print(f"Total width: {max_col} columns")
