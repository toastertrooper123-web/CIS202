import turtle
import random
import winsound #Added Sound Library For Sound FX - Jack

# --- Difficulty Settings ---
DIFFICULTY_SETTINGS = {
    "EASY": {"ball_speed": 4, "paddle_speed": 30},
    "NORMAL": {"ball_speed": 5, "paddle_speed": 40},
    "HARD": {"ball_speed": 7, "paddle_speed": 50}
}
# Variable to hold the current selected difficulty
current_difficulty = "NORMAL" 

#Create screen
sc = turtle.Screen()
sc.title("Pong Game")
sc.bgcolor("black")
sc.setup(width=1000, height=600)
sc.tracer(0) #Added Tracer control from turtle to control screen updates (Speeds Animations)

# COLOR CYLCES MAIN MENU -T
MENU_COLORS = ["blue", "green", "yellow", "purple", "orange", "cyan", "white"]
COLOR_INDEX = 0

# Turtle dedicated for the cycling PONG v6/7/8 title -T
menu_title_turtle = turtle.Turtle()
menu_title_turtle.speed(0)
menu_title_turtle.penup()
menu_title_turtle.hideturtle()
menu_title_turtle.goto(0, 150)

# Main Menu sketch (This turtle is used for all static text: score, controls, paused message) -T
sketch = turtle.Turtle()
sketch.speed(0)
sketch.color ("white") # Set to white for visibility
sketch.penup()
sketch.hideturtle()
sketch.goto(0, 0) # Initial position is center

# Main Menu Display Function (Initial Screen) -T
def draw_start_menu():
    sketch.clear()
    
    # R key will now go to the Difficulty Menu -T
    sketch.goto(0, 50)
    sketch.write("Press 'R' to Select Difficulty", align="center", font=("Arial", 30, "normal"))
    
    sketch.goto(0, -50)
    sketch.write("Player 1: W/S | Player 2: Up/Down", align="center", font=("Arial", 20, "normal"))

# Difficulty Menu Function -T
def draw_difficulty_menu():
    sketch.clear()
    
    sketch.goto(0, 90)
    sketch.write("Select Difficulty", align="center", font=("Arial", 40, "bold"))
    
    sketch.goto(0, -10)
    sketch.write("1: EASY (Slower)", align="center", font=("Arial", 25, "normal"))
    
    sketch.goto(0, -60)
    sketch.write("2: NORMAL (Default)", align="center", font=("Arial", 25, "normal"))
    
    sketch.goto(0, -110)
    sketch.write("3: HARD (Faster)", align="center", font=("Arial", 25, "normal"))
    
    sketch.goto(0, -210)
    # Shows the currently selected difficulty
    sketch.write(f"Current: {current_difficulty}", align="center", font=("Arial", 20, "normal"))

# Pong net center line -T
obstacle = turtle.Turtle()
obstacle.speed(0)
obstacle.shape("square")
obstacle.color("white")
obstacle.shapesize(stretch_wid=30, stretch_len=0.5) 
obstacle.penup()
obstacle.goto(0, 0) # Center of the screen -T

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
# Initial values set in restart_game based on difficulty -T
hit_ball.dx = 0
hit_ball.dy = 0

#Score - Added a Win/Paused/Game Over Function For Better Control Over Game - Jack
left_player = 0
right_player = 0
win_score = 10
paused = False
game_over = False
# Initial state is the start menu -T
game_state = "MENU"

#Paddle controls - Sped Up Original Paddle Speed - Jack
#CHECKS FOR GAME_STATE PLAYING -T
def paddleaup():
    global current_difficulty
    PADDLE_SPEED = DIFFICULTY_SETTINGS[current_difficulty]["paddle_speed"] 
    if not game_over and game_state == "PLAYING":
        y = left_pad.ycor()
        if y < 250:
            left_pad.sety(y + PADDLE_SPEED)

def paddleadown():
    global current_difficulty
    PADDLE_SPEED = DIFFICULTY_SETTINGS[current_difficulty]["paddle_speed"] 
    if not game_over and game_state == "PLAYING":
        y = left_pad.ycor()
        if y > -240:
            left_pad.sety(y - PADDLE_SPEED)

def paddlebup():
    global current_difficulty
    PADDLE_SPEED = DIFFICULTY_SETTINGS[current_difficulty]["paddle_speed"] 
    if not game_over and game_state == "PLAYING":
        y = right_pad.ycor()
        if y < 250:
            right_pad.sety(y + PADDLE_SPEED)

def paddlebdown():
    global current_difficulty
    PADDLE_SPEED = DIFFICULTY_SETTINGS[current_difficulty]["paddle_speed"] 
    if not game_over and game_state == "PLAYING":
        y = right_pad.ycor()
        if y > -240:
            right_pad.sety(y - PADDLE_SPEED)

# Difficulty Control Functions -T
def set_difficulty(level):
    global current_difficulty, game_state
    # Only allow difficulty change in the menu -T
    if game_state == "DIFFICULTY_MENU":
        current_difficulty = level
        # Redraw the menu -T
        draw_difficulty_menu()

def select_easy():
    set_difficulty("EASY")

def select_normal():
    set_difficulty("NORMAL")

def select_hard():
    set_difficulty("HARD")

def start_game_from_menu():
    global game_state
    if game_state == "MENU":
        # Move from Start Screen to Difficulty Selection -T
        game_state = "DIFFICULTY_MENU"
    elif game_state == "DIFFICULTY_MENU":
        # Move from DIFFICULTY_MENU to PLAYING state -T
        game_state = "PLAYING"
        restart_game()
    elif game_state == "PLAYING" and game_over:
        # If the game is over, restart it
        game_state = "DIFFICULTY_MENU" # Return to difficulty menu after a win
        restart_game()
        

#Ball Effects - Imported Random to Change Ball On Impact - Jack
def ball_effect():
    colors = ["blue", "green", "yellow", "purple", "orange", "cyan", "white"]
    hit_ball.color(random.choice(colors))
    hit_ball.dx *= 1.05
    hit_ball.dy *= 1.05


#Sound FX - Jack
def play_bounce():
    winsound.PlaySound("bounce.wav", winsound.SND_ASYNC)
    pass

#Win Check - Creating A Function That Checks For A Winner - Jack
#Creating A Post Game Screen - Jack
def check_win():
    global game_over, game_state 
    if left_player >= win_score:
        sketch.goto(0, 0)
        sketch.write("Player One Wins!\nPress R to Restart", align="center", font=("Arial", 36, "bold"))
        game_over = True
        obstacle.hideturtle()
        return True
    elif right_player >= win_score:
        sketch.goto(0, 0)
        sketch.write("Player Two Wins!\nPress R to Restart", align="center", font=("Arial", 36, "bold"))
        game_over = True
        obstacle.hideturtle()
        return True
    return False

# Creating Functions For Pausing and Restarting The Game - Jack
def toggle_pause():
    global paused
    if game_state == "PLAYING": # Only allow pausing while playing
        paused = not paused
    # PAUSE SCREEN message logic -T
        if paused:
            # Hide the net when paused -T
            obstacle.hideturtle()
            # Clears the score and write the PAUSED message in the center -T
            sketch.clear()
            sketch.goto(0, 0)
            sketch.write("PAUSED (Press 'P' to Resume)", align="center", font=("Arial", 36, "bold"))
        else:
            # Show the net when resuming -T
            obstacle.showturtle()
            # Resume: Clear the PAUSED message and redraw the score -T
            sketch.clear()
            # Redraw the score line -T
            sketch.write("Player One : {}    Player Two: {}".format(left_player, right_player), align="center", font=("Arial", 24, "normal"))

def restart_game():
    global left_player, right_player, paused, game_over, game_state 
    
    # GET THE CURRENT DIFFICULTY SETTINGS -T
    settings = DIFFICULTY_SETTINGS[current_difficulty]
    
    # Reset Scores/States
    left_player = 0
    right_player = 0
    paused = False
    game_over = False
    
    # Reset positions
    hit_ball.goto(0, 0)
    left_pad.goto(-400, 0)
    right_pad.goto(400, 0)
    
    # APPLY THE DIFFICULTY SETTINGS -T
    hit_ball.dx = settings["ball_speed"] 
    hit_ball.dy = -settings["ball_speed"] 
    
    sketch.clear()
    
    # If starting from difficulty menu, transition to playing
    if game_state == "PLAYING":
        sketch.goto(0, 260)
        sketch.write("Player One : 0    Player Two: 0", align="center", font=("Arial", 24, "normal"))
        # Show paddles and ball -T
        left_pad.showturtle()
        right_pad.showturtle()
        hit_ball.showturtle()
        obstacle.showturtle() # Ensure the net is visible when starting -T
    else: 
        # If we restart from a win, we now back to DIFFICULTY_MENU state -T
        draw_difficulty_menu()
    
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
        # Player One scores
        hit_ball.goto(0, 0)
        hit_ball.dx = -DIFFICULTY_SETTINGS[current_difficulty]["ball_speed"]
        hit_ball.dy = -DIFFICULTY_SETTINGS[current_difficulty]["ball_speed"]
        left_player += 1
        sketch.clear()
        sketch.goto(0, 260)
        sketch.write("Player One : {}    Player Two: {}".format(left_player, right_player),
                     align="center", font=("Arial", 24, "normal"))
        if check_win():
            return

    if hit_ball.xcor() < -500:
        # Player Two scores
        hit_ball.goto(0, 0)
        hit_ball.dx = DIFFICULTY_SETTINGS[current_difficulty]["ball_speed"]
        hit_ball.dy = -DIFFICULTY_SETTINGS[current_difficulty]["ball_speed"]
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

#Function that allows MAIN MENU to cycle between colors, only affects "PONG v6" Text. -T
def cycle_menu_color():
    global COLOR_INDEX, game_state 
    
    if game_state == "MENU" or game_state == "DIFFICULTY_MENU":
        # Clear the old title text stopping flickering -T
        menu_title_turtle.clear()
        
        # Gets next color -T
        current_color = MENU_COLORS[COLOR_INDEX]
        
        # Update turtle color and redraw title -T
        menu_title_turtle.color(current_color)
        menu_title_turtle.write("PONG v8", align="center", font=("Arial", 60, "bold"))

        # Increment the index, wrap around to 0 -T
        COLOR_INDEX = (COLOR_INDEX + 1) % len(MENU_COLORS)
        
        # Schedule next color change (2000 milliseconds = 2 seconds) DO NOT SET TO 2. Your retinas will perish. -T
        sc.ontimer(cycle_menu_color, 2000)
    else:
        # If not in the menu state, hide and clear the title to clean up -T
        menu_title_turtle.hideturtle()
        menu_title_turtle.clear()

#Main Game Loop 
def game_loop():
    global game_state 
    
    if game_state == "MENU":
        draw_start_menu() # Draws the initial start screen
        # Hide game elements while in menu
        left_pad.hideturtle()
        right_pad.hideturtle()
        hit_ball.hideturtle()
        obstacle.hideturtle()
        menu_title_turtle.showturtle()

    elif game_state == "DIFFICULTY_MENU":
        draw_difficulty_menu() # Draw the selection menu
        
        # Hide all game elements
        left_pad.hideturtle()
        right_pad.hideturtle()
        hit_ball.hideturtle()
        obstacle.hideturtle()
        menu_title_turtle.showturtle()
        
    elif game_state == "PLAYING":
        #Hides main menu turtle when play state active -T
        menu_title_turtle.hideturtle()
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

# Difficulty Selection Keys (only active in DIFFICULTY_MENU state) -T
sc.onkeypress(select_easy, "1")
sc.onkeypress(select_normal, "2")
sc.onkeypress(select_hard, "3")

sc.onkeypress(toggle_pause, "p")
# R now moves between the menu states and starts the game -T
sc.onkeypress(start_game_from_menu, "r") 

#Starts the color menu turtle's color cycle -T
cycle_menu_color()
#Start game
game_loop()
sc.mainloop()
