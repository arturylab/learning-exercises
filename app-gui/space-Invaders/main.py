import math
import random
import os
import pygame
from pygame import mixer

# --- Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_SPEED = 5
ENEMY_INITIAL_SPEED_X = 3  # Initial X speed for enemy
ENEMY_Y_INCREMENT_ON_WALL_HIT = 40  # How much Y changes when enemy hits a side wall
NUM_OF_ENEMIES = 6
BULLET_SPEED = 10
FPS = 60  # Frames per second

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Asset filenames (assuming they are in the same directory as the script)
BACKGROUND_IMG_FILE = 'background.png'
UFO_ICON_IMG_FILE = 'ufo.png'
PLAYER_IMG_FILE = 'player.png'
ENEMY_IMG_FILE = 'enemy.png'
BULLET_IMG_FILE = 'bullet.png'
BACKGROUND_MUSIC_FILE = "background.wav"
LASER_SOUND_FILE = "laser.wav"
EXPLOSION_SOUND_FILE = "explosion.wav"
FONT_FILE = 'freesansbold.ttf'

# --- Global Variables ---
# script_dir will be set in the main execution block
script_dir = ""


# --- Asset Loading Functions ---
def load_image(filename, use_alpha=False):
    """Loads an image, converts it for performance, and handles errors."""
    path = os.path.join(script_dir, filename)
    try:
        image = pygame.image.load(path)
        if use_alpha:
            return image.convert_alpha()
        return image.convert()
    except pygame.error as e:
        print(f"Error loading image '{filename}': {e}")
        pygame.quit()
        exit()


def load_sound(filename):
    """Loads a sound and handles errors."""
    path = os.path.join(script_dir, filename)
    try:
        return mixer.Sound(path)
    except pygame.error as e:
        print(f"Error loading sound '{filename}': {e}")
        pygame.quit()
        exit()


def load_font(font_filename, size):
    """Loads a font and handles errors."""
    path = os.path.join(script_dir, font_filename)
    try:
        return pygame.font.Font(path, size)
    except pygame.error as e:
        print(f"Error loading font '{font_filename}': {e}")
        pygame.quit()
        exit()
    except FileNotFoundError:
        print(f"Font file not found: '{path}'")
        pygame.quit()
        exit()


# --- Game Object Classes ---
class Player(pygame.sprite.Sprite):
    """Represents the player spaceship."""
    def __init__(self, initial_x, initial_y, speed):
        super().__init__()
        self.image = load_image(PLAYER_IMG_FILE, use_alpha=True)
        self.rect = self.image.get_rect(topleft=(initial_x, initial_y))
        self.speed = speed
        self.x_change = 0

    def update(self):
        """Updates the player's position based on x_change."""
        self.rect.x += self.x_change
        # Keep player within screen boundaries
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

    def draw(self, surface):
        """Draws the player on the given surface."""
        surface.blit(self.image, self.rect)


class Enemy(pygame.sprite.Sprite):
    """Represents an enemy alien."""
    def __init__(self, initial_x, initial_y, initial_x_speed, y_increment):
        super().__init__()
        self.image = load_image(ENEMY_IMG_FILE, use_alpha=True)
        self.rect = self.image.get_rect(topleft=(initial_x, initial_y))
        self.x_speed = initial_x_speed
        self.base_x_speed = abs(initial_x_speed) # To maintain speed magnitude
        self.y_increment = y_increment

    def update(self):
        """Updates the enemy's position and handles wall collisions."""
        self.rect.x += self.x_speed
        # Enemy wall collision logic
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.x_speed *= -1  # Reverse horizontal direction
            self.rect.y += self.y_increment # Move down
            # Ensure enemy doesn't get stuck by moving one step in new direction
            self.rect.x += self.x_speed


    def reset_position(self):
        """Resets the enemy to a new random position at the top."""
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(50, 150)
        # Optionally, randomize direction upon reset
        self.x_speed = self.base_x_speed if random.random() < 0.5 else -self.base_x_speed


    def draw(self, surface):
        """Draws the enemy on the given surface."""
        surface.blit(self.image, self.rect)


class Bullet(pygame.sprite.Sprite):
    """Represents a bullet fired by the player."""
    def __init__(self, speed, fire_sound_path):
        super().__init__()
        self.image = load_image(BULLET_IMG_FILE, use_alpha=True)
        self.rect = self.image.get_rect()
        self.speed = speed
        self.state = "ready"  # "ready" (not on screen) or "fire" (moving)
        try:
            self.fire_sound = load_sound(fire_sound_path)
        except Exception as e: # Catch if sound loading fails specifically here
            print(f"Could not load bullet fire sound: {e}")
            self.fire_sound = None


    def fire(self, player_center_x, player_top_y):
        """Fires the bullet from the player's position if it's ready."""
        if self.state == "ready":
            if self.fire_sound:
                self.fire_sound.play()
            self.rect.centerx = player_center_x
            self.rect.bottom = player_top_y  # Bullet appears from top of player
            self.state = "fire"

    def update(self):
        """Moves the bullet upwards if it's in 'fire' state."""
        if self.state == "fire":
            self.rect.y -= self.speed
            # Reset bullet if it goes off-screen
            if self.rect.bottom < 0:
                self.state = "ready"

    def draw(self, surface):
        """Draws the bullet on the surface if it's in 'fire' state."""
        if self.state == "fire":
            surface.blit(self.image, self.rect)


# --- UI Functions ---
def show_score(surface, font, current_score, x, y):
    """Renders and displays the current score."""
    score_render = font.render(f"Score : {current_score}", True, WHITE)
    surface.blit(score_render, (x, y))


def display_game_over_text(surface, font):
    """Renders and displays the 'GAME OVER' message."""
    game_over_render = font.render("GAME OVER", True, WHITE)
    # Center the text on the screen
    text_rect = game_over_render.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
    surface.blit(game_over_render, text_rect)


# --- Main Game Function ---
def game_loop():
    """Main function to run the Space Invaders game."""
    global script_dir # Allow modification of global script_dir

    # Determine the script directory (works even if run from elsewhere)
    try:
        # If run as a script, __file__ is defined
        script_dir = os.path.dirname(os.path.abspath(__file__))
    except NameError:
        # If __file__ is not defined (e.g., in an interactive session or frozen app)
        script_dir = os.path.abspath(".")

    # Initialize Pygame modules
    pygame.init()
    mixer.init()  # Initialize the sound mixer

    # Create the game screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Space Invader")
    try:
        icon = load_image(UFO_ICON_IMG_FILE, use_alpha=True)
        pygame.display.set_icon(icon)
    except Exception as e:
        print(f"Could not load or set icon: {e}")


    clock = pygame.time.Clock() # For controlling FPS

    # Load game assets
    background_image = load_image(BACKGROUND_IMG_FILE)
    try:
        mixer.music.load(os.path.join(script_dir, BACKGROUND_MUSIC_FILE))
        mixer.music.play(-1)  # Play background music indefinitely
    except pygame.error as e:
        print(f"Error loading/playing background music: {e}")
        # Game can continue without music

    explosion_sound = load_sound(EXPLOSION_SOUND_FILE)
    score_font = load_font(FONT_FILE, 32)
    game_over_font = load_font(FONT_FILE, 64)

    # Create game objects
    player_initial_x = (SCREEN_WIDTH / 2) - (load_image(PLAYER_IMG_FILE).get_width() / 2)
    player_initial_y = SCREEN_HEIGHT - 100 # A bit above the bottom
    player = Player(player_initial_x, player_initial_y, PLAYER_SPEED)

    bullet = Bullet(BULLET_SPEED, LASER_SOUND_FILE)

    enemies = pygame.sprite.Group() # Group to manage all enemy sprites
    for _ in range(NUM_OF_ENEMIES):
        enemy_start_x = random.randint(0, SCREEN_WIDTH - load_image(ENEMY_IMG_FILE).get_width())
        enemy_start_y = random.randint(50, 150)
        # Randomize initial horizontal direction for enemies
        initial_enemy_speed = ENEMY_INITIAL_SPEED_X if random.random() < 0.5 else -ENEMY_INITIAL_SPEED_X
        enemy = Enemy(enemy_start_x, enemy_start_y, initial_enemy_speed, ENEMY_Y_INCREMENT_ON_WALL_HIT)
        enemies.add(enemy)

    # Game variables
    current_score = 0
    running = True
    game_over_state = False

    # --- Main Game Loop ---
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if not game_over_state: # Only process game input if not game over
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        player.x_change = -player.speed
                    if event.key == pygame.K_RIGHT:
                        player.x_change = player.speed
                    if event.key == pygame.K_SPACE:
                        bullet.fire(player.rect.centerx, player.rect.top)
                
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT and player.x_change < 0:
                        player.x_change = 0 # Stop movement if left key is released
                    if event.key == pygame.K_RIGHT and player.x_change > 0:
                        player.x_change = 0 # Stop movement if right key is released

        if not game_over_state:
            # Update game objects
            player.update()
            enemies.update()  # Calls update() on all Enemy sprites in the group
            bullet.update()

            # Collision detection: bullet with enemies
            if bullet.state == "fire":
                # pygame.sprite.spritecollide(sprite, group, dokill)
                # dokill=False means enemy is not automatically removed from group
                hit_enemies_list = pygame.sprite.spritecollide(bullet, enemies, False)
                for enemy_hit in hit_enemies_list:
                    if explosion_sound:
                        explosion_sound.play()
                    current_score += 1
                    enemy_hit.reset_position() # Reset this enemy's position
                    bullet.state = "ready"    # Reset bullet state
                    # Move bullet off-screen effectively until next fire
                    bullet.rect.y = SCREEN_HEIGHT + bullet.rect.height 
                    break # Bullet hits only one enemy per frame

            # Game Over condition: if any enemy reaches near the bottom
            for enemy_obj in enemies:
                if enemy_obj.rect.top > 440: # Original game over Y-threshold
                    game_over_state = True
                    mixer.music.stop()
                    break 
            
            if game_over_state:
                # Clear enemies or make them inactive
                for enemy_obj in enemies:
                    enemy_obj.kill() # Removes sprite from all groups it's in

        # --- Drawing ---
        screen.blit(background_image, (0, 0)) # Draw background first

        player.draw(screen)
        enemies.draw(screen) # Draws all Enemy sprites in the group
        bullet.draw(screen)  # Bullet's draw method handles if it's visible

        show_score(screen, score_font, current_score, 10, 10)

        if game_over_state:
            display_game_over_text(screen, game_over_font)

        pygame.display.flip() # Update the full display surface to the screen
        clock.tick(FPS)       # Control the game speed

    pygame.quit() # Uninitialize Pygame modules
    # exit() # Not strictly necessary after pygame.quit()

# --- Script Execution ---
if __name__ == '__main__':
    game_loop()
