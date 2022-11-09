import pygame
import pymunk
import pymunk.pygame_util
import math, time, sys

pygame.init()
width, height = 1700, 1000
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pong!")
white = (255, 255, 255)
green = (50, 168, 82)
black = (0, 0, 0)
red = (200, 0, 0)
grey = (105, 105, 105)
blue = (66, 185, 189)
elastic = 1.03
FONT = pygame.font.Font(None, 40)


def draw(space, window, draw_options, ball, p1_score, p2_score):
    window.fill(blue)

    if ball.body.position[0] < 0 or ball.body.position[0] > width:
        if ball.body.position[0] < 0:
            p2_score += 1
        else:
            p1_score += 1
        space.remove(ball, ball.body)
        ball = False
    window.blit(
        FONT.render(
            str(p1_score),
            False,
            (0, 0, 0),
        ),
        (width / 4 - 20, 30),
    )
    window.blit(
        FONT.render(
            str(p2_score),
            False,
            (0, 0, 0),
        ),
        (width / 1.25 - 20, 30),
    )
    space.debug_draw(draw_options)
    pygame.display.update()
    return ball, p1_score, p2_score


def create_boundaries(space, width, height):
    rects = [
        [(width / 2, height - 10), (width, 20)],
        [(width / 2, 10), (width, 20)],
    ]
    for pos, size in rects:
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = pos

        shape = pymunk.Poly.create_box(body, size)
        shape.elasticity = elastic
        shape.friction = 0
        space.add(body, shape)


def create_ball(space, radius, mass, pos):
    body = pymunk.Body(body_type=pymunk.Body.DYNAMIC)
    body.position = pos
    # SHAPE STATS
    shape = pymunk.Circle(body, radius)
    shape.mass = mass
    shape.color = (*red, 100)
    shape.elasticity = elastic
    shape.friction = 0
    # ADD TO SIMULATION
    space.add(body, shape)
    return shape


def create_paddles(space, position, color):
    body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
    body.position = position
    ###
    shape = pymunk.Poly.create_box(body, size=(20, 120))
    # shape.mass = 1000
    shape.friction = 0
    shape.elasticity = elastic
    shape.color = (*color, 100)
    space.add(body, shape)
    return shape


def reset(
    space,
    p1_score,
    p2_score,
    ball=None,
    paddle1=None,
    paddle2=None,
    playing=False,
):
    if playing:
        space.remove(paddle1, paddle1.body)
        space.remove(paddle2, paddle2.body)

    ball = create_ball(space, 18, 10, (width / 2, height / 2))
    paddle1, paddle2 = create_paddles(space, (50, height / 2), red), create_paddles(
        space, (width - 50, height / 2), green
    )

    ball.body.apply_impulse_at_local_point((3000, 3000), (0, 0))

    return ball, paddle1, paddle2


def play():
    p1_score, p2_score = 0, 0
    run = True
    clock = pygame.time.Clock()
    FPS = 60
    dt = 1 / FPS
    space = pymunk.Space()
    space.gravity = (0, 0)
    create_boundaries(space, width, height)
    draw_options = pymunk.pygame_util.DrawOptions(window)
    (
        ball,
        paddle1,
        paddle2,
    ) = reset(space, p1_score, p2_score)
    speed = 5
    rotation = 0.03
    while run:
        keys = pygame.key.get_pressed()  # checking pressed keys
        pos1 = paddle1.body.position
        pos2 = paddle2.body.position

        # LEFT PLAYER CONTROLS
        if keys[pygame.K_w]:
            paddle1.body.position = (pos1[0], pos1[1] - speed)
            pos1 = paddle1.body.position
        if keys[pygame.K_s]:
            paddle1.body.position = (pos1[0], pos1[1] + speed)
            pos1 = paddle1.body.position
        if keys[pygame.K_a]:
            paddle1.body.position = (pos1[0] - speed, pos1[1])
            pos1 = paddle1.body.position
        if keys[pygame.K_d]:
            paddle1.body.position = (pos1[0] + speed, pos1[1])
            pos1 = paddle1.body.position
        if keys[pygame.K_c]:
            paddle1.body.angle -= rotation
        if keys[pygame.K_v]:
            paddle1.body.angle += rotation

        # RIGHT PLAYER CONTROLS
        if keys[pygame.K_UP]:
            paddle2.body.position = (pos2[0], pos2[1] - speed)
            pos2 = paddle2.body.position
        if keys[pygame.K_DOWN]:
            paddle2.body.position = (pos2[0], pos2[1] + speed)
            pos2 = paddle2.body.position
        if keys[pygame.K_LEFT]:
            paddle2.body.position = (pos2[0] - speed, pos2[1])
            pos2 = paddle2.body.position
        if keys[pygame.K_RIGHT]:
            paddle2.body.position = (pos2[0] + speed, pos2[1])
            pos2 = paddle2.body.position
        if keys[pygame.K_SLASH]:
            paddle2.body.angle -= rotation
        if keys[pygame.K_RSHIFT]:
            paddle2.body.angle += rotation

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        if not ball:
            (ball, paddle1, paddle2,) = reset(
                space,
                p1_score,
                p2_score,
                ball,
                paddle1,
                paddle2,
                True,
            )
        ball, p1_score, p2_score = draw(
            space, window, draw_options, ball, p1_score, p2_score
        )
        space.step(dt)
        clock.tick(FPS)
    pygame.quit()


if __name__ == "__main__":
    play()
