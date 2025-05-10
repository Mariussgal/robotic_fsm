class State:
    def __init__(self, name, action=None, is_final=False, is_success=False):
        """
        Initialise un état.
        
        Argument:
            name (str): Nom de l'état
            action (callable, optZional): Action à exécuter dans cet état
            is_final (bool): Indique si c'est un état final
            is_success (bool): Indique si c'est un état de succès (pertinent si is_final=True)
        """
        self.name = name
        self.action = action
        self.is_final = is_final
        self.is_success = is_success
        self.transitions = [] 
    
    def add_transition(self, transition):
        """Ajoute une transition sortante à l'état"""
        self.transitions.append(transition)
    
    def __str__(self):
        return f"State({self.name}, final={self.is_final}, success={self.is_success})"


class Transition:
    def __init__(self, target_state, condition, probability=1.0):
        """
        Initialise une transition.
        
        Argument:
            target_state (State): État cible de la transition
            condition (callable): Fonction qui évalue si la transition doit être prise
            probability (float): Probabilité que la transition réussisse (entre 0 et 1)
        """
        self.target_state = target_state
        self.condition = condition
        self.probability = probability
    
    def should_transition(self, event):
        """
        Vérifie si la transition doit être prise en fonction de l'événement.
        
        Argument:
            event (str): Événement à évaluer
            
        Return:
            bool: True si la transition doit être prise, False sinon
        """
        return self.condition(event)


class FSM:
    def __init__(self, initial_state):
        """
        Initialise la FSM avec un état initial.
        """
        self.states = {initial_state.name: initial_state}
        self.current_state = initial_state
        self.initial_state = initial_state
        self.history = []  
    
    def add_state(self, state):
        """
        Ajoute un état à la FSM.
        """
        self.states[state.name] = state
    
    def process_event(self, event):
        """
        Traite un événement et effectue la transition appropriée.
        
        Argument:
            event (str): Événement à traiter
            
        Return:
            bool: True si la FSM a atteint un état final, False sinon
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
        """Réinitialise la FSM à son état initial"""
        self.current_state = self.initial_state
        self.history = []
    
    def display(self):
        """Affiche la FSM sous forme de liste dans la console"""
        print("États de la FSM:")
        for state in self.states.items():
            print(f"  {state}")
            for i, transition in enumerate(state.transitions):
                print(f"    Transition {i+1} -> {transition.target_state.name} (Prob: {transition.probability})")