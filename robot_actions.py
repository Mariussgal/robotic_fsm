def go_to_ball(robot):
    """Robot moves towards the ball"""
    print(f"Robot {robot} moves towards the ball")
    return True

def align_with_target(robot, target):
    """Robot aligns with the target (goal or other robot)"""
    print(f"Robot {robot} aligns with {target}")
    return True

def kick_ball(robot, power=1.0):
    """Robot kicks the ball"""
    print(f"Robot {robot} kicks the ball with power {power}")
    return True

def pass_ball(robot, target_robot):
    """Robot passes the ball to another robot"""
    print(f"Robot {robot} passes the ball to {target_robot}")
    return True

def block_robot(robot, target_robot):
    """Robot blocks an opponent robot"""
    print(f"Robot {robot} blocks {target_robot}")
    return True

def is_near_ball(event):
    """Check if the robot is near the ball"""
    return event == "NEAR_BALL"

def is_aligned(event):
    """Check if the robot is aligned with its target"""
    return event == "ALIGNED"

def ball_kicked(event):
    """Check if the ball has been kicked"""
    return event == "BALL_KICKED"

def ball_received(event):
    """Check if the ball has been received"""
    return event == "BALL_RECEIVED"