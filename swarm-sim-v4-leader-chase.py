import pygame
import random
import math

# --- Parameters ---
WIDTH, HEIGHT = 900, 600
NUM_FOLLOWERS = 22
RADIUS = 6
LEADER_SPEED = 3.0
FOLLOWER_SPEED = 2.5
MAX_TURN = 0.28

SEPARATION_RANGE = 38
SEPARATION_STRENGTH = 0.8
PURSUIT_WEIGHT = 0.18
RANDOM_WIGGLE = 0.06

BG = (23, 23, 28)
LEADER_COLOR = (250, 210, 70)
FOLLOWER_COLOR = (80, 210, 255)
HEADING_COLOR = (200, 200, 200)

def clamp(val, lo, hi):
    return max(lo, min(hi, val))

class Agent:
    def __init__(self, x=None, y=None, angle=None):
        self.x = x if x is not None else random.uniform(RADIUS, WIDTH - RADIUS)
        self.y = y if y is not None else random.uniform(RADIUS, HEIGHT - RADIUS)
        self.angle = angle if angle is not None else random.uniform(0, 2*math.pi)

    def _bounce_and_clamp(self):
        if self.x <= RADIUS or self.x >= WIDTH - RADIUS:
            self.angle = math.pi - self.angle
        if self.y <= RADIUS or self.y >= HEIGHT - RADIUS:
            self.angle = -self.angle
        self.x = clamp(self.x, RADIUS, WIDTH - RADIUS)
        self.y = clamp(self.y, RADIUS, HEIGHT - RADIUS)

    def draw(self, screen, color, show_heading=False):
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), RADIUS)
        if show_heading:
            hx = self.x + 12*math.cos(self.angle)
            hy = self.y + 12*math.sin(self.angle)
            pygame.draw.line(screen, HEADING_COLOR, (int(self.x), int(self.y)), (int(hx), int(hy)), 2)

class Leader(Agent):
    def move(self, keys, dash=False):
        speed = LEADER_SPEED * (1.8 if dash else 1.0)
        ax, ay = 0, 0
        if keys[pygame.K_w] or keys[pygame.K_UP]:    ay -= 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:  ay += 1
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:  ax -= 1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]: ax += 1
        if ax != 0 or ay != 0:
            self.angle = math.atan2(ay, ax)
            self.x += speed * math.cos(self.angle)
            self.y += speed * math.sin(self.angle)
        else:
            # glide forward a bit if no key pressed
            self.x += 0.6 * math.cos(self.angle)
            self.y += 0.6 * math.sin(self.angle)

        self._bounce_and_clamp()

class Follower(Agent):
    def move(self, leader, all_followers):
        # Separation from other followers
        sep_x, sep_y = 0.0, 0.0
        for other in all_followers:
            if other is self: 
                continue
            dx = self.x - other.x
            dy = self.y - other.y
            d = math.hypot(dx, dy)
            if 0 < d < SEPARATION_RANGE:
                w = (SEPARATION_RANGE - d) / SEPARATION_RANGE
                sep_x += (dx / d) * w * SEPARATION_STRENGTH
                sep_y += (dy / d) * w * SEPARATION_STRENGTH

        # Pursuit toward leader
        lx = leader.x - self.x
        ly = leader.y - self.y
        ld = math.hypot(lx, ly)
        if ld > 1e-6:
            lx /= ld
            ly /= ld

        # Combine: forward dir + pursuit + separation + a bit of noise
        dir_x = math.cos(self.angle) + PURSUIT_WEIGHT * lx + sep_x + random.uniform(-RANDOM_WIGGLE, RANDOM_WIGGLE)
        dir_y = math.sin(self.angle) + PURSUIT_WEIGHT * ly + sep_y + random.uniform(-RANDOM_WIGGLE, RANDOM_WIGGLE)

        desired = math.atan2(dir_y, dir_x)
        da = (desired - self.angle + math.pi) % (2*math.pi) - math.pi
        da = clamp(da, -MAX_TURN, MAX_TURN)
        self.angle += da

        # Move
        self.x += FOLLOWER_SPEED * math.cos(self.angle)
        self.y += FOLLOWER_SPEED * math.sin(self.angle)

        self._bounce_and_clamp()

def run():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Leader & Followers — Chase Mode (WASD / arrows, Space = dash, H = headings)")
    clock = pygame.time.Clock()

    leader = Leader(WIDTH/2, HEIGHT/2)
    followers = [Follower() for _ in range(NUM_FOLLOWERS)]
    show_heading = False

    running = True
    while running:
        dash = False
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_h:
                    show_heading = not show_heading
                if e.key == pygame.K_SPACE:
                    dash = True

        keys = pygame.key.get_pressed()
        # Move agents
        leader.move(keys, dash=dash)
        for f in followers:
            f.move(leader, followers)

        # Draw
        screen.fill(BG)
        leader.draw(screen, LEADER_COLOR, show_heading)
        for f in followers:
            f.draw(screen, FOLLOWER_COLOR, show_heading)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    run()
