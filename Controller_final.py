import pygame
from datetime import datetime

# Initialize Pygame
pygame.init()

# Set up the joystick
pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()

print("Press button 3 to exit and save the log...")

# Input log to store axis values with timestamps
input_log = []

running = True
try:
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Check if the window is closed
                running = False
            
            if event.type == pygame.JOYBUTTONDOWN:
                button_id = event.button
                
                # Exit and save log when button 3 is pressed
                if button_id == 1:
                    running = False
                    print("Button 1 pressed. Exiting and saving log...")
            
            elif event.type == pygame.JOYAXISMOTION:
                axis_id = event.axis
                axis_value = joystick.get_axis(axis_id)
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

                # Log only specific axes
                if axis_id == 4:  # Axis 4 for brakes
                    input_log.append((f"Brake (Axis {axis_id}) moved to {axis_value:.2f}", timestamp))
                    print(f"Brake (Axis {axis_id}) moved to {axis_value:.2f} at {timestamp}")
                
                elif axis_id == 5:  # Axis 5 for acceleration
                    input_log.append((f"Accelerator (Axis {axis_id}) moved to {axis_value:.2f}", timestamp))
                    print(f"Accelerator (Axis {axis_id}) moved to {axis_value:.2f} at {timestamp}")

                elif axis_id in [0, 1, 2]:  # Axis 0, 1, and 2 for left/right controls
                    input_log.append((f"Left/Right Control (Axis {axis_id}) moved to {axis_value:.2f}", timestamp))
                    print(f"Left/Right Control (Axis {axis_id}) moved to {axis_value:.2f} at {timestamp}")

except KeyboardInterrupt:
    print("Exiting...")

finally:
    # Save input_log to a file upon exit
    with open('input_log.txt', 'w') as f:
        for entry in input_log:
            f.write(f"{entry[0]} at {entry[1]}\n")
    pygame.quit()