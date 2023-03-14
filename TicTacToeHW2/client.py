import tkinter as tk
import socket
import threading

class TicTacToeApp:
    def __init__(self, parent):
        self.parent = parent
        self.parent.title("Tic Tac Toe")
        self.board = [" "] * 9
        self.current_player = "X"
        self.game_over = False
        self.server_address = "localhost"
        self.server_port = 8888
        self.username = ""
        self.password = ""
        self.create_widgets()

        # Connect to the server
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.server_address, self.server_port))

        # Start the receiver thread
        self.receiver_thread = threading.Thread(target=self.receive_messages)
        self.receiver_thread.start()

    def create_widgets(self):
        # Create the login frame
        self.login_frame = tk.Frame(self.parent)
        self.login_frame.pack()

        self.username_label = tk.Label(self.login_frame, text="Username:", font=("Arial", 16))
        self.username_label.pack(side=tk.LEFT)

        self.username_entry = tk.Entry(self.login_frame, font=("Arial", 16))
        self.username_entry.pack(side=tk.LEFT)

        self.password_label = tk.Label(self.login_frame, text="Password:", font=("Arial", 16))
        self.password_label.pack(side=tk.LEFT)

        self.password_entry = tk.Entry(self.login_frame, font=("Arial", 16), show="*")
        self.password_entry.pack(side=tk.LEFT)

        self.login_button = tk.Button(self.login_frame, text="Login", font=("Arial", 16), command=self.login)
        self.login_button.pack(side=tk.LEFT)

        # Create the game board
        self.board_frame = tk.Frame(self.parent)
        self.board_frame.pack()

        self.cells = []
        for i in range(3):
            for j in range(3):
                cell = tk.Button(self.board_frame, text=" ", font=("Arial", 32), width=3, height=1,
                                 command=lambda row=i, col=j: self.handle_click(row, col))
                cell.grid(row=i, column=j, padx=5, pady=5)
                self.cells.append(cell)

        # Create the status label
        self.status_label = tk.Label(self.parent, text=f"Current player: {self.current_player}", font=("Arial", 16))
        self.status_label.pack()

        # Create the reset button
        self.reset_button = tk.Button(self.parent, text="Reset", font=("Arial", 16), command=self.reset_game)
        self.reset_button.pack()

    def login(self):
        self.username = self.username_entry.get()
        self.password = self.password_entry.get()
        if self.username and self.password:
            self.send_message(f"LOGIN {self.username} {self.password}")
            self.login_frame.destroy()
            self.board_frame.pack()


def handle_click(self, row, col):
    # Ignore clicks if the game is over
    if self.game_over:
        return

    index = row * 3 + col
    if self.board[index] == " " and self.current_player == "X":
        self.board[index] = self.current_player
        self.cells[index].config(text=self.current_player)
        self.send_message(f"MOVE {index}")
        winner = self.check_for_winner()
        if winner:
            self.status_label.config(text=f"{winner} wins!")
            self.game_over = True
        elif " " not in self.board:
            self.status_label.config(text="It's a tie!")
            self.game_over = True
        else:
            self.current_player = "O"
            self.status_label.config(text=f"Current player: {self.current_player}")
    else:
        # Prompt the user to make a valid move
        self.status_label.config(text="Please make a valid move.")

def check_for_winner(self):
    for i in range(0, 9, 3):
        # Check rows
        if self.board[i] == self.board[i+1] == self.board[i+2] and self.board[i] != " ":
            return self.board[i]
    for i in range(3):
        # Check columns
        if self.board[i] == self.board[i+3] == self.board[i+6] and self.board[i] != " ":
            return self.board[i]
    # Check diagonals
    if self.board[0] == self.board[4] == self.board[8] and self.board[0] != " ":
        return self.board[0]
    if self.board[2] == self.board[4] == self.board[6] and self.board[2] != " ":
        return self.board[2]
    # If no winner, return None
    return None

def reset_game(self):
    self.board = [" "] * 9
    self.current_player = "X"
    self.game_over = False
    for cell in self.cells:
        cell.config(text=" ")
    self.status_label.config(text=f"Current player: {self.current_player}")
