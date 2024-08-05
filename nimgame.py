import sys
class NimRBGame:
    def __init__(self,num_red,num_blue, version='standard', first_player = 'computer', depth=3):
        self.num_red = num_red
        self.num_blue = num_blue
        self.version = version
        self.current_player = first_player
        self.depth = depth

    def the_game_over(self,num_red,num_blue):
        if self.version == "standard":
            return num_red == 0 or num_blue == 0
        elif self.version == "misere":
            return num_red == 0 or num_blue == 0
        
    def give_score(self):
        return self.num_red* 3 + self.num_blue * 2
    
    def human_move(self):
        while True:
            try:
                num_red = int(input("Enter number of red marbles to be removed:"))
                num_blue = int(input("Enter number of blue marbles to be removed:"))
                if 0 <= num_red <= self.num_red and 0 <= num_blue <= self.num_blue and ( num_red + num_blue) > 0:
                    self.num_red -= num_red
                    self.num_blue -= num_blue
                    break
                else:
                 print("Move not accepted. Try again.")
            except ValueError:
                print("Invalid input. Please Try again.")
    def computer_move(self):
        move = self.minimax(self.num_red, self.num_blue, True, self.depth)
        num_red,num_blue = move[1], move[2]
        self.num_red -= num_red
        self.num_blue -= num_blue
        print(f"Computer removes {num_red} red marbles and {num_blue} blue marbles.")

    def minimax(self, red, blue, maximizing , depth):
        if self.the_game_over(red,blue):
            if self.version == 'standard':
                return (-(red* 2 + blue * 3), 0,0)
            else:
                return((red * 2 + blue * 3), 0,0)
        if depth ==0:
             return(self.search_value(red,blue), 0, 0)
        if maximizing:
            best_value = float('-inf')
            best_move = (0,0)
            for move in self.get_possible_moves(red,blue):
                new_red, new_blue = red - move[0] , blue - move[1]
                value = self.minimax(new_red, new_blue, False, depth - 1) [0]
                if value > best_value:
                    best_value = value
                    best_move = move
            return(best_value, best_move[0], best_move[1])
        else:
            best_value = float('inf')
            best_move = (0,0)
            for move in self.get_possible_moves(red,blue):
                new_red , new_blue = red - move[0] , blue - move[1]
                value = self.minimax(new_red , new_blue , True, depth - 1)[0]
                if value < best_value:
                    best_value = value
                    best_move = move
            return(best_value , best_move[0], best_move[1])
    def search_value(self , red , blue):
        return red * 2 + blue * 3
    def get_possible_moves(self, red , blue):
        moves = []
        if self.version == 'standard':
            if red >= 2: moves.append((2,0))
            if blue >= 2: moves.append((0,2))
            if red >= 1: moves.append((1,0))
            if blue >= 1: moves.append((0,1))
        elif self.version == 'misere':
            if blue >= 1: moves.append((0,1))
            if red >= 1: moves.append((1,0))
            if blue >= 2: moves.append((0,2))
            if red >= 2: moves.append((2,0))
        return moves
    def play_game(self):
        while not self.the_game_over(self.num_red, self.num_blue):
            print(f"Red Marbles:{ self.num_red}, Blue Marbles : { self.num_blue}")
            if self.current_player == 'human' :
                self.human_move()
                self.current_player = 'computer'
            else:
                self.computer_move()
                self.current_player ='human'
        print("Game over!")
        print(f"Final score: {self.give_score()}")
if __name__ == '__main__':
    num_red = int(input("Enter the number of red marbles to be played with:"))
    num_blue = int(input("Enter the number of blue marbles to be played with:"))
    version = input("Enter the game version(standard/misere):")
    first_player = input("Enter the first player to initialize the (computer/human):")
    depth = int(input("Enter the depth(like 3):"))

    game = NimRBGame(num_red , num_blue, version, first_player, depth)
    game.play_game()

