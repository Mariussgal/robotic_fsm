from fsm import FSM, State, Transition, random
import robot_actions as ra

def create_simple_pass_fsm():

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
    FSM pour un tir au but.
    """
    initial = State("INITIAL", None)
    go_to_ball_state = State("GO_TO_BALL", lambda e: ra.go_to_ball("R1"))
    align_goal_state = State("ALIGN_GOAL", lambda e: ra.align_with_target("R1", "GOAL"))
    shoot_state = State("SHOOT", lambda e: ra.kick_ball("R1", power=1.0))
    goal_state = State("GOAL", None, is_final=True, is_success=True)
    missed_state = State("MISSED", None, is_final=True, is_success=False)
    
    # Création des transitions
    t1 = Transition(go_to_ball_state, ra.is_near_ball)
    t2 = Transition(align_goal_state, ra.is_aligned)
    t3 = Transition(shoot_state, ra.ball_kicked)
    t4 = Transition(goal_state, lambda e: e == "GOAL_SCORED", probability=1.0)  # 100% au lieu de 70%
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
    FSM pour bloquer un robot adverse.
    """
    initial = State("INITIAL", None)
    calc_pos_state = State("CALCULATE_POSITION", lambda e: print(f"Calcul de la position pour bloquer {target_robot}"))
    go_to_pos_state = State("GO_TO_POSITION", lambda e: print(f"Robot R1 se déplace vers la position de blocage"))
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
    FSM pour intercepter la balle.
    """
    initial = State("INITIAL", None)
    calc_trajectory_state = State("CALCULATE_TRAJECTORY", lambda e: print("Calcul de la trajectoire de la balle"))
    go_to_intercept_state = State("GO_TO_INTERCEPT_POSITION", lambda e: print("Robot R1 se déplace vers la position d'interception"))
    intercept_state = State("INTERCEPT", lambda e: print("Robot R1 tente d'intercepter la balle"))
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
    Crée FSM à partir d'une instruction textuelle.

    """
    instruction = instruction.lower().strip()
    
    if "pass" in instruction:
        # Recherche robot cible (R1, R2, R3, etc.)
        target = "R2"  # Par défaut
        for i in range(1, 10):
            if f"r{i}" in instruction:
                target = f"R{i}"
                break
        return create_pass_fsm(), f"Passe au robot {target}"
    
    elif "shoot" in instruction or "goal" in instruction:
        return create_shoot_fsm(), "Tir au but"
    
    elif "block" in instruction:
        # Recherche robot à bloquer
        target = "R3"  # Par défaut
        for i in range(1, 10):
            if f"r{i}" in instruction:
                target = f"R{i}"
                break
        return create_block_fsm(target), f"Blocage du robot {target}"
    
    elif "intercept" in instruction:
        return create_intercept_fsm(), "Interception de la balle"
    
    else:
        return None, "Instruction non reconnue"

def display_fsm_with_explanation(fsm, action_type):
    """
    Affiche la FSM avec une explication en langage naturel.
    """
    print(f"\nFSM générée pour: {action_type}")
    fsm.display()
    
    # Ajouter une explication en langage naturel
    print("\nExplication de cette FSM:")
    
    if "Passe" in action_type:
        print("1. Le robot commence dans l'état INITIAL")
        print("2. Il va chercher la balle (GO_TO_BALL)")
        print("3. Il s'aligne avec le robot cible (ALIGN)")
        print("4. Il effectue la passe (PASS)")
        print("5. Si la passe est réussie, il atteint l'état SUCCESS")
        print("   Sinon, il atteint l'état FAILURE")
    elif "Tir" in action_type:
        print("1. Le robot commence dans l'état INITIAL")
        print("2. Il va chercher la balle (GO_TO_BALL)")
        print("3. Il s'aligne avec le but (ALIGN_GOAL)")
        print("4. Il tire au but (SHOOT)")
        print("5. Si le tir est réussi, il atteint l'état GOAL")
        print("   Sinon, il atteint l'état MISSED")
    elif "Blocage" in action_type:
        print("1. Le robot commence dans l'état INITIAL")
        print("2. Il calcule la position pour bloquer (CALCULATE_POSITION)")
        print("3. Il se déplace vers cette position (GO_TO_POSITION)")
        print("4. Il effectue le blocage (BLOCK)")
        print("5. Si le blocage est efficace, il atteint l'état BLOCKING_SUCCESS")
        print("   Sinon, il atteint l'état BLOCKING_FAILURE")
    elif "Interception" in action_type:
        print("1. Le robot commence dans l'état INITIAL")
        print("2. Il calcule la trajectoire de la balle (CALCULATE_TRAJECTORY)")
        print("3. Il se déplace vers la position d'interception (GO_TO_INTERCEPT_POSITION)")
        print("4. Il tente d'intercepter la balle (INTERCEPT)")
        print("5. Si l'interception réussit, il atteint l'état INTERCEPTION_SUCCESS")
        print("   Sinon, il atteint l'état INTERCEPTION_FAILURE")
    
    print("\nChaque transition entre états dépend d'événements spécifiques")
    print("et a une certaine probabilité de réussite.")

def get_instruction_with_help():
    """
    Demande une instruction à l'utilisateur avec des exemples.
    """
    print("\nVeuillez entrer une instruction pour le robot.")
    print("Exemples d'instructions valides:")
    print("  - Pass the ball to R2")
    print("  - Shoot the ball into the goal")
    print("  - Block R3")
    print("  - Intercept the ball")
    
    return input("\nVotre instruction: ")

def text_visualize_fsm(fsm):
    """
    Visualise FSM sous forme de texte ASCII.
    """
    print("\nVisualisation de la FSM:")
    
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
                print("  (Succès)    (Échec)")
            else:
                print("    |         |")
                print(f"    v         v")
                print(f"  [{finals[0].name}]    [{finals[1].name}]")

def show_help_and_glossary():
    """
    Affiche aide.
    """
    print("\n=== Aide et Glossaire ===")
    
    print("\nConcepts clés:")
    print("  FSM (Machine à États Finis) : Un modèle mathématique utilisé pour représenter")
    print("  des systèmes qui peuvent être dans un nombre fini d'états distincts.")
    print("\n  État : Une situation ou action dans laquelle le robot peut se trouver")
    print("  (ex: GO_TO_BALL, ALIGN, PASS).")
    print("\n  Transition : Un changement d'un état à un autre en réponse à un événement.")
    print("\n  Événement : Un signal qui déclenche une transition (ex: NEAR_BALL, ALIGNED).")
    
    print("\nTypes d'actions:")
    print("  Passe : Le robot va chercher la balle et la passe à un autre robot.")
    print("  Tir : Le robot va chercher la balle et tire au but.")
    print("  Blocage : Le robot se positionne pour bloquer un adversaire.")
    print("  Interception : Le robot calcule la trajectoire de la balle et tente de l'intercepter.")
    
    print("\nNavigation dans le programme:")
    print("  Menu principal : Permet de choisir les différentes fonctionnalités.")
    print("  Simulation : Permet de voir le comportement du robot étape par étape.")
    print("  Exportation : Permet de sauvegarder la FSM dans un fichier.")
    
    input("\nAppuyez sur Entrée pour revenir au menu principal...")

def simulate_fsm(fsm, action_type):
    """
    Simule l'exécution d'une FSM selon une séquence prédéfinie d'événements.
    """
    print(f"\nSimulation de la FSM pour: {action_type}")
    fsm.reset()  
    
   
    sequences = {
        "Passe": [
            ("NEAR_BALL", "GO_TO_BALL"),
            ("ALIGNED", "ALIGN"),
            ("BALL_KICKED", "PASS"),
            ("BALL_RECEIVED", "SUCCESS")  
        ],
        "Tir": [
            ("NEAR_BALL", "GO_TO_BALL"),
            ("ALIGNED", "ALIGN_GOAL"),
            ("BALL_KICKED", "SHOOT"),
            ("GOAL_SCORED", "GOAL")  
        ],
        "Blocage": [
            ("START", "CALCULATE_POSITION"),
            ("POSITION_CALCULATED", "GO_TO_POSITION"),
            ("POSITION_REACHED", "BLOCK"),
            ("BLOCKING_EFFECTIVE", "BLOCKING_SUCCESS")  
        ],
        "Interception": [
            ("START", "CALCULATE_TRAJECTORY"),
            ("TRAJECTORY_CALCULATED", "GO_TO_INTERCEPT_POSITION"),
            ("INTERCEPT_POSITION_REACHED", "INTERCEPT"),
            ("BALL_INTERCEPTED", "INTERCEPTION_SUCCESS")  
        ]
    }
    
    if "Passe" in action_type:
        sequence = sequences["Passe"]
    elif "Tir" in action_type:
        sequence = sequences["Tir"]
    elif "Blocage" in action_type:
        sequence = sequences["Blocage"]
    elif "Interception" in action_type:
        sequence = sequences["Interception"]
    else:
        sequence = sequences["Passe"]
    
    print("\nSéquence d'événements proposée:")
    for i, (event, next_state) in enumerate(sequence):
        print(f"{i+1}. {event} -> {next_state}")
    
    print("\nAppuyez sur Entrée pour progresser dans la simulation, ou tapez 'q' pour quitter.")
    
    for event, expected_state in sequence:
        input_val = input(f"\nAppuyez sur Entrée pour envoyer l'événement '{event}', ou tapez 'q' pour quitter: ")
        
        if input_val.lower() == 'q':
            print("Simulation arrêtée.")
            break
        
        print(f"Événement envoyé: {event}")
        
        random.seed(0)  
        
        print(f"État actuel: {fsm.current_state.name}")
        
        if fsm.current_state.name != expected_state:
            print(f"Note: La transition vers {expected_state} ne s'est pas produite comme prévu.")
            print("Cela peut être dû à la probabilité de transition ou à une condition incorrecte.")
            
            if input("Voulez-vous forcer la transition vers l'état attendu? (o/n): ").lower() == "o":
                if expected_state in fsm.states:
                    fsm.current_state = fsm.states[expected_state]
                    print(f"État actuel forcé à: {fsm.current_state.name}")
        
        if fsm.current_state.is_final:
            result = "Succès" if fsm.current_state.is_success else "Échec"
            print(f"Simulation terminée: {result}")
            break
    
    if not fsm.current_state.is_final:
        print("\nLa séquence d'événements est terminée, mais la FSM n'a pas atteint un état final.")
        
        final_states = [name for name, state in fsm.states.items() if state.is_final]
        
        if final_states and input("Voulez-vous forcer un état final? (o/n): ").lower() == "o":
            print("\nÉtats finaux disponibles:")
            for i, name in enumerate(final_states):
                state = fsm.states[name]
                result = "Succès" if state.is_success else "Échec"
                print(f"{i+1}. {name} ({result})")
            
            try:
                choice = int(input("\nChoisissez un état final: "))
                if 1 <= choice <= len(final_states):
                    fsm.current_state = fsm.states[final_states[choice-1]]
                    print(f"État final forcé à: {fsm.current_state.name}")
            except ValueError:
                print("Choix invalide.")
    
    print("\nHistorique des états:")
    print(" -> ".join(fsm.history + [fsm.current_state.name]))

def export_fsm_to_text(fsm, filename="fsm_export.txt"):
    """
    Exporte la FSM au format texte.
    """
    with open(filename, 'w') as f:
        f.write("=== Export de la Machine à États Finis ===\n\n")
        
        f.write("États:\n")
        for state_name, state in fsm.states.items():
            f.write(f"  - {state}\n")
            
            for i, transition in enumerate(state.transitions):
                f.write(f"    Transition {i+1} -> {transition.target_state.name} (Prob: {transition.probability})\n")
        
        f.write("\nÉtat initial: " + fsm.initial_state.name + "\n")
    
    print(f"FSM exportée avec succès dans le fichier '{filename}'")

def create_pass_fsm():
    """
    Alias pour create_simple_pass_fsm
    """
    return create_simple_pass_fsm()

def main():
    """Fonction principale du programme"""
    print("\n=== Système de planification d'actions robotiques pour RoboCup SSL ===")
    print("\nCe programme vous permet de générer et simuler des comportements robotiques")
    print("pour des matchs de football, en utilisant des machines à états finis (FSM).")
    print("\nChaque FSM représente une séquence d'actions qu'un robot peut exécuter,")
    print("comme aller vers la balle, s'aligner, passer, tirer, etc.")
    
    while True:
        print("\nMenu principal:")
        print("1. Générer une FSM à partir d'une instruction")
        print("2. Simuler une FSM prédéfinie")
        print("3. Exporter une FSM")
        print("4. Aide et glossaire")
        print("5. Quitter")
        
        choice = input("\nChoisissez une option: ")
        
        if choice == "1":
            instruction = get_instruction_with_help()
            fsm, action_desc = create_fsm_from_instruction(instruction)
            
            if fsm:
                display_fsm_with_explanation(fsm, action_desc)
                text_visualize_fsm(fsm)
                
                if input("\nVoulez-vous simuler cette FSM? (o/n): ").lower() == "o":
                    simulate_fsm(fsm, action_desc)
                
                if input("\nVoulez-vous exporter cette FSM? (o/n): ").lower() == "o":
                    filename = input("Nom du fichier d'exportation (défaut: fsm_export.txt): ")
                    if not filename:
                        filename = "fsm_export.txt"
                    export_fsm_to_text(fsm, filename)
            else:
                print(f"\n{action_desc}")
        
        elif choice == "2":
            print("\nChoisissez une FSM prédéfinie:")
            print("1. Passe entre robots")
            print("2. Tir au but")
            print("3. Blocage d'un robot adverse")
            print("4. Interception de la balle")
            
            fsm_choice = input("\nChoisissez une FSM: ")
            
            if fsm_choice == "1":
                fsm = create_simple_pass_fsm()
                action_desc = "Passe entre robots"
                display_fsm_with_explanation(fsm, action_desc)
                text_visualize_fsm(fsm)
                simulate_fsm(fsm, action_desc)
            elif fsm_choice == "2":
                fsm = create_shoot_fsm()
                action_desc = "Tir au but"
                display_fsm_with_explanation(fsm, action_desc)
                text_visualize_fsm(fsm)
                simulate_fsm(fsm, action_desc)
            elif fsm_choice == "3":
                fsm = create_block_fsm()
                action_desc = "Blocage d'un robot adverse"
                display_fsm_with_explanation(fsm, action_desc)
                text_visualize_fsm(fsm)
                simulate_fsm(fsm, action_desc)
            elif fsm_choice == "4":
                fsm = create_intercept_fsm()
                action_desc = "Interception de la balle"
                display_fsm_with_explanation(fsm, action_desc)
                text_visualize_fsm(fsm)
                simulate_fsm(fsm, action_desc)
            else:
                print("Choix invalide.")
        
        elif choice == "3":
            print("\nExporter une FSM:")
            print("1. Passe entre robots")
            print("2. Tir au but")
            print("3. Blocage d'un robot adverse")
            print("4. Interception de la balle")
            
            fsm_choice = input("\nChoisissez une FSM à exporter: ")
            
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
                print("Choix invalide.")
                continue
            
            filename = input("Nom du fichier d'exportation (défaut: fsm_export.txt): ")
            if not filename:
                filename = "fsm_export.txt"
            
            export_fsm_to_text(fsm, filename)
        
        elif choice == "4":
            show_help_and_glossary()
        
        elif choice == "5":
            print("Merci d'avoir utilisé le système de planification d'actions robotiques!")
            break
        
        else:
            print("Option non valide. Veuillez réessayer.")

if __name__ == "__main__":
    main()