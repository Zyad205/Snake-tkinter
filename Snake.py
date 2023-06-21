import customtkinter as ctk
from random import randint

SNAKE_HEAD_COLOR = "#01ff25"
SNAKE_BODY_COLOR = "#239b00"

FOOD_COLOR = "#d11404"


class Apple:
    def __init__(self, player_body_pos, window):

        # Save player body pos
        self.player_body_pos = player_body_pos

        # Makes a label for the apple
        self.body = ctk.CTkLabel(window, bg_color=FOOD_COLOR, text="")

        # Choose a position for the apple and grid it
        self.randomize()
        self.draw()

    def randomize(self):
        """Choose a new {self.position}"""
        temp_pos = [randint(0, 29), randint(0, 29)]
        collision = False

        # Makes sure the new position don't collide with the player
        for player_body_part in self.player_body_pos:
            if player_body_part == temp_pos:
                collision = True
                break
        
        if collision:
            self.randomize()
        else:
            self.position = temp_pos

    def draw(self):
        """Draw {self.body}"""
        self.body.grid(row=self.position[0],
                       column=self.position[1], sticky="nsew")

    def collision(self):
        """Returns {True} if player collied with the apple"""
        collision = False
        for player_body_part in self.player_body_pos:
            if player_body_part == self.position:
                collision = True
                break

        if collision:
            # Get another position and grid it
            self.randomize()
            self.draw()

        return collision


class Player:
    def __init__(self):
        # Player Position
        row = randint(0, 29)
        column = randint(1, 29)
        self.position = [row, column]

        # Default attributes
        self.add_block = False
        self.length = 2
        self.score = 0

        # First two body parts
        self.body_pos = [[row, column], [row, column - 1]]

    def body_collision(self):
        """Return {True} is the player head hits a body part"""
        for body_part in self.body_pos[1:]:
            if self.body_pos[0] == body_part:
                return True

    def move_player(self, dir):
        """Change the {self.body_pos} to the new position"""
        direction_dict = {"w": (-1, 0),
                          "d": (0, 1),
                          "s": (1, 0),
                          "a": (0, -1)}
        
        value_from_dict = direction_dict[dir]

        # Assign a new row and column for the head
        new_row = self.body_pos[0][0] + value_from_dict[0]
        new_column = self.body_pos[0][1] + value_from_dict[1]

        # Checks if the head is going out of bounds
        if new_row == -1:
            new_row = 29
        elif new_row == 30:
            new_row = 0
        elif new_column == -1:
            new_column = 29
        elif new_column == 30:
            new_column = 0

        # Update the head position
        self.body_pos[0] = [new_row, new_column]

        # The {self.position} is now storing the head last position
        for index, body_part in enumerate(self.body_pos[1:]):
            # save the body part position
            body_part_index = body_part.copy()

            # Part the current body part to the saved position
            self.body_pos[index + 1] = self.position

            # Update the {self.position} to the body part position before changing
            # So the next body part takes it's place
            self.position = body_part_index

        if self.add_block:
            # Adds a block with position = {self.position} that has the
            # value of the last moved body part before moving
            self.body_pos.append(self.position)
            self.add_block = False
            self.length += 1

        # Updates {self.position} to the head position    
        self.position = self.body_pos[0]


class Game(ctk.CTk):
    def __init__(self):
        super().__init__("#202124")  # gives the original init func the background color

        # Size
        self.geometry("800x800")
        self.resizable(False, False)

        # Layout
        self.rowconfigure(tuple(range(30)), weight=1, uniform="a")
        self.columnconfigure(tuple(range(30)), weight=1, uniform="a")

        # Name
        self.title("PyNake")

        # Makes player instances
        self.player = Player()

        # Makes apple instances
        self.apple = Apple(self.player.body_pos, self)

        # Makes labels for the player body
        self.labels = [ctk.CTkLabel(self, bg_color=SNAKE_HEAD_COLOR, text=""),
                       ctk.CTkLabel(self, bg_color=SNAKE_BODY_COLOR, text="")]

        # Game state
        self.game_running = True

        # Default direction
        self.last_key_pressed = "d"

        # Score label
        self.score_label = ctk.CTkLabel(
            self,
            text=f"Score: {self.player.score}",
            font=("Comic Sans MS Bold", 20))
        self.score_label.place(relx=0.01)

        # Makes it under any other widget
        self.score_label.lower()

        # Keypress events
        self.bind("<KeyPress>", self.key_press)

        # Exit event
        self.bind("<Escape>", lambda event: exit())
        # Start the game
        self.move()

        # Mainloop
        self.mainloop()

    def key_press(self, event):
        """Put the direction to the {self.last_key_pressed}"""
        if any((event.char == "w",
                event.char == "d",
                event.char == "s",
                event.char == "a")):  # Makes sure the value of the key press if valued

            keys_dict = {"w": "s",
                         "s": "w",
                         "a": "d",
                         "d": "a"}

            new_key = keys_dict[event.char]
            # Make sure the direction isn't opposite to the last movement direction
            if self.last_move_dir != new_key:
                self.last_key_pressed = event.char

    def move(self):
        """If the game is still running: Moves the player the checks for body collision, then
        collision with the apple and increase the score if so then calls {self.draw()},
        then put a timer for 200 ms for the func to be called again. If the game stopped 
        it calls {self.lose()}"""

        if self.game_running:
            self.last_move_dir = self.last_key_pressed
            self.player.move_player(self.last_key_pressed)

            # Body collision
            player_hit_himself = self.player.body_collision()
            if player_hit_himself:
                self.game_running = False

        if self.game_running:
            # Give the apple updated player body pos
            self.apple.player_body_pos = self.player.body_pos
            collision_happened = self.apple.collision(self.player.body_pos)

            if collision_happened:
                self.player.score += 1
                self.score_label.configure(text=f"Score: {self.player.score}")
                self.player.add_block = True

            self.draw()
            self.after(200, self.move)
        else:
            self.lose()

    def draw(self):
        """Draw the labels in {self.labels} with {self.player.body_pos} and append a new label
        if the player length increases"""
        if self.player.length != len(self.labels):
            self.labels.append(
                ctk.CTkLabel(self, bg_color=SNAKE_BODY_COLOR, text=""))

        for index, label in enumerate(self.labels):
            pos = self.player.body_pos[index]
            label.grid(row=pos[0], column=pos[1], sticky="nsew")

    def lose(self):
        """Uses {.grid_forget()} on the {self.labels} and {self.apple.body}
        and {.place_forget()} on {self.score_label} and creates a label says \"Game over\" """
        for label in self.labels:
            label.grid_forget()
        self.score_label.place_forget()
        self.apple.body.grid_forget()

        ctk.CTkLabel(
            self,
            text="Game over",
            font=("Ebrima", 40),
            text_color="red").place(relx=0.5, rely=0.5, anchor="center")


app = Game()
