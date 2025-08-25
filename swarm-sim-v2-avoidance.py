import pygame
import random
import math

# --- Parameters ---
WIDTH, HEIGHT = 800, 600
NUM_ROBOTS = 25
ROBOT_RADIUS = 6
SPEED = 2.2
MAX_TURN = 0.25             # max turn (radians) per frame from steering
REPULSION_RANGE = 40.0      # how far robots "feel" each other
REPULSION_STRENGTH = 0.9    # bigger = stronger push apart
RANDOM_WIGGLE = 0.1         # small noise so they don’t freeze

BG = (25, 25, 30)
ROBOT_COLOR = (0, 220, 120)

class Robot:
    def __init__(self):
        self.x = random.uniform(ROBOT_RADIUS, WIDTH - ROBOT_RADIUS)
        self.y = random.uniform(ROBOT_RADIUS, HEIGHT - ROBOT_RADIUS)
        self.angle = random.uniform(0, 2 * math.pi)

    def move(self, robots):
        # --- Separation / Repulsion steering vector (sum over neighbors) ---
        steer_x, steer_y = 0.0, 0.0
        for other in robots:
            if other is self:
                continue
            dx = self.x - other.x
            dy = self.y - other.y
            d = math.hypot(dx, dy)
            if 0 < d < REPULSION_RANGE:
                # inverse-distance weighting (stronger when closer)
                s = (REPULSION_RANGE - d) / REPULSION_RANGE
                s *= REPULSION_STRENGTH
                steer_x += (dx / d) * s
                steer_y += (dy / d) * s

        # Convert steering vector to desired heading
        desired_angle = math.atan2(
            math.sin(self.angle) + steer_y + random.uniform(-RANDOM_WIGGLE, RANDOM_WIGGLE),
            math.cos(self.angle) + steer_x + random.uniform(-RANDOM_WIGGLE, RANDOM_WIGGLE)
        )

        # Limit turn rate (to avoid jittery snaps)
        da = (desired_angle - self.angle + math.pi) % (2 * math.pi) - math.pi
        da = max(-MAX_TURN, min(MAX_TURN, da))
        self.angle += da

        # Move forward
        self.x += SPEED * math.cos(self.angle)
        self.y += SPEED * math.sin(self.angle)

        # Wall bounce (reflect heading)
        if self.x <= ROBOT_RADIUS or self.x >= WIDTH - ROBOT_RADIUS:
            self.angle = math.pi - self.angle
        if self.y <= ROBOT_RADIUS or self.y >= HEIGHT - ROBOT_RADIUS:
            self.angle = -self.angle

        # Clamp inside
        self.x = max(ROBOT_RADIUS, min(WIDTH - ROBOT_RADIUS, self.x))
        self.y = max(ROBOT_RADIUS, min(HEIGHT - ROBOT_RADIUS, self.y))

    def draw(self, screen):
        pygame.draw.circle(screen, ROBOT_COLOR, (int(self.x), int(self.y)), ROBOT_RADIUS)

def run():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Swarm — Collision Avoidance")
    clock = pygame.time.Clock()
    robots = [Robot() for _ in range(NUM_ROBOTS)]

    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False

        for r in robots:
            r.move(robots)

        screen.fill(BG)
        for r in robots:
            r.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    run()
