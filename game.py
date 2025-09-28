import pygame
import time
import sys
import component
import config
import threading
import cv2
import mediapipe as mp
from gesture_identify import classify_hand

class GestureDetector:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5,
            max_num_hands=1
        )
        self.mp_drawing = mp.solutions.drawing_utils
        self.cap = cv2.VideoCapture(0)
        self.current_gesture = "None"
        self.running = False
        
    def start_detection(self):
        self.running = True
        def detect_loop():
            while self.running:
                ret, frame = self.cap.read()
                if not ret:
                    continue
                    
                frame = cv2.resize(frame, (640, 480))
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = self.hands.process(rgb_frame)
                
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        landmarks = []
                        for id, pt in enumerate(hand_landmarks.landmark):
                            x = int(pt.x * 640)
                            y = int(pt.y * 480)
                            landmarks.append([id, x, y])
                        
                        gesture = classify_hand(landmarks)
                        self.current_gesture = gesture
                else:
                    self.current_gesture = "None"
                    
                time.sleep(0.1)  
        
        detection_thread = threading.Thread(target=detect_loop)
        detection_thread.daemon = True
        detection_thread.start()
    
    def stop_detection(self):
        self.running = False
        self.cap.release()
        cv2.destroyAllWindows()

class ReactionGame:

    def __init__(self):
        self.screen = config.screen
        self.pointing_to = -1
        self.sword = True
        self.amulet = False
        self.shield = False
        self.eyeball = False
        self.gesture_detector = GestureDetector()
        self.gesture_detector.start_detection()

    SetHealth = pygame.event.custom_type()
    SetGesture = pygame.event.custom_type()

    def set_health(self, health):
        health_event = pygame.event.Event(self.SetHealth, health = health)
        pygame.event.post(health_event)
    
    def set_gesture(self, gesture):
        gesture_event = pygame.event.Event(self.SetGesture, gesture = gesture)
        pygame.event.post(gesture_event)

    def preparation_scene(self):
        def quit_game():
            self.gesture_detector.stop_detection()
            pygame.quit()
            sys.exit()

        preparation_image = component.load_preparation_image()
        config.screen.blit(preparation_image, (0, 0))
        pygame.display.flip()

        level1_button = component.Button("Level 1", [313, 259], self.level1)
        level2_button = component.Button("Level 2", [281, 207], self.level2)
        level3_button = component.Button("Level 3", [321, 124], self.level3)
        level4_button = component.Button("Level 4", [270, 46], self.level4)

        level1_button.draw(config.screen)
        level2_button.draw(config.screen)
        level3_button.draw(config.screen)
        level4_button.draw(config.screen)

        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit_game()
                elif event.type == pygame.MOUSEMOTION:
                    x = event.pos[0]
                    y = event.pos[1]
                    if (x > 280 and x < 346 and y > 240 and y < 278): # Level 1
                        self.pointing_to = 1
                    elif (x > 248 and x < 314 and y > 188 and y < 226): # Level 2
                        self.pointing_to = 2
                    elif (x > 288 and x < 354 and y > 105 and y < 143): # Level 3
                        self.pointing_to = 3
                    elif (x > 237 and x < 303 and y > 27 and y < 65): # Level 4
                        self.pointing_to = 4
                    else:
                        config.screen.blit(preparation_image, (0, 0))
                        level1_button.draw(config.screen)
                        level2_button.draw(config.screen)
                        level3_button.draw(config.screen)
                        level4_button.draw(config.screen)

                    if self.pointing_to == 1:
                        pygame.draw.circle(self.screen, (255,255,255), [313, 259], 30, width=3)
                    elif self.pointing_to == 2:
                        pygame.draw.circle(self.screen, (255,255,255), [281, 207], 30, width=3)
                    elif self.pointing_to == 3:
                        pygame.draw.circle(self.screen, (255,255,255), [321, 124], 30, width=3)
                    elif self.pointing_to == 4:
                        pygame.draw.circle(self.screen, (255,255,255), [270, 46], 30, width=3)
                    else:
                        config.screen.blit(preparation_image, (0, 0))
                        pygame.display.flip()
                level1_button.is_clicked(event)
                level2_button.is_clicked(event)
                level3_button.is_clicked(event)
                level4_button.is_clicked(event)
                    
            pygame.display.update()

    def level1(self):
        print("Level 1")
        
        if not hasattr(self.gesture_detector, 'running') or not self.gesture_detector.running:
            self.gesture_detector.start_detection()
            print("Gesture Detection Activate")

        self.gesture_stability_counter = 0
        self.confirmed_gesture = "None"
        self.gesture_lock_time = 500 

        def init():
            self.health = 5
            self.gesture = "None"
            self.objects = []
            self.spawn_times = [item[1] * 1000 for item in config.Level1Recipe]
            self.spawn_index = 0
            self.enemy_health = 10
            self.level_start_time = pygame.time.get_ticks()

        def updateVisual():
            # Adjust positions to fit within screen (400x600)
            config.screen.blit(component.level1_image, (0, 0))  # Move to (0,0) instead of (550,0)
            component.HealthStatusBar().draw(config.screen, self.health)
            component.GestureStatusBar().draw(config.screen, self.gesture)
            component.EnemyHealthStatusBar().draw(config.screen, self.enemy_health)
            component.TuneBoard().draw(config.screen)  # tune.jpg at (0,0), may overlap with level1_image
            # Adjust Enemy position to be visible, e.g., (200,100) instead of (550,100)
            enemy = component.Enemy((200, 100))  # Create instance with adjusted position
            enemy.draw(config.screen)
            for obj in self.objects:
                obj.draw(config.screen)
            pygame.display.flip()

        def checkwin():
            if self.health <= 0:
                print("You lose")
                self.spawn_index = 0
                self.objects = []
                self.gesture_detector.stop_detection()
                # Re-initialize the gesture detector for the next game
                self.gesture_detector = GestureDetector()
                self.preparation_scene()
            if self.enemy_health <= 0:
                print("You win !")
                print(" You have unlocked the amulet ")
                self.amulet = True
                self.spawn_index = 0
                self.objects = []
                self.gesture_detector.stop_detection()
                # Re-initialize the gesture detector for the next game
                self.gesture_detector = GestureDetector()
                self.preparation_scene()

        init()
        last_update_time = pygame.time.get_ticks()

        while True:
            current_time = pygame.time.get_ticks()
            if current_time - last_update_time > config.Level1UpdateFreq:
                for obj in self.objects:
                    obj.move(10)
                    if obj.rect.y > 830:
                        self.objects.remove(obj)
                        if obj.__class__.__name__ == "Sword":
                            if self.gesture == "Sword":
                                self.enemy_health -= 1
                                print(f"Correct Sword! Enemy Health -1 (Enemy Health: {self.enemy_health})")
                            else:
                                self.health -= 1
                                print(f"Incorrect Gesture! Sword required, but detected {self.gesture}, player health -1 (remained: {self.health})")
                        elif obj.__class__.__name__ == "Fist":
                            if self.gesture == "Fist":
                                self.enemy_health -= 1
                                print(f"Correct Fist! Enemy Health -1 (Enemy Health: {self.enemy_health})")
                            else:
                                self.health -= 1
                                print(f"Incorrect Gesture! Fist required, but detected {self.gesture}, player health -1 (remained: {self.health})")
                        elif obj.__class__.__name__ == "Shield":
                            if self.gesture == "Shield":
                                self.enemy_health -= 1
                                print(f"Correct Shield! Enemy Health -1 (Enemy Health: {self.enemy_health})")
                            else:
                                self.health -= 1
                                print(f"Incorrect Gesture! Shield required, but detected {self.gesture}, player health -1 (remained: {self.health})")
                        checkwin()
                last_update_time = current_time

            if self.spawn_index < len(self.spawn_times) and current_time - self.level_start_time >= self.spawn_times[self.spawn_index]:
                item = config.Level1Recipe[self.spawn_index]
                if item[0] == "sword":
                    self.objects.append(component.Sword((300, 0)))
                    print("Sword")
                elif item[0] == "fist":
                    self.objects.append(component.Fist((300, 0)))
                    print("Fist")
                elif item[0] == "shield":
                    self.objects.append(component.Shield((300, 0)))
                    print("shield")
                self.spawn_index += 1

            detected_gesture = self.gesture_detector.current_gesture

            # Improve consistency
            if detected_gesture == self.confirmed_gesture:
                self.gesture_stability_counter += 1
                if self.gesture_stability_counter >= 3: 
                    mapped_gesture = "None"
                    if detected_gesture == "scissor":
                        mapped_gesture = "Sword"
                    elif detected_gesture == "fist":
                        mapped_gesture = "Fist"
                    elif detected_gesture == "paper":  
                        mapped_gesture = "Shield"
                    
                    if self.gesture != mapped_gesture:
                        self.gesture = mapped_gesture
                        print(f"Gesture: {detected_gesture} -> {mapped_gesture}")
            else:
                self.gesture_stability_counter = 0
                self.confirmed_gesture = detected_gesture

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.gesture_detector.stop_detection()
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        self.gesture = "Sword"
                        print("keyboard: Sword")
                    if event.key == pygame.K_f:
                        self.gesture = "Fist"
                        print("keyboard: Fist")
                    if event.key == pygame.K_h:
                        self.gesture = "Shield"
                        print("keyboard: Shield")

            updateVisual()
            pygame.display.update()

    def level2(self):
        print("Level 2")

        def init():
            self.health = 5
            self.gesture = "None"
            self.objects = []
            self.spawn_times = [item[1] * 1000 for item in config.Level2Recipe]  # Convert seconds to milliseconds
            self.spawn_index = 0
            self.enemy_health = 10
            self.level_start_time = pygame.time.get_ticks()  # Record the start time of the level

        def updateVisual():
            config.screen.blit(component.level1_image, (550, 0))
            component.HealthStatusBar().draw(config.screen, self.health)
            component.GestureStatusBar().draw(config.screen, self.gesture)
            component.EnemyHealthStatusBar().draw(config.screen, self.enemy_health)
            component.TuneBoard().draw(config.screen)
            component.Enemy().draw(config.screen)
            for obj in self.objects:
                obj.draw(config.screen)
            pygame.display.flip()

        def checkwin():
            if self.health <= 0:
                print("You lose")
                self.spawn_index = 0
                self.objects = []
                self.gesture_detector.stop_detection()
                # Re-initialize the gesture detector for the next game
                self.gesture_detector = GestureDetector()
                self.preparation_scene()
            if self.enemy_health <= 0:
                print("You win !")
                print(" You have unlocked the amulet ")
                self.amulet = True
                self.spawn_index = 0
                self.objects = []
                self.gesture_detector.stop_detection()
                # Re-initialize the gesture detector for the next game
                self.gesture_detector = GestureDetector()
                self.preparation_scene()

        init()
        last_update_time = pygame.time.get_ticks()  # Reset last update time when the level starts

        while True:
            current_time = pygame.time.get_ticks()
            if current_time - last_update_time > config.Level2UpdateFreq:
                for obj in self.objects:
                    obj.move(10)
                    if obj.rect.y > 830:
                        self.objects.remove(obj)
                        if obj.__class__.__name__ == "Sword":
                            if self.gesture == "Sword":
                                self.enemy_health -= 1
                            else:
                                self.health -= 1
                        elif obj.__class__.__name__ == "Fist":
                            if self.gesture == "Fist":
                                self.enemy_health -= 1
                            else:
                                self.health -= 1
                        elif obj.__class__.__name__ == "ok":
                            if self.gesture == "Ok":
                                self.enemy_health -= 1
                            else:
                                self.health -= 1
                        elif obj.__class__.__name__ == "Shield":
                            if self.gesture == "Shield":
                                self.enemy_health -= 1
                            else:
                                self.health -= 1
                        checkwin()
                last_update_time = current_time

            if self.spawn_index < len(self.spawn_times) and current_time - self.level_start_time >= self.spawn_times[self.spawn_index]:
                item = config.Level2Recipe[self.spawn_index]
                if item[0] == "sword":
                    self.objects.append(component.Sword((300, 0)))
                    print("Sword")
                elif item[0] == "fist":
                    self.objects.append(component.Fist((300, 0)))
                    print("Fist")
                elif item[0] == "ok":
                    self.objects.append(component.ok((300, 0)))
                    print("Ok")
                elif item[0] == "shield":
                    self.objects.append(component.Shield((300, 0)))
                    print("Shield")
                self.spawn_index += 1

            detected_gesture = self.gesture_detector.current_gesture
            if detected_gesture == "scissor":
                self.gesture = "Sword"
            elif detected_gesture == "fist":
                self.gesture = "Fist"
            elif detected_gesture == "paper":
                self.gesture = "Shield"
            else:
                self.gesture = "None"

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.gesture_detector.stop_detection()
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEMOTION:
                    print(event.pos)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        self.gesture = "Sword"
                    if event.key == pygame.K_f:
                        self.gesture = "Fist"
                    if event.key == pygame.K_o:
                        self.gesture = "Ok"
                    if event.key == pygame.K_b:
                        self.gesture = "Shield"

            updateVisual()
            pygame.display.update()

    def level3(self):
        print("Level 3")
    def level4(self):
        print("Level 4")