# # Tic-Tac-Toe with Minimax and Alpha-Beta Pruning
import time

# Constants
HUMAN = 'O'
AI = 'X'
EMPTY = ' '

# Initialize board
board = [EMPTY for _ in range(9)]

def print_board(b):
    for i in range(3):
        print(f"{b[3*i]} | {b[3*i+1]} | {b[3*i+2]}")
        if i < 2:
            print("--+---+--")
    print()

def print_reference_board():
    print("Reference board with positions:")
    for i in range(3):
        print(f"{3*i} | {3*i+1} | {3*i+2}")
        if i < 2:
            print("--+---+--")
    print()

def is_winner(b, player):
    win_cond = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]
    return any(all(b[i] == player for i in line) for line in win_cond)

def is_full(b):
    return all(cell != EMPTY for cell in b)

def get_available_moves(b):
    return [i for i, cell in enumerate(b) if cell == EMPTY]

# Minimax algorithm
def minimax(b, is_maximizing):
    if is_winner(b, AI):
        return 1
    elif is_winner(b, HUMAN):
        return -1
    elif is_full(b):
        return 0

    if is_maximizing:
        best_score = float('-inf')
        for move in get_available_moves(b):
            b[move] = AI
            score = minimax(b, False)
            b[move] = EMPTY
            best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for move in get_available_moves(b):
            b[move] = HUMAN
            score = minimax(b, True)
            b[move] = EMPTY
            best_score = min(score, best_score)
        return best_score

def best_move_minimax():
    best_score = float('-inf')
    move = None
    for i in get_available_moves(board):
        board[i] = AI
        score = minimax(board, False)
        board[i] = EMPTY
        if score > best_score:
            best_score = score
            move = i
    return move

# Minimax with Alpha-Beta Pruning
def minimax_ab(b, depth, alpha, beta, is_maximizing):
    if is_winner(b, AI):
        return 1
    elif is_winner(b, HUMAN):
        return -1
    elif is_full(b):
        return 0

    if is_maximizing:
        max_eval = float('-inf')
        for move in get_available_moves(b):
            b[move] = AI
            eval = minimax_ab(b, depth+1, alpha, beta, False)
            b[move] = EMPTY
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in get_available_moves(b):
            b[move] = HUMAN
            eval = minimax_ab(b, depth+1, alpha, beta, True)
            b[move] = EMPTY
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def best_move_ab():
    best_score = float('-inf')
    move = None
    for i in get_available_moves(board):
        board[i] = AI
        score = minimax_ab(board, 0, float('-inf'), float('inf'), False)
        board[i] = EMPTY
        if score > best_score:
            best_score = score
            move = i
    return move

# Play the game using Alpha-Beta Pruning
def play_game():
    global board
    board = [EMPTY for _ in range(9)]
    current_player = HUMAN  # Human always starts

    print("Tic-Tac-Toe Game\n")
    print("Player 1: Human (O)")
    print("Player 2: AI (X)\n")
    print_reference_board()
    print_board(board)

    while True:
        if current_player == HUMAN:
            print("Player 1 - Human's turn")
            move = int(input("Enter your move (0-8): "))
            if board[move] != EMPTY:
                print("Invalid move. Try again.")
                continue
            board[move] = HUMAN
        else:
            print("Player 2 - AI's turn")
            move = best_move_ab()
            board[move] = AI

        print_board(board)

        if is_winner(board, current_player):
            winner = "Player 1 - Human" if current_player == HUMAN else "Player 2 - AI"
            print(f"{winner} wins!")
            break
        elif is_full(board):
            print("It's a draw!")
            break

        current_player = HUMAN if current_player == AI else AI

# Performance comparison
def compare_algorithms():
    global board
    board = [EMPTY for _ in range(9)]
    print("\nMinimax performance:")
    start = time.time()
    best_move_minimax()
    end = time.time()
    print(f"Time taken: {end - start:.6f} seconds")

    board = [EMPTY for _ in range(9)]
    print("\nAlpha-Beta Pruning performance:")
    start = time.time()
    best_move_ab()
    end = time.time()
    print(f"Time taken: {end - start:.6f} seconds")

# Run game and comparison
if __name__ == '__main__':
    play_game()
    compare_algorithms()