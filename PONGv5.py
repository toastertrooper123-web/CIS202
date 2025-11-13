import turtle
import random #Added Random Library For Ball Color Change FX
import winsound #Added Sound Library For Sound FX - Jack

#Create screen
sc = turtle.Screen()
sc.title("Pong Game")
sc.bgcolor("black")
sc.setup(width=1000, height=600)
sc.tracer(0) #Added Tracer control from turtle to control screen updates (Speeds Animations)

#Left paddle
left_pad = turtle.Turtle()
left_pad.speed(0)
left_pad.shape("square")
left_pad.color("red")
left_pad.shapesize(stretch_wid=6, stretch_len=0.5)
left_pad.penup()
left_pad.goto(-400, 0)

#Right paddle
right_pad = turtle.Turtle()
right_pad.speed(0)
right_pad.shape("square")
right_pad.color("red")
right_pad.shapesize(stretch_wid=6, stretch_len=0.5)
right_pad.penup()
right_pad.goto(400, 0)

#Ball
hit_ball = turtle.Turtle()
hit_ball.speed(0)
hit_ball.shape("circle")
hit_ball.color("blue")
hit_ball.penup()
hit_ball.goto(0, 0)
hit_ball.dx = 5
hit_ball.dy = -5

#Score - Added a Win/Paused/Game Over Function For Better Control Over Game - Jack
left_player = 0
right_player = 0
win_score = 10
paused = False
game_over = False

#Score display
sketch = turtle.Turtle()
sketch.speed(0)
sketch.color("white")
sketch.penup()
sketch.hideturtle()
sketch.goto(0, 260)
sketch.write("Player One : 0    Player Two: 0", align="center", font=("Arial", 24, "normal"))


#Control Instructions, Pause and Restart
instructions = turtle.Turtle()
instructions.speed(0)
instructions.color("white")
instructions.penup()
instructions.hideturtle()
instructions.goto(0,-270) #The Coord -270 Is The Very Bottom Of Screen - Jack
instructions.write ("Press 'P' To Pause | Press 'R' To Restart Game", align = "center", font =("Arial", 18, "normal"))

#Paddle controls - Sped Up Original Paddle Speed - Jack
def paddleaup():
    if not game_over:
        y = left_pad.ycor()
        if y < 250:
            left_pad.sety(y + 40)

def paddleadown():
    if not game_over:
        y = left_pad.ycor()
        if y > -240:
            left_pad.sety(y - 40)

def paddlebup():
    if not game_over:
        y = right_pad.ycor()
        if y < 250:
            right_pad.sety(y + 40)

def paddlebdown():
    if not game_over:
        y = right_pad.ycor()
        if y > -240:
            right_pad.sety(y - 40)

#Creating Functions For Pausing and Restarting The Game - Jack
def toggle_pause():
    global paused
    paused = not paused

def restart_game():
    global left_player, right_player, paused, game_over
    left_player = 0
    right_player = 0
    paused = False
    game_over = False
    hit_ball.goto(0, 0)
    hit_ball.dx = 5
    hit_ball.dy = -5
    sketch.clear()
    sketch.goto(0, 260)
    sketch.write("Player One : 0    Player Two: 0", align="center", font=("Arial", 24, "normal"))

#Ball Effects - Imported Random to Change Ball On Impact - Jack
def ball_effect():
    colors = ["blue", "green", "yellow", "purple", "orange", "cyan", "white"]
    hit_ball.color(random.choice(colors))
    hit_ball.dx *= 1.05
    hit_ball.dy *= 1.05


#Sound FX - Jack
def play_bounce():
    winsound.PlaySound("bounce.wav", winsound.SND_ASYNC)

#Win Check - Creating A Function That Checks For A Winner - Jack
#Creating A Post Game Screen - Jack
def check_win():
    global game_over
    if left_player >= win_score:
        sketch.goto(0, 0)
        sketch.write("Player One Wins!\nPress R to Restart", align="center", font=("Arial", 36, "bold"))
        game_over = True
        return True
    elif right_player >= win_score:
        sketch.goto(0, 0)
        sketch.write("Player Two Wins!\nPress R to Restart", align="center", font=("Arial", 36, "bold"))
        game_over = True
        return True
    return False

#Paddle to Ball Collision Detection, Checking For A Win Upon Score - Jack
def check_collisions():
    global left_player, right_player

    if hit_ball.ycor() > 280:
        hit_ball.sety(280)
        hit_ball.dy *= -1
    if hit_ball.ycor() < -280:
        hit_ball.sety(-280)
        hit_ball.dy *= -1

    if hit_ball.xcor() > 500:
        hit_ball.goto(0, 0)
        hit_ball.dx = -5
        hit_ball.dy = -5
        left_player += 1
        sketch.clear()
        sketch.goto(0, 260)
        sketch.write("Player One : {}    Player Two: {}".format(left_player, right_player),
                     align="center", font=("Arial", 24, "normal"))
        if check_win():
            return

    if hit_ball.xcor() < -500:
        hit_ball.goto(0, 0)
        hit_ball.dx = 5
        hit_ball.dy = -5
        right_player += 1
        sketch.clear()
        sketch.goto(0, 260)
        sketch.write("Player One : {}    Player Two: {}".format(left_player, right_player),
                     align="center", font=("Arial", 24, "normal"))
        if check_win():
            return
#Changes made to paddle collision for the RIGHT PADDLE -T
    if (385 < hit_ball.xcor() < 395) and (right_pad.ycor() - 60 < hit_ball.ycor() < right_pad.ycor() + 50):
        hit_ball.setx(385)
        hit_ball.dx *= -1
        ball_effect()
        play_bounce() #Jack

#Changes made to the paddle collision for the LEFT PADDLE -T
    if (-395 < hit_ball.xcor() < -385) and (left_pad.ycor() - 60 < hit_ball.ycor() < left_pad.ycor() + 50):
        hit_ball.setx(-385)
        hit_ball.dx *= -1
        ball_effect()
        play_bounce() #Jack

#Main Game Loop 
def game_loop():
    if not paused and not game_over:
        if check_win():
            return
        hit_ball.setx(hit_ball.xcor() + hit_ball.dx)
        hit_ball.sety(hit_ball.ycor() + hit_ball.dy)
        check_collisions()
    sc.update()
    sc.ontimer(game_loop, 10)

#Key bindings
sc.listen()
sc.onkeypress(paddleaup, "w")
sc.onkeypress(paddleadown, "s")
sc.onkeypress(paddlebup, "Up")
sc.onkeypress(paddlebdown, "Down")
sc.onkeypress(toggle_pause, "p")
sc.onkeypress(restart_game, "r")

#Start game
game_loop()
sc.mainloop()
