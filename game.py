import pygame
import random
import sys
import time

# Initialize Pygame
pygame.init()

# Load the board image
BOARD_IMG = "snak n ladder photo.jpg"  # your uploaded image file
board = pygame.image.load(BOARD_IMG)
board = pygame.transform.scale(board, (600, 600))

# Load or generate sounds
pygame.mixer.init()
try:
    dice_sound = pygame.mixer.Sound(pygame.mixer.Sound('dice_roll.wav'))
    win_sound = pygame.mixer.Sound(pygame.mixer.Sound('win.wav'))
except:
    dice_sound = None
    win_sound = None

# Create window
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("🐍 Snake & Ladder 🎲")

# Colors
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

font = pygame.font.SysFont("Comic Sans MS", 28)

# Players start at position 1
positions = [1, 1]
turn = 0
winner = None

# Snakes and ladders mapping
snakes = {99: 78, 95: 75, 92: 88, 89: 68, 74: 53, 64: 60, 62: 19, 49: 11, 46: 25, 16: 6}
ladders = {2: 38, 7: 14, 8: 31, 15: 26, 21: 42, 28: 84, 36: 44, 51: 67, 71: 91, 78: 98, 87: 94}

# Convert 1–100 to (x, y)
def get_pos(num):
    row = (num - 1) // 10
    col = (num - 1) % 10
    if row % 2 == 0:
        x = col
    else:
        x = 9 - col
    y = 9 - row
    return (x * 60 + 30, y * 60 + 30)

# Dice rolling function
def roll_dice_animation():
    for _ in range(10):
        dice_val = random.randint(1, 6)
        draw_board(dice_val)
        pygame.display.update()
        pygame.time.delay(100)
    return dice_val

# Draw board, players, and dice
def draw_board(dice_val=None):
    screen.blit(board, (0, 0))
    # Draw player tokens
    for i, pos in enumerate(positions):
        x, y = get_pos(pos)
        color = RED if i == 0 else BLUE
        pygame.draw.circle(screen, color, (x, y), 15)
    # Show dice value
    text = font.render(f"🎲 Player {turn+1}'s Turn", True, BLACK)
    screen.blit(text, (10, 10))
    if dice_val:
        dice_text = font.render(f"Dice: {dice_val}", True, BLACK)
        screen.blit(dice_text, (10, 50))
    pygame.display.update()

# Main loop
running = True
while running:
    draw_board()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not winner:
                # Play dice roll sound
                if dice_sound: dice_sound.play()

                dice = roll_dice_animation()
                positions[turn] += dice

                if positions[turn] > 100:
                    positions[turn] -= dice

                if positions[turn] in snakes:
                    positions[turn] = snakes[positions[turn]]
                elif positions[turn] in ladders:
                    positions[turn] = ladders[positions[turn]]

                if positions[turn] == 100:
                    winner = turn + 1
                    if win_sound: win_sound.play()

                turn = 1 - turn  # switch turn

            if event.key == pygame.K_q:
                pygame.quit()
                sys.exit()

    if winner:
        screen.fill(WHITE)
        msg = font.render(f"🏆 Player {winner} Wins! Press Q to Quit.", True, BLACK)
        screen.blit(msg, (100, 280))
        pygame.display.update()
