import pygame
import sys
import random

# — Initialization —
pygame.init()
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")
CLOCK = pygame.time.Clock()
FPS = 60

# — Colors —
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# — Game settings —
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
PADDLE_SPEED = 6
BALL_SIZE = 20
BALL_SPEED_X = 5
BALL_SPEED_Y = 5

# — Game objects —
left_paddle = pygame.Rect(10, (HEIGHT - PADDLE_HEIGHT) // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
right_paddle = pygame.Rect(WIDTH - 10 - PADDLE_WIDTH, (HEIGHT - PADDLE_HEIGHT) // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect((WIDTH - BALL_SIZE) // 2, (HEIGHT - BALL_SIZE) // 2, BALL_SIZE, BALL_SIZE)

ball_vel = [BALL_SPEED_X * random.choice((1, -1)), BALL_SPEED_Y * random.choice((1, -1))]

score_left = 0
score_right = 0
FONT = pygame.font.Font(None, 36)


def reset_ball():
    ball.center = (WIDTH // 2, HEIGHT // 2)
    ball_vel[0] *= random.choice((1, -1))
    ball_vel[1] *= random.choice((1, -1))


def draw():
    SCREEN.fill(BLACK)
    pygame.draw.rect(SCREEN, WHITE, left_paddle)
    pygame.draw.rect(SCREEN, WHITE, right_paddle)
    pygame.draw.ellipse(SCREEN, WHITE, ball)
    # Draw center line
    pygame.draw.aaline(SCREEN, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))
    # Draw scores
    left_text = FONT.render(str(score_left), True, WHITE)
    right_text = FONT.render(str(score_right), True, WHITE)
    SCREEN.blit(left_text, (WIDTH * 0.25, 20))
    SCREEN.blit(right_text, (WIDTH * 0.75, 20))
    pygame.display.flip()


def handle_input():
    keys = pygame.key.get_pressed()
    # Left paddle: W, S
    if keys[pygame.K_w] and left_paddle.top > 0:
        left_paddle.y -= PADDLE_SPEED
    if keys[pygame.K_s] and left_paddle.bottom < HEIGHT:
        left_paddle.y += PADDLE_SPEED
    # Right paddle: Up, Down
    if keys[pygame.K_UP] and right_paddle.top > 0:
        right_paddle.y -= PADDLE_SPEED
    if keys[pygame.K_DOWN] and right_paddle.bottom < HEIGHT:
        right_paddle.y += PADDLE_SPEED


def update_ball():
    global score_left, score_right

    ball.x += ball_vel[0]
    ball.y += ball_vel[1]

    # Bounce off top / bottom
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_vel[1] = -ball_vel[1]

    # Check paddles
    if ball.colliderect(left_paddle) and ball_vel[0] < 0:
        ball_vel[0] = -ball_vel[0]
    if ball.colliderect(right_paddle) and ball_vel[0] > 0:
        ball_vel[0] = -ball_vel[0]

    # Check for scoring
    if ball.left <= 0:
        score_right += 1
        reset_ball()
    if ball.right >= WIDTH:
        score_left += 1
        reset_ball()


def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        handle_input()
        update_ball()
        draw()
        CLOCK.tick(FPS)


if __name__ == "__main__":
    main()
