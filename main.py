
import pygame
from game.game_engine import GameEngine

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 700, 500
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Target Aim Trainer")

# Colors
DARK_GRAY = (35, 35, 40)
WHITE = (255, 255, 255)
YELLOW = (255, 220, 80)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Fonts
title_font = pygame.font.SysFont("Arial", 48)
menu_font = pygame.font.SysFont("Arial", 30)
instruction_font = pygame.font.SysFont("Arial", 22)

# Difficulty settings
DIFFICULTIES = {
    "Easy": {
        "base_radius": 50,
        "min_radius": 18,
        "lifespan_frames": 120,
    },
    "Medium": {
        "base_radius": 40,
        "min_radius": 12,
        "lifespan_frames": 90,
    },
    "Hard": {
        "base_radius": 30,
        "min_radius": 8,
        "lifespan_frames": 60,
    },
}

selected_difficulty = 0
difficulty_names = list(DIFFICULTIES.keys())

# Application states
MENU = "menu"
PLAYING = "playing"
GAME_OVER = "game_over"

state = MENU
engine = None


def draw_menu():
    SCREEN.fill(DARK_GRAY)

    title = title_font.render("TARGET AIM TRAINER", True, WHITE)
    SCREEN.blit(
        title,
        title.get_rect(center=(WIDTH // 2, 100))
    )

    instruction = menu_font.render(
        "Select Difficulty", True, WHITE
    )
    SCREEN.blit(
        instruction,
        instruction.get_rect(center=(WIDTH // 2, 190))
    )

    for index, difficulty in enumerate(difficulty_names):
        color = YELLOW if index == selected_difficulty else WHITE

        text = menu_font.render(difficulty, True, color)
        SCREEN.blit(
            text,
            text.get_rect(
                center=(WIDTH // 2, 250 + index * 45)
            )
        )

    help_text = instruction_font.render(
        "UP/DOWN: Select   ENTER: Start   ESC: Exit",
        True,
        WHITE,
    )
    SCREEN.blit(
        help_text,
        help_text.get_rect(center=(WIDTH // 2, 440))
    )


def start_game():
    global engine, state

    difficulty = difficulty_names[selected_difficulty]
    settings = DIFFICULTIES[difficulty]

    engine = GameEngine(
        WIDTH,
        HEIGHT,
        **settings
    )

    state = PLAYING


def main():
    global state, selected_difficulty

    running = True

    while running:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            elif state == MENU:
                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_UP:
                        selected_difficulty = (
                            selected_difficulty - 1
                        ) % len(difficulty_names)

                    elif event.key == pygame.K_DOWN:
                        selected_difficulty = (
                            selected_difficulty + 1
                        ) % len(difficulty_names)

                    elif event.key == pygame.K_RETURN:
                        start_game()

                    elif event.key == pygame.K_ESCAPE:
                        running = False

            elif state == PLAYING:
                engine.handle_event(event)

            elif state == GAME_OVER:
                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_RETURN:
                        state = MENU

                    elif event.key == pygame.K_ESCAPE:
                        running = False

        if state == MENU:
            draw_menu()

        elif state == PLAYING:
            SCREEN.fill(DARK_GRAY)

            engine.handle_input()
            engine.update()
            engine.render(SCREEN)

            if engine.game_over:
                state = GAME_OVER

        elif state == GAME_OVER:
            SCREEN.fill(DARK_GRAY)
            engine.render(SCREEN)

            instruction = instruction_font.render(
                "ENTER: Replay   ESC: Exit",
                True,
                WHITE,
            )
            SCREEN.blit(
                instruction,
                instruction.get_rect(
                    center=(WIDTH // 2, HEIGHT - 35)
                )
            )

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
