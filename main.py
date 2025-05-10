from fsm import FSM, State, Transition
import random
import robot_actions as ra

def create_simple_pass_fsm(target_robot="R2"):
    initial = State("INITIAL", None)
    go_to_ball_state = State("GO_TO_BALL", lambda e: ra.go_to_ball("R1"))
    align_state = State("ALIGN", lambda e: ra.align_with_target("R1", "R2"))
    pass_state = State("PASS", lambda e: ra.pass_ball("R1", "R2"))
    success_state = State("SUCCESS", None, is_final=True, is_success=True)
    failure_state = State("FAILURE", None, is_final=True, is_success=False)
    
    t1 = Transition(go_to_ball_state, ra.is_near_ball)
    t2 = Transition(align_state, ra.is_aligned)
    t3 = Transition(pass_state, ra.ball_kicked)
    t4 = Transition(success_state, ra.ball_received, probability=0.85)
    t5 = Transition(failure_state, lambda e: e == "PASS_FAILED", probability=1.0)
    
    initial.add_transition(t1)
    go_to_ball_state.add_transition(t2)
    align_state.add_transition(t3)
    pass_state.add_transition(t4)
    pass_state.add_transition(t5)

    fsm = FSM(initial)
    fsm.add_state(go_to_ball_state)
    fsm.add_state(align_state)
    fsm.add_state(pass_state)
    fsm.add_state(success_state)
    fsm.add_state(failure_state)
    
    return fsm

def create_shoot_fsm():
    """
    FSM for shooting at goal.
    """
    initial = State("INITIAL", None)
    go_to_ball_state = State("GO_TO_BALL", lambda e: ra.go_to_ball("R1"))
    align_goal_state = State("ALIGN_GOAL", lambda e: ra.align_with_target("R1", "GOAL"))
    shoot_state = State("SHOOT", lambda e: ra.kick_ball("R1", power=1.0))
    goal_state = State("GOAL", None, is_final=True, is_success=True)
    missed_state = State("MISSED", None, is_final=True, is_success=False)
    
    # Create transitions
    t1 = Transition(go_to_ball_state, ra.is_near_ball)
    t2 = Transition(align_goal_state, ra.is_aligned)
    t3 = Transition(shoot_state, ra.ball_kicked)
    t4 = Transition(goal_state, lambda e: e == "GOAL_SCORED", probability=1.0)  # 100% instead of 70%
    t5 = Transition(missed_state, lambda e: e == "SHOT_MISSED", probability=1.0)
    
    initial.add_transition(t1)
    go_to_ball_state.add_transition(t2)
    align_goal_state.add_transition(t3)
    shoot_state.add_transition(t4)
    shoot_state.add_transition(t5)
    
    fsm = FSM(initial)
    fsm.add_state(go_to_ball_state)
    fsm.add_state(align_goal_state)
    fsm.add_state(shoot_state)
    fsm.add_state(goal_state)
    fsm.add_state(missed_state)
    
    return fsm

def create_block_fsm(target_robot="R3"):
    """
    FSM for blocking an opponent robot.
    """
    initial = State("INITIAL", None)
    calc_pos_state = State("CALCULATE_POSITION", lambda e: print(f"Calculating position to block {target_robot}"))
    go_to_pos_state = State("GO_TO_POSITION", lambda e: print(f"Robot R1 moves to blocking position"))
    block_state = State("BLOCK", lambda e: ra.block_robot("R1", target_robot))
    success_state = State("BLOCKING_SUCCESS", None, is_final=True, is_success=True)
    failure_state = State("BLOCKING_FAILURE", None, is_final=True, is_success=False)
    
    t1 = Transition(calc_pos_state, lambda e: e == "START")
    t2 = Transition(go_to_pos_state, lambda e: e == "POSITION_CALCULATED")
    t3 = Transition(block_state, lambda e: e == "POSITION_REACHED")
    t4 = Transition(success_state, lambda e: e == "BLOCKING_EFFECTIVE", probability=0.9)
    t5 = Transition(failure_state, lambda e: e == "BLOCKING_INEFFECTIVE", probability=1.0)

    initial.add_transition(t1)
    calc_pos_state.add_transition(t2)
    go_to_pos_state.add_transition(t3)
    block_state.add_transition(t4)
    block_state.add_transition(t5)

    fsm = FSM(initial)
    fsm.add_state(calc_pos_state)
    fsm.add_state(go_to_pos_state)
    fsm.add_state(block_state)
    fsm.add_state(success_state)
    fsm.add_state(failure_state)
    
    return fsm

def create_intercept_fsm():
    """
    FSM for intercepting the ball.
    """
    initial = State("INITIAL", None)
    calc_trajectory_state = State("CALCULATE_TRAJECTORY", lambda e: print("Calculating ball trajectory"))
    go_to_intercept_state = State("GO_TO_INTERCEPT_POSITION", lambda e: print("Robot R1 moves to interception position"))
    intercept_state = State("INTERCEPT", lambda e: print("Robot R1 attempts to intercept the ball"))
    success_state = State("INTERCEPTION_SUCCESS", None, is_final=True, is_success=True)
    failure_state = State("INTERCEPTION_FAILURE", None, is_final=True, is_success=False)

    t1 = Transition(calc_trajectory_state, lambda e: e == "START")
    t2 = Transition(go_to_intercept_state, lambda e: e == "TRAJECTORY_CALCULATED")
    t3 = Transition(intercept_state, lambda e: e == "INTERCEPT_POSITION_REACHED")
    t4 = Transition(success_state, lambda e: e == "BALL_INTERCEPTED", probability=0.75)
    t5 = Transition(failure_state, lambda e: e == "INTERCEPTION_MISSED", probability=1.0)
    
    initial.add_transition(t1)
    calc_trajectory_state.add_transition(t2)
    go_to_intercept_state.add_transition(t3)
    intercept_state.add_transition(t4)
    intercept_state.add_transition(t5)
    
    fsm = FSM(initial)
    fsm.add_state(calc_trajectory_state)
    fsm.add_state(go_to_intercept_state)
    fsm.add_state(intercept_state)
    fsm.add_state(success_state)
    fsm.add_state(failure_state)
    
    return fsm

def create_fsm_from_instruction(instruction):
    """
    Creates FSM from a text instruction.
    """
    instruction = instruction.lower().strip()
    
    if "pass" in instruction:
        # Find target robot (R1, R2, R3, etc.)
        target = "R2"  # Default
        for i in range(1, 10):
            if f"r{i}" in instruction:
                target = f"R{i}"
                break
        return create_pass_fsm(target), f"Pass to robot {target}"
    
    elif "shoot" in instruction or "goal" in instruction:
        return create_shoot_fsm(), "Shoot at goal"
    
    elif "block" in instruction:
        # Find robot to block
        target = "R3"  # Default
        for i in range(1, 10):
            if f"r{i}" in instruction:
                target = f"R{i}"
                break
        return create_block_fsm(target), f"Block robot {target}"
    
    elif "intercept" in instruction:
        return create_intercept_fsm(), "Intercept the ball"
    
    else:
        return None, "Unrecognized instruction"

def display_fsm_with_explanation(fsm, action_type):
    """
    Displays the FSM with a natural language explanation.
    """

    print("\nExplanation of this FSM:")
    
    if "Pass" in action_type:
        print("1. Robot starts in INITIAL state")
        print("2. It goes to get the ball (GO_TO_BALL)")
        print("3. It aligns with the target robot (ALIGN)")
        print("4. It performs the pass (PASS)")
        print("5. If the pass is successful, it reaches SUCCESS state")
        print("   Otherwise, it reaches FAILURE state")
    elif "Shoot" in action_type:
        print("1. Robot starts in INITIAL state")
        print("2. It goes to get the ball (GO_TO_BALL)")
        print("3. It aligns with the goal (ALIGN_GOAL)")
        print("4. It shoots at goal (SHOOT)")
        print("5. If the shot is successful, it reaches GOAL state")
        print("   Otherwise, it reaches MISSED state")
    elif "Block" in action_type:
        print("1. Robot starts in INITIAL state")
        print("2. It calculates the blocking position (CALCULATE_POSITION)")
        print("3. It moves to this position (GO_TO_POSITION)")
        print("4. It performs the block (BLOCK)")
        print("5. If the block is effective, it reaches BLOCKING_SUCCESS state")
        print("   Otherwise, it reaches BLOCKING_FAILURE state")
    elif "Intercept" in action_type:
        print("1. Robot starts in INITIAL state")
        print("2. It calculates the ball trajectory (CALCULATE_TRAJECTORY)")
        print("3. It moves to the interception position (GO_TO_INTERCEPT_POSITION)")
        print("4. It attempts to intercept the ball (INTERCEPT)")
        print("5. If the interception succeeds, it reaches INTERCEPTION_SUCCESS state")
        print("   Otherwise, it reaches INTERCEPTION_FAILURE state")
    
    print("\nEach transition between states depends on specific events")
    print("and has a certain probability of success.")

def get_instruction_with_help():
    """
    Asks for an instruction with examples.
    """
    print("\nPlease enter an instruction for the robot.")
    print("Valid instruction examples:")
    print("  - Pass the ball to R2")
    print("  - Shoot the ball into the goal")
    print("  - Block R3")
    print("  - Intercept the ball")
    
    return input("\nYour instruction: ")

def text_visualize_fsm(fsm):
    """
    Visualizes FSM as ASCII text.
    """
    print("\nFSM Visualization:")
    
    initial = fsm.initial_state
    finals = [state for state in fsm.states.values() if state.is_final]
    intermediates = [state for state in fsm.states.values() 
                     if state != initial and state not in finals]
    
    print(f"  [{initial.name}]")
    print("    |")
    
    for i, state in enumerate(intermediates):
        print(f"    v")
        print(f"  [{state.name}]")
        if i < len(intermediates) - 1:
            print("    |")
    
    if finals:
        if len(finals) == 1:
            print("    |")
            print("    v")
            state = finals[0]
            success = "✓" if state.is_success else "✗"
            print(f"  [{state.name}] {success}")
        else:
            print("    |")
            print("    +---------+") 
            
            success_states = [state for state in finals if state.is_success]
            if success_states:
                print("    |         |")
                print(f"    v         v")
                state = success_states[0]
                print(f"  [{state.name}] ✓    [{finals[1].name}] ✗")
                print("  (Success)   (Failure)")
            else:
                print("    |         |")
                print(f"    v         v")
                print(f"  [{finals[0].name}]    [{finals[1].name}]")

def show_help_and_glossary():
    """
    Shows help.
    """
    print("\n=== Help and Glossary ===")
    
    print("\nKey concepts:")
    print("  FSM (Finite State Machine): A mathematical model used to represent")
    print("  systems that can be in a finite number of distinct states.")
    print("\n  State: A situation or action in which the robot can be")
    print("  (ex: GO_TO_BALL, ALIGN, PASS).")
    print("\n  Transition: A change from one state to another in response to an event.")
    print("\n  Event: A signal that triggers a transition (ex: NEAR_BALL, ALIGNED).")
    
    print("\nTypes of actions:")
    print("  Pass: Robot goes to get the ball and passes it to another robot.")
    print("  Shoot: Robot goes to get the ball and shoots at goal.")
    print("  Block: Robot positions itself to block an opponent.")
    print("  Intercept: Robot calculates the ball trajectory and attempts to intercept it.")
    
    print("\nProgram navigation:")
    print("  Main menu: Allows choosing different features.")
    print("  Simulation: Allows seeing robot behavior step by step.")
    print("  Export: Allows saving the FSM to a file.")
    
    input("\nPress Enter to return to main menu...")

def simulate_fsm(fsm, action_type):
    """
    Simulates FSM execution with a predefined sequence of events.
    """
    print(f"\nFSM simulation for: {action_type}")
    fsm.reset()  
    
    sequences = {
        "Pass": [
            ("NEAR_BALL", "GO_TO_BALL"),
            ("ALIGNED", "ALIGN"),
            ("BALL_KICKED", "PASS"),
            ("BALL_RECEIVED", "SUCCESS")  
        ],
        "Shoot": [
            ("NEAR_BALL", "GO_TO_BALL"),
            ("ALIGNED", "ALIGN_GOAL"),
            ("BALL_KICKED", "SHOOT"),
            ("GOAL_SCORED", "GOAL")  
        ],
        "Block": [
            ("START", "CALCULATE_POSITION"),
            ("POSITION_CALCULATED", "GO_TO_POSITION"),
            ("POSITION_REACHED", "BLOCK"),
            ("BLOCKING_EFFECTIVE", "BLOCKING_SUCCESS")  
        ],
        "Intercept": [
            ("START", "CALCULATE_TRAJECTORY"),
            ("TRAJECTORY_CALCULATED", "GO_TO_INTERCEPT_POSITION"),
            ("INTERCEPT_POSITION_REACHED", "INTERCEPT"),
            ("BALL_INTERCEPTED", "INTERCEPTION_SUCCESS")  
        ]
    }
    
    if "Pass" in action_type:
        sequence = sequences["Pass"]
    elif "Shoot" in action_type:
        sequence = sequences["Shoot"]
    elif "Block" in action_type:
        sequence = sequences["Block"]
    elif "Intercept" in action_type:
        sequence = sequences["Intercept"]
    else:
        sequence = sequences["Pass"]
    
    print("\nProposed event sequence:")
    for i, (event, next_state) in enumerate(sequence):
        print(f"{i+1}. {event} -> {next_state}")
    
    print("\nPress Enter to progress in the simulation, or type 'q' to quit.")
    
    for event, expected_state in sequence:
        input_val = input(f"\nPress Enter to send event '{event}', or type 'q' to quit: ")
        
        if input_val.lower() == 'q':
            print("Simulation stopped.")
            break
        
        print(f"Event sent: {event}")
        
        final_reached = fsm.process_event(event)
        
        print(f"State after event: {fsm.current_state.name}")
        
        if fsm.current_state.is_final:
            result = "Success" if fsm.current_state.is_success else "Failure"
            print(f"Simulation ended: {result}")
            break
    
    print("\nState history:")
    print(" -> ".join(fsm.history + [fsm.current_state.name]))

def export_fsm_to_text(fsm, filename="fsm_export.txt"):
    """
    Exports FSM to text format.
    """
    with open(filename, 'w') as f:
        f.write("=== Finite State Machine Export ===\n\n")
        
        f.write("States:\n")
        for state in fsm.states.items():
            f.write(f"  - {state}\n")
            
            for i, transition in enumerate(state.transitions):
                f.write(f"    Transition {i+1} -> {transition.target_state.name} (Prob: {transition.probability})\n")
        
        f.write("\nInitial state: " + fsm.initial_state.name + "\n")
    
    print(f"FSM successfully exported to file '{filename}'")

def create_pass_fsm(target_robot="R2"):
    """
    Alias for create_simple_pass_fsm
    """
    return create_simple_pass_fsm(target_robot)

def main():
    """Main program function"""
    print("\n=== Robotic Action Planning System for RoboCup SSL ===")
    print("\nThis program allows you to generate and simulate robotic behaviors")
    print("for soccer matches using finite state machines (FSM).")
    print("\nEach FSM represents a sequence of actions a robot can perform,")
    print("such as going to the ball, aligning, passing, shooting, etc.")
    
    while True:
        print("\nMain menu:")
        print("1. Generate FSM from instruction")
        print("2. Simulate predefined FSM")
        print("3. Export FSM")
        print("4. Help and glossary")
        print("5. Quit")
        
        choice = input("\nChoose an option: ")
        
        if choice == "1":
            instruction = get_instruction_with_help()
            fsm, action_desc = create_fsm_from_instruction(instruction)
            
            if fsm:
                display_fsm_with_explanation(fsm, action_desc)
                text_visualize_fsm(fsm)
                
                if input("\nDo you want to simulate this FSM? (y/n): ").lower() == "y":
                    simulate_fsm(fsm, action_desc)
                
                if input("\nDo you want to export this FSM? (y/n): ").lower() == "y":
                    filename = input("Export filename (default: fsm_export.txt): ")
                    if not filename:
                        filename = "fsm_export.txt"
                    export_fsm_to_text(fsm, filename)
            else:
                print(f"\n{action_desc}")
        
        elif choice == "2":
            print("\nChoose a predefined FSM:")
            print("1. Pass between robots")
            print("2. Shoot at goal")
            print("3. Block opponent robot")
            print("4. Intercept ball")
            
            fsm_choice = input("\nChoose a FSM: ")
            
            if fsm_choice == "1":
                fsm = create_simple_pass_fsm()
                action_desc = "Pass between robots"
                display_fsm_with_explanation(fsm, action_desc)
                text_visualize_fsm(fsm)
                simulate_fsm(fsm, action_desc)
            elif fsm_choice == "2":
                fsm = create_shoot_fsm()
                action_desc = "Shoot at goal"
                display_fsm_with_explanation(fsm, action_desc)
                text_visualize_fsm(fsm)
                simulate_fsm(fsm, action_desc)
            elif fsm_choice == "3":
                fsm = create_block_fsm()
                action_desc = "Block opponent robot"
                display_fsm_with_explanation(fsm, action_desc)
                text_visualize_fsm(fsm)
                simulate_fsm(fsm, action_desc)
            elif fsm_choice == "4":
                fsm = create_intercept_fsm()
                action_desc = "Intercept ball"
                display_fsm_with_explanation(fsm, action_desc)
                text_visualize_fsm(fsm)
                simulate_fsm(fsm, action_desc)
            else:
                print("Invalid choice.")
        
        elif choice == "3":
            print("\nExport FSM:")
            print("1. Pass between robots")
            print("2. Shoot at goal")
            print("3. Block opponent robot")
            print("4. Intercept ball")
            
            fsm_choice = input("\nChoose a FSM to export: ")
            
            fsm = None
            if fsm_choice == "1":
                fsm = create_simple_pass_fsm()
            elif fsm_choice == "2":
                fsm = create_shoot_fsm()
            elif fsm_choice == "3":
                fsm = create_block_fsm()
            elif fsm_choice == "4":
                fsm = create_intercept_fsm()
            else:
                print("Invalid choice.")
                continue
            
            filename = input("Export filename (default: fsm_export.txt): ")
            if not filename:
                filename = "fsm_export.txt"
            
            export_fsm_to_text(fsm, filename)
        
        elif choice == "4":
            show_help_and_glossary()
        
        elif choice == "5":
            print("Thank you for using the robotic action planning system!")
            break
        
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()