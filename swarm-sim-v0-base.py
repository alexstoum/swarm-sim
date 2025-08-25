import pygame
import random
import math

# --- Simulation Parameters ---
WIDTH, HEIGHT = 800, 600
NUM_ROBOTS = 15
ROBOT_RADIUS = 5
SPEED = 2
TURN_ANGLE = 0.2  # max random turn

# --- Robot Class ---
class Robot:
    def __init__(self):
        self.x = random.randint(100, WIDTH - 100)
        self.y = random.randint(100, HEIGHT - 100)
        self.angle = random.uniform(0, 2 * math.pi)

    def move(self):
        # Random small turn
        self.angle += random.uniform(-TURN_ANGLE, TURN_ANGLE)

        # Forward step
        self.x += SPEED * math.cos(self.angle)
        self.y += SPEED * math.sin(self.angle)

        # Wall collision (bounce)
        if self.x <= ROBOT_RADIUS or self.x >= WIDTH - ROBOT_RADIUS:
            self.angle = math.pi - self.angle
        if self.y <= ROBOT_RADIUS or self.y >= HEIGHT - ROBOT_RADIUS:
            self.angle = -self.angle

    def draw(self, screen):
        pygame.draw.circle(screen, (0, 200, 0), (int(self.x), int(self.y)), ROBOT_RADIUS)

# --- Main Simulation ---
def run_simulation():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Swarm Simulation")

    robots = [Robot() for _ in range(NUM_ROBOTS)]
    clock = pygame.time.Clock()

    # Coverage map (pixel-based)
    coverage = [[0 for _ in range(HEIGHT)] for _ in range(WIDTH)]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update robots
        for r in robots:
            r.move()

        # Draw
        screen.fill((30, 30, 30))  # background

        for r in robots:
            r.draw(screen)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    run_simulation()
