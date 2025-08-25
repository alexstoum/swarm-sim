import pygame
import random
import math

# --- Parameters ---
WIDTH, HEIGHT = 800, 600
NUM_ROBOTS = 25
ROBOT_RADIUS = 6
SPEED = 2.2
MAX_TURN = 0.25
RANDOM_WIGGLE = 0.06

GOAL_ATTRACTION = 0.10      # weight pulling towards the goal
GOAL_REACH_RADIUS = 20      # stop jitter near goal

BG = (25, 25, 30)
ROBOT_COLOR = (0, 220, 120)
GOAL_COLOR = (240, 60, 60)

class Robot:
    def __init__(self):
        self.x = random.uniform(ROBOT_RADIUS, WIDTH - ROBOT_RADIUS)
        self.y = random.uniform(ROBOT_RADIUS, HEIGHT - ROBOT_RADIUS)
        self.angle = random.uniform(0, 2 * math.pi)

    def move(self, goal):
        # Random small wiggle
        base_x = math.cos(self.angle) + random.uniform(-RANDOM_WIGGLE, RANDOM_WIGGLE)
        base_y = math.sin(self.angle) + random.uniform(-RANDOM_WIGGLE, RANDOM_WIGGLE)

        # Goal steering (vector toward goal)
        gx = goal[0] - self.x
        gy = goal[1] - self.y
        gd = math.hypot(gx, gy)
        if gd > 1e-6:
            gx /= gd
            gy /= gd

        # Blend forward direction with goal attraction
        dir_x = base_x + GOAL_ATTRACTION * gx
        dir_y = base_y + GOAL_ATTRACTION * gy
        desired_angle = math.atan2(dir_y, dir_x)

        # Limit turn
        da = (desired_angle - self.angle + math.pi) % (2 * math.pi) - math.pi
        da = max(-MAX_TURN, min(MAX_TURN, da))
        self.angle += da

        # Slow down near goal to reduce orbiting
        speed = SPEED * (0.4 if gd < GOAL_REACH_RADIUS else 1.0)

        # Move
        self.x += speed * math.cos(self.angle)
        self.y += speed * math.sin(self.angle)

        # Bounce off walls
        if self.x <= ROBOT_RADIUS or self.x >= WIDTH - ROBOT_RADIUS:
            self.angle = math.pi - self.angle
        if self.y <= ROBOT_RADIUS or self.y >= HEIGHT - ROBOT_RADIUS:
            self.angle = -self.angle

        # Clamp
        self.x = max(ROBOT_RADIUS, min(WIDTH - ROBOT_RADIUS, self.x))
        self.y = max(ROBOT_RADIUS, min(HEIGHT - ROBOT_RADIUS, self.y))

    def draw(self, screen):
        pygame.draw.circle(screen, ROBOT_COLOR, (int(self.x), int(self.y)), ROBOT_RADIUS)

def run():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Swarm — Goal Seeking (click to set goal)")
    clock = pygame.time.Clock()
    robots = [Robot() for _ in range(NUM_ROBOTS)]
    goal = (WIDTH // 2, HEIGHT // 2)

    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            if e.type == pygame.MOUSEBUTTONDOWN:
                goal = pygame.mouse.get_pos()

        for r in robots:
            r.move(goal)

        screen.fill(BG)
        # draw goal
        pygame.draw.circle(screen, GOAL_COLOR, (int(goal[0]), int(goal[1])), 8)
        # robots
        for r in robots:
            r.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    run()
