import pygame

# RGB colors
WHITE = (255, 255, 255) # unfilled cell on board + background
BLACK = (0, 0, 0)
LIGHT_GRAY = (240, 240, 240)
SHADE_GRAY = (200, 200, 200)
RED = (196, 30, 58) # Human player
NAVY_BLUE = (0, 0, 128) # AI Player
TRANSPARENT = (0, 0, 0, 0)

# Screen
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Connect4 - Artificial Intelligence - Ngoc Linh Le")

# Board settings (square board)
ROWS = 6
COLS = 7
CELL_SIZE = 100
WIDTH = COLS * CELL_SIZE
HEIGHT = (ROWS + 1) * CELL_SIZE  # Extra row for top spacing/text

# Disc 
DISC_WIDTH = 0
DISC_RADIUS = 45

# Game states
AI_TURN = 0
HUMAN_TURN = 1
HIGHEST_SCORE = 10000000
LOWEST_SCORE = -10000000
DEPTH = 4
ALPHA = float("inf")
BETA = float("-inf")

"""
Rules:
- Pick either (0 - AI) or (1 - Human) to play first
- Alternatively take turn to make a move
- Winning if either Human or AI place 4 discs in a row/ col/ horizontal first
- Draw if all the columns are filled with disc but no winning state is satisfied

Game UI Idea:
- Base on the player (AI or human) to draw a disc to a valid board[row][col] on cell
- A valid cell to draw a new disc in is:
(1) empty 
(2) 0 <= row <= ROWS - 1, 0 <= col <= COLS - 1
(3) append disc to the col as stack, which means that its previous cell must either be out of range 
so it is the first cell to be filled in the col stack, or its previous cell must be in range and is filled

Define:
[] UI: disc, board/ screen
[] Roles
[] Turn
[] Game states

Alpha-Beta Pruning - Minimimax:
- An optimization of Minimax
- AI is the maximizer - try to maximize its score/ evaluation
- Human is the minimizer - from AI's perspective, the human is trying to minimize the AI's advantage
- If HUMAN_TURN, human is only allowed to place the disc in valid position (define) in any column that they are placing mouse on
- If AI_TURN, use Alpha Beta Pruning Algorithm to find the best/ most optimal column in the valid columns list to place its disc in

"""