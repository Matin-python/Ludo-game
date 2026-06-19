"""
LUDO GAME SIMULATION
MohammadReza Bakhshandeh 2024
RULE:
    A player will get spawned only if he/she gets 6 in the dice. 
    After that, if the player gets the number n in the dice, he/she moves forward n boxes.
    He/she can't put more than 1 piece in start place
    start place is safe and can't hit by other piece

"""


import random
import itertools
import time

end_spaces = [41, 42, 43, 44]  # End spaces for the pieces
safe_spaces = [0, 1, 41, 42, 43, 44]  # you can't hit the piece in there spaces
class Dice:
    #Since all the players will use the same dice to play, there need not be more than one instances of dice
    #So, it is better if Dice is made static.
    @staticmethod
    def roll():
        while True:
            if input("Press enter to roll a dice: ") == "":
                return random.randint(1, 6)
            else:
                print("Invalid input. Press enter to roll a dice.")

    
class Players:    
    def __init__(self, name, color= 'R'):
        self.name = name
        self.color = color
        self.position = [0, 0, 0, 0]
        self.which_move = 0
        # set this variable to know where the pieces are and if they are in the same position they hit each other
        self.real_position = [0, 0, 0, 0]
        self.flag_not_move = 1
        
        # The player is not born (meaning he/she will remain at position 0 till dice shows 6)
        self.born = [False, False, False, False]
    
    def has_won(self):
        # All pieces arrived at home every color must full 41 42 43 44 of there place
        if all(piece in end_spaces for piece in self.position):
            print(self.name, ' win.')
    
    def update_position(self, dicevalue):
        self.double_check(dicevalue)
        if self.flag_not_move == 1:
            return
        while True:
            try:
                self.which_move = int(input("Enter a number between 1 to 4 to move your piece: "))
                self.which_move = self.which_move - 1
                if 0 <= self.which_move <= 3:
                    if self.born[self.which_move] == True:
                        self.flag_not_move = 0
                        break
                    elif dicevalue == 6:
                        for i in range (len(self.position)):
                            if self.position[i] == 1:
                                print('You can\'t born new piece because you have already one in start position')
                                self.update_position(dicevalue)
                                return
                            
                        self.born[self.which_move] = True
                        self.flag_not_move = 0
                        break
                    else:
                        print("Please enter a number(piece) that you can move.") 
                else:
                    print("Invalid input. Please enter a number between 1 to 4.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")
                
        new_pos = self.position[self.which_move] + dicevalue

        if dicevalue == 6 and self.position[self.which_move] == 0:
            new_pos = 1

        #if new position exceeds 44, don't update the current position
        #instead, return
        if new_pos > 44:
            #if he can change the piece and move it
            for i in range (len(self.position)):
                if self.position[i] in [0, 41, 42, 43, 44]:
                    self.flag_not_move = 1
                    
                else:
                    self.flag_not_move = 0
                    break
                
            if self.flag_not_move == 0 or dicevalue == 6:
                print ('You can\'t move this piece choose another piece.')
                self.update_position(dicevalue)
            else:    
                print ('You can\'t move any piece. ')   
            return
        else:
            if self.position.count(new_pos) == 1:
                print ('You can\'t move this piece because occupied by another piece, please choose another piece.')
                self.update_position(dicevalue)
                return

            if new_pos in end_spaces:
                self.position[self.which_move] = new_pos
                print(self.name,' piece number ', str(self.which_move + 1), ' is home and safe')
            else:    
                self.position[self.which_move] = new_pos

        match self.color:
            #Each player piece position set base on Red 
            case 'R':
                print(self.name, "'s positions are based on RED position on the board.")
                for i in range (len(self.position)):
                    self.real_position[i] = self.position[i]
                    print(self.name, "POSITION ==>", self.real_position[i])
            case 'G':
                print(self.name, "'s positions are based on RED position on the board.")
                for i in range (len(self.position)):
                    self.real_position[i] = self.position[i] + 10
                    if self.real_position[i] > 40:
                        self.real_position[i] = self.real_position[i] - 40
                    print(self.name, "POSITION ==>", self.real_position[i])
            case 'B':
                print(self.name, "'s positions are based on RED position on the board.")
                for i in range (len(self.position)):
                    self.real_position[i] = self.position[i] + 20
                    if self.real_position[i] > 40:
                        self.real_position[i] = self.real_position[i] - 40
                    print(self.name, "POSITION ==>", self.real_position[i])
            case 'Y':
                print(self.name, "'s positions are based on RED position on the board.")
                for i in range (len(self.position)):
                    self.real_position[i] = self.position[i] + 30
                    if self.real_position[i] > 40:
                        self.real_position[i] = self.real_position[i] - 40
                    print(self.name, "POSITION ==>", self.real_position[i])
            case default:
                print ('Inputs are not what we expected')
            
        self.hit_piece()
        
    def double_check(self, dicevalue):
        # check if any piece born
        for i in range (len(self.position)):
            if self.position[i] == 0 and dicevalue != 6:
                self.flag_not_move = 1
            else:
                self.flag_not_move = 0
                break 

        if self.flag_not_move == 1:
            print(self.name + " player is not born yet")
            return
        
        # check if any piece can move
        for i in range(0, 4):
            new_pos = self.position[i] + dicevalue
            if new_pos > 44 or self.position.count(new_pos) == 1:
                self.flag_not_move = 1
                    
            else:
                self.flag_not_move = 0
                break
        
        if self.flag_not_move == 1:
            print ('You can\'t move any piece. ')   
        return
        

    def print_position(self):
        print(self.name, "'s positions are based on his own position on the board.")
        for i in range (0,4):
            print(self.name, "POSITION ==>", str(self.position[i]), '\tstatus =', str(self.born[i]))
    
    def play(self):
        dicevalue = Dice.roll()

        print(self.name + ": DICE SHOWS: " + str(dicevalue))

        while True:
            #The following is emulation of a do-while loop
            self.update_position(dicevalue)

            if self.flag_not_move == 1:
                break

            self.print_position()

            #if dicevalue is not 6, her turn is finished
            if dicevalue != 6:
                break
            #else roll the dice again
            else:
                dicevalue = Dice.roll()
                print(self.name + ": DICE SHOWS: " + str(dicevalue))
                    
    def hit_piece(self):
        for player in players:
            if player != self:  # Compare with other players only
                for i in range (4):
                    for j in range (4):
                        print(i)
                        print (self.real_position[i], player.real_position[j])
                        if self.real_position[i] == player.real_position[j]:
                            if self.born[i] == True:
                                # If the piece is on a safe space, or the player hasn't spawned yet,
                                # or the player's current position is a safe space...
                                if self.real_position[i] in safe_spaces or \
                                    not player.born[j] or \
                                    player.position[j] in safe_spaces:
                                    pass
                                else:
                                    # Change the position of the hit piece to 0 and set its alive status to False
                                    print(f"Your piece at position {self.real_position[i]} hit {player.name}'s piece.")
                                    player.position[j] = 0
                                    player.born[j] = False
                                    print(f"{player.name}'s piece at position {player.real_position[j]} is now eliminated.")
                            else:
                                pass
                            
class Game:
    def __init__(self, players):
        self.players = itertools.cycle(players)
        self.num_players = len(players)

        #This list is created so that we can check if any players have won
        #For checking that, we have called next(..) function on the list
        #If we had used the next(..) function on the original players iterator list,
        #then it would alter the playing sequence and it is difficult to know which player's turn it is next
        #So, self.players is for the sole purpose of tracking next player
        #and self.mutable_players is kind of temporary list
        self.mutable_players = itertools.cycle(players)

    def has_finished(self): 
        for i in range(self.num_players):
            player = next(self.mutable_players)
            if player.has_won():
                return True
        return False

    def next_player(self):
        return next(self.players)
    

# current script is being run directly or being imported
if __name__ == "__main__":
    while True:
        try:
            no_of_players = int(input("Enter the no of player(1 to 4 player): "))
            if 1 <= no_of_players <= 4:
                break
            else:
                print("Invalid input. Please enter a number between 1 to 4.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")
    print("Enter the name of players:")
    player_names = [input(f'Player {i + 1}: ') for i in range(no_of_players)]

    print("Enter the color of players(Green= G, Red= R, Yellow= Y, Blue= B):")
    player_color = []
    for i in range(no_of_players):
        color = input(f'Player {i + 1}: ')
        color = color.capitalize()
        while color not in ['G', 'R', 'Y', 'B'] or color in player_color:
            if color in player_color:
                print("Color has already been chosen. Please select a different color.")
            else:
                print("Invalid input. Please enter a valid color (G, R, Y, B).")
            color = input(f'Player {i + 1}: ')
            color = color.capitalize()
        player_color.append(color)
    
    players = [Players(name, color) for name,color in zip(player_names, player_color)]

    game = Game(players)
    while not game.has_finished():
        player = game.next_player()
        player.play()
        print("-----------End turn-----------")
        #time.sleep(1)

print ('Congrats')
