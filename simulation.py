import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import pygame
import pygame.gfxdraw

from ball import Ball


class Simulation:
    def __init__(self):
        pygame.init()
        self.window_rect = pygame.Rect(0, 0, 1000, 800)
        self.window_center = self.window_rect.center
        self.window = pygame.display.set_mode(self.window_rect.size)
        self.balls = tuple()
        self.background_color = (32, 32, 32)
        self.circle_color = (230, 230, 230)
        self.circle_radius = 350
        self.g = pygame.Vector2(0, 1500)
        self.reset_balls()
        # Simulation is inaccurate and keeps adding energy with every bounce. I could
        # use a proper integration but its easier to just remove some
        # percentage from the velocity.
        self.bounce_factor = 0.99
        self.paused = True

    def run(self):
        clock = pygame.time.Clock()
        steps_per_frame = 10
        while True:
            dt = clock.tick(60) / 1000  # seconds

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return
                    elif event.key == pygame.K_SPACE:
                        self.paused = not self.paused
                    elif event.key == pygame.K_r:
                        self.reset_balls()

            if not self.paused:
                dt_step = dt / steps_per_frame
                gravity = self.g * dt_step
                gravity_half = gravity / 2
                for ball in self.balls:
                    for _ in range(steps_per_frame):
                        ball.update(
                            dt_step,
                            gravity,
                            gravity_half,
                            self.bounce_factor
                        )
                    ball.extend_path()

            self.window.fill(self.background_color)
            pygame.gfxdraw.aacircle(
                self.window,
                self.window_center[0],
                self.window_center[1],
                self.circle_radius,
                self.circle_color
            )
            for ball in self.balls:
                pygame.draw.aalines(
                    self.window,
                    ball.color,
                    False,
                    ball.path,
                    1
                )
            for ball in self.balls:
                pygame.draw.circle(
                    self.window,
                    ball.color,
                    ball.position + self.window_center,
                    ball.radius
                )
            pygame.display.flip()

    def reset_balls(self):
        self.balls = (
            Ball(self.window_center, self.circle_radius, pygame.Color("#00ffff"), 10, 0.1, -200),
            Ball(self.window_center, self.circle_radius, pygame.Color("#ff00ff"), 10, 0.2, -200),
            Ball(self.window_center, self.circle_radius, pygame.Color("#ffff00"), 10, 0.3, -200),
            Ball(self.window_center, self.circle_radius, pygame.Color("#ff0000"), 10, 0.4, -200),
            Ball(self.window_center, self.circle_radius, pygame.Color("#00ff00"), 10, 0.5, -200),
            Ball(self.window_center, self.circle_radius, pygame.Color("#0000ff"), 10, 0.6, -200)
        )


Simulation().run()
