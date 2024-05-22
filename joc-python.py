import turtle
import time
import random

# Setarea inițială a variabilelor pentru întârziere și scoruri
delay = 0.1
score = 0
high_score = 0

# Configurarea ferestrei jocului
wn = turtle.Screen()
wn.title("Snake Game")
wn.bgcolor("light green")
wn.setup(width=600, height=600)
wn.tracer(0)  # Dezactivează actualizările ecranului pentru a crește performanța

# Capul șarpelui
head = turtle.Turtle()
head.speed(0)
head.shape("square")
head.color("blue")
head.penup()
head.goto(0, 0)
head.direction = "stop"

# Mâncarea pentru șarpe
food = turtle.Turtle()
food.speed(0)
food.shape("circle")
food.color("red")
food.penup()
food.goto(0, 100)

# Lista de obstacole
obstacles = []
for _ in range(5):
    obstacle = turtle.Turtle()
    obstacle.speed(0)
    obstacle.shape("square")
    obstacle.color("gray")
    obstacle.penup()
    x = random.randint(-280, 280)
    y = random.randint(-280, 280)
    obstacle.goto(x, y)
    obstacles.append(obstacle)

# Segmentele corpului șarpelui
segments = []

# Afișarea scorului
pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("black")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write("Score: 0  High Score: 0", align="center", font=("Courier", 24, "normal"))

# Funcții pentru controlul mișcării șarpelui
def go_up():
    if head.direction != "down":
        head.direction = "up"

def go_down():
    if head.direction != "up":
        head.direction = "down"

def go_left():
    if head.direction != "right":
        head.direction = "left"

def go_right():
    if head.direction != "left":
        head.direction = "right"

def move():
    if head.direction == "up":
        y = head.ycor()
        head.sety(y + 20)
    if head.direction == "down":
        y = head.ycor()
        head.sety(y - 20)
    if head.direction == "left":
        x = head.xcor()
        head.setx(x - 20)
    if head.direction == "right":
        x = head.xcor()
        head.setx(x + 20)

# Funcție pentru resetarea jocului în caz de coliziune
def reset_game():
    global score, delay
    time.sleep(1)
    head.goto(0, 0)
    head.direction = "stop"
    for segment in segments:
        segment.goto(1000, 1000)  # Mută segmentele în afara ecranului
    segments.clear()
    score = 0
    delay = 0.1
    pen.clear()
    pen.write("Score: {}  High Score: {}".format(score, high_score), align="center", font=("Courier", 24, "normal"))

# Legături de taste pentru controlul șarpelui
wn.listen()
wn.onkeypress(go_up, "w")
wn.onkeypress(go_down, "s")
wn.onkeypress(go_left, "a")
wn.onkeypress(go_right, "d")

# Bucle principală a jocului
while True:
    wn.update()

    # Verificarea coliziunii cu marginile ferestrei
    if head.xcor() > 290 or head.xcor() < -290 or head.ycor() > 290 or head.ycor() < -290:
        reset_game()

    # Verificarea coliziunii cu mâncarea
    if head.distance(food) < 20:
        x = random.randint(-290, 290)
        y = random.randint(-290, 290)
        food.goto(x, y)

        # Adăugarea unui segment la șarpe
        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape("square")
        new_segment.color("green" if len(segments) % 3 == 0 else "blue")
        new_segment.penup()
        segments.append(new_segment)

        # Creșterea scorului
        score += 10
        if score > high_score:
            high_score = score
        pen.clear()
        pen.write("Score: {}  High Score: {}".format(score, high_score), align="center", font=("Courier", 24, "normal"))

        # Creșterea vitezei șarpelui
        delay -= 0.001

    # Verificarea coliziunii cu obstacolele
    for obstacle in obstacles:
        if head.distance(obstacle) < 20:
            reset_game()

    # Mutarea segmentelor corpului șarpelui în ordine inversă
    for index in range(len(segments)-1, 0, -1):
        x = segments[index-1].xcor()
        y = segments[index-1].ycor()
        segments[index].goto(x, y)

    # Mutarea primului segment la poziția capului
    if len(segments) > 0:
        x = head.xcor()
        y = head.ycor()
        segments[0].goto(x, y)

    move()

    # Verificarea coliziunii capului șarpelui cu segmentele corpului
    for segment in segments:
        if segment.distance(head) < 20:
            reset_game()

    time.sleep(delay)

wn.mainloop()
