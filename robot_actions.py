def go_to_ball(robot):
    """Le robot se déplace vers la balle"""
    print(f"Robot {robot} se déplace vers la balle")
    return True

def align_with_target(robot, target):
    """Le robot s'aligne avec la cible (but ou autre robot)"""
    print(f"Robot {robot} s'aligne avec {target}")
    return True

def kick_ball(robot, power=1.0):
    """Le robot frappe la balle"""
    print(f"Robot {robot} frappe la balle avec une puissance de {power}")
    return True

def pass_ball(robot, target_robot):
    """Le robot passe la balle à un autre robot"""
    print(f"Robot {robot} passe la balle à {target_robot}")
    return True

def block_robot(robot, target_robot):
    """Le robot bloque un robot adverse"""
    print(f"Robot {robot} bloque {target_robot}")
    return True

def is_near_ball(event):
    """Vérifie si le robot est près de la balle"""
    return event == "NEAR_BALL"

def is_aligned(event):
    """Vérifie si le robot est aligné avec sa cible"""
    return event == "ALIGNED"

def ball_kicked(event):
    """Vérifie si la balle a été frappée"""
    return event == "BALL_KICKED"

def ball_received(event):
    """Vérifie si la balle a été reçue"""
    return event == "BALL_RECEIVED"