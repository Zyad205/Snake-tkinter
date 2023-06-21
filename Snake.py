import customtkinter as ctk
from random import randint

SNAKE_HEAD_COLOR = "#01ff25"
SNAKE_BODY_COLOR = "#239b00"

FOOD_COLOR = "#d11404"


class Apple:
    def __init__(self, player_body_pos, window):
        self.player_body_pos = player_body_pos
        self.body = ctk.CTkLabel(window, bg_color=FOOD_COLOR, text="")
        self.randomize()
        self.draw()

    def randomize(self):

        temp_pos = [randint(0, 29), randint(0, 29)]
        collision = False

        for player_body_part in self.player_body_pos:
            if player_body_part == temp_pos:
                collision = True
                break

        if collision:
            self.randomize()
            self.draw()
        else:
            self.position = temp_pos

    def draw(self):
        self.body.grid(row=self.position[0], column=self.position[1], sticky="nsew")

    def collision(self, player_body_pos):
        collision = False

        for player_body_part in player_body_pos:
            if player_body_part == self.position:
                collision = True
                break
        if collision:
            self.randomize()
            self.draw()
        return collision
    

 
class Player:
    def __init__(self):
        # Player Position
        row = randint(0, 29)
        column = randint(1, 29)

        self.position = [row, column]

        self.add_block = False
        
        self.length = 2

        self.score = 0

        self.body_pos = [[row, column], [row, column - 1]]

    def body_collision(self):
        for body_part in self.body_pos[1:]:
            if self.body_pos[0] == body_part:
                return True

    def move_player(self, dir):
        direction_dict = {"w": (-1, 0),
                          "d": (0, 1),
                          "s": (1, 0),
                          "a": (0, -1)}
        value_from_dict = direction_dict.get(dir)

        new_row = self.body_pos[0][0] + value_from_dict[0]
        new_column = self.body_pos[0][1] + value_from_dict[1]
        if new_row == -1:
            new_row = 29
        elif new_row == 30:
            new_row = 0
        elif new_column == -1:
            new_column = 29
        elif new_column == 30:
            new_column = 0            

        self.body_pos[0] = [new_row, new_column]
        for index, body_part in enumerate(self.body_pos[1:]):
            body_part_index = body_part.copy()
            self.body_pos[index + 1] = self.position
            self.position = body_part_index
            
        if self.add_block:
            self.body_pos.append(self.position)
            self.add_block = False
            self.length += 1
        self.position = self.body_pos[0]


class Game(ctk.CTk):
    def __init__(self):
        super().__init__("#202124")
        # Size

        self.geometry("800x800")
        self.resizable(False, False)

        self.rowconfigure(tuple(range(30)), weight=1, uniform="a")
        self.columnconfigure(tuple(range(30)), weight=1, uniform="a")

        # Name
        self.title("PyNake")

        self.player = Player()

        self.apple = Apple(self.player.body_pos, self)

        self.labels = [ctk.CTkLabel(self, bg_color=SNAKE_HEAD_COLOR, text=""),
                       ctk.CTkLabel(self, bg_color=SNAKE_BODY_COLOR, text="")]

        self.game_running = True

        self.last_key_pressed = "d"

        self.score_label = ctk.CTkLabel(
            self,
            text=f"Score: {self.player.score}",
            font=("Comic Sans MS Bold", 20))
        self.score_label.lower()
        self.score_label.place(relx=0.01, relheight=0.05)

        # Exit event
        self.bind("<Escape>", lambda event: exit())
        self.bind("<KeyPress>", self.key_press)

        self.move()
        # Mainloop
        self.mainloop()

    def key_press(self, event):
        if any((event.char == "w",
                event.char == "d",
                event.char == "s",
                event.char == "a")):

            keys_dict = {"w": "s",
                         "s": "w",
                         "a": "d",
                         "d": "a"}
            new_key = keys_dict[event.char]

            if self.last_move_dir != new_key:
                self.last_key_pressed = event.char

    def move(self):
        if self.game_running:
            self.last_move_dir = self.last_key_pressed
            self.player.move_player(self.last_key_pressed)

            player_hit_himself = self.player.body_collision()
            if player_hit_himself:
                self.game_running = False
                
        if self.game_running:
            self.apple.player_body_pos = self.player.body_pos

            collision_happened = self.apple.collision(self.player.body_pos)

            if collision_happened:
                self.player.score += 1
                self.score_label.configure(text=f"Score: {self.player.score}")
                self.player.add_block = True

            self.draw()
            self.after(200, self.move)
        else:
            for label in self.labels:
                label.grid_forget()
            self.score_label.place_forget()
            self.apple.body.grid_forget()
            ctk.CTkLabel(
                self,
                text="Game over",
                font=("Ebrima", 40),
                text_color="red").grid(row=13, column=13, columnspan=4, rowspan=2)


    def draw(self):
        if self.player.length != len(self.labels):
            self.labels.append(
                ctk.CTkLabel(self, bg_color=SNAKE_BODY_COLOR, text=""))

        for index, label in enumerate(self.labels):
            pos = self.player.body_pos[index]
            label.grid(row=pos[0], column=pos[1], sticky="nsew")
        


app = Game()
