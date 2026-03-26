import pygame
from sys import exit
import random
import math
import os
import numpy as np
import wave
import struct

# --- ASSET GENERATION FUNCTIONS (Self-Contained and Safe) ---

def save_wav(filename, samples, framerate=44100):
    """Generates and saves a WAV file from numpy samples."""
    if os.path.exists(filename): return
    print(f"Generating {filename}...")
    try:
        with wave.open(filename, 'w') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(framerate)
            for s in samples:
                wf.writeframes(struct.pack('<h', int(s)))
    except Exception as e:
        print(f"Error generating WAV file {filename}: {e}")

def gen_sine(frequency, duration, amplitude=16000, framerate=44100):
    """Generates a sine wave."""
    t = np.linspace(0, duration, int(framerate * duration), False)
    return amplitude * np.sin(2 * np.pi * frequency * t)

def gen_swoosh():
    t = np.linspace(0, 0.3, int(44100 * 0.3), False)
    freq = np.linspace(400, 1200, len(t))
    samples = 12000 * np.sin(2 * np.pi * freq * t)
    return samples

def gen_wing():
    return gen_sine(900, 0.08) * np.hanning(int(44100 * 0.08))

def gen_point():
    return gen_sine(1400, 0.07) * np.hanning(int(44100 * 0.07))

def gen_hit():
    return gen_sine(120, 0.12) * np.hanning(int(44100 * 0.12))

def gen_die():
    t = np.linspace(0, 0.5, int(44100 * 0.5), False)
    freq = np.linspace(900, 120, len(t))
    samples = 12000 * np.sin(2 * np.pi * freq * t)
    return samples

def gen_music():
    notes = [440, 554.37, 659.25, 880, 659.25, 554.37]
    duration = 0.15
    music_samples = np.array([])
    for note in notes * 8:
        samples = gen_sine(note, duration, amplitude=8000) * np.hanning(int(44100 * duration))
        music_samples = np.append(music_samples, samples)
    return music_samples

def create_placeholder_assets():
    """Generates placeholder assets if they are missing."""
    print("Checking/Generating required assets...")
    save_wav('swoosh.wav', gen_swoosh())
    save_wav('wing.wav', gen_wing())
    save_wav('point.wav', gen_point())
    save_wav('hit.wav', gen_hit())
    save_wav('die.wav', gen_die())
    save_wav('title_music.wav', gen_music())

    try:
        if not pygame.get_init():
            pygame.init()
        
        if not os.path.exists("flappybirdbg.png"):
            surf = pygame.Surface((480, 640))
            surf.fill((135, 206, 235))
            pygame.image.save(surf, "flappybirdbg.png")
            print("Generated flappybirdbg.png placeholder.")
        if not os.path.exists("flappybird.png"):
            surf = pygame.Surface((34, 24), pygame.SRCALPHA)
            pygame.draw.circle(surf, (255, 255, 0), (17, 12), 12)
            pygame.image.save(surf, "flappybird.png")
            print("Generated flappybird.png placeholder.")
        if not os.path.exists("toppipe.png"):
            surf = pygame.Surface((64, 512), pygame.SRCALPHA)
            surf.fill((100, 200, 100))
            pygame.image.save(surf, "toppipe.png")
            print("Generated toppipe.png placeholder.")
        if not os.path.exists("bottompipe.png"):
            surf = pygame.Surface((64, 512), pygame.SRCALPHA)
            surf.fill((100, 200, 100))
            pygame.image.save(surf, "bottompipe.png")
            print("Generated bottompipe.png placeholder.")
    except Exception as e:
        print(f"Could not generate placeholder image: {e}")

# --- GAME SETUP ---

GAME_WIDTH = 480 
GAME_HEIGHT = 640

bird_x = GAME_WIDTH / 8
bird_start_y = GAME_HEIGHT / 2
bird_width = 34
bird_height = 24

class Bird(pygame.Rect):
    def __init__(self, img):
        pygame.Rect.__init__(self, bird_x, bird_start_y, bird_width, bird_height)
        self.img = img
        self.title_x = -bird_width

pipe_x = GAME_WIDTH
pipe_y = 0
pipe_width = 64
pipe_height = 512

class Pipe(pygame.Rect):
    def __init__(self, img):
        pygame.Rect.__init__(self, pipe_x, pipe_y, pipe_width, pipe_height)
        self.img = img
        self.passed = False

pygame.init()
pygame.mixer.init()
pygame.font.init()

create_placeholder_assets()

window = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
pygame.display.set_caption("Flappy Bird: The Game")
clock = pygame.time.Clock()

try:
    background_image = pygame.image.load("flappybirdbg.png").convert()
    background_image = pygame.transform.scale(background_image, (GAME_WIDTH, GAME_HEIGHT))
    original_bird_image = pygame.image.load("flappybird.png").convert_alpha()
    bird_image = pygame.transform.scale(original_bird_image, (bird_width, bird_height))
    top_pipe_image = pygame.image.load("toppipe.png").convert_alpha()
    top_pipe_image = pygame.transform.scale(top_pipe_image, (pipe_width, pipe_height))
    bottom_pipe_image = pygame.image.load("bottompipe.png").convert_alpha()
    bottom_pipe_image = pygame.transform.scale(bottom_pipe_image, (pipe_width, pipe_height))
except pygame.error as e:
    print(f"CRITICAL ERROR: Failed to load an image file. Details: {e}")
    pygame.quit()
    exit()

class DummySound:
    def play(self):
        pass

try:
    swoosh_sound = pygame.mixer.Sound("swoosh.wav")
    wing_sound = pygame.mixer.Sound("wing.wav")
    point_sound = pygame.mixer.Sound("point.wav")
    hit_sound = pygame.mixer.Sound("hit.wav")
    die_sound = pygame.mixer.Sound("die.wav")
    title_music = "title_music.wav"
    pygame.mixer.music.load(title_music)
except Exception as e:
    print(f"WARNING: Failed to load a sound file. Details: {e}")
    swoosh_sound, wing_sound, point_sound, hit_sound, die_sound = [DummySound()] * 5


# --- GAME STATE MANAGEMENT ---
TITLE_SCREEN = 0
GAME_RUNNING = 1
GAME_OVER = 2
game_state = TITLE_SCREEN

bird = Bird(bird_image)
pipes = []
velocity_x = -2
velocity_y = 0
gravity = 0.4
score = 0
death_sound_played = False
hover_time = 0
title_fly_speed = 3

create_pipes_timer = pygame.USEREVENT + 0
pygame.time.set_timer(create_pipes_timer, 1500)

start_button_rect = pygame.Rect(0, 0, 200, 60)
try_again_button_rect = pygame.Rect(0, 0, 200, 60)

# --- DRAWING UTILITIES ---
def draw_rotated_bird(surface, bird_rect, bird_img, angle):
    """Handles rotation and blitting of the bird image."""
    rotated_bird = pygame.transform.rotate(bird_img, angle)
    rotated_rect = rotated_bird.get_rect(center=bird_rect.center)
    surface.blit(rotated_bird, rotated_rect)

def render_text_center(surface, text, size, color, center_y, font_name="Comic Sans MS", bold=False):
    """Renders text centered horizontally on the screen."""
    font = pygame.font.SysFont(font_name, size, bold=bold)
    text_render = font.render(text, True, color)
    text_rect = text_render.get_rect(center=(GAME_WIDTH // 2, center_y))
    surface.blit(text_render, text_rect)
    return text_rect

def draw_button(surface, rect, text, font_size, bg_color=(100, 100, 100), text_color=(255, 255, 255)):
    """Draws a button with text centered on it."""
    pygame.draw.rect(surface, bg_color, rect, border_radius=10)
    pygame.draw.rect(surface, (255, 255, 255), rect, 3, border_radius=10)
    
    font = pygame.font.SysFont("Comic Sans MS", font_size, bold=True)
    text_render = font.render(text, True, text_color)
    text_rect = text_render.get_rect(center=rect.center)
    surface.blit(text_render, text_rect)

# ----------------------------------------------------------------------
## Title Screen Function
# ----------------------------------------------------------------------

def title_screen():
    """Renders the title screen with the title box and start button."""
    global hover_time, title_fly_speed, bird, start_button_rect

    window.blit(background_image, (0, 0))

    # --- Draw Title Box ---
    title_box_rect = pygame.Rect(0, 0, 350, 200)
    title_box_rect.center = (GAME_WIDTH // 2, GAME_HEIGHT // 2 - 100)
    s = pygame.Surface((title_box_rect.width, title_box_rect.height), pygame.SRCALPHA)
    s.fill((0, 0, 0, 128))
    window.blit(s, title_box_rect.topleft)
    pygame.draw.rect(window, (255, 255, 255), title_box_rect, 3, border_radius=10)

    # --- Title Text inside the box ---
    render_text_center(window, "FLAPPY BIRD", 60, (255, 255, 255), title_box_rect.top + 50, bold=True)
    render_text_center(window, "The Game", 30, (255, 255, 255), title_box_rect.top + 120, bold=True)
    
    # --- Start Button ---
    start_button_rect.center = (GAME_WIDTH // 2, GAME_HEIGHT // 2 + 100)
    draw_button(window, start_button_rect, "CLICK HERE TO START", 24)

    # --- Bird Flying Animation ---
    bird.title_x += title_fly_speed
    if bird.title_x > GAME_WIDTH + bird_width:
        bird.title_x = -bird_width

    hover_time += 0.1
    current_y = bird_start_y + 10 * math.sin(hover_time)
    flying_bird_rect = bird.copy()
    flying_bird_rect.x = bird.title_x
    flying_bird_rect.y = current_y

    draw_rotated_bird(window, flying_bird_rect, bird.img, 0)
    
    pygame.display.update()

# ----------------------------------------------------------------------
## Game Over Screen Function
# ----------------------------------------------------------------------

def game_over_screen():
    """Renders the game over screen with final score and a 'Try Again' button."""
    global try_again_button_rect

    # 1. Draw the final game state (background, pipes, bird)
    window.blit(background_image, (0, 0))
    for pipe in pipes:
        window.blit(pipe.img, pipe)
    # Bird should be drawn with collision rotation (-90 degrees)
    draw_rotated_bird(window, bird, bird.img, -90) 
    
    # Draw score in the corner (part of the last game frame)
    score_font = pygame.font.SysFont("Comic Sans MS", 45)
    score_render = score_font.render(str(int(score)), True, "white")
    window.blit(score_render, (5, 0))

    # 2. Overlay the Game Over UI Box
    game_over_box_rect = pygame.Rect(0, 0, 300, 250)
    game_over_box_rect.center = (GAME_WIDTH // 2, GAME_HEIGHT // 2 - 50)
    s = pygame.Surface((game_over_box_rect.width, game_over_box_rect.height), pygame.SRCALPHA)
    s.fill((0, 0, 0, 128))
    window.blit(s, game_over_box_rect.topleft)
    pygame.draw.rect(window, (255, 255, 255), game_over_box_rect, 3, border_radius=10)

    # 3. Text and Button inside the box
    render_text_center(window, "GAME OVER", 40, (255, 0, 0), game_over_box_rect.top + 40, bold=True)
    render_text_center(window, f"Score: {int(score)}", 30, (255, 255, 255), game_over_box_rect.top + 100, bold=True)

    try_again_button_rect.center = (GAME_WIDTH // 2, game_over_box_rect.top + 180)
    draw_button(window, try_again_button_rect, "TRY AGAIN", 24)
    
    pygame.display.update()

# ----------------------------------------------------------------------
## Helper Functions (Movement, Pipes, Reset)
# ----------------------------------------------------------------------

def draw():
    """Draws only the running game state (background, pipes, bird, score)."""
    window.blit(background_image, (0, 0))
    for pipe in pipes:
        window.blit(pipe.img, pipe)

    max_down_rotation = -90
    max_up_rotation = 25
    
    # Calculate rotation for running game
    rotation_angle = velocity_y * -4
    rotation_angle = max(rotation_angle, max_down_rotation)
    rotation_angle = min(rotation_angle, max_up_rotation)

    draw_rotated_bird(window, bird, bird.img, rotation_angle)

    # Draw score
    score_font = pygame.font.SysFont("Comic Sans MS", 45)
    score_str = str(int(score))
    score_render = score_font.render(score_str, True, "white")
    window.blit(score_render, (5, 0))
    
    pygame.display.update()


def move():
    """Updates the bird and pipe positions and checks for collisions."""
    global velocity_y, score, game_state, death_sound_played

    if game_state != GAME_RUNNING:
        return

    velocity_y += gravity
    bird.y += velocity_y
    bird.y = max(bird.y, 0)

    # Collision with Ground
    if bird.y > GAME_HEIGHT:
        game_state = GAME_OVER
        if not death_sound_played:
            hit_sound.play()
            die_sound.play()
            death_sound_played = True
        pygame.mixer.music.stop()
        return

    for pipe in pipes:
        pipe.x += velocity_x

        # Scoring
        if not pipe.passed and bird.x > pipe.x + pipe.width:
            score += 0.5
            pipe.passed = True
            if score == int(score):
                point_sound.play()

        # Collision with Pipe
        if bird.colliderect(pipe):
            game_state = GAME_OVER
            if not death_sound_played:
                hit_sound.play()
                die_sound.play()
                death_sound_played = True
            pygame.mixer.music.stop()
            return

    while len(pipes) > 0 and pipes[0].x < -pipe_width:
        pipes.pop(0)

def create_pipes():
    """Creates a new set of top and bottom pipes."""
    random_pipe_y = pipe_y - pipe_height / 4 - random.random() * (pipe_height / 2)
    opening_space = GAME_HEIGHT / 4
    top_pipe = Pipe(top_pipe_image)
    top_pipe.y = random_pipe_y
    pipes.append(top_pipe)
    bottom_pipe = Pipe(bottom_pipe_image)
    bottom_pipe.y = top_pipe.y + top_pipe.height + opening_space
    pipes.append(bottom_pipe)

def reset_game():
    """Resets all variables for a new game or title screen."""
    global pipes, score, velocity_y, death_sound_played, hover_time
    bird.y = bird_start_y
    bird.x = bird_x
    pipes.clear()
    score = 0
    death_sound_played = False
    velocity_y = 0
    hover_time = 0
    pygame.mixer.music.stop()

# ----------------------------------------------------------------------
## Main Game Loop
# ----------------------------------------------------------------------

if not pygame.mixer.music.get_busy() and game_state == TITLE_SCREEN:
    try:
        pygame.mixer.music.play(-1)
    except Exception:
        pass

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == create_pipes_timer and game_state == GAME_RUNNING:
            create_pipes()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            
            # Start Game button click
            if game_state == TITLE_SCREEN and start_button_rect.collidepoint(mouse_pos):
                reset_game()
                game_state = GAME_RUNNING
                create_pipes()
                velocity_y = -6
                swoosh_sound.play()
                pygame.mixer.music.stop()
            
            # Try Again button click
            elif game_state == GAME_OVER and try_again_button_rect.collidepoint(mouse_pos):
                reset_game()
                game_state = TITLE_SCREEN
                swoosh_sound.play()
                try:
                    pygame.mixer.music.play(-1)
                except Exception:
                    pass

        if event.type == pygame.KEYDOWN:
            # Spacebar jump during gameplay
            if game_state == GAME_RUNNING and event.key == pygame.K_SPACE:
                velocity_y = -6
                wing_sound.play()

    # --- STATE MACHINE EXECUTION ---
    if game_state == TITLE_SCREEN:
        if not pygame.mixer.music.get_busy():
            try:
                pygame.mixer.music.play(-1)
            except Exception:
                pass
        title_screen()
    
    elif game_state == GAME_RUNNING:
        move()
        draw() # Calls draw only for the running game
    
    # When game_state changes to GAME_OVER in move(), the loop skips draw() and moves here.
    elif game_state == GAME_OVER:
        game_over_screen() # Calls the dedicated game over drawing function

    clock.tick(60)