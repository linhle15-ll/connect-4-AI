from constants import ROWS, COLS, DISC_RADIUS, CELL_SIZE, RED, WHITE, LIGHT_GRAY, NAVY_BLUE, RED 
from disc import Disc
import pygame

class Board:
    def __init__(self):
        # Store board as 0s (AI), 1s (Human), or None (empty)
        self.board = [[None] * COLS for _ in range (ROWS)]
    
    def place_value(self, row: int, col: int, turn: int):
        """Place a value (0 or 1) on the board
        
        Args:
            row (int): row to place value
            col (int): column to place value
            turn (int): value 0 for AI, 1 for Human
        """
        self.board[row][col] = turn
    
    def is_valid_column(self, col: int):
        """Check if a column has space for a new piece
        
        Args:
            col (int): column to check
            
        Returns:
            bool: True if column not full, False otherwise
        """
        return self.board[0][col] is None
    
    def get_next_open_row(self, col: int):
        """Get the next available row in a column
        
        Args:
            col (int): column to check
        
        Returns:
            int or None: row index if available, None if column is full
        """
        for row in range(ROWS - 1, -1, -1):
            if self.board[row][col] is None:
                return row
        return None
    
        
    def draw_board(self, screen):
        """Draw the entire board with all placed discs
        
        Args:
            screen: pygame screen to draw on
        """
        for row in range(ROWS):
            for col in range(COLS):
                # Draw rectangle for each cell
                pygame.draw.rect(
                    surface=screen,
                    color=LIGHT_GRAY,
                    rect=(col * CELL_SIZE, row * CELL_SIZE + CELL_SIZE, CELL_SIZE, CELL_SIZE),
                )
                
                # Calculate center of the cell
                center_x = int(col * CELL_SIZE + CELL_SIZE // 2)
                center_y = int(row * CELL_SIZE + CELL_SIZE + CELL_SIZE // 2) # one more CELL_SIZE here since we have an extra space to display title near Ox axis
                
                if self.board[row][col] == 0: # AI 
                    Disc.draw(color=NAVY_BLUE, center_x=center_x, center_y=center_y)
                    
                elif self.board[row][col] == 1: # HUMAN
                    Disc.draw(color=RED, center_x=center_x, center_y=center_y)
                    
                else: # Empty cell 
                    Disc.draw(color=WHITE, center_x=center_x, center_y=center_y)
        pygame.display.update()  
        
                    
    def copy(self):
        """Create a deep copy of the current board
        We want to copy the nested objects inside, and create a new object from the original version (deep copy > shallow copy)
        
        Returns: A deep copy of the current board (Board type)
        """
        new_board = Board()
        new_board.board = [row[:] for row in self.board]
        
        return new_board