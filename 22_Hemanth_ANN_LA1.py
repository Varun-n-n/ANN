#!/usr/bin/env python
# coding: utf-8

# In[20]:


# Importing necessary libraries
import random
import math

print('Successfully imported necessary libraries!')


# In[21]:


# Class representing the Tic Tac Toe game
class TicTacToe:
    def __init__(self):
        self.board = [' ']*9  # Initialize an empty board
        self.current_player = 'X'  # Start with player 'X'

    # Method to print the current state of the board
    def print_board(self):
        for i in range(3):
            print('|'.join(self.board[i*3:i*3+3]))
            if i < 2:
                print('-'*5)

    # Method to get available moves (empty spaces) on the board
    def available_moves(self):
        return [i for i, v in enumerate(self.board) if v == ' ']

    # Method to make a move on the board
    def make_move(self, move):
        new_game = self.copy()  # Create a copy of the current game state
        new_game.board[move] = new_game.current_player  # Set the current player's symbol in the chosen position
        new_game.current_player = 'O' if new_game.current_player == 'X' else 'X'  # Switch player
        return new_game  # Return the modified game state

    # Method to check if there's a winner or a tie
    def check_winner(self):
        winning_combinations = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
        for combo in winning_combinations:
            if self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] != ' ':
                return self.board[combo[0]]  # Return the winning symbol ('X' or 'O')
        if ' ' not in self.board:  # If there are no empty spaces and no winner, it's a tie
            return 'Tie'
        return None  # If there's no winner yet, return None

    # Method to create a copy of the current game state
    def copy(self):
        new_game = TicTacToe()  # Create a new TicTacToe instance
        new_game.board = self.board[:]  # Copy the board
        new_game.current_player = self.current_player  # Copy the current player
        return new_game  # Return the copied game state

print('Successfully defined \'TicTacToe\' class!')


# In[22]:


# Class representing a node in the Monte Carlo Tree Search (MCTS)
class Node:
    def __init__(self, move=None, parent=None, state=None):
        self.move = move  # Move that led to this node from parent
        self.parent = parent
        self.children = []
        self.wins = 0  # Number of wins
        self.visits = 0  # Number of visits
        self.untried_moves = state.available_moves()  # List of untried moves
        self.current_player = state.current_player  # Current player symbol

    # Method to select a child node based on UCB1 formula
    def select_child(self):
        # Use UCB1 formula to select child node
        return max(self.children, key=lambda c: c.wins/c.visits + math.sqrt(2*math.log(self.visits)/c.visits))

    # Method to add a child node
    def add_child(self, move, state):
        child = Node(move=move, parent=self, state=state)
        self.untried_moves.remove(move)  # Remove the move from untried moves
        self.children.append(child)  # Add the child node to the children list
        return child

    # Method to update the number of wins and visits of a node
    def update(self, result):
        self.visits += 1  # Increment visits count
        self.wins += result  # Increment wins count based on the result of the simulation
        
print('Successfully defined \'Node\'!')


# In[23]:


# Simple evaluation function for Tic Tac Toe
def neural_network_evaluation(state):
    if state.check_winner() == 'X':  # If 'X' wins
        return -1
    elif state.check_winner() == 'O':  # If 'O' wins
        return 1
    else:  # If it's a tie
        return 0
    
print('Successfully defined the Evaluation Function!')


# In[24]:


# Monte Carlo Tree Search algorithm(deep_learning_technique)

def mcts(state, iterations):
    root = Node(state=state)  # Create the root node with the initial game state
    for _ in range(iterations):
        node = root  # Start from the root node
        current_state = state.copy()  # Create a copy of the current game state
        depth = 0  # Track the depth of the search tree
        # Selection phase
        while not node.untried_moves and node.children:
            node = node.select_child()  # Select the child node with the highest UCB1 value
            current_state = current_state.make_move(node.move)  # Update the game state based on the selected move
            depth += 1  # Increment depth
        # Expansion phase
        if node.untried_moves:
            # First, check if there are winning moves available
            winning_moves = [move for move in node.untried_moves if current_state.make_move(move).check_winner() == current_state.current_player]
            if winning_moves:
                move = random.choice(winning_moves)  # Choose a winning move randomly
            else:
                move = random.choice(node.untried_moves)  # Choose a random move from untried moves
            current_state = current_state.make_move(move)  # Update the game state based on the chosen move
            node = node.add_child(move, current_state)  # Add the new child node
            depth += 1  # Increment depth
        # Simulation phase
        while not current_state.check_winner():  # Continue simulation until there's a winner
            move = random.choice(current_state.available_moves())  # Choose a random move
            current_state = current_state.make_move(move)  # Update the game state based on the chosen move
            depth += 1  # Increment depth
        result = neural_network_evaluation(current_state)  # Evaluate the final game state
        # Backpropagation phase
        while node:  # Update all nodes visited during the search
            node.update(result)  # Update the node with the simulation result
            node = node.parent  # Move to the parent node
    best_move = max(root.children, key=lambda c: c.visits).move  # Choose the best move based on visit counts
    return best_move  # Return the best move

print('Successfully Implemented \'Monte-Carlo Tree Search\',[A deep_learning technique]!')


# In[25]:


#lets integrate above functions into main_function!
# Function to play the Tic Tac Toe game

def play_game():
    game = TicTacToe()  # Create a new TicTacToe instance
    print("Welcome to Tic Tac Toe!")
    while not game.check_winner():  # Continue playing until there's a winner or a tie
        game.print_board()  # Print the current state of the board
        if game.current_player == 'X':  # If it's player X's turn
            move = int(input("Enter your move (1-9): "))-1  # Get input from the user
        else:  # If it's AI's turn
            print("AI is thinking...\n")
            move = mcts(game, iterations=1000)  # Use MCTS to find the best move
        if move in game.available_moves():  # Check if the chosen move is valid
            game = game.make_move(move)  # Make the move
        else:
            print("Invalid move, try again.\n")  # If the move is invalid, prompt the user to try again
    game.print_board()  # Print the final state of the board
    winner = game.check_winner()  # Get the winner or 'Tie'
    if winner == 'Tie':
        print("It's a tie!")  # Print if it's a tie
    else:
        print(f"{winner} wins!")  # Print the winner


# In[31]:


#Model is Ready
#Lets Execute it!

if __name__ == "__main__":
    play_game()


# In[ ]:




