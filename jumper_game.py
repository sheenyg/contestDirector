#!/usr/bin/env python3
"""
Jumper Game

A simple 2D game where a player character jumps to avoid incoming obstacles.
The game features increasing difficulty and score tracking.

Dependencies:
- Python 3.x
- Pygame (install with: pip install pygame)
- Actually we need more dependencies 
- Would this maybe
- Create a merge conflict

Controls:
- SPACE: Jump
- R: Restart after game over
- ESC: Quit game

Run the game by executing this script:
    python jumper_game.py
"""

import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
GROUND_HEIGHT = 50
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (100, 100, 100)

# Set up the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jumper Game")
clock = pygame.time.Clock()

class Player:
    """
    Player character that can jump to avoid obstacles.
    """
    def __init__(self):
        self.width = 40
        self.height = 60
        self.x = 100
        self.y = SCREEN_HEIGHT - GROUND_HEIGHT - self.height
        self.y_velocity = 0
        self.jump_strength = -15
        self.gravity = 0.8
        self.is_jumping = False
        self.color = BLUE

    def jump(self):
        """Initiate a jump if the player is on the ground"""
        if not self.is_jumping:
            self.y_velocity = self.jump_strength
            self.is_jumping = True

    def update(self):
        """Update player's position and velocity"""
        # Apply gravity
        self.y_velocity += self.gravity
        self.y += self.y_velocity

        # Check if player has landed
        ground_level = SCREEN_HEIGHT - GROUND_HEIGHT - self.height
        if self.y >= ground_level:
            self.y = ground_level
            self.y_velocity = 0
            self.is_jumping = False

    def draw(self):
        """Draw the player on the screen"""
        pygame.draw.rect(screen, self.color, 
                        (self.x, self.y, self.width, self.height))

    def get_rect(self):
        """Return a pygame Rect object for collision detection"""
        return pygame.Rect(self.x, self.y, self.width, self.height)


class Obstacle:
    """
    Obstacles that the player must avoid by jumping over them.
    """
    def __init__(self, speed):
        self.width = random.randint(20, 50)
        self.height = random.randint(30, 70)
        self.x = SCREEN_WIDTH
        self.y = SCREEN_HEIGHT - GROUND_HEIGHT - self.height
        self.speed = speed
        self.color = RED

    def update(self):
        """Move the obstacle from right to left"""
        self.x -= self.speed

    def draw(self):
        """Draw the obstacle on the screen"""
        pygame.draw.rect(screen, self.color, 
                        (self.x, self.y, self.width, self.height))

    def get_rect(self):
        """Return a pygame Rect object for collision detection"""
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def is_off_screen(self):
        """Check if the obstacle has moved off the screen"""
        return self.x < -self.width


class Game:
    """
    Main game class that manages the game state, scoring, and difficulty.
    """
    def __init__(self):
        self.player = Player()
        self.obstacles = []
        self.score = 0
        self.game_speed = 5
        self.obstacle_frequency = 1500  # milliseconds
        self.last_obstacle_time = 0
        self.game_over = False
        self.font = pygame.font.SysFont(None, 36)

    def spawn_obstacle(self):
        """Create a new obstacle and add it to the list"""
        self.obstacles.append(Obstacle(self.game_speed))

    def update(self):
        """Update game state including player, obstacles, and scoring"""
        if not self.game_over:
            # Update player
            self.player.update()
            
            # Update obstacles and check for collisions
            for obstacle in self.obstacles[:]:
                obstacle.update()
                
                # Check for collision
                if self.player.get_rect().colliderect(obstacle.get_rect()):
                    self.game_over = True
                
                # Remove obstacles that have gone off screen and increase score
                if obstacle.is_off_screen():
                    self.obstacles.remove(obstacle)
                    self.score += 1
                    
                    # Increase game speed gradually
                    if self.score % 5 == 0:
                        self.game_speed += 0.5
                        self.obstacle_frequency = max(500, self.obstacle_frequency - 100)
            
            # Spawn new obstacles based on time
            current_time = pygame.time.get_ticks()
            if current_time - self.last_obstacle_time > self.obstacle_frequency:
                self.spawn_obstacle()
                self.last_obstacle_time = current_time

    def draw(self):
        """Draw all game elements to the screen"""
        # Clear the screen
        screen.fill(WHITE)
        
        # Draw the ground
        pygame.draw.rect(screen, GRAY, (0, SCREEN_HEIGHT - GROUND_HEIGHT, 
                                       SCREEN_WIDTH, GROUND_HEIGHT))
        
        # Draw the player
        self.player.draw()
        
        # Draw obstacles
        for obstacle in self.obstacles:
            obstacle.draw()
        
        # Draw the score
        score_text = self.font.render(f"Score: {self.score}", True, BLACK)
        screen.blit(score_text, (20, 20))
        
        # Display game over message if applicable
        if self.game_over:
            game_over_text = self.font.render("GAME OVER - Press R to Restart", True, RED)
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(game_over_text, text_rect)
        
        # Update the display
        pygame.display.flip()

    def reset(self):
        """Reset the game to its initial state"""
        self.__init__()


def main():
    """Main function to run the game"""
    game = Game()
    
    # Game loop
    running = True
    while running:
        # Process events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    game.player.jump()
                elif event.key == pygame.K_r and game.game_over:
                    game.reset()
        
        # Update game state
        game.update()
        
        # Draw everything
        game.draw()
        
        # Control game speed
        clock.tick(FPS)
    
    # Clean up
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
