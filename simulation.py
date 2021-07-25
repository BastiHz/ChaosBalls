import pygame
import pygame.gfxdraw

from ball import Ball


class Simulation:
    def __init__(self):
        pygame.init()
        self.window_rect = pygame.Rect(0, 0, 1000, 800)
        self.window_center = self.window_rect.center
        self.window = pygame.display.set_mode(self.window_rect.size)
        self.balls = (
            Ball(self.window_center, pygame.Color("#00ffff"), 10, 0.1, -200),
            Ball(self.window_center, pygame.Color("#ff00ff"), 10, 0.2, -200),
            # Ball(self.window_center, pygame.Color("#ffff00"), 10, 0.3, -200),
            # Ball(self.window_center, pygame.Color("#ff0000"), 10, 0.4, -200),
            # Ball(self.window_center, pygame.Color("#00ff00"), 10, 0.5, -200),
            # Ball(self.window_center, pygame.Color("#0000ff"), 10, 0.6, -200)
        )
        self.background_color = (32, 32, 32)
        self.circle_color = (230, 230, 230)
        self.circle_radius = 350
        self.g = pygame.Vector2(0, 1500)
        # Simulation is inaccurate and keeps adding energy with every bounce. I could
        # use a proper integration like euler but its easier to just remove some
        # percentage from the velocity.
        self.bounce_factor = 0.98

    def run(self):
        clock = pygame.time.Clock()
        paused = True
        while True:
            dt = clock.tick(60) / 1000  # seconds

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return
                    elif event.key == pygame.K_SPACE:
                        paused = not paused

            if not paused:
                gravity = self.g * dt
                gravity_half = gravity / 2
                for ball in self.balls:
                    ball.update(
                        dt,
                        self.circle_radius,
                        gravity,
                        gravity_half,
                        self.bounce_factor
                    )
                    # ball.extend_path(self.window_center)

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
                x, y = ball.position + self.window_center
                x = int(x)
                y = int(y)
                pygame.draw.circle(
                    self.window,
                    ball.color,
                    (x, y),
                    ball.radius
                )
                # pygame.gfxdraw.aacircle(
                #     self.window,
                #     x,
                #     y,
                #     ball.radius,
                #     ball.color
                # )
                # pygame.gfxdraw.filled_circle(
                #     self.window,
                #     x,
                #     y,
                #     ball.radius,
                #     ball.color
                # )
            pygame.display.flip()


Simulation().run()
