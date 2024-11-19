import pygame
from datetime import datetime

# Initialize Pygame
pygame.init()
pygame.joystick.init()

joystick = pygame.joystick.Joystick(0)
joystick.init()

input_log = []

print("Press buttons on your controller...")

try:
    while True:
        for event in pygame.event.get():
            if event.type == pygame.JOYBUTTONDOWN:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                button_id = event.button
                input_log.append((button_id, timestamp))
                print(f"Button {button_id} pressed at {timestamp}")

except KeyboardInterrupt:
    print("Exiting...")
finally:
    # Optionally save input_log to a file or process it further
    with open('input_log.txt', 'w') as f:
        for entry in input_log:
            f.write(f"Button {entry[0]} pressed at {entry[1]}\n")
    pygame.quit()