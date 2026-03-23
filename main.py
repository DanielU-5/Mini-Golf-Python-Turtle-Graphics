import turtle
import time
import math
import random

##########
# CONSTANTS
##########
ball_colors = ["white", "red", "blue", "yellow", "orange"]

# Each hole defines: ball start, hole position, par, and a list of obstacles.
# Each obstacle has a bottom-left corner position (x, y), width, and height.
HOLES = [
    {
        # Hole 1 - Par 3: simple intro, clear path with a few blocks
        "ball_start": (-300, 0),
        "hole_pos": (280, 0),
        "par": 3,
        "obstacles": [
            {"pos": (-50, -30),  "w": 100, "h": 60},
            {"pos": (120, -180), "w": 80,  "h": 60},
            {"pos": (-150, 100), "w": 80,  "h": 40},
        ],
    },
    {
        # Hole 2 - Par 4: two long walls that funnel the ball into a narrow gap
        "ball_start": (-300, 50),
        "hole_pos": (280, -80),
        "par": 4,
        "obstacles": [
            # Long top wall forcing ball low
            {"pos": (-200, 80),   "w": 280, "h": 20},
            # Long bottom wall forcing ball high
            {"pos": (-50,  -200), "w": 250, "h": 20},
            # Central blocker in the middle — must go around
            {"pos": (30,   -60),  "w": 25,  "h": 160},
            # Near-hole blocker
            {"pos": (170,   20),  "w": 20,  "h": 120},
        ],
    },
    {
        # Hole 3 - Par 5: maze-like layout, ball must weave through tight gaps
        "ball_start": (-300, 0),
        "hole_pos": (280, 0),
        "par": 5,
        "obstacles": [
            # Left section — staggered walls creating a chicane
            {"pos": (-220, -200), "w": 20, "h": 220},
            {"pos": (-120,  -20), "w": 20, "h": 230},
            # Mid section — island blocks to navigate around
            {"pos": (-10,  -150), "w": 70,  "h": 70},
            {"pos": (-10,   80),  "w": 70,  "h": 70},
            # Right section — narrow corridor to the hole
            {"pos": (120,  -200), "w": 20,  "h": 180},
            {"pos": (120,   60),  "w": 20,  "h": 160},
            # Final guard right in front of the hole
            {"pos": (210,  -50),  "w": 20,  "h": 80},
        ],
    },
]

##########
# GAME STATE
##########
dx = 0
dy = 0
strokes = 0
current_hole = 0
total_strokes = 0
game_over = False
obstacle_turtles = []

##########
# SCREEN SETUP
##########
screen = turtle.Screen()
screen.setup(830, 630)
screen.title("Mini Golf")
screen.bgcolor("green")
screen.tracer(0)   # We'll call screen.update() manually for smooth animation

##########
# PERSISTENT TURTLES (reused across holes)
##########

# Fairway background
fairway = turtle.Turtle()
fairway.hideturtle()
fairway.speed(0)

# Border
border = turtle.Turtle()
border.hideturtle()
border.speed(0)

# Hole (black ring + white fill)
outer_hole = turtle.Turtle()
outer_hole.hideturtle()
outer_hole.speed(0)

inner_hole = turtle.Turtle()
inner_hole.hideturtle()
inner_hole.speed(0)

# Ball
ball = turtle.Turtle()
ball.shape("circle")
ball.speed(0)
ball.pu()

# Score / HUD
score_turtle = turtle.Turtle()
score_turtle.hideturtle()
score_turtle.speed(0)
score_turtle.pu()
score_turtle.color("white")

# Hole number display
hole_label = turtle.Turtle()
hole_label.hideturtle()
hole_label.speed(0)
hole_label.pu()
hole_label.color("white")


##########
# DRAWING HELPERS
##########

def draw_fairway():
    fairway.clear()
    fairway.pu()
    fairway.goto(-375, 275)
    fairway.color("#2d8a2d")
    fairway.begin_fill()
    for _ in range(2):
        fairway.fd(750)
        fairway.right(90)
        fairway.fd(550)
        fairway.right(90)
    fairway.end_fill()


def draw_border():
    border.clear()
    border.pu()
    border.pensize(12)
    border.color("#1a5c9e")
    border.goto(-400, 300)
    border.pd()
    border.setheading(0)
    for _ in range(2):
        border.fd(800)
        border.right(90)
        border.fd(600)
        border.right(90)
    border.pu()


def draw_hole(hx, hy):
    outer_hole.clear()
    outer_hole.pu()
    outer_hole.goto(hx, hy)
    outer_hole.dot(38, "black")

    inner_hole.clear()
    inner_hole.pu()
    inner_hole.goto(hx, hy)
    inner_hole.dot(28, "#111111")

    # Small flag pin
    inner_hole.goto(hx, hy)
    inner_hole.pd()
    inner_hole.color("white")
    inner_hole.pensize(2)
    inner_hole.setheading(90)
    inner_hole.fd(30)
    # Flag triangle
    inner_hole.color("red")
    inner_hole.begin_fill()
    inner_hole.setheading(0)
    inner_hole.fd(18)
    inner_hole.setheading(270)
    inner_hole.fd(12)
    inner_hole.setheading(180)
    inner_hole.fd(18)
    inner_hole.end_fill()
    inner_hole.pu()


def draw_obstacle(t, ox, oy, w, h):
    t.clear()
    t.pu()
    t.goto(ox, oy)
    t.color("#1a5c9e")
    t.pd()
    t.begin_fill()
    for _ in range(2):
        t.fd(w)
        t.left(90)
        t.fd(h)
        t.left(90)
    t.end_fill()
    # Highlight edge
    t.pu()
    t.goto(ox, oy)
    t.color("#4a8ecf")
    t.pensize(2)
    t.pd()
    for _ in range(2):
        t.fd(w)
        t.left(90)
        t.fd(h)
        t.left(90)
    t.pu()


def draw_hud():
    score_turtle.clear()
    score_turtle.goto(-380, 240)
    par = HOLES[current_hole]["par"]
    diff = total_strokes + strokes - sum(h["par"] for h in HOLES[:current_hole])
    diff_str = f"+{diff}" if diff > 0 else str(diff) if diff < 0 else "E"
    score_turtle.write(
        f"Hole: {current_hole + 1}/{len(HOLES)}  Strokes: {strokes}  Par: {par}\n"
        f"Total: {total_strokes + strokes} ({diff_str})  |  Press 'r' to reset",
        font=("Arial", 13, "normal")
    )

    hole_label.clear()
    hole_label.goto(300, 240)
    hole_label.write(f"Hole {current_hole + 1}", align="center", font=("Arial", 16, "bold"))


##########
# LEVEL LOADER
##########

def load_hole(hole_index):
    global dx, dy, strokes, current_hole, obstacle_turtles, game_over

    game_over = False
    dx = 0
    dy = 0
    strokes = 0
    current_hole = hole_index
    hole_data = HOLES[hole_index]

    bx, by = hole_data["ball_start"]
    hx, hy = hole_data["hole_pos"]

    # Clear old obstacle turtles
    for t in obstacle_turtles:
        t.clear()
        t.hideturtle()
    obstacle_turtles = []

    # Draw scene layers (order matters!)
    draw_fairway()
    draw_border()
    draw_hole(hx, hy)

    # Draw obstacles
    for obs in hole_data["obstacles"]:
        t = turtle.Turtle()
        t.hideturtle()
        t.speed(0)
        t.pu()
        draw_obstacle(t, obs["pos"][0], obs["pos"][1], obs["w"], obs["h"])
        obstacle_turtles.append(t)

    # Place ball
    ball.color(random.choice(ball_colors))
    ball.goto(bx, by)

    draw_hud()
    screen.update()


##########
# INPUT HANDLERS
##########

def hit(x, y):
    global dx, dy, strokes
    if game_over:
        return
    if abs(dx) > 0.1 or abs(dy) > 0.1:
        return   # Ball still moving

    dx = (x - ball.xcor()) / 65
    dy = (y - ball.ycor()) / 65
    strokes += 1
    draw_hud()


def reset():
    global total_strokes, current_hole
    total_strokes = 0
    current_hole = 0
    load_hole(0)
    main_loop()


screen.listen()
screen.onkey(reset, "r")
screen.onclick(hit)


##########
# END SCREENS
##########

def show_win_screen():
    score_turtle.clear()
    hole_label.clear()

    par_total = sum(h["par"] for h in HOLES)
    diff = total_strokes - par_total
    if diff < 0:
        diff_str = f"{diff} (Under par! 🏆)"
    elif diff == 0:
        diff_str = "Even par"
    else:
        diff_str = f"+{diff} (Over par)"

    msg_t = turtle.Turtle()
    msg_t.hideturtle()
    msg_t.pu()
    msg_t.color("white")
    msg_t.goto(0, 60)
    msg_t.write("🏌️ COURSE COMPLETE! 🏌️", align="center", font=("Arial", 28, "bold"))
    msg_t.goto(0, 10)
    msg_t.write(f"Total strokes: {total_strokes}  |  Par: {par_total}", align="center", font=("Arial", 18, "normal"))
    msg_t.goto(0, -30)
    msg_t.write(diff_str, align="center", font=("Arial", 18, "normal"))
    msg_t.goto(0, -80)
    msg_t.write("Press 'r' to play again", align="center", font=("Arial", 14, "normal"))
    screen.update()


def show_hole_complete():
    """Flash a brief 'hole complete' message before loading next hole."""
    score_turtle.clear()
    msg_t = turtle.Turtle()
    msg_t.hideturtle()
    msg_t.pu()
    msg_t.color("white")
    msg_t.goto(0, 0)
    msg_t.write(
        f"Hole {current_hole + 1} complete!  Strokes: {strokes}",
        align="center", font=("Arial", 22, "bold")
    )
    screen.update()
    time.sleep(1.8)
    msg_t.clear()


def show_too_many_strokes():
    score_turtle.clear()
    hole_label.clear()
    msg_t = turtle.Turtle()
    msg_t.hideturtle()
    msg_t.pu()
    msg_t.color("white")
    msg_t.goto(0, 20)
    msg_t.write("Too many strokes! 😬", align="center", font=("Arial", 26, "bold"))
    msg_t.goto(0, -30)
    msg_t.write("Press 'r' to try again", align="center", font=("Arial", 16, "normal"))
    screen.update()


##########
# MAIN GAME LOOP
##########

def main_loop():
    global dx, dy, strokes, total_strokes, game_over

    hole_data = HOLES[current_hole]
    hx, hy = hole_data["hole_pos"]
    max_strokes = hole_data["par"] + 5   # Generous limit per hole

    while True:
        x = ball.xcor()
        y = ball.ycor()

        # --- Wall collisions ---
        if x > 375 or x < -375:
            dx = -dx * 0.85
        if y > 270 or y < -270:
            dy = -dy * 0.85

        # --- Obstacle collisions ---
        for obs in hole_data["obstacles"]:
            ox, oy = obs["pos"]
            ow, oh = obs["w"], obs["h"]
            # Expand bounds slightly for smoother feel
            if (ox - 5) < x < (ox + ow + 5) and (oy - 5) < y < (oy + oh + 5):
                # Determine which axis to bounce on
                overlap_left   = x - ox
                overlap_right  = (ox + ow) - x
                overlap_bottom = y - oy
                overlap_top    = (oy + oh) - y
                min_overlap = min(overlap_left, overlap_right, overlap_bottom, overlap_top)
                if min_overlap in (overlap_left, overlap_right):
                    dx = -dx * 0.85
                else:
                    dy = -dy * 0.85

        # --- Move ball ---
        ball.goto(x + dx, y + dy)

        # --- Friction ---
        dx *= 0.985
        dy *= 0.985

        # Stop tiny drift
        if abs(dx) < 0.05:
            dx = 0
        if abs(dy) < 0.05:
            dy = 0

        screen.update()

        # --- Win condition: ball in hole ---
        if math.dist((ball.xcor(), ball.ycor()), (hx, hy)) < 13:
            dx = 0
            dy = 0
            ball.goto(hx, hy)
            screen.update()
            total_strokes += strokes

            if current_hole + 1 < len(HOLES):
                show_hole_complete()
                load_hole(current_hole + 1)
                # Restart the loop for the new hole
                main_loop()
                return
            else:
                show_win_screen()
                game_over = True
                return

        # --- Lose condition: too many strokes ---
        elif strokes >= max_strokes and abs(dx) < 0.05 and abs(dy) < 0.05:
            dx = 0
            dy = 0
            show_too_many_strokes()
            game_over = True
            return

        time.sleep(0.008)


##########
# MENU
##########

def show_menu():
    menu_turtles = []

    def make(color="white"):
        t = turtle.Turtle()
        t.hideturtle()
        t.pu()
        t.color(color)
        t.speed(0)
        menu_turtles.append(t)
        return t

    # Background
    bg = make("#1a5c1a")
    bg.goto(-375, 275)
    bg.begin_fill()
    for _ in range(2):
        bg.fd(750)
        bg.right(90)
        bg.fd(550)
        bg.right(90)
    bg.end_fill()

    # Border
    brd = make("#1a5c9e")
    brd.pensize(12)
    brd.goto(-400, 300)
    brd.pd()
    for _ in range(2):
        brd.fd(800)
        brd.right(90)
        brd.fd(600)
        brd.right(90)
    brd.pu()

    # Title
    t1 = make("white")
    t1.goto(0, 130)
    t1.write("MINI GOLF", align="center", font=("Arial", 48, "bold"))

    t2 = make("#ccffcc")
    t2.goto(0, 70)
    t2.write("3 Holes  -  How few strokes can you take?", align="center", font=("Arial", 16, "normal"))

    # Hole previews
    t3 = make("white")
    t3.goto(0, 10)
    t3.write("Hole 1: Par 3    Hole 2: Par 4    Hole 3: Par 5", align="center", font=("Arial", 14, "normal"))

    # Start prompt
    t4 = make("yellow")
    t4.goto(0, -80)
    t4.write("Press  SPACE  or  click  to start", align="center", font=("Arial", 20, "bold"))

    # Controls reminder
    t5 = make("#aaaaaa")
    t5.goto(0, -140)
    t5.write("Click anywhere to aim & shoot  -  Press 'r' to reset", align="center", font=("Arial", 13, "normal"))

    screen.update()

    started = [False]

    def start_game():
        if started[0]:
            return
        started[0] = True
        for t in menu_turtles:
            t.clear()
        screen.onclick(None)
        screen.onkey(None, "space")
        screen.onclick(hit)
        load_hole(0)
        main_loop()

    screen.listen()
    screen.onclick(lambda x, y: start_game())
    screen.onkey(start_game, "space")


##########
# START
##########
show_menu()
screen.mainloop()
