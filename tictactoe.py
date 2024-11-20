import random

# Tic-Tac-Toe board
board = [' ' for _ in range(9)]  # 3x3 board represented as a list of 9 elements

# Print the current board
def print_board():
    for i in range(3):
        print(f"{board[i*3]} | {board[i*3 + 1]} | {board[i*3 + 2]}")
        if i < 2:
            print("--+---+--")
    print("\n")

# Check for a win condition
def check_winner(b):
    # Win conditions for rows, columns, and diagonals
    winning_combinations = [(0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
                            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columns
                            (0, 4, 8), (2, 4, 6)]  # Diagonals
    for combo in winning_combinations:
        if b[combo[0]] == b[combo[1]] == b[combo[2]] != ' ':
            return b[combo[0]]
    return None

# Check if the board is full (draw condition)
def is_board_full(b):
    return ' ' not in b

# Minimax algorithm to choose the best move for AI
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

# Get the best move for AI
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

# Main game loop
def play_game():
    print("Tic-Tac-Toe Game")
    print_board()

    while True:
        # Player's move
        while True:
            try:
                player_move = int(input("Choose your move (1-9): ")) - 1
                if board[player_move] == ' ':
                    board[player_move] = 'X'
                    break
                else:
                    print("This spot is already taken. Try again.")
            except (ValueError, IndexError):
                print("Invalid input. Please choose a number between 1 and 9.")

        print_board()

        # Check if the player wins
        if check_winner(board) == 'X':
            print("You win!")
            break

        # Check if the board is full (draw condition)
        if is_board_full(board):
            print("It's a draw!")
            break

        # AI's move
        ai_move = get_ai_move()
        board[ai_move] = 'O'
        print(f"AI's move: {ai_move + 1}")
        print_board()

        # Check if the AI wins
        if check_winner(board) == 'O':
            print("AI wins!")
            break

        # Check if the board is full (draw condition)
        if is_board_full(board):
            print("It's a draw!")
            break

# Start the game
if __name__ == "__main__":
    play_game()
