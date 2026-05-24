import pygame
import sys
import math

pygame.init()

WIDTH = 800
HEIGHT = 600
TILE = 40

MAZE_WIDTH = 15
MAZE_HEIGHT = 15
OFFSET_X = (WIDTH - (MAZE_WIDTH * TILE)) // 2
OFFSET_Y = (HEIGHT - (MAZE_HEIGHT * TILE)) // 2

BLACK = (0, 0, 0)
BLUE = (25, 0, 255)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
PINK = (255, 100, 150)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🍬 КОНФЕТНЫЙ ЛАБИРИНТ - 2 УРОВНЯ 🍬")
clock = pygame.time.Clock()

maze_level1 = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,3,1,0,0,0,0,0,0,0,1],
    [1,0,1,1,1,0,1,0,1,1,1,0,1,0,1],
    [1,0,1,3,0,0,0,0,0,0,1,0,1,0,1],
    [1,0,1,0,1,1,1,1,1,0,1,0,1,0,1],
    [1,0,0,0,1,0,3,0,0,0,1,0,0,0,1],
    [1,1,1,0,1,0,1,1,1,1,1,0,1,1,1],
    [1,0,0,0,0,0,1,0,0,0,0,0,0,0,1],
    [1,0,1,1,1,0,1,0,1,1,1,0,1,0,1],
    [1,0,3,0,0,0,0,0,0,0,1,0,0,3,1],
    [1,0,1,1,1,1,1,1,1,0,1,1,1,0,1],
    [1,0,0,0,0,0,0,0,1,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,0,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,2,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]

maze_level2 = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,1,0,0,0,0,0,1,0,0,0,3,0,1],
    [1,0,1,0,1,1,1,0,1,0,1,1,1,0,1],
    [1,0,0,0,1,3,1,0,0,0,1,0,0,0,1],
    [1,1,1,0,1,0,1,1,1,0,1,0,1,1,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,1,0,1,1,1,1,1,1,1,0,1],
    [1,0,0,0,1,0,0,0,3,0,0,0,0,0,1],
    [1,1,1,0,1,1,1,1,1,0,1,1,1,0,1],
    [1,0,0,0,0,0,1,0,0,0,1,0,0,0,1],
    [1,0,1,1,1,0,1,0,1,1,1,0,1,0,1],
    [1,0,3,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,1,1,1,1,1,0,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,2,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]

class AppleCore:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.animation_frame = 0

    def draw(self):
        center_x = self.x * TILE + OFFSET_X + TILE // 2
        center_y = self.y * TILE + OFFSET_Y + TILE // 2
        size = TILE - 12

        pygame.draw.circle(screen, (210, 180, 100), (center_x, center_y), size // 2)
        pygame.draw.ellipse(screen, (200, 100, 50), (center_x - 8, center_y - 4, 16, 20))
        pygame.draw.circle(screen, WHITE, (center_x - 5, center_y - 4), 3)
        pygame.draw.circle(screen, WHITE, (center_x + 5, center_y - 4), 3)
        pygame.draw.circle(screen, BLACK, (center_x - 5, center_y - 4), 1)
        pygame.draw.circle(screen, BLACK, (center_x + 5, center_y - 4), 1)
        pygame.draw.arc(screen, BLACK, (center_x - 6, center_y - 2, 12, 10), 0, math.pi, 2)
        pygame.draw.line(screen, BLACK, (center_x - 9, center_y - 10), (center_x - 3, center_y - 8), 2)
        pygame.draw.line(screen, BLACK, (center_x + 9, center_y - 10), (center_x + 3, center_y - 8), 2)
        pygame.draw.ellipse(screen, (80, 50, 20), (center_x - 2, center_y - 12, 4, 6))

        if self.animation_frame > 0:
            self.animation_frame -= 1
            pygame.draw.circle(screen, (255, 200, 100), (center_x, center_y - 3), 3)

    def move(self, dx, dy, current_maze):
        global candies_collected
        new_x = self.x + dx
        new_y = self.y + dy

        if 0 <= new_y < len(current_maze) and 0 <= new_x < len(current_maze[0]):
            if current_maze[new_y][new_x] != 1:
                if current_maze[new_y][new_x] == 3:
                    candies_collected += 1
                    current_maze[new_y][new_x] = 0
                    self.animation_frame = 10
                self.x = new_x
                self.y = new_y

class Exit:
    def __init__(self, maze):
        self.find_exit(maze)

    def find_exit(self, maze):
        for i in range(len(maze)):
            for j in range(len(maze[0])):
                if maze[i][j] == 2:
                    self.x = j
                    self.y = i

    def draw(self):
        pulse = abs(pygame.time.get_ticks() % 1000 - 500) / 500
        size = int((TILE - 10) * (0.7 + pulse * 0.3))
        center_x = self.x * TILE + OFFSET_X + TILE // 2
        center_y = self.y * TILE + OFFSET_Y + TILE // 2
        pygame.draw.circle(screen, YELLOW, (center_x, center_y), size // 2 + 5)
        pygame.draw.circle(screen, RED, (center_x, center_y), size // 2)

def count_candies(maze):
    return sum(cell == 3 for row in maze for cell in row)

def draw_maze(maze):
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            x = j * TILE + OFFSET_X
            y = i * TILE + OFFSET_Y
            if maze[i][j] == 1:
                pygame.draw.rect(screen, BLUE, (x, y, TILE, TILE))
            elif maze[i][j] == 3:
                center_x = x + TILE // 2
                center_y = y + TILE // 2
                pygame.draw.circle(screen, PINK, (center_x, center_y), 8)
                pygame.draw.circle(screen, WHITE, (center_x, center_y), 4)

def show_level_transition(level_num):
    screen.fill(BLACK)
    big_font = pygame.font.Font(None, 72)
    text = big_font.render(f"УРОВЕНЬ {level_num}", True, YELLOW)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)

    small_font = pygame.font.Font(None, 36)
    text2 = small_font.render("Приготовься...", True, WHITE)
    text2_rect = text2.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 60))
    screen.blit(text2, text2_rect)

    pygame.display.flip()
    pygame.time.wait(2000)

def reset_game():
    global current_maze, candies_collected, total_candies, player, exit_door, current_level, victory, level_complete, victory_timer
    current_maze = [row[:] for row in maze_level1]
    candies_collected = 0
    current_level = 1
    total_candies = count_candies(current_maze)
    player = AppleCore(1, 1)
    exit_door = Exit(current_maze)
    victory = False
    level_complete = False
    victory_timer = 0

current_level = 1
current_maze = [row[:] for row in maze_level1]
total_candies = count_candies(current_maze)
candies_collected = 0
player = AppleCore(1, 1)
exit_door = Exit(current_maze)
running = True
victory = False
victory_timer = 0
level_complete = False
font = pygame.font.Font(None, 36)

while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                reset_game()
            elif not victory and not level_complete:
                if event.key == pygame.K_LEFT:
                    player.move(-1, 0, current_maze)
                elif event.key == pygame.K_RIGHT:
                    player.move(1, 0, current_maze)
                elif event.key == pygame.K_UP:
                    player.move(0, -1, current_maze)
                elif event.key == pygame.K_DOWN:
                    player.move(0, 1, current_maze)

    draw_maze(current_maze)
    exit_door.draw()
    player.draw()

    candy_text = font.render(f"🍬 {candies_collected}/{total_candies}", True, YELLOW)
    screen.blit(candy_text, (20, 20))
    level_text = font.render(f"УРОВЕНЬ {current_level}", True, WHITE)
    screen.blit(level_text, (WIDTH - 150, 20))

    if player.x == exit_door.x and player.y == exit_door.y and not victory and not level_complete:
        if candies_collected == total_candies:
            level_complete = True
            victory_timer = pygame.time.get_ticks()
        else:
            need_text = font.render(f"Собери ещё {total_candies - candies_collected} конфет!", True, RED)
            need_rect = need_text.get_rect(center=(WIDTH // 2, HEIGHT - 50))
            screen.blit(need_text, need_rect)

    if level_complete:
        big_font = pygame.font.Font(None, 56)
        text = big_font.render(f"УРОВЕНЬ {current_level} ПРОЙДЕН!", True, YELLOW)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, text_rect)

        if pygame.time.get_ticks() - victory_timer > 1500:
            if current_level == 1:
                current_level = 2
                current_maze = [row[:] for row in maze_level2]
                total_candies = count_candies(current_maze)
                candies_collected = 0
                player = AppleCore(1, 1)
                exit_door = Exit(current_maze)
                level_complete = False
                show_level_transition(2)
            else:
                victory = True
                level_complete = False

    if victory:
        big_font = pygame.font.Font(None, 64)
        text = big_font.render("🍔 ПОЛНАЯ ПОБЕДА! 🍔", True, YELLOW)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 30))
        shadow = big_font.render("🍔 ПОЛНАЯ ПОБЕДА! 🍔", True, BLUE)
        shadow_rect = shadow.get_rect(center=(WIDTH // 2 + 3, HEIGHT // 2 - 27))
        screen.blit(shadow, shadow_rect)
        screen.blit(text, text_rect)

        small_font = pygame.font.Font(None, 36)
        text2 = small_font.render("Нажми R чтобы начать заново", True, WHITE)
        text2_rect = text2.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 40))
        screen.blit(text2, text2_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
