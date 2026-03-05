import tkinter as tk
import random
import time

WIDTH = 600
HEIGHT = 600
CELL = 20


def start_game():

    snake = [(300, 300)]
    direction = "Right"
    food = None
    particles = []
    last_move_time = time.time()

    root = tk.Tk()
    root.title("Snake")

    canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black")
    canvas.pack()

    def spawn_food():
        nonlocal food
        x = random.randint(0, (WIDTH // CELL) - 1) * CELL
        y = random.randint(0, (HEIGHT // CELL) - 1) * CELL
        food = (x, y)

    def create_particles(x, y):
        for _ in range(15):
            particles.append({
                "x": x,
                "y": y,
                "dx": random.uniform(-3, 3),
                "dy": random.uniform(-3, 3),
                "life": 20
            })

    def move_snake():
        nonlocal snake, direction, food

        head_x, head_y = snake[0]

        if direction == "Up":
            head_y -= CELL
        elif direction == "Down":
            head_y += CELL
        elif direction == "Left":
            head_x -= CELL
        elif direction == "Right":
            head_x += CELL

        # ПРОВЕРКА ГРАНИЦ
        if head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT:
            return  # змейка просто останавливается

        new_head = (head_x, head_y)

        if new_head in snake:
            game_over()
            return

        snake.insert(0, new_head)

        if new_head == food:
            create_particles(food[0], food[1])
            spawn_food()
        else:
            snake.pop()

    def update_particles():
        new_particles = []

        for p in particles:
            p["x"] += p["dx"]
            p["y"] += p["dy"]
            p["life"] -= 1

            if p["life"] > 0:
                new_particles.append(p)

        particles.clear()
        particles.extend(new_particles)

    def draw():
        canvas.delete("all")

        # яблоко
        canvas.create_oval(
            food[0], food[1],
            food[0] + CELL, food[1] + CELL,
            fill="red"
        )

        # змейка
        for x, y in snake:
            canvas.create_rectangle(x, y, x + CELL, y + CELL, fill="green")

        # партиклы
        for p in particles:
            canvas.create_oval(
                p["x"], p["y"],
                p["x"] + 4, p["y"] + 4,
                fill="yellow"
            )

    def game_loop():
        nonlocal last_move_time

        if time.time() - last_move_time >= 3:
            root.destroy()
            return

        move_snake()
        update_particles()
        draw()

        root.after(120, game_loop)

    def change_direction(event):
        nonlocal direction, last_move_time

        key = event.keysym.lower()

        if key == "w":
            direction = "Up"
        elif key == "s":
            direction = "Down"
        elif key == "a":
            direction = "Left"
        elif key == "d":
            direction = "Right"

        last_move_time = time.time()

    def game_over():
        canvas.create_text(
            WIDTH // 2,
            HEIGHT // 2,
            text="GAME OVER",
            fill="white",
            font=("Arial", 40)
        )

    root.bind("<Key>", change_direction)

    spawn_food()
    game_loop()

    root.mainloop()


def menu():
    while True:

        print("\n=== МЕНЮ ИГРЫ ===")
        print("1. Начать игру")
        print("2. Выход")

        choice = input("Выберите: ").lower()

        if choice == "1" or choice == "начать игру":
            start_game()

        elif choice == "2" or choice == "выход":
            print("Выход из программы")
            break

        else:
            print("Неверный ввод")


menu()