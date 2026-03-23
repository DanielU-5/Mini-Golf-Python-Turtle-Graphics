import turtle
import time
import math
import random


##########
#CONSTANTS
##########
HOLE_X = 200
HOLE_Y = 0
BALLSTART_X = -300
BALLSTART_Y = 0


dx = 0
dy = 0
strokes = 0

ball_colors = ["white", "red", "blue", "yellow", "orange"]
screen = turtle.Screen()
screen.setup(830,630)
screen.title("Mini Golf")
screen.bgcolor("green")

ball = turtle.Turtle()
ball.shape("circle")
ball.color(random.choice(ball_colors))
ball.pu()
ball.goto(BALLSTART_X, BALLSTART_Y)

outerhole = turtle.Turtle()
outerhole.hideturtle()
outerhole.pu()
outerhole.goto(200,0)
outerhole.dot(37, "black")

hole = turtle.Turtle()
hole.hideturtle()
hole.pu()
hole.goto(200,0)
hole.dot(30, "white")

score = turtle.Turtle()
score.hideturtle()
score.pu()
score.goto(-380, 240)
score.color("white")
score.write("Strokes: 0 \nPress 'r' to reset", font=("Arial", 14, "normal"))

outline = turtle.Turtle()
outline.hideturtle()
outline.pu()
outline.speed(0)
outline.pensize(15)
outline.goto(-400, 300)
outline.color("blue")
outline.pd()
outline.setheading(0)
for x in range(2):
    outline.fd(800)
    outline.right(90)
    outline.fd(600)
    outline.right(90)

obstacle1 = turtle.Turtle()
obstacle1.hideturtle()
obstacle1.pu()
obstacle1.color("blue")
obstacle1.goto(-50, -30)
obstacle1.pd()
obstacle1.speed(0)
obstacle1.begin_fill()
for x in range(2):
    obstacle1.fd(100)
    obstacle1.left(90)
    obstacle1.fd(60)
    obstacle1.left(90)
obstacle1.end_fill()

obstacle2 = turtle.Turtle()
obstacle2.hideturtle()
obstacle2.pu()
obstacle2.color("blue")
obstacle2.goto(120, -180)
obstacle2.pd()
obstacle2.speed(0)
obstacle2.begin_fill()
for x in range(2):
    obstacle2.fd(80)
    obstacle2.left(90)
    obstacle2.fd(60)
    obstacle2.left(90)
obstacle2.end_fill()

obstacle3 = turtle.Turtle()
obstacle3.hideturtle()
obstacle3.pu()
obstacle3.color("blue")
obstacle3.goto(-150, 100)
obstacle3.pd()
obstacle3.speed(0)
obstacle3.begin_fill()
for x in range(2):
    obstacle3.fd(80)
    obstacle3.left(90)
    obstacle3.fd(40)
    obstacle3.left(90)
obstacle3.end_fill()

def reset():
    global dx, dy, strokes

    dx = 0
    dy = 0
    strokes = 0

    ball.goto(BALLSTART_X, BALLSTART_Y)
    score.clear()
    score.goto(-380, 240)
    score.write("Strokes: 0 \nPress 'r' to reset", font=("Arial", 14, "normal"))
    main()
screen.listen()
screen.onkey(reset, "r")

def stroke_message():
    return f"Strokes: {strokes} \nPress 'r' to reset"

def hit(x, y):
    global dx, dy, strokes
    if abs(dx) > 0.1 or abs(dy) > 0.1:
         return

    dx = (x - ball.xcor()) / 65
    dy = (y - ball.ycor()) / 65
    strokes += 1
    score.clear()
    score.write(stroke_message(), font=("Arial", 14, "normal"))
screen.onclick(hit)

def main():
    global dx, dy, strokes, ball
    ball.color(random.choice(ball_colors))
    while True:
        x = ball.xcor()
        y = ball.ycor()

        #Check for walls
        if x > 380 or x < -380:
            dx = -dx
        if y > 280 or y < -280:
            dy = -dy
        #obstacle bounds
        left1 = -50
        right1 = 50
        bottom1 = -30
        top1 = 30

        left2 = 120
        right2 = 200
        bottom2 = -180
        top2 = -120

        left3 = -150
        right3 = -70
        bottom3 = 100
        top3 = 140
        #check if it hits obstacles
        if left1 < x < right1 and bottom1 < y < top1:
            dx = -dx
            dy = -dy
        if left2 < x < right2 and bottom2 < y < top2:
            dx = -dx
            dy = -dy
        if left3 < x < right3 and bottom3 < y < top3:
            dx = -dx
            dy = -dy
        #Move ball
        ball.goto(x + dx, y + dy)
        #Slow down ball (friction)
        dx *= 0.99
        dy *= 0.99

        #check if the ball is in the hole
        if math.dist((ball.xcor(), ball.ycor()), (200, 0)) < 10:
            print("YOU WIN!")
            dx = 0
            dy = 0
            score.goto(0,0)
            score.write(f"You made it in {strokes} strokes!", align ="center", font=("Arial", 25, "normal"))
            break
        elif strokes > 20:
            print("You lose! Too many strokes!")
            dx = 0
            dy = 0
            score.goto(0, 0)
            score.write(f"You lose! Too many strokes!", align="center", font=("Arial", 25, "normal"))
            break
        else:
            pass

    time.sleep(0.001)

main()
screen.mainloop()
