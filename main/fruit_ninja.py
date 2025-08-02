import pygame
import os
import random
import sys

# Initialize pygame and set up display
pygame.init()
pygame.font.init()  # Initialize font module explicitly
WIDTH, HEIGHT = 800, 600  # Set screen dimensions
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fruit Ninja Game")
clock = pygame.time.Clock()

LIVES_START = 7  # Set starting lives to 7
FRUIT_SIZE = (80, 80)  # Consistent fruit size

def load_image(name, size=None):
    try:
        img = pygame.image.load(os.path.join("assets", name)).convert_alpha()
        if size:
            img = pygame.transform.smoothscale(img, size)
        return img
    except:
        print(f"Could not load image: {name}")
        surf = pygame.Surface(size if size else (50, 50))
        surf.fill((200, 200, 200))
        return surf

# Load background and scale to fit window
background = pygame.transform.scale(load_image("background.jpg"), (WIDTH, HEIGHT))

# Load fruits (scaled)
apple_img = load_image("apple_small.png", FRUIT_SIZE)
banana_img = load_image("banana.png", FRUIT_SIZE)
orange_img = load_image("orange_small.png", FRUIT_SIZE)
pineapple_img = load_image("pineapple_small.png", FRUIT_SIZE)
watermelon_img = load_image("watermelon_small.png", FRUIT_SIZE)
coconut_img = load_image("coconut.png", FRUIT_SIZE)
bomb_img = load_image("bomb_small.png", FRUIT_SIZE)

# Load sliced fruits (scaled)
apple_half_1 = load_image("apple_half_1_small.png", FRUIT_SIZE)
apple_half_2 = load_image("apple_half_2_small.png", FRUIT_SIZE)
banana_half_1 = load_image("banana_half_1_small.png", FRUIT_SIZE)
banana_half_2 = load_image("banana_half_2_small.png", FRUIT_SIZE)
orange_half_1 = load_image("orange_half_1_small.png", FRUIT_SIZE)
orange_half_2 = load_image("orange_half_2_small.png", FRUIT_SIZE)
pineapple_half_1 = load_image("pineapple_half_1_small.png", FRUIT_SIZE)
pineapple_half_2 = load_image("pineapple_half_2_small.png", FRUIT_SIZE)
watermelon_half_1 = load_image("watermelon_half_1_small.png", FRUIT_SIZE)
watermelon_half_2 = load_image("watermelon_half_2_small.png", FRUIT_SIZE)
coconut_half_1 = load_image("coconut_half_1_small.png", FRUIT_SIZE)
coconut_half_2 = load_image("coconut_half_2_small.png", FRUIT_SIZE)

# Load effects (scaled)
explosion_img = load_image("explosion_small.png", FRUIT_SIZE)
splash_red = load_image("splash_red_small.png", FRUIT_SIZE)
splash_orange = load_image("splash_orange_small.png", FRUIT_SIZE)
splash_yellow = load_image("splash_yellow_small.png", FRUIT_SIZE)
splash_transparent = load_image("splash_transparent_small.png", FRUIT_SIZE)

# Load knife image
knife_img = load_image("KNIFE.png", (60, 60))

# Create fruit dictionary for easy access
fruits = {
    'apple': {'whole': apple_img, 'half1': apple_half_1, 'half2': apple_half_2, 'splash': splash_red},
    'banana': {'whole': banana_img, 'half1': banana_half_1, 'half2': banana_half_2, 'splash': splash_yellow},
    'orange': {'whole': orange_img, 'half1': orange_half_1, 'half2': orange_half_2, 'splash': splash_orange},
    'pineapple': {'whole': pineapple_img, 'half1': pineapple_half_1, 'half2': pineapple_half_2, 'splash': splash_yellow},
    'watermelon': {'whole': watermelon_img, 'half1': watermelon_half_1, 'half2': watermelon_half_2, 'splash': splash_red},
    'coconut': {'whole': coconut_img, 'half1': coconut_half_1, 'half2': coconut_half_2, 'splash': splash_transparent}
}

# Sound effects with error handling
try:
    slice_sfx = pygame.mixer.Sound("Mobile - Fruit Ninja - Sound Effects/Sound/combo-1.wav")
    bomb_sfx = pygame.mixer.Sound("Mobile - Fruit Ninja - Sound Effects/Sound/pome-burst.wav")
    slice_sfx.set_volume(0.5)
    bomb_sfx.set_volume(0.5)
except:
    print("Sound effects not found. Game will run without sound.")
    slice_sfx = None
    bomb_sfx = None

# Font with fallback
try:
    font = pygame.font.SysFont("Arial", 36)
except:
    font = pygame.font.Font(None, 36)  # Use default font as fallback

# Utility function to render text with outline for better visibility
def render_text_with_outline(text, font, text_color, outline_color, pos, surface):
    base = font.render(text, True, text_color)
    outline = font.render(text, True, outline_color)
    x, y = pos
    # Draw outline
    for dx in [-2, 0, 2]:
        for dy in [-2, 0, 2]:
            if dx != 0 or dy != 0:
                surface.blit(outline, (x + dx, y + dy))
    # Draw main text
    surface.blit(base, (x, y))

# Classes
class Object:
    def __init__(self, img, x, y, speed, is_bomb=False, fruit_type=None):
        self.img = img
        self.x = x
        self.y = y
        self.speed = speed
        self.angle = random.uniform(-1.5, 1.5)
        self.is_bomb = is_bomb
        self.fruit_type = fruit_type
        self.rect = self.img.get_rect(center=(self.x, self.y))
        self.hit = False
        self.velocity_y = -speed * 2  # Initial upward velocity
        self.gravity = 0.25  # Slower gravity

    def update(self):
        self.velocity_y += self.gravity
        self.y += self.velocity_y
        self.x += self.angle * 5
        self.rect = self.img.get_rect(center=(self.x, self.y))

    def draw(self, surface):
        surface.blit(self.img, (self.x - self.img.get_width() // 2, self.y - self.img.get_height() // 2))

class SlicedFruit:
    def __init__(self, x, y, fruit_type):
        self.fruit_type = fruit_type
        self.half1 = fruits[fruit_type]['half1']
        self.half2 = fruits[fruit_type]['half2']
        self.splash = fruits[fruit_type]['splash']
        self.x = x
        self.y = y
        self.timer = 30
        self.angle1 = random.uniform(-30, -10)
        self.angle2 = random.uniform(10, 30)
        self.speed1 = random.uniform(-3, -1)
        self.speed2 = random.uniform(1, 3)
        self.velocity_y1 = -5
        self.velocity_y2 = -5
        self.gravity = 0.3

    def draw(self, surface):
        # Draw splash effect
        surface.blit(self.splash, (self.x - self.splash.get_width()//2, self.y - self.splash.get_height()//2))
        
        # Update positions with gravity
        self.velocity_y1 += self.gravity
        self.velocity_y2 += self.gravity
        
        # Draw fruit halves with gravity
        surface.blit(self.half1, (self.x - 32 + self.speed1 * self.timer, 
                                self.y - 32 + self.velocity_y1 * self.timer))
        surface.blit(self.half2, (self.x - 32 + self.speed2 * self.timer, 
                                self.y - 32 + self.velocity_y2 * self.timer))
        
        self.timer -= 1

def show_game_over(score):
    game_over_font = pygame.font.Font(None, 72)
    score_font = pygame.font.Font(None, 48)
    # Use the same outline function for visibility
    render_text_with_outline("Game Over!", game_over_font, (255, 0, 0), (0, 0, 0), (WIDTH//2 - 200, HEIGHT//2 - 100), screen)
    render_text_with_outline(f"Final Score: {score}", score_font, (255, 255, 0), (0, 0, 0), (WIDTH//2 - 180, HEIGHT//2), screen)
    render_text_with_outline("Press SPACE to restart", score_font, (0, 255, 255), (0, 0, 0), (WIDTH//2 - 220, HEIGHT//2 + 100), screen)
    pygame.display.update()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

# Game State
def reset_game():
    global objects, sliced_fruits, spawn_timer, score, lives, game_time, start_ticks, blank_life_cooldown
    objects = []
    sliced_fruits = []
    spawn_timer = 0
    score = 0
    lives = LIVES_START
    game_time = 60  # seconds
    start_ticks = pygame.time.get_ticks()
    blank_life_cooldown = 0  # Cooldown for blank space life loss

reset_game()

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    screen.blit(background, (0, 0))

    # Draw knife at mouse position
    mouse = pygame.mouse.get_pos()
    knife_rect = knife_img.get_rect(center=mouse)
    screen.blit(knife_img, (mouse[0] - knife_img.get_width() // 2, mouse[1] - knife_img.get_height() // 2))

    # Knife collision with fruits
    knife_hit_fruit = False
    for obj in objects[:]:
        if not obj.hit and knife_rect.colliderect(obj.rect):
            obj.hit = True
            knife_hit_fruit = True
            if obj.is_bomb:
                if bomb_sfx:
                    bomb_sfx.play()
                lives = 0
            else:
                if slice_sfx:
                    slice_sfx.play()
                score += 1
                if obj.fruit_type:
                    sliced_fruits.append(SlicedFruit(obj.x, obj.y, obj.fruit_type))
                objects.remove(obj)

    # Lose a life if mouse moved and not over any fruit (with cooldown)
    if blank_life_cooldown > 0:
        blank_life_cooldown -= 1
    if pygame.mouse.get_rel() != (0, 0) and not knife_hit_fruit and blank_life_cooldown == 0:
        lives -= 1
        blank_life_cooldown = 100  # 100 frames cooldown (even less sensitive)

    # Spawn objects
    spawn_timer += 1
    if spawn_timer > 30:
        spawn_timer = 0
        if random.random() < 0.1:
            objects.append(Object(bomb_img, random.randint(100, WIDTH - 100), HEIGHT // 2 + 50, random.randint(2, 4), True))
        else:
            fruit_type = random.choice(list(fruits.keys()))
            img = fruits[fruit_type]['whole']
            objects.append(Object(img, random.randint(100, WIDTH - 100), HEIGHT // 2 + 50, random.randint(2, 4), False, fruit_type))

    # Update objects
    for obj in objects[:]:
        obj.update()
        obj.draw(screen)
        # Remove objects that fall off screen, but do not lose a life
        if obj.y > HEIGHT + 100 and not obj.hit:
            objects.remove(obj)

    # Draw sliced animation
    for sliced in sliced_fruits[:]:
        sliced.draw(screen)
        if sliced.timer <= 0:
            sliced_fruits.remove(sliced)

    # Timer logic
    seconds = (pygame.time.get_ticks() - start_ticks) // 1000
    remaining = max(0, game_time - seconds)
    
    # Draw score and HUD
    render_text_with_outline(f"Score: {score}", font, (255, 255, 0), (0, 0, 0), (10, 10), screen)  # Bright yellow
    render_text_with_outline(f"Lives: {lives}", font, (255, 50, 50), (0, 0, 0), (WIDTH - 150, 10), screen)  # Bright red
    render_text_with_outline(f"Time: {remaining}", font, (0, 255, 255), (0, 0, 0), (WIDTH//2 - 50, 10), screen)  # Bright cyan

    pygame.display.update()
    clock.tick(60)

    # Check game over conditions
    if remaining == 0 or lives <= 0:
        show_game_over(score)
        reset_game()

pygame.quit() 