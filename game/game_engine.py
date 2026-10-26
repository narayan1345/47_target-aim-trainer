import pygame
import random
import math
from array import array
from .target import Target

# Game Engine

WHITE = (255, 255, 255)
RED = (220, 60, 60)


def create_tone(frequency, duration, volume=0.25):
    sample_rate = 44100
    samples = int(sample_rate * duration)

    buffer = array("h")

    for i in range(samples):
        value = int(
            32767
            * volume
            * math.sin(
                2 * math.pi * frequency * i / sample_rate
            )
        )
        buffer.append(value)

    return pygame.mixer.Sound(buffer=buffer)


class GameEngine:
    
    def __init__(
        self,
        width,
        height,
        base_radius=40,
        min_radius=12,
        lifespan_frames=90,
    ):
        self.width = width
        self.height = height

        self.margin = 60
        self.hud_height = 60

        self.base_radius = base_radius
        self.min_radius = min_radius
        self.lifespan_frames = lifespan_frames

        self.target = self._spawn_target()

        self.round_seconds = 30
        self.time_left_frames = self.round_seconds * 60

        self.hits = 0
        self.misses = 0
        self.score = 0

        self.font = pygame.font.SysFont("Arial", 26)
        self.game_over = False

        self.hit_sound = create_tone(880, 0.08)
        self.miss_sound = create_tone(220, 0.12)
        self.game_over_sound = create_tone(440, 0.5)


    
    def _spawn_target(self):
        x = random.randint(self.margin, self.width - self.margin)
        y = random.randint(
            self.margin + self.hud_height,
            self.height - self.margin
        )

        return Target(
            x,
            y,
            base_radius=self.base_radius,
            min_radius=self.min_radius,
            lifespan_frames=self.lifespan_frames,
        )


    def handle_event(self, event):
        if self.game_over:
            return
        if event.type == pygame.MOUSEBUTTONDOWN:
            self._handle_click(event.pos)

   
    def _handle_click(self, pos):
        x, y = pos

        if self.target.contains_point(x, y):
            self.hits += 1
            self.score += 1

            self.hit_sound.play()
            self.target = self._spawn_target()

        else:
            self.misses += 1
            self.miss_sound.play()


    def handle_input(self):
        # Reserved for continuously-held-key input; this game is
        # entirely mouse-driven, so there's nothing to poll here.
        pass

    def update(self):
        if self.game_over:
            return

        self.time_left_frames -= 1
        
        if self.time_left_frames <= 0:
            self.game_over = True
            self.game_over_sound.play()
            return


        self.target.update()
        
        if self.target.expired():
            self.misses += 1
            self.miss_sound.play()
            self.target = self._spawn_target()


    def accuracy(self):
        total = self.hits + self.misses
        if total == 0:
            return 0.0
        return round(100 * self.hits / total, 1)

    
    def render(self, screen):
        if not self.game_over:
            # Draw the target during gameplay
            r = int(self.target.visual_radius())
            pygame.draw.circle(
                screen, RED, (self.target.x, self.target.y), r
            )
            pygame.draw.circle(
                screen, WHITE, (self.target.x, self.target.y), r, 2
            )

        # Display the HUD
        score_text = self.font.render(
            f"Score: {self.score}", True, WHITE
        )
        screen.blit(score_text, (10, 10))

        seconds_left = max(0, self.time_left_frames // 60)
        timer_text = self.font.render(
            f"Time: {seconds_left}s", True, WHITE
        )
        screen.blit(timer_text, (self.width - 140, 10))

        acc_text = self.font.render(
            f"Accuracy: {self.accuracy()}%", True, WHITE
        )
        screen.blit(
            acc_text, (self.width // 2 - 90, 10)
        )

        # Display the Game Over screen
        if self.game_over:
            overlay = pygame.Surface(
                (self.width, self.height), pygame.SRCALPHA
            )
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))

            title_font = pygame.font.SysFont("Arial", 56)
            result_font = pygame.font.SysFont("Arial", 32)
            instruction_font = pygame.font.SysFont("Arial", 24)

            title = title_font.render(
                "GAME OVER", True, WHITE
            )
            final_score = result_font.render(
                f"Final Score: {self.score}", True, WHITE
            )
            final_accuracy = result_font.render(
                f"Final Accuracy: {self.accuracy()}%", True, WHITE
            )
            instruction = instruction_font.render(
                "Round complete!", True, WHITE
            )

            screen.blit(
                title,
                title.get_rect(
                    center=(self.width // 2, self.height // 2 - 100)
                )
            )
            screen.blit(
                final_score,
                final_score.get_rect(
                    center=(self.width // 2, self.height // 2 - 30)
                )
            )
            screen.blit(
                final_accuracy,
                final_accuracy.get_rect(
                    center=(self.width // 2, self.height // 2 + 20)
                )
            )
            screen.blit(
                instruction,
                instruction.get_rect(
                    center=(self.width // 2, self.height // 2 + 90)
                )
            )
