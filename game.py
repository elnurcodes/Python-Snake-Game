# *************************************
# Python Snake by Elnur Husyenov 161385
# *************************************
from tkinter import *
import random
import os
from PIL import Image, ImageTk  # Only needed for snake head

# ----- Game Constants -----
GAME_WIDTH = 700
GAME_HEIGHT = 700
SPEED = 200
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"

# ----- Setup Main Window -----
window = Tk()
window.title("Snake Game by Elnur")
window.resizable(False, False)

score = 0
direction = 'down'

label = Label(window, text="Score:0", font=('consolas', 40))
label.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

window.update()

# Center window on screen
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))
window.geometry(f"{window_width}x{window_height}+{x}+{y}")

# ----- Load Snake Head Image -----
script_dir = os.path.dirname(__file__)
head_path = os.path.join(script_dir, "snake_head.png")
head_img_pil = Image.open(head_path).resize((SPACE_SIZE, SPACE_SIZE), Image.LANCZOS)
SNAKE_HEAD_IMAGE = ImageTk.PhotoImage(head_img_pil)

# ----- Classes and Functions -----
class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(BODY_PARTS):
            self.coordinates.append([0, 0])

        for index, (x, y) in enumerate(self.coordinates):
            if index == 0:
                head = canvas.create_image(x, y, anchor=NW, image=SNAKE_HEAD_IMAGE, tag="snake")
                self.squares.append(head)
            else:
                body = canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
                self.squares.append(body)

class Food:
    def __init__(self):
        x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE
        self.coordinates = [x, y]
        self.image = canvas.create_oval(
            x, y, x + SPACE_SIZE, y + SPACE_SIZE,
            fill=FOOD_COLOR, outline="", tag="food"
        )

def draw_grid():
    for i in range(0, GAME_WIDTH, SPACE_SIZE):
        canvas.create_line([(i, 0), (i, GAME_HEIGHT)], tag='grid_line', fill="#333333")
    for i in range(0, GAME_HEIGHT, SPACE_SIZE):
        canvas.create_line([(0, i), (GAME_WIDTH, i)], tag='grid_line', fill="#333333")

def next_turn(snake, food):
    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))
    new_head = canvas.create_image(x, y, anchor=NW, image=SNAKE_HEAD_IMAGE, tag="snake")
    snake.squares.insert(0, new_head)

    if len(snake.squares) > 1:
        canvas.delete(snake.squares[1])
        body_x, body_y = snake.coordinates[1]
        body = canvas.create_oval(body_x, body_y, body_x + SPACE_SIZE, body_y + SPACE_SIZE,
                                  fill=SNAKE_COLOR, tag="snake")
        snake.squares[1] = body

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1
        label.config(text=f"Score:{score}")
        canvas.delete("food")
        food = Food()
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collisions(snake):
        game_over()
    else:
        window.after(SPEED, next_turn, snake, food)

def change_direction(new_direction):
    global direction
    if new_direction == 'left' and direction != 'right':
        direction = new_direction
    elif new_direction == 'right' and direction != 'left':
        direction = new_direction
    elif new_direction == 'up' and direction != 'down':
        direction = new_direction
    elif new_direction == 'down' and direction != 'up':
        direction = new_direction

def check_collisions(snake):
    x, y = snake.coordinates[0]
    if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
        return True
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True
    return False

def game_over():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2 - 50,
                       font=('consolas', 60), text="You Lost!", fill="red")
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2 + 50,
                       font=('consolas', 40), text=f"Final Score: {score}", fill="white")

def start_game(event=None):
    global snake, food, score, direction
    score = 0
    direction = 'down'
    canvas.delete("all")
    draw_grid()
    label.config(text="Score:0")
    snake = Snake()
    food = Food()
    next_turn(snake, food)

# ----- Key Bindings and Start -----
window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))
window.bind('<Return>', start_game)

canvas.create_text(GAME_WIDTH / 2, GAME_HEIGHT / 2,
                   font=('consolas', 40), fill="white",
                   text="Press Enter to Start")

window.mainloop()