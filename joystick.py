import pygame
from datetime import datetime

# Initialize Pygame
pygame.init()

# Set up the joystick
pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()

print("Press buttons on your controller or ESC to exit...")

# Input log to store button presses and axis values with timestamps
input_log = []

running = True
try:
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Check if the window is closed
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Check for ESC key
                    running = False
            
            if event.type == pygame.JOYBUTTONDOWN:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                button_id = event.button
                input_log.append((f"Button {button_id} pressed", timestamp))
                print(f"Button {button_id} pressed at {timestamp}")

            elif event.type == pygame.JOYAXISMOTION:
                axis_id = event.axis
                axis_value = joystick.get_axis(axis_id)
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                input_log.append((f"Axis {axis_id} moved to {axis_value:.2f}", timestamp))
                print(f"Axis {axis_id} moved to {axis_value:.2f} at {timestamp}")

            # Check for specific buttons for acceleration and braking
            if joystick.get_button(1):  # Assuming button 1 is for acceleration
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                input_log.append(("Accelerating", timestamp))
                print(f"Accelerating at {timestamp}")

            if joystick.get_button(2):  # Assuming button 2 is for braking
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                input_log.append(("Braking", timestamp))
                print(f"Braking at {timestamp}")

except KeyboardInterrupt:
    print("Exiting...")

finally:
    # Optionally save input_log to a file or process it further
    with open('input_log.txt', 'w') as f:
        for entry in input_log:
            f.write(f"{entry[0]} at {entry[1]}\n")
    pygame.quit()