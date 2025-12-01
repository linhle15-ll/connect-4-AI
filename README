# Connect 4 - AI Game with Alpha-Beta Pruning

A Connect 4 game implementation featuring an AI opponent powered by the Minimax algorithm with Alpha-Beta Pruning optimization.

## Demo

![Gameplay Demo](public/Demo.gif)

_Gameplay demonstration_

<img src="public/Initial_State.png" alt="Human Wins" width="400"/>

_Initial State: Connect 4 game board with column highlighting on hover_


<img src="public/Human_Wins.png" alt="Human Wins" width="400"/>

_Human player wins after connecting 4 discs_

<img src="public/AI_Wins.png" alt="AI Wins" width="400"/>

_AI player wins after connecting 4 discs_

**Note**

- First player is assigned on random: if `turn == AI_TURN`, then it is AI playing first, else if `turn == HUMAN_TURN`, then it is Human playing first.
- Human player must click Exit to exit the game, otherwise it will automatically reset new game after 5 seconds on Game Over.

## Game Description

Connect 4 is a two-player strategy game where players take turns dropping colored discs into a 7-column, 6-row vertical grid. The objective is to be the first to form a horizontal, vertical, or diagonal line of four of one's own discs.

In this implementation, you play against an intelligent AI that uses the **Alpha-Beta Pruning** algorithm to make optimal moves.

## Game Rules

- The game randomly selects who plays first (AI or Human)
- Players alternate turns to place a disc in any available column
- Discs fall to the lowest available position in the selected column
- **Win Condition**: First player to connect 4 discs in a row (horizontal, vertical, or diagonal)
- **Draw Condition**: All columns are filled without a winner
- After game over, the board automatically resets after 5 seconds

## Game Features

- **Intelligent AI Player**: Uses Minimax with Alpha-Beta Pruning (depth = 4)
- **Interactive UI**: Click on columns to place your disc
- **Visual Feedback**: Column highlighting on mouse hover during your turn
- **Auto-Reset**: Game automatically resets after completion
- **Color Scheme**:
  - 🔴 **Red Discs**: Human Player
  - ⚫ **Navy Blue Discs**: AI Player

## Installation & Setup

### Prerequisites

- **Python 3.x** (Python 3.7 or higher recommended)
- **pip** (Python package manager)

### Step 1: Install Python 3

If you don't have Python 3 installed:

**macOS:**

```bash
# Using Homebrew
brew install python3

# Or download from python.org
# https://www.python.org/downloads/
```

**Windows:**

```bash
# Download from python.org
# https://www.python.org/downloads/
```

**Linux:**

```bash
sudo apt update
sudo apt install python3 python3-pip
```

### Step 2: Clone/Download the Project

```bash
# If using git:
git clone <repository-url>
cd final-project
```

### Step 3: Set Up Virtual Environment (Recommended)

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

# Your terminal should now show (venv) prefix
```

### Step 4: Install Dependencies

```bash
# Install pygame
pip install pygame
```

## How to Run

```bash
# Activate virtual environment
source activate.sh

# Run the game
python3 main.py
```

## How to Play

1. **Launch the game** using one of the methods above
2. **Wait for your turn**:
   - If you're first: Click on any column to place your red disc
   - If AI is first: Wait for the AI to make its move (navy blue disc)
3. **During your turn**:
   - Move your mouse over the board to see column highlights
   - Click on a column to drop your disc
4. **Win the game** by connecting 4 discs in a row
5. **Game resets automatically** after 5 seconds when someone wins

## AI Algorithm: Alpha-Beta Pruning

This AI implementation uses **Minimax with Alpha-Beta Pruning**, a decision-making algorithm that:

- **Maximizer (AI)**: Tries to maximize its score/evaluation
- **Minimizer (Human)**: From AI's perspective, tries to minimize the AI's advantage
- **Alpha-Beta Pruning**: Optimization technique that skips evaluating branches that won't affect the final decision
- **Depth**: Looks ahead 4 moves to evaluate positions
- **Evaluation Function**: Scores positions based on:
  - Center column control (strategic advantage)
  - Number of connected pieces (2, 3, or 4 in a row)
  - Blocking opponent's threats
  - Creating winning opportunities

## Project Structure

```
final-project/
├── main.py           # Game loop and alpha-beta pruning logic
├── board.py          # Board class and rendering
├── disc.py           # Disc class (game pieces)
├── constants.py      # Game constants and configuration
├── activate.sh       # Virtual environment activation script
├── venv/             # Virtual environment (created after setup)
└── README            # Documentation
```

## Academic Context

This project was developed for **COMSC-334 AI (Fall 2025)** at Mount Holyoke College.

This project is for educational purposes. Please contact me at le224l@mtholyoke.edu for questions.

## References

Sawwan, A. (2021). _Artificial Intelligence-Based Connect4 Player using Python_. AI Course Project Document. Available in the `Public` folder of this project.

---

**Enjoy playing Connect 4 against the AI! 🎮🤖**
