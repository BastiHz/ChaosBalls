import pygame


class Ball:
    def __init__(self,
                 window_center,
                 circle_radius,
                 color,
                 radius,
                 position_x=0,
                 position_y=0,
                 velocity_x=0,
                 velocity_y=0):
        self.window_center = window_center
        self.max_length = circle_radius - radius
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

    def update(self, dt, acceleration, acceleration_half, bounce_factor):
        self.previous_position.update(self.position)
        self.velocity += acceleration
        self.position += (self.velocity - acceleration_half) * dt
        current_length = self.position.length()
        if current_length >= self.max_length:  # bounce
            previous_length = self.previous_position.length()
            ratio = (self.max_length - previous_length) / (current_length - previous_length)
            # collision point = normal vector for reflection
            normal = self.previous_position.lerp(self.position, ratio)
            self.extend_path(normal)
            self.previous_position.update(normal)
            self.position = (self.position - normal).reflect(normal) + normal
            # Try to correct the acceleraton. The ball has been reflected, which means that
            # for part of the last frame the acceleration downwards grew too high.
            self.velocity -= acceleration * (1 - ratio)
            self.velocity *= bounce_factor
            self.velocity.reflect_ip(normal)

    def extend_path(self, pos=None):
        # Convert world position to position in screen space for the path.
        if pos is None:
            pos = self.position
        self.path.append(pos + self.window_center)
