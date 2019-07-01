## Clue Simulation
## CS 480
## File basePuzzle
## Implements and runs the game of clue
## Jonathan Rogers, Kate Kielkopf

import player
import Board
import random
import movement2

class BaseGame():

    """
    The game consists of a board, movement, players, and stragedy
    There is also a set of cards, with three subsets:
    - Suspects
    - Possible Weapons
    - Possible Murder Scene
    The goal of the game is to figure out the who, how, and where
    The first player to successfully do that wins
    """

    """
    Start up baseGame
    """
    def __init__(self, totalPlayers):
        self.totalPlayers = totalPlayers
        self.suspects = ["Mr. Green", "Col Mustard", "Mrs. Peacock", "Prof. Plum", 
           "Miss Scarlet", "Mrs. White"]
        self.weapons = ["Candlestick", "Knife", "Lead Pipe", "Revolver", "Rope", "Wrench"]
        self.rooms = ["Ball Room", "Billiard Room", "Conservatory", "Dining Room", "Hall",
        "Kitchen", "Library", "Lounge", "Study"]
        self.totalDeck = self.suspects + self.weapons + self.rooms
        self.envelope = self.whatHappenedToMrBobby()
        self.players = self.set_up_players()
        self.board = Board.Board()
        
        self.movemnt = []
        for i in range(self.totalPlayers):
            self.movemnt += [movement2.Movement(self.board, self.players[i])]
    
 

    """
    This sets up the envelope which contains the murder scenario which is a set of {suspect, weapon, room}
    
    """
    def whatHappenedToMrBobby(self):
        whoCard = random.randint(0,5)
        howCard = random.randint(0,5)
        whereCard = random.randint(0,8)
        envelope = [self.suspects[whoCard], self.weapons[howCard], self.rooms[whereCard]]
        ##This checks to see if the cards go into the envelope
        print(envelope)
        self.totalDeck.remove(self.suspects[whoCard])
        self.totalDeck.remove(self.weapons[howCard])
        self.totalDeck.remove(self.rooms[whereCard])
        return envelope

    def set_up_players(self):

        characterTraits = self.set_up_character_traits()
        characterHands = self.dealDeck()
        for i in range(len(characterHands)):
            for j in range(len(characterHands[i])):
                print(characterHands[i][j])
        
        players = ([player.Player(characterTraits[i][0], characterHands[0][i], 
                                 i, characterTraits[i][1], characterHands[1]) 
    for i in range(0, self.totalPlayers)])

        return players

    def set_up_character_traits(self):

        characterTraits = []
        for i in range(self.totalPlayers):
            characterTraits += [[], []]
       
        for count in range(0, self.totalPlayers):
            try:    
                print("Miss Scarlet: S")
                print("Kernel Mustard: M")
                print("Mrs. White: W")
                print("Mr. Green: G")
                print("Professor Plum: P")
                print("Mrs. Peacock: E")
                characterTraits[count] += input("What character does player " + str(count) + " want ")
                isHuman = input("Is player " + str(count) + " a human True/False: ")
                if isHuman == "True":
                    characterTraits[count] += [True]
                elif isHuman == "False":
                    characterTraits[count] += [False]

            except Exception as e:
                print("Oh dear you seem to have made a typo would you kindly re-enter in the information")
                count = count - 1 
                print(e)          

        return characterTraits

    """
    dealDeck deals a hand to each player
    """
    def dealDeck(self):
        hands = []
        size = []
        for i in range(self.totalPlayers):
            hands += [[]]
            size += [0]
        
        random.shuffle(self.totalDeck)
        while self.totalDeck:
            for i in range(self.totalPlayers):
                hands[i] += [self.totalDeck.pop()]
                size[i] += 1
        
        return [hands] + [size]

    def make_suggestion(self, suggestion, num):
        refute = False
        card = []
        count = num + 1
        while(not refute):
            if count == self.totalPlayers:
                count = 0
            if count == num:
                refute = True
                print("No one could refute this...")
                card = [count, []]
            else:
                card = [count, self.players[count].refute(suggestion, num)]
                if card[1] != "Nah":
                    print("Player " + str(count) + " has refuted with " + card[1] + ".")
                    refute = True
                else:
                    print("Player " + str(count) + " cannot refute. \n")
            count += 1   
                
        return card
            
    def start(self):
        count = 0
        gameOver = 0
        done = 0
        accusation = []
        while(done == 0):
            if (count == len(self.players)):
                count = 0
            for i in range(len(self.players)):
                if self.players[i].checkSpect():
                    gameOver += 1
            if gameOver == self.totalPlayers + 1:
                print("Game Over. No one wins. :(")
                done = 1
            if self.players[count].checkSpect():
                print("Player " + str(count) + " was wrong and can no longer play.")    
            else:
                decision = self.players[count].take_turn(self.board)
                print(decision)
                action = decision[1]
                roll = decision[0]
                if (roll < 3 and action != "Accuse" and not 
                    self.board.inSecret(self.players[count].get_positionX(),
                                        self.players[count].get_positionY())):
                    print("Bummer. You didn't roll high enough to do anything.")
                elif action == "Accuse":
                    accusation = decision[2]
                elif action == "Move":
                    self.movemnt[count].moveTo(decision[2][2], roll)
                    suggestion = decision[2]
                    suggest = (decision[2][0] + " with the " + decision[2][1] +
                               " in the " + decision[2][2] + ".")
                        
                    print("Player " + str(count) + " has suggested: " + suggest)
                    refute = self.make_suggestion(suggestion, count)
                    if refute != "Nah":
                        self.players[count].getRefute(refute, decision[2])
                    
                    if refute != "Nah" and refute:
                        for i in range(len(self.players)):
                            if not self.players[i].human:
                                self.players[i].wilyComp(count, decision[2], refute[0])
                if accusation:
                    print("Player " + str(count) + " is making an accusation.")
                    print("They accuse: " + accusation[0] + " with the " + accusation[1] +
                          " in the " + accusation[2] + ".")
                    if(accusation[0] == self.envelope[0] and
                       accusation[1] == self.envelope[1] and
                       accusation[2] == self.envelope[2]):
                        print(self.players[count].character() + " wins! Horray!")
                        done = 1
                    else:
                        self.players[count].setAccuse()
            
            count = count + 1
