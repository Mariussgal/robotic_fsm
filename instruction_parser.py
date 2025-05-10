INSTRUCTION_MAPPING = {
    "pass": {
        "task_sequence": ["GO_TO_BALL", "ALIGN", "PASS"],
        "params": ["target_robot"]
    },
    "shoot": {
        "task_sequence": ["GO_TO_BALL", "ALIGN_GOAL", "SHOOT"],
        "params": []
    },
    "block": {
        "task_sequence": ["GO_TO_POSITION", "BLOCK"],
        "params": ["target_robot"]
    },
    "intercept": {
        "task_sequence": ["CALCULATE_TRAJECTORY", "GO_TO_POSITION", "INTERCEPT"],
        "params": []
    }
}

def parse_instruction(instruction):
    """
    Analyse une instruction textuelle et retourne une séquence de tâches.

    """
    instruction = instruction.lower().strip()
    
    action = None
    params = {}
    
    for key in INSTRUCTION_MAPPING:
        if key in instruction:
            action = key
            break
    
    if not action:
        return None  
    
    if "to r" in instruction:
        for i in range(1, 10):  
            if f"r{i}" in instruction:
                params["target_robot"] = f"R{i}"
                break
    
    return {
        "action": action,
        "task_sequence": INSTRUCTION_MAPPING[action]["task_sequence"],
        "params": params
    }


def generate_task_sequence(instruction):
    """
    Génère séquence tâches à partir d'une instruction.

    """
    parsed = parse_instruction(instruction)
    
    if not parsed:
        return None
    
    return {
        "action": parsed["action"],
        "tasks": parsed["task_sequence"],
        "params": parsed["params"]
    }

if __name__ == "__main__":
    test_instructions = [
        "Pass the ball to R2",
        "Shoot the ball into the goal",
        "Block R3",
        "Intercept the ball"
    ]
    
    for instr in test_instructions:
        result = generate_task_sequence(instr)
        print(f"Instruction: '{instr}'")
        print(f"Résultat: {result}")
        print()