# Flappy Bird for the micro:bit (MakeCode Python)
# Press A to start, B to flap, and touch the logo to restart after a crash.

BIRD_X = 1
TICK_MS = 220
GRAVITY = 0.35
JUMP_SPEED = -2.0


def draw_game(bird_y, pipe_x, gap_top):
    basic.clear_screen()

    # Draw the top and bottom parts of the pipe, leaving a two-LED gap.
    if pipe_x >= 0:
        for y in range(5):
            if y < gap_top or y > gap_top + 1:
                led.plot(pipe_x, y)

    led.plot(BIRD_X, bird_y)


def wait_for_logo_release():
    # Avoid treating the same long touch as multiple restart presses.
    while input.logo_is_pressed():
        basic.pause(50)


def play_game():
    bird_y = 2.0
    velocity = 0.0
    pipe_x = -1
    gap_top = 1
    score = 0
    frames = 0
    previous_b = False
    crashed = False

    while not crashed:
        b_now = input.button_is_pressed(Button.B)
        if b_now and not previous_b:
            velocity = JUMP_SPEED
        previous_b = b_now

        # Apply gravity and keep the bird within the 5x5 display.
        velocity += GRAVITY
        bird_y += velocity
        bird_row = int(bird_y)
        if bird_row < 0 or bird_row > 4:
            crashed = True

        # Move the current pipe one LED to the left.
        if pipe_x >= 0:
            pipe_x -= 1
            if pipe_x == BIRD_X and not (gap_top <= bird_row <= gap_top + 1):
                crashed = True
            if pipe_x == BIRD_X - 1:
                score += 1

        # Pipes are spaced far enough apart that only one is on screen at once.
        frames += 1
        if pipe_x < 0 and frames % 6 == 0:
            pipe_x = 4
            gap_top = Math.random_range(1, 2)

        if not crashed:
            draw_game(bird_row, pipe_x, gap_top)
            basic.pause(TICK_MS)

    # Show the final score, then accept a logo touch during the five-second
    # game-over period. If untouched, a fresh game starts automatically.
    basic.clear_screen()
    basic.show_string("SCORE")
    basic.show_number(score)
    basic.show_icon(IconNames.NO)

    elapsed = 0
    while elapsed < 5000:
        if input.logo_is_pressed():
            wait_for_logo_release()
            return
        basic.pause(50)
        elapsed += 50


basic.show_string("A=GO")
while not input.button_is_pressed(Button.A):
    basic.pause(50)

while True:
    play_game()
