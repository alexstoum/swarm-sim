import pygame
import random
import math
import numpy as np

# --- Parameters ---
WIDTH, HEIGHT = 800, 600
NUM_ROBOTS = 20
ROBOT_RADIUS = 5
SPEED = 2
TURN_ANGLE = 0.3

GRID_SIZE = 10   # resolution of coverage map

class Robot:
    def __init__(self):
        self.x = random.uniform(ROBOT_RADIUS, WIDTH - ROBOT_RADIUS)
        self.y = random.uniform(ROBOT_RADIUS, HEIGHT - ROBOT_RADIUS)
        self.angle = random.uniform(0, 2 * math.pi)

    def move(self):
        self.angle += random.uniform(-TURN_ANGLE, TURN_ANGLE)
        self.x += SPEED * math.cos(self.angle)
        self.y += SPEED * math.sin(self.angle)

        # Bounce off walls
        if self.x <= ROBOT_RADIUS or self.x >= WIDTH - ROBOT_RADIUS:
            self.angle = math.pi - self.angle
        if self.y <= ROBOT_RADIUS or self.y >= HEIGHT - ROBOT_RADIUS:
            self.angle = -self.angle

    def draw(self, screen):
        pygame.draw.circle(screen, (0, 255, 0), (int(self.x), int(self.y)), ROBOT_RADIUS)


def run_simulation():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Swarm Coverage Heatmap")

    robots = [Robot() for _ in range(NUM_ROBOTS)]
    clock = pygame.time.Clock()

    # Coverage map (2D grid)
    cols = WIDTH // GRID_SIZE
    rows = HEIGHT // GRID_SIZE
    coverage = np.zeros((rows, cols))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Move robots
        for r in robots:
            r.move()

            # Update coverage grid
            cx, cy = int(r.x // GRID_SIZE), int(r.y // GRID_SIZE)
            if 0 <= cy < rows and 0 <= cx < cols:
                coverage[cy, cx] += 1

        # Draw heatmap (dark = unvisited, bright = visited)
        screen.fill((0, 0, 0))
        max_val = np.max(coverage) if np.max(coverage) > 0 else 1
        for y in range(rows):
            for x in range(cols):
                intensity = int((coverage[y, x] / max_val) * 255)
                color = (intensity, intensity, intensity)
                pygame.draw.rect(screen, color, (x*GRID_SIZE, y*GRID_SIZE, GRID_SIZE, GRID_SIZE))

        # Draw robots on top
        for r in robots:
            r.draw(screen)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    run_simulation()
