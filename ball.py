import pygame


class Ball:
    def __init__(self,
                 window_center,
                 color,
                 radius,
                 position_x=0,
                 position_y=0,
                 velocity_x=0,
                 velocity_y=0):
        self.window_center = window_center
        self.color = color
        self.radius = radius
        # Position is relative to the top left window corner. Not the position inside the window!
        # This simplifies the math.
        self.position = pygame.Vector2(position_x, position_y)
        self.velocity = pygame.Vector2(velocity_x, velocity_y)
        self.previous_position = pygame.Vector2(self.position)
        self.path = []
        # Path contains the first point twice because pygame.draw.lines
        # needs at least two points.
        self.extend_path(self.previous_position)
        self.extend_path(self.position)

    def update(self, dt, circle_radius, acceleration, acceleration_half, bounce_factor):
        self.previous_position.update(self.position)
        self.velocity += acceleration
        self.position += (self.velocity - acceleration_half) * dt
        max_radius = circle_radius - self.radius
        while self.position.length() >= max_radius:
            self.bounce(max_radius, bounce_factor)
        self.extend_path(self.position)

    def bounce(self, max_radius, bounce_factor):
        previous_length = self.previous_position.length()
        length = self.position.length()
        # collision point = normal vector for reflection
        normal = self.previous_position.lerp(
            self.position,
            (max_radius - previous_length) / (length - previous_length)
        )
        self.extend_path(normal)
        self.previous_position = (self.previous_position - normal).reflect(normal) + normal
        self.position = (self.position - normal).reflect(normal) + normal
        self.velocity.reflect_ip(normal)
        self.velocity *= bounce_factor

    def extend_path(self, pos):
        self.path.append(pos + self.window_center)
