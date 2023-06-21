import customtkinter as ctk
from random import randint

SNAKE_HEAD_COLOR = "#01ff25"
SNAKE_BODY_COLOR = "#239b00"

FOOD_COLOR = "#d11404"


class Apple:
    def __init__(self, game):
        self.game = game
        self.body = ctk.CTkLabel(self.game, bg_color=FOOD_COLOR, text="")
        self.randomize()

    def randomize(self):

        temp_pos = [randint(0, 29), randint(0, 29)]
        collision = False

        for player_body_part in self.game.player.body_pos:
            if player_body_part == temp_pos:
                collision = True
                break

        if collision:
            self.randomize()
        else:
            self.position = temp_pos

    def draw(self):
        self.body.grid(row=self.position[0], column=self.position[1], sticky="nsew")

    def collision(self):
        collision = False

        for player_body_part in self.game.player.body_pos:
            if player_body_part == self.position:
                collision = True
                break
        if collision:
            self.game.player.score += 1
            self.game.score_label.configure(text=f"Score: {self.game.player.score}")
            
            self.randomize()
            
            self.game.player.add_block = True

 
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

    def move_player(self, dir):
        direction_dict = {"w": (-1, 0),
                          "d": (0, 1),
                          "s": (1, 0),
                          "a": (0, -1)}
        value_from_dict = direction_dict.get(dir)

        new_row = self.body_pos[0][0] + value_from_dict[0]
        new_column = self.body_pos[0][1] + value_from_dict[1]
        if new_row < 0 or new_column < 0 or new_row == 30 or new_column == 30:
            pass
        else:
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

        self.apple = Apple(self)

        self.labels = [ctk.CTkLabel(self, bg_color=SNAKE_HEAD_COLOR, text=""),
                       ctk.CTkLabel(self, bg_color=SNAKE_BODY_COLOR, text="")]

        self.last_key_pressed = "d"

        self.score_label = ctk.CTkLabel(
            self,
            text=f"Score: {self.player.score}",
            font=("Comic Sans MS Bold", 20))

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
        self.last_move_dir = self.last_key_pressed
        self.player.move_player(self.last_key_pressed)

        self.apple.collision()
        self.draw()
        self.after(200, self.move)

    def draw(self):
        if self.player.length != len(self.labels):
            self.labels.append(
                ctk.CTkLabel(self, bg_color=SNAKE_BODY_COLOR, text=""))

        for index, label in enumerate(self.labels):
            pos = self.player.body_pos[index]
            label.grid(row=pos[0], column=pos[1], sticky="nsew")
        self.apple.draw()


app = Game()
