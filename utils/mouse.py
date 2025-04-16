import pyautogui
import random
import time
import math

def human_move_to(x_target, y_target, duration=0.4, final_adjustment=True):
    x_start, y_start = pyautogui.position()
    steps = max(10, int(duration * 60))

    # Random curve offset parameters
    curve_strength = random.uniform(0.2, 0.5)  # 0 = straight, higher = more curve
    direction = random.choice([-1, 1])  # curve up/down or left/right
    max_arc_amplitude = random.uniform(100, 500)  # how far the arc goes out

    for step in range(steps):
        t = step / steps
        smooth_t = t * t * (3 - 2 * t)  # Smoothstep

        # Basic linear interpolation
        x = x_start + (x_target - x_start) * smooth_t
        y = y_start + (y_target - y_start) * smooth_t

        # Add curve – simulate arc using a sine wave perpendicular to direction
        arc_offset = math.sin(smooth_t * math.pi) * curve_strength * max_arc_amplitude

        # Rotate arc to be perpendicular to movement direction
        dx = x_target - x_start
        dy = y_target - y_start
        length = math.hypot(dx, dy)
        if length == 0:
            perp_x, perp_y = 0, 0
        else:
            perp_x = -dy / length * arc_offset * direction
            perp_y = dx / length * arc_offset * direction

        final_x = int(x + perp_x + random.uniform(-1, 1))
        final_y = int(y + perp_y + random.uniform(-1, 1))

        pyautogui.moveTo(final_x, final_y, duration=0.01)

    if final_adjustment:
        pyautogui.moveTo(
            x_target + random.uniform(-1, 1),
            y_target + random.uniform(-1, 1),
            duration=random.uniform(0.01, 0.03)
        )

def human_click(x, y, offset_range=5):
    offset_x = random.randint(-offset_range, offset_range)
    offset_y = random.randint(-offset_range, offset_range)
    human_move_to(x + offset_x, y + offset_y, duration=random.uniform(0.3, 0.6))
    time.sleep(random.uniform(0.05, 0.2))
    pyautogui.click()

def human_move_offscreen():
    screen_width, screen_height = pyautogui.size()
    y = screen_height // 2 + random.randint(-100, 100)
    x_target = random.choice([20, screen_width - 20])
    human_move_to(x_target, y, duration=random.uniform(0.4, 0.7), final_adjustment=False)

def human_scroll(clicks: int):
    """
    Scrolls the mouse wheel with slight human-like delay.
    Positive clicks scroll up, negative scroll down.
    """
    delay = random.uniform(0.1, 0.3)
    pyautogui.scroll(clicks)
    time.sleep(delay)


