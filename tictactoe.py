import tkinter as tk
from tkinter import messagebox

# Initialize scores
player_score = 0
ai_score = 0
draws = 0

# Initialize the board
board = [' ' for _ in range(9)]  # 3x3 grid (flattened to a list of 9 elements)

# Minimax algorithm
def minimax(b, depth, is_maximizing):
    winner = check_winner(b)
    if winner == 'O':
        return 10 - depth  # AI win
    elif winner == 'X':
        return depth - 10  # Player win
    elif is_board_full(b):
        return 0  # Draw

    if is_maximizing:
        best_score = float('-inf')
        for i in range(9):
            if b[i] == ' ':
                b[i] = 'O'  # AI's move
                score = minimax(b, depth + 1, False)
                b[i] = ' '  # Undo the move
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(9):
            if b[i] == ' ':
                b[i] = 'X'  # Player's move
                score = minimax(b, depth + 1, True)
                b[i] = ' '  # Undo the move
                best_score = min(score, best_score)
        return best_score

# Get the best AI move
def get_ai_move():
    best_move = -1
    best_score = float('-inf')
    for i in range(9):
        if board[i] == ' ':
            board[i] = 'O'  # Try AI's move
            score = minimax(board, 0, False)
            board[i] = ' '  # Undo the move
            if score > best_score:
                best_score = score
                best_move = i
    return best_move

# Check for a winner
def check_winner(b):
    # Win conditions for rows, columns, and diagonals
    winning_combinations = [(0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
                            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columns
                            (0, 4, 8), (2, 4, 6)]  # Diagonals
    for combo in winning_combinations:
        if b[combo[0]] == b[combo[1]] == b[combo[2]] != ' ':
            return b[combo[0]]
    return None

# Check if the board is full
def is_board_full(b):
    return ' ' not in b

# Update the game state
def update_game_state():
    winner = check_winner(board)
    if winner == 'X':
        result_label.config(text="You Win!")
        update_score('player')
        disable_buttons()
    elif winner == 'O':
        result_label.config(text="AI Wins!")
        update_score('ai')
        disable_buttons()
    elif is_board_full(board):
        result_label.config(text="It's a Draw!")
        update_score('draw')
        disable_buttons()

# Handle a player's move
def player_move(index):
    if board[index] == ' ':
        board[index] = 'X'
        buttons[index].config(text='X', state='disabled')
        update_game_state()

        if not is_board_full(board) and check_winner(board) is None:
            ai_move = get_ai_move()
            board[ai_move] = 'O'
            buttons[ai_move].config(text='O', state='disabled')
            update_game_state()

# Disable all buttons after the game is over
def disable_buttons():
    for btn in buttons:
        btn.config(state='disabled')

# Update the score display
def update_score(result):
    global player_score, ai_score, draws
    if result == 'player':
        player_score += 1
    elif result == 'ai':
        ai_score += 1
    else:
        draws += 1
    score_label.config(text=f"Player: {player_score} | AI: {ai_score} | Draws: {draws}")

# Reset the game
def reset_game():
    global board, player_score, ai_score, draws
    board = [' ' for _ in range(9)]  # Reset the board
    player_score = 0  # Reset player score
    ai_score = 0  # Reset AI score
    draws = 0  # Reset draws
    for btn in buttons:
        btn.config(text=' ', state='normal')
    result_label.config(text="")
    score_label.config(text=f"Player: {player_score} | AI: {ai_score} | Draws: {draws}")  # Reset score display
    enable_buttons()

# Enable all buttons for a new game
def enable_buttons():
    for btn in buttons:
        btn.config(state='normal')

# Ask if the player wants to play again
def play_again():
    response = messagebox.askyesno("Play Again?", "Do you want to play again?")
    if response:
        reset_game()
    else:
        root.quit()

# GUI setup using Tkinter
root = tk.Tk()
root.title("Tic-Tac-Toe - Unbeatable AI")

# Create the grid of buttons (3x3)
buttons = []
for i in range(9):
    button = tk.Button(root, text=' ', font=('Arial', 20), width=5, height=2,
                       command=lambda i=i: player_move(i))
    buttons.append(button)

# Place the buttons in a grid
for i in range(3):
    for j in range(3):
        buttons[i*3 + j].grid(row=i, column=j)

# Result label to show the game result
result_label = tk.Label(root, text="", font=('Arial', 16))
result_label.grid(row=3, column=0, columnspan=3)

# Score label to show the scores
score_label = tk.Label(root, text=f"Player: {player_score} | AI: {ai_score} | Draws: {draws}",
                       font=('Arial', 16))
score_label.grid(row=4, column=0, columnspan=3)

# Reset button
reset_button = tk.Button(root, text="Reset Game", font=('Arial', 14), command=reset_game)
reset_button.grid(row=5, column=0, columnspan=3)

# Play Again button
play_again_button = tk.Button(root, text="Play Again", font=('Arial', 14), command=play_again)
play_again_button.grid(row=6, column=0, columnspan=3)

# Start the GUI loop
root.mainloop()
