# Flappy Bird for the micro:bit (MakeCode Python)
# Press A to start, B to flap, and touch the logo to restart after a crash.

BIRD_X = 1
TICK_MS = 220
GRAVITY = 0.35
JUMP_SPEED = -2.0


def draw_game(bird_y, pipe_xs, pipe_gaps, pipe_count):
    basic.clear_screen()

    # Draw the top and bottom parts of each pipe, leaving a two-LED gap.
    for i in range(pipe_count):
        x = pipe_xs[i]
        gap_top = pipe_gaps[i]
        for y in range(5):
            if y < gap_top or y > gap_top + 1:
                led.plot(x, y)

    led.plot(BIRD_X, bird_y)


def wait_for_logo_release():
    # Avoid treating the same long touch as multiple restart presses.
    while input.logo_is_pressed():
        basic.pause(50)


def play_game():
    bird_y = 2.0
    velocity = 0.0
    pipe_xs = []
    pipe_gaps = []
    pipe_count = 0
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

        # Move existing pipes one LED to the left.
        remaining_xs = []
        remaining_gaps = []
        remaining_count = 0
        for i in range(pipe_count):
            x = pipe_xs[i] - 1
            gap_top = pipe_gaps[i]

            if x == BIRD_X and not (gap_top <= bird_row <= gap_top + 1):
                crashed = True

            if x == BIRD_X - 1:
                score += 1

            if x >= 0:
                remaining_xs.append(x)
                remaining_gaps.append(gap_top)
                remaining_count += 1
        pipe_xs = remaining_xs
        pipe_gaps = remaining_gaps
        pipe_count = remaining_count

        # Add a new pipe from the right every six ticks.
        frames += 1
        if frames % 6 == 0:
            pipe_xs.append(4)
            pipe_gaps.append(Math.random_range(1, 2))
            pipe_count += 1

        if not crashed:
            draw_game(bird_row, pipe_xs, pipe_gaps, pipe_count)
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
