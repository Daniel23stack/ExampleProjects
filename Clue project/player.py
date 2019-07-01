import Board
import random
import movement2
import strategy

"""
Player Class
@author Jonathan Rogers
"""
class Player:
    
    def __init__(self, name, hand, num, human, handSize):
        self.name = name
        self.hand = hand
        self.human = human
        self.num = num
        self.handSize = handSize
        self.falseAccuse = False
        
        self.knowledgeBase = strategy.KB(self.hand, handSize, num, human)
        """
        Miss Scarlet: Dining S
        Kernel Mustard: Dining M 
        Mrs. White: Ball W
        Mr. Green: Ball G
        Professor Plum: Lib P
        Mrs. Peacock: Billiard E
        """
        if(self.name == "S"):
            self.positionX = 0
            self.positionY = 6
        if(self.name == "M"):
            self.positionX = 0
            self.positionY = 6
        if(self.name == "P"):
            self.positionX = 14
            self.positionY = 8
        if(self.name == "E"):
            self.positionX = 14
            self.positionY = 5
        if(self.name == "W"):
            self.positionX = 6
            self.positionY = 0
        if(self.name == "G"):
            self.positionX = 7
            self.positionY = 0

        if(not human):
            self.aiStrat = strategy.ProStrat(self.knowledgeBase, self.positionX, self.positionY)

    def get_name(self):
        return self.name
    
    def character(self):
        if self.name == "S":
            return "Miss Scarlet"
        if self.name == "M":
            return "Col Mustard"
        if self.name == "P":
            return "Prof. Plum"
        if self.name == "W":
            return "Mrs. White"
        if self.name == "E":
            return "Mrs. Peacock"
        if self.name == "G":
            return "Mr. Green"
    
    def role_dice(self):
        return random.randint(1,6)       

    def get_hand(self):
        return self.hand

    def get_hand_size(self):
        return len(self.hand)

    def update_position(self, newPosition):
        self.positionX = newPosition[0]
        self.positionY = newPosition[1]

    def get_positionX(self):
        return self.positionX

    def get_positionY(self):
        return self.positionY

    def get_accusation(self):
        self.aiStrat

    def make_accusation(self):
        accusation = []
        no_suspect_selected = True
        while(no_suspect_selected):
            print("Miss Scarlet")
            print("Col Mustard")
            print("Mrs. White")
            print("Mr. Green")
            print("Prof. Plum")
            print("Mrs. Peacock")
            print("Go back")
            suspect_accusation = input("Please select a suspect: ")

            if(suspect_accusation == "Miss Scarlet" or "Col Mustard" or
               "Mrs. White" or "Mr. Green" or "Prof. Plum" or "Mrs. Peacock"):
                accusation += [suspect_accusation]
                no_suspect_selected = False

            elif(suspect_accusation == "Go Back"):
                return []

            else:
                print("Please choose one of the provided options")

        no_weapon_selected = True
        while(no_weapon_selected):
            print("Candlestick")
            print("Knife")
            print("Lead Pipe")
            print("Revolver")
            print("Rope")
            print("Wrench")
            weapon_accusation = input("Please select a weapon: ")

            if(weapon_accusation == "Candlestick" or "Knife" or "Lead Pipe" or
               "Revolver" or "Rope" or "Wrench"):
                accusation += [weapon_accusation]
                no_weapon_selected = False

            else:
               print("Please select a weapon that is listed")

        no_room_selected = True
        while(no_room_selected):
            print("Ball Room")
            print("Billiard Room")
            print("Conservatory")
            print("Dining Room")
            print("Kitchen")
            print("Hall")
            print("Library")
            print("Lounge")
            print("Study")
            room_selection = input("Please select a room: ")

            if(room_selection == "Ball Room" or "Billiard Room" or 
               "Conservatory" or "Dining Room" or "Kitchen" or "Hall" or
               "Library" or "Lounge" or "Study"):

               accusation += [room_selection]
               no_room_selected = False

            else:
                print("Please select a room that is listed")
               
        return accusation
    
    def suggestion(self):
        suggestion = []
        no_suspect_selected = True
        while(no_suspect_selected):
            print("Miss Scarlet")
            print("Col Mustard")
            print("Mrs. White")
            print("Mr. Green")
            print("Prof. Plum")
            print("Mrs. Peacock")
            suspect_suggestion = input("Please select a suspect: ")

            if(suspect_suggestion == "Miss Scarlet" or "Col Mustard" or
               "Mrs. White" or "Mr. Green" or "Prof. Plum" or "Mrs. Peacock"):
                suggestion += [suspect_suggestion]
                no_suspect_selected = False

            else:
                print("Please choose one of the provided options")

        no_weapon_selected = True
        while(no_weapon_selected):
            print("Candlestick")
            print("Knife")
            print("Lead Pipe")
            print("Revolver")
            print("Rope")
            print("Wrench")
            weapon_suggestion = input("Please select a weapon: ")

            if(weapon_suggestion == "Candlestick" or "Knife" or "Lead Pipe" or
               "Revolver" or "Rope" or "Wrench"):
                suggestion += [weapon_suggestion]
                no_weapon_selected = False

            else:
               print("Please select a weapon that is listed")
               
        return suggestion
    
    def refute(self, suggestion, num):
        card = "Nah"
        if self.human:
            option = []
            for i in range(len(self.hand)):
                if self.hand[i] in suggestion:
                    option += [self.hand[i]]
            if option:
                print("\n".join(option))
                card = input("Please select a card to show: ")
        else:
            card = self.aiStrat.canRefute(suggestion)
            if card:
                if len(card) > 1:
                    card = self.aiStrat.myRefute(num, card)
                else:
                    card = card[0]
            else:
                card = "Nah"
        
        return card
    
    def getRefute(self, refute, suggestion):
        card = refute[1]
        if self.human:
            self.knowledgeBase.humanRefute(card, suggestion)
        else:
            self.knowledgeBase.compRefute(card, refute[0], suggestion)
            
    def wilyComp(self, whoTurn, suggestion, whoDisprove):
        self.aiStrat.notMyTurn(whoTurn, suggestion, whoDisprove)

    def checkSpect(self):
        return self.falseAccuse
        
    def setAccuse(self):
        self.falseAccuse = True            
        
    def take_turn(self, board):
        action = []
        accusation = []
        print("\nPlayer " + str(self.num) + ":\n")
        print("Hand: ")
        print(self.hand)
        print("Knowledge Base: ")
        self.knowledgeBase.showKb()
        print("\n")
        roll = self.role_dice()
        print("Player " + str(self.num) + " rolled a " + str(roll) + ".")
        print("Current Room: " + board.getLocation(self.positionX, self.positionY))
        if(self.human):
            does_the_human_want_to_accuse = input("Do you wish to accuse? y/n ")
            if(does_the_human_want_to_accuse == "y"):
                accusation = self.make_accusation()
                action += [roll] + ["Accuse"] + [accusation]
            if not accusation:  # Not sure what to do
                if board.inSecret(self.positionX, self.positionY):
                    secrets = input("Would you like to go through the secret passage? y/n ")
                    if secrets == "y":
                        room_to_move_to = board.secret(self.positionX, self.positionY)
                        
                        suggestion = self.suggestion() + [room_to_move_to]
                        action += [roll] + ["Move"] + [suggestion]
                else:
                    secrets = "n"
                if secrets == "n" and roll > 2:
                    adjacentRooms = board.get_adjacent_rooms(self.positionX, self.positionY)
                    print("\n".join(adjacentRooms))
                    room_to_move_to = input("What room would you like to move to: ")
                    
                    suggestion = self.suggestion() + [room_to_move_to]
                    action += [roll] + ["Move"] + [suggestion]
                elif secrets == "n" and roll < 3:
                    action += [roll, "Nothing"]
        else:
            action = [roll] + self.aiStrat.myTurn(self.positionX, self.positionY, roll)
        
        print('\n')
        return action