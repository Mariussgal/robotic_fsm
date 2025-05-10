class State:
    def __init__(self, name, action=None, is_final=False, is_success=False):
        """
        Initialize a state.
        
        Args:
            name (str): Name of the state
            action (callable, optional): Action to execute in this state
            is_final (bool): Indicates if this is a final state
            is_success (bool): Indicates if this is a success state (relevant if is_final=True)
        """
        self.name = name
        self.action = action
        self.is_final = is_final
        self.is_success = is_success
        self.transitions = [] 
    
    def add_transition(self, transition):
        """Add an outgoing transition to the state"""
        self.transitions.append(transition)
    
    def __str__(self):
        return f"State({self.name}, final={self.is_final}, success={self.is_success})"


class Transition:
    def __init__(self, target_state, condition, probability=1.0):
        """
        Initialize a transition.
        
        Args:
            target_state (State): Target state of the transition
            condition (callable): Function that evaluates if the transition should be taken
            probability (float): Probability that the transition succeeds (between 0 and 1)
        """
        self.target_state = target_state
        self.condition = condition
        self.probability = probability
    
    def should_transition(self, event):
        """
        Check if the transition should be taken based on the event.
        
        Args:
            event (str): Event to evaluate
            
        Returns:
            bool: True if the transition should be taken, False otherwise
        """
        return self.condition(event)


class FSM:
    def __init__(self, initial_state):
        """
        Initialize the FSM with an initial state.
        """
        self.states = {initial_state.name: initial_state}
        self.current_state = initial_state
        self.initial_state = initial_state
        self.history = []  
    
    def add_state(self, state):
        """
        Add a state to the FSM.
        """
        self.states[state.name] = state
    
    def process_event(self, event):
        """
        Process an event and perform the appropriate transition.
        
        Args:
            event (str): Event to process
            
        Returns:
            bool: True if the FSM has reached a final state, False otherwise
        """
        self.history.append(self.current_state.name)
        
        if self.current_state.action:
            self.current_state.action(event)
        
        if self.current_state.is_final:
            return True
        
        possible_transitions = []
        for transition in self.current_state.transitions:
            if transition.should_transition(event):
                possible_transitions.append(transition)
        
        if not possible_transitions:
            return False
        
        if event in ["GOAL_SCORED", "BALL_RECEIVED", "BLOCKING_EFFECTIVE", "BALL_INTERCEPTED"]:
            for transition in possible_transitions:
                if transition.target_state.is_final and transition.target_state.is_success:
                    self.current_state = transition.target_state
                    return True
        
        if event in ["SHOT_MISSED", "PASS_FAILED", "BLOCKING_INEFFECTIVE", "INTERCEPTION_MISSED"]:
            for transition in possible_transitions:
                if transition.target_state.is_final and not transition.target_state.is_success:
                    self.current_state = transition.target_state
                    return True
        
        transition = possible_transitions[0]
        
        self.current_state = transition.target_state
        
        return False
    
    def reset(self):
        """Reset the FSM to its initial state"""
        self.current_state = self.initial_state
        self.history = []
    
    def display(self):
        """Display the FSM as a list in the console"""
        print("FSM States:")
        for name, state in self.states.items():
            print(f"  {state}")
            for i, transition in enumerate(state.transitions):
                print(f"    Transition {i+1} -> {transition.target_state.name} (Prob: {transition.probability})")