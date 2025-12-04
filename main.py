# Set up game state and main algorithm here
import pygame
import sys
import random

from board import Board
from disc import Disc
from constants import (DEPTH, AI_TURN, HUMAN_TURN, SCREEN,
                       ROWS, COLS, HIGHEST_SCORE, LOWEST_SCORE, ALPHA, BETA, 
                       RED, WHITE, CELL_SIZE, NAVY_BLUE, SHADE_GRAY)

# end the game which will close the window eventually
def end_game():
    global game_over
    game_over = True
        
def reset_game():
    """Reset the game to initial state"""
    board = Board()
    turn = random.choice([HUMAN_TURN, AI_TURN])
    game_over = False
    SCREEN.fill(WHITE)
    board.draw_board(SCREEN)
    pygame.display.update()
    return board, turn, game_over

def get_valid_columns(board: Board):
    valid_columns = []
    for col in range(COLS):
        if board.is_valid_column(col):
            valid_columns.append(col)
    return valid_columns

def highlight_column(board, column):
    """Highlight a column when mouse hovers over it
    
    Args:
        board: Board object to redraw
        column: Column index to highlight
    """
    if column < 0 or column >= COLS:
        return
    
    # Redraw the board first
    SCREEN.fill(WHITE)
    board.draw_board(SCREEN)
    
    # Draw semi-transparent highlight over the column
    highlight_surface = pygame.Surface((CELL_SIZE, CELL_SIZE * ROWS))
    highlight_surface.set_alpha(50)  # Transparency level (0-255)
    highlight_surface.fill(SHADE_GRAY)
    SCREEN.blit(highlight_surface, (column * CELL_SIZE, CELL_SIZE))
    
    pygame.display.update()

# ==== Alpha-Beta Pruning Algorithm ====
def winning_move(board: Board, turn: int):
    """Check if a player (0 for AI, or 1 for Human) has won 

    Args:
        board (Board): Board object
        turn (int): 0 (AI) or 1 (Human)

    Returns:
        bool: check if the player in turn (HUMAN_TURN or AI_TURN) is the winner
    """
    curr_board = board.board
    
    # check horizonal range of 4 for win
    # range of row and col is determined so that they are not out of range when increase/ decrease by i
    for row in range(ROWS):
        for col in range(COLS - 3): # 7 - 3 = 4
            if all(curr_board[row][col+i] == turn for i in range(4)):
                return True
        
    # check vertical range of 4 for win
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(curr_board[row+i][col] == turn for i in range(4)):
                return True
    
    # check positively sloped diagonal for win - decreased row, increased col
    for col in range(COLS - 3):
        for row in range(3, ROWS):
            if all(curr_board[row-i][col+i] == turn for i in range(4)):
                return True

    # check negatively sloped diagonal for win - increased row, increased col
    for col in range(COLS - 3): 
        for row in range(ROWS - 3):
            if all(curr_board[row+i][col+i] == turn for i in range(4)):
                return True
    
    return False
    
def is_termninal_node(board: Board):
    """Check if the current turn or node in the minimax tree is terminal
    A terminal node is either human or AI winning, or draw if board is filled up without winner

    Args:
        board (Board)

    Returns:
        bool: check if the current turn is terminal
    """
    valid_columns = get_valid_columns(board)

    # terminal if someone has won or there are no valid columns left
    return (winning_move(board, HUMAN_TURN) or 
        winning_move(board, AI_TURN) or 
        len(valid_columns) == 0)
    
def evaluate_window(window, turn:int):
    """ Evaluatation function
    Evaluate a window of 4 locations in a row/ col/ horizontal based on what value/turn value it contains (0 or 1)
    From AI's perspective   
    
    positive scores = good for AI
    negative scores = bad for AI
    
    Args:
        window: list of 4 disc objects or None
        turn (int): 0 if AI_TURN, 1 if HUMAN_TURN
    """
    score = 0
    
    # Count number of friendly values, opponent values, and None in the window list
    if window is None:
        return score
    
    ai_count = window.count(AI_TURN)
    human_count = window.count(HUMAN_TURN)
    none_count = window.count(None)
    
    # Positive scores for AI's good positions (scale chosen so human threats
    # outweigh AI's similar-length threats)
    if ai_count == 4:  # AI wins
        score += HIGHEST_SCORE
    elif ai_count == 3 and none_count == 1:
        score += 500
    elif ai_count == 2 and none_count == 2:
        score += 300
    elif ai_count == 1 and none_count == 3:
        score += 100

    # Decrease scores if Human's good positions (threats to AI)
    if human_count == 4:  # Human wins
        score += LOWEST_SCORE
    elif human_count == 3 and none_count == 1:
        # Very large negative: block immediate human win should be top priority
        score -= 1000
    elif human_count == 2 and none_count == 2:
        score -= 700
    elif human_count == 1 and none_count == 3:
        score -= 300
    
    return score

def score_position(board: Board, turn: int):
    """Evaluate the entire board position

    Args:
        board (Board): Board object
        turn (int): 0 if AI_TURN, 1 if HUMAN_TURN
    """
    score = 0
    curr_board = board.board  # Get the 2D array, not a copy
    
    # Score center column (connecting in center is often advantageous)
    center_col_idx= COLS // 2
  
    # get the center columnn values
    center_col = [curr_board[row][center_col_idx] for row in range(ROWS)]
    center_count = center_col.count(turn)
    score += center_count * 100

    # score for horizonal, range of 4 
    for row in range(ROWS):
        for col in range(COLS - 3): # 7 - 3 = 4
            window = [curr_board[row][col+i] for i in range(4)]
            score += evaluate_window(window, turn)
                    
    # score for vertical, range of 4
    for col in range(COLS):
        for row in range(ROWS - 3):
            window = [curr_board[row+i][col] for i in range(4)]
            score += evaluate_window(window, turn)
            
    # score for positively sloped diagonal range of 4
    for col in range(COLS - 3):
        for row in range(3, ROWS):
            window = [curr_board[row-i][col+i] for i in range(4)]
            score += evaluate_window(window, turn)
            
    # score for negatively sloped diagonal, range of 4
    for col in range(COLS - 3): 
        for row in range(ROWS - 3):
            window = [curr_board[row+i][col+i] for i in range(4)]
            score += evaluate_window(window, turn)
            
    return score

def alpha_beta_pruning(board: Board, depth: int, player_turn: int, alpha: float, beta: float):
    """Implement Alpha-Beta Pruning Algorithm

    Args:
        board (Board): board that is active
        depth (int): depth of tree
        player_turn (int): 0 if AI_TURN (Maximizer), 1 if HUMAN_TURN
        alpha (float): alpha value, initiatially -infinity
        beta (float): beta value, initially +infinity
    """
    valid_columns = get_valid_columns(board)
    is_termninal = is_termninal_node(board)
    
    # base case
    if is_termninal: 
        if winning_move(board, AI_TURN): # if AI has won
            return (None, HIGHEST_SCORE)
        elif winning_move(board, HUMAN_TURN):  # if Human has won
            return (None, LOWEST_SCORE)
        else: # if draw
            return (None, 0)
    
    # if depth == 0, simply score the current board
    elif depth == 0:
        return (None, score_position(board, AI_TURN)) # Note: score in the AI's perspective (the maximizer), regardless of whose turn in the simulation
    
    # if maximizer (AI)
    if player_turn == AI_TURN:
        max_eval = float("-inf")
        best_column = random.choice(valid_columns) # initially choose a random valid column
        
        # for every valid column, simulate placing a disc/ place a turn value
        # use copy of board, run alpha beta pruning 
        # imagine from a board version, we have different scenerios leading different game states for different ways of placing disc to different columns
        for column in valid_columns:
            board_copy = board.copy() # A copy of current copy 
            row = board.get_next_open_row(column)
            board_copy.place_value(row, column, AI_TURN) # place turn value in the simulated space of current board
            
            eval = alpha_beta_pruning(board_copy, depth - 1, HUMAN_TURN, alpha, beta)[1] # column, eval
            if eval > max_eval:
                max_eval = eval
                best_column = column
                
            alpha = max(alpha, eval)
            
            if beta <= alpha:
                break
            
        return best_column, max_eval
          
    # if minimizer        
    elif player_turn == HUMAN_TURN:
        min_eval = float("inf")
        best_column = random.choice(valid_columns)
        
        for column in valid_columns:
            board_copy = board.copy() 
            row = board_copy.get_next_open_row(column)
            board_copy.place_value(row, column, HUMAN_TURN)
            
            eval = alpha_beta_pruning(board_copy, depth - 1, AI_TURN, alpha, beta)[1]
            if eval < min_eval:
                min_eval = eval
                best_column = column
            
            beta = min(beta, eval)
            if beta <= alpha:
                break
            
        return best_column, min_eval
    
if __name__ == "__main__":
    board = Board()
    turn = random.choice([HUMAN_TURN, AI_TURN]) # randomize the first turn
    game_over = False
    
    # initialize game
    pygame.init()
    
    # Fill screen with background color
    SCREEN.fill(WHITE)  # White background
    
    # draw GUI
    board.draw_board(SCREEN)
    
    pygame.display.update()
    my_font = pygame.font.SysFont("Arial", 75, bold=True)
    
    # Game loop that runs while game is not over (GAME_OVER == False) (i.e, none has placed 4 in a row/col/horizontal axis yet)
    running = True
    last_hovered_col = -1  # Track last highlighted column
    
    while running:
        # for every player's event
        for event in pygame.event.get():
            # if player closes the window, exit the game
            if event.type == pygame.QUIT:
                sys.exit()
            
            # Track mouse motion for column highlighting (only during human's turn)
            if event.type == pygame.MOUSEMOTION and not game_over and turn == HUMAN_TURN:
                x_pos = event.pos[0]
                curr_col = int(x_pos // CELL_SIZE)
                
                # Only redraw if hovering over a different column
                if curr_col != last_hovered_col and 0 <= curr_col < COLS:
                    highlight_column(board, curr_col)
                    last_hovered_col = curr_col
            
            # if that stack is valid to place a disc on the top + curr_player == HUMAN_PLAYER, on user's mouse click, place the disc (note: disc color is based on current player)
            if not game_over and turn == HUMAN_TURN and event.type == pygame.MOUSEBUTTONDOWN:
                x_pos = event.pos[0]
                curr_col = int(x_pos // CELL_SIZE)
                
                # check for the validity of the curr_col to place turn value (0 for AI, 1 for Human)
                # only allow player's move if they click mouse in a valid column
                if curr_col >= 0 and curr_col < COLS and board.is_valid_column(curr_col):
                    valid_row = board.get_next_open_row(curr_col)
                    if valid_row >= 0 and valid_row < ROWS:
                        board.place_value(valid_row, curr_col, HUMAN_TURN)
                        
                        # Redraw the entire board
                        SCREEN.fill(WHITE)
                        board.draw_board(SCREEN)
                        pygame.display.update()
                        
                        # check if it is a winning move
                        if winning_move(board, HUMAN_TURN):
                            print("Human player wins!")
                            SCREEN.fill(WHITE)
                            board.draw_board(SCREEN)
                            label = my_font.render("HUMAN WINS!", 1, RED)
                            SCREEN.blit(label, (80, 10))
                            pygame.display.update()
                            
                            game_over = True
                            pygame.time.wait(5000)  # Wait 5 seconds
                            board, turn, game_over = reset_game()
                            continue
                                                    
                    # switch turn
                    turn = (turn + 1) % 2
                                   
                # if mouse not on valid column, does not allow to create a new disc
            
            # if current_player == AI_PLAYER
            elif not game_over and turn == AI_TURN:
                # run alpha-beta pruning algorithm: find the column to create a new AI's disc 
                depth = DEPTH
                best_column, minimax_score = alpha_beta_pruning(board, depth, player_turn=turn, alpha = ALPHA, beta = BETA)
                
                if best_column >= 0 and best_column < COLS and board.is_valid_column(best_column):
                    valid_row = board.get_next_open_row(best_column)
                    
                    if valid_row >= 0 and valid_row < ROWS:
                        board.place_value(valid_row, best_column, AI_TURN)
                        
                        # Redraw the entire board
                        SCREEN.fill(WHITE)
                        board.draw_board(SCREEN)
                        pygame.display.update()
                        
                        # check if it is a winning move
                        if winning_move(board, AI_TURN):
                            print("AI player wins!")
                            SCREEN.fill(WHITE)
                            board.draw_board(SCREEN)
                            label = my_font.render("AI WINS!", 1, NAVY_BLUE)
                            SCREEN.blit(label, (150, 10))
                            pygame.display.update()
                            
                            game_over = True
                            pygame.time.wait(5000)  # Wait 5 seconds
                            board, turn, game_over = reset_game()
                            continue
                        
                    # switch turn
                    turn = (turn + 1) % 2
    
            pygame.display.update()

    pygame.quit()
    sys.exit()      
