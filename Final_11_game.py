import tkinter as tk
import random

class WelcomeScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe - Welcome")
        self.root.configure(bg="dodger blue")

        self.label = tk.Label(root, text="Welcome to Tic Tac Toe\nDo You want to play the game??", font=("Times New Roman", 20, "bold"))
        self.label.pack(pady=20)
        self.label.configure(bg="dodger blue")

        button_frame = tk.Frame(root)
        button_frame.pack()

        yes_button = tk.Button(button_frame, text="Enter", command=self.start_game_modes, bg="light green", font=("Times New Roman", 20, "bold"))
        yes_button.pack(side=tk.LEFT, padx=10)

        no_button = tk.Button(button_frame, text=" Exit ", command=root.quit, bg="red", font=("Times New Roman", 20, "bold"))
        no_button.pack(side=tk.LEFT)

    def start_game_modes(self):
        self.root.destroy()
        game_modes_root = tk.Tk()
        game_modes_root.geometry("400x300")
        game_modes_screen = GameModesScreen(game_modes_root)
        game_modes_root.mainloop()

class GameModesScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe - Game Modes")
        self.root.configure(bg="purple")

        self.label = tk.Label(root, text="Choose a Game Mode", font=("Times New Roman", 25, "bold"), fg="white")
        self.label.pack(pady=20)
        self.label.configure(bg="purple")

        multiplayer_button = tk.Button(root, text="Multiplayer", command=self.start_multiplayer_game, bg="blue", font=("Times New Roman", 20, "bold"), fg="white")
        multiplayer_button.pack()

        single_player_button = tk.Button(root, text="Single Player", command=self.start_single_player_game, bg="blue", font=("Times New Roman", 20, "bold"), fg="white")
        single_player_button.pack()
        exit_button = tk.Button(root, text="Exit", command=root.quit, bg="red", font=("Times New Roman", 20, "bold"), fg="white")
        exit_button.pack()

    def start_multiplayer_game(self):
        self.root.destroy()
        game_root = tk.Tk()
        game_root.title("Tic Tac Toe (Multiplayer)")
        game = TicTacToe(game_root, size=5, multiplayer=True)

    def start_single_player_game(self):
        self.root.destroy()
        game_root = tk.Tk()
        game_root.title("Tic Tac Toe (Single Player)")
        game = TicTacToe(game_root, size=5, multiplayer=False)

class TicTacToe:
    def __init__(self, root, size=5, multiplayer=False):
        self.root = root
        self.size = size
        self.board = [["" for _ in range(size)] for _ in range(size)]
        self.current_player = "X"
        self.multiplayer = multiplayer
        self.buttons = []
        self.x_score = 0
        self.o_score = 0
        self.move_history = []  # Store move history
        self.move_counter = 0
        self.previous_move = None  # Store the previous move

        self.create_score_labels()
        self.create_turn_indicator()  # Add turn indicator
        self.create_board()
        self.result_label = tk.Label(root, text="", font=("Times New Roman", 24, "bold"), fg="lime green")
        self.result_label.grid(row=self.size + 3, columnspan=self.size + 2)  # Adjust the columnspan
        self.restart_button = tk.Button(root, text="Restart", font=("Times New Roman", 24, "bold"), command=self.restart, state=tk.DISABLED, fg="blue")
        self.restart_button.grid(row=self.size + 5, columnspan=self.size + 2)  # Adjust the columnspan
        self.move_counter_label = tk.Label(root, text=f"Moves: {self.move_counter}", font=("Times New Roman", 20, "bold"), fg="Green")
        self.move_counter_label.grid(row=self.size + 4, column=0, columnspan=2, sticky="w")  # Adjust the column and sticky
        self.undo_button = tk.Button(root, text="Undo", font=("Times New Roman", 20, "bold"), command=self.undo_move, fg="green")
        self.undo_button.grid(row=self.size + 5, column=0, columnspan=self.size + 2, sticky="w")
        self.previous_button = tk.Button(root, text="Previous", font=("Times New Roman", 24, "bold"), command=self.go_to_game_modes, state=tk.DISABLED, fg="blue")
        self.previous_button.grid(row=self.size + 5, columnspan=self.size + 2, column=1, sticky="e")  # Adjust the columnspan and add sticky

        self.root.mainloop()

    def create_turn_indicator(self):
        self.turn_label = tk.Label(self.root, text="Player X's Turn", font=("Times New Roman", 18, "bold"), fg="blue")
        self.turn_label.grid(row=1, columnspan=self.size, pady=10)

    def create_score_labels(self):
        score_frame = tk.Frame(self.root)
        score_frame.grid(row=0, column=0, columnspan=self.size, sticky="w")

        self.x_score_label = tk.Label(score_frame, text=f"Player X Score: {self.x_score}", font=("Times New Roman", 20, "bold"), fg="Green")
        self.x_score_label.grid(row=0, column=0, padx=10, pady=5)

        self.o_score_label = tk.Label(score_frame, text=f"Player O Score: {self.o_score}", font=("Times New Roman", 20, "bold"), fg="Green")
        self.o_score_label.grid(row=1, column=0, padx=10, pady=5)

    def create_board(self):
        for i in range(self.size):
            row = []
            for j in range(self.size):
                button = tk.Button(
                    self.root,
                    text="",
                    width=5,
                    height=2,
                    font=("Times New Roman", 24, "bold"),
                    command=lambda i=i, j=j: self.make_move(i, j),
                    state=tk.NORMAL,
                    bg="pink"
                )
                button.grid(row=i + 2, column=j)
                row.append(button)
            self.buttons.append(row)

        if not self.multiplayer and self.current_player == "O":
            self.ai_move()

    def make_move(self, row, col):
        if self.board[row][col] == "" and not self.check_winner():
            self.board[row][col] = self.current_player
            font_color = "white"
            self.buttons[row][col].config(text=self.current_player, state=tk.DISABLED, bg="yellow", fg=font_color)  # Set the button color to yellow
            self.move_counter += 1
            self.move_counter_label.config(text=f"Moves count: {self.move_counter}")

            self.move_history.append((row, col))
            self.previous_move = (row, col)

            if self.check_winner():
                self.display_winner(self.current_player)
                if self.current_player == "X":
                    self.x_score += 1
                else:
                    self.o_score += 1
                self.update_score_labels()
            elif all(self.board[i][j] != "" for i in range(self.size) for j in range(self.size)):
                self.display_winner("Tie")

            self.current_player = "O" if self.current_player == "X" else "X"
            self.update_turn_indicator()  # Update turn indicator

            if not self.multiplayer and self.current_player == "O":
                self.ai_move()

    def update_turn_indicator(self):
        player = "Player X" if self.current_player == "X" else "Player O"
        self.turn_label.config(text=f"{player}'s Turn")


    def undo_move(self):
        if self.move_history and not self.result_label.cget("text"):
            if self.previous_move:
                prev_row, prev_col = self.previous_move
                self.buttons[prev_row][prev_col].config(bg="yellow")  # Reset the color of the previously clicked button

            row, col = self.move_history.pop()
            self.board[row][col] = ""
            self.buttons[row][col].config(text="", state=tk.NORMAL)

            self.move_counter -= 1
            self.move_counter_label.config(text=f"Moves count: {self.move_counter}")

            if self.move_history:
                prev_row, prev_col = self.move_history[-1]
                prev_player = "X" if self.current_player == "O" else "O"
                self.buttons[prev_row][prev_col].config(bg="yellow", text=prev_player)  # Restore the previous move

            self.current_player = "X" if self.current_player == "O" else "O"
            self.previous_move = (prev_row, prev_col)



    def update_score_labels(self):
        self.x_score_label.config(text=f"Player X Score: {self.x_score}")
        self.o_score_label.config(text=f"Player O Score: {self.o_score}")

    def ai_move(self):
        empty_cells = [(i, j) for i in range(self.size) for j in range(self.size) if self.board[i][j] == ""]
        if empty_cells:
            ai_move = random.choice(empty_cells)
            self.make_move(ai_move[0], ai_move[1])

    def check_winner(self):
        def check_consecutive(lst, player, consecutive):
            count = 0
            for val in lst:
                if val == player:
                    count += 1
                    if count == consecutive:
                        return True
                else:
                    count = 0
            return False

        for i in range(self.size):
            if (
                check_consecutive(self.board[i], "X", 4) or check_consecutive(self.board[i], "O", 4) or
                check_consecutive([self.board[j][i] for j in range(self.size)], "X", 4) or
                check_consecutive([self.board[j][i] for j in range(self.size)], "O", 4)
            ):
                return True

        for i in range(self.size):
            for j in range(self.size):
                if (
                    i <= self.size - 4 and
                    check_consecutive([self.board[i + k][j] for k in range(4)], self.current_player, 4)
                ):
                    return True
                if (
                    j <= self.size - 4 and
                    check_consecutive([self.board[i][j + k] for k in range(4)], self.current_player, 4)
                ):
                    return True
                if (
                    i <= self.size - 4 and j <= self.size - 4 and
                    check_consecutive([self.board[i + k][j + k] for k in range(4)], self.current_player, 4)
                ):
                    return True
                if (
                    i <= self.size - 4 and j >= 3 and
                    check_consecutive([self.board[i + k][j - k] for k in range(4)], self.current_player, 4)
                ):
                    return True

        return False

    def display_winner(self, winner):
        if winner == "Tie":
            self.result_label.config(text="It's a Tie!")
        else:
            self.result_label.config(text=f"{winner} is the winner! \nCongratulations")
        self.restart_button.config(state=tk.NORMAL)
        self.previous_button.config(state=tk.NORMAL)
        if self.turn_label:
            self.turn_label.grid_forget()
    def restart(self):
        for i in range(self.size):
            for j in range(self.size):
                self.board[i][j] = ""
                self.buttons[i][j].config(text="", state=tk.NORMAL, bg="pink")  # Reset button colors to default (pink)
        self.current_player = "X"
        self.result_label.config(text="")
        self.restart_button.config(state=tk.DISABLED)
        self.previous_button.config(state=tk.DISABLED)
        self.move_counter = 0  # Reset the move counter to 0
        self.move_counter_label.config(text=f"Moves count: {self.move_counter}")
        self.move_history.clear()  # Clear the move history
        self.previous_move = None  # Reset the previous move
        # Re-create the turn indicator
        self.create_turn_indicator()
        # Re-show the turn indicator
        if self.turn_label:
            self.turn_label.grid(row=1, columnspan=self.size, pady=10)

    def go_to_game_modes(self):
        self.root.destroy()
        game_modes_root = tk.Tk()
        game_modes_root.geometry("400x300")
        game_modes_screen = GameModesScreen(game_modes_root)
        game_modes_root.mainloop()

if __name__ == "__main__":
    menu_root = tk.Tk()
    menu_root.geometry("400x200")
    welcome_screen = WelcomeScreen(menu_root)
    menu_root.mainloop()
