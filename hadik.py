import traceback


try:
    import tkinter as tk
    import random as rd
    import datetime
    import os, sys

    script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    file_path = os.path.join(script_dir, "highscore_snake.txt")

    with open(file_path, "r") as f:
        highscore = int(f.readline())
        score_log = [line.strip() for line in f]

    game_on = False
    paused = None
    game_speed = 500


    def resize_canvas(event):
        global window_height, window_width
        window_height = root.winfo_height()
        window_width = root.winfo_width()

        canvas.place(x=0, y=0, width=window_width, height=window_height - 70)
        bottom_frame.place(x=0, y=window_height - 70, width=window_width, height=70)

    def change_speed(value):
        global game_speed
        game_speed = value

    def toggle_pause(event):
        global is_paused, game_on, paused, window_height, window_width
        if game_on:
            is_paused = not is_paused
        if is_paused:
            paused = canvas.create_text(window_width/2, (window_height-70)/2, text="PAUSED", font=("Arial", 20), tags="paused_text")
            canvas.config(bg="grey")
        else:
            canvas.config(bg="white")
            if paused:
                canvas.delete("paused_text")

    def focus_in(event):
        login.delete(0, tk.END)
        login.config(fg="black")

    def log_nick():
        global nick, play_button
        if login.get() != "":
            nick = login.get()
            login.destroy()
            change_player.config(state="normal")
            login_button.destroy()
            play_button.config(state="normal")

    def change_player():
        global login, login_button
        login = tk.Entry(canvas, width=40, fg="grey")
        login.insert(0, "Who is playing?")
        login.bind("<FocusIn>", focus_in)
        login.place(x=250, y=250, anchor="center")
        login_button = tk.Button(root, text="Login", command=log_nick)
        login_button.place(x=250, y=275, anchor="center")

    def place_apple():
        global x_apple, y_apple, apple
        x_apple = rd.randint(1, window_width - 40)
        y_apple = rd.randint(1, window_height - 110)
        apple = canvas.create_oval(x_apple, y_apple, x_apple + 20, y_apple + 20, fill="green")

    def game_over():
        global score, highscore, score_log, game_on, heads, head, window_width, window_height
        change_player.config(state="normal")
        game_end = tk.Label(canvas, text="GAME OVER")
        score_display = tk.Label(canvas, text="Score : " + str(score))
        canvas.config(highlightcolor="black")
        game_on = False

        def delete_snake_parts(index=0):
            if index < len(heads):
                canvas.delete(heads[-(index + 1)])  # Start from the end
                canvas.after(100, delete_snake_parts, index + 1)

        delete_snake_parts()


        if score > highscore:
            highscore = score
            with open(file_path, 'w') as f:
                score_log.append("\n" + "New High Score : " + str(highscore) + " / " + datetime.datetime.now().strftime(" %A %m/%d/%Y %H:%M") + " by: " + str(nick))
                f.write(str(highscore) + "\n")
                for line in score_log:
                    f.write(line + "\n")

            highscore_display.config(text="Highscore: " + str(highscore))
        game_end.place(relx=0.5, rely=0.5, anchor="center")
        score_display.place(relx=0.5, rely=0.55, anchor="center")
        score_display.after(3000, score_display.destroy)
        game_end.after(3000, game_end.destroy)
        return

    def create_snake():
        global heads, score, x_apple, y_apple, head, x_vector, y_vector, score_display, is_paused, game_on, body_color
        heads = []
        x_vector = 0
        y_vector = 25
        score = 0
        game_on = True
        is_paused = False
        canvas.delete("all")
        canvas.config(highlightcolor="#880808")
        canvas.focus_set()
        head = canvas.create_rectangle(240, 240, 260, 260, fill="#880808")
        body_color = "#AA4A44"
        change_player.config(state="disabled")
        score_display = tk.Label(bottom_frame, text="Score : " + str(score))
        score_display.place(relx=0.35, rely=0.5, anchor="center")
        heads.append(head)
        place_apple()
        move()

    def go_up(event):
        global x_vector, y_vector
        x_vector = 0
        y_vector = -25

    def go_down(event):
        global x_vector, y_vector
        x_vector = 0
        y_vector = 25

    def go_left(event):
        global x_vector, y_vector
        x_vector = -25
        y_vector = 0

    def go_right(event):
        global x_vector, y_vector
        x_vector = 25
        y_vector = 0

    def move():
        global heads, x_vector, y_vector, score, x_apple, y_apple, head, apple, highscore, score_display, body_color
        x1, y1, x2, y2 = canvas.coords(head)
        positions = [canvas.coords(part) for part in heads]
        eat = canvas.find_overlapping(x1, y1, x2, y2)

        if is_paused:
            canvas.after(100, move)
            return

        if x1 < 0 or y1 < 0 or x2 > window_width or y2 > window_height-70:
            game_over()
            return

        for i in range(1, len(heads)):
            if heads[i] in eat:
                game_over()
                return

        if 40 > score >= 20:
            canvas.config(highlightcolor="#355E3B")
            body_color = "#008000"
            canvas.itemconfig(heads[0], fill="#355E3B")
        elif 60 > score >= 40:
            canvas.config(highlightcolor="#000080")
            body_color = "#1434A4"
            canvas.itemconfig(heads[0], fill="#000080")
        elif 80 > score >= 60:
            canvas.config(highlightcolor="#301934")
            body_color = "#702963"
            canvas.itemconfig(heads[0], fill="#301934")
        elif 100 > score >= 80:
            canvas.config(highlightcolor="#B59410")
            body_color = "#D4AF37"
            canvas.itemconfig(heads[0], fill="#B59410")
        elif score >= 100:
            canvas.config(highlightcolor="#0080FF")
            body_color = "#7EF9FF"
            canvas.itemconfig(heads[0], fill="0080FF")

        for i in range(1, len(heads)):
            canvas.itemconfig(heads[i], fill=body_color)

        if heads[0] and apple in eat:
            score += 1
            score_display.config(text="Score: " + str(score))
            canvas.delete(apple)
            place_apple()
            x1, y1, x2, y2 = positions[len(heads) - 1]
            if x_vector == 0 and y_vector == -25:
                new_head = canvas.create_rectangle(x1, y1 + 25, x2, y2 + 25, fill=body_color)
            elif x_vector == 0 and y_vector == 25:
                new_head = canvas.create_rectangle(x1, y1 - 25, x2, y2 - 25, fill=body_color)
            elif x_vector == 25 and y_vector == 0:
                new_head = canvas.create_rectangle(x1 - 25, y1, x2 - 25, y2, fill=body_color)
            elif x_vector == -25 and y_vector == 0:
                new_head = canvas.create_rectangle(x1 + 25, y1, x2 + 25, y2, fill=body_color)
            heads.append(new_head)

        canvas.move(heads[0], x_vector, y_vector)
        for i in range(1, len(heads)):
            canvas.coords(heads[i], positions[i - 1])

        canvas.after(game_speed, move)

    root = tk.Tk()
    root.geometry("500x570")

    canvas = tk.Canvas(root, background="white", highlightthickness=5, highlightbackground="black", highlightcolor="black")
    bottom_frame = tk.Frame(root, bg="gray")
    bottom_frame.place(x=0, y=500, width=500, height=70)

    play_button = tk.Button(bottom_frame, text="Play", command=create_snake)
    play_button.place(relx=0.5, rely=0.5, anchor="center")
    play_button.config(state="disabled")
    highscore_display = tk.Label(bottom_frame, text="High Score : " + str(highscore))
    highscore_display.place(relx=0.15, rely=0.5, anchor="center")


    login = tk.Entry(canvas, width=40, fg="grey")
    login.insert(0, "Who is playing?")
    login.bind("<FocusIn>", focus_in)
    login.place(relx=0.5, rely=0.5, anchor="center")
    login_button = tk.Button(root, text="Login", command=log_nick)
    login_button.place(relx=0.5, rely=0.5, anchor="center")

    change_player = tk.Button(bottom_frame, text="Change Player", command=change_player, state="disabled")
    change_player.place(relx=0.9, rely=0.5, anchor="center")

    slider = tk.Scale(bottom_frame, from_=500, to=200, orient="horizontal", command=change_speed)
    slider.set(500)
    slider.place(relx=0.675, rely=0.4, anchor="center")

    slider_desc = tk.Label(bottom_frame, text="Moves once every: 0.x sec", font=("Arial", 7))
    slider_desc.place(relx=0.675, rely=0.8, anchor="center")

    root.focus_set()

    canvas.bind("w", go_up)
    canvas.bind("s", go_down)
    canvas.bind("a", go_left)
    canvas.bind("d", go_right)
    canvas.bind("<space>", toggle_pause)
    root.bind("<Configure>", resize_canvas)

    root.mainloop()

except Exception as e:
    print("An error occurred:")
    traceback.print_exc()
    input("Press Enter to exit...")