import pygame
while True:
        # EVENT PROCESSING STEP
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                done=True # Flag that we are done so we exit this loop
            
            # Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
            if event.type == pygame.JOYBUTTONDOWN:
                print("Joystick button pressed.")
                
            if event.type == pygame.JOYBUTTONUP:
                print("Joystick button released.")

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    print("UP")
                if event.key == pygame.K_DOWN:
                    print("DOWN")
                if event.key == pygame.K_RIGHT:
                    print("RIGHT")
                if event.key == pygame.K_LEFT:
                    print("LEFT")
                if event.key == pygame.K_a:
                    print("A")
                if event.key == pygame.K_s:
                    print("S")
                if event.key == pygame.K_d:
                    print("D")
                if event.key == pygame.K_d:
                    print("W")