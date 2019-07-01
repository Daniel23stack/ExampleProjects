"""
File: strategy.py
This file implements strategies for winning a game of clue, including the use of
propositional logic to figure out who has what cards in an attempt to find what
cards are in the case file.

@author: Elisabeth Goggin
@version: 29 April 2018
"""
import random

CONST_SUSPECT = ["Mr. Green", "Col Mustard", "Mrs. Peacock", "Prof. Plum", 
           "Miss Scarlet", "Mrs. White"]
CONST_WEAPON = ["Candlestick", "Knife", "Lead Pipe", "Revolver", "Rope", "Wrench"]
CONST_ROOM = ["Ball Room", "Billiard Room", "Conservatory", "Dining Room", "Hall",
        "Kitchen", "Library", "Lounge", "Study"]
CONST_DECK = CONST_SUSPECT + CONST_WEAPON + CONST_ROOM

class ProStrat:
    """
    A class that figures out the best action to take in order to maximize
    chances of victory.
    """
    def __init__(self, kb, locX, locY):
        self.kb = kb
        self.locX = locX
        self.locY = locY
        #list of where rooms are located
        self.roomLoc = ([[0, 0, 4, 4], [5, 0, 9, 4], [10, 0, 14, 4], 
                         [0, 5, 4, 9], [5, 5, 9, 9], [10, 5, 14, 6],
                         [10, 14, 7, 9], [0, 10, 4, 14], [0, 10, 4, 14],
                         [10, 14, 10, 14], [5, 10, 9, 14]])
        
        
        #list of the rooms known
        self.knownR = self.kb.getRoom()
        #string saying what room the player is in
        self.currentR = self.currentRoom()
        
        self.secretPass = ["Kitchen", "Study", "Conservatory", "Lounge"]
        
    def updateKB(self, kb):
        """
        This method updates the knowledge base
        """
        self.kb = kb
        
    def updateLoc(self, locX, locY):
        """
        This method updates the player's location
        """
        self.locX = locX
        self.locY = locY
        
    def updateKnownR(self):
        """
        This method updates the list of rooms the player knows
        """
        self.knownR = self.kb.getRoom()
        
    def roomName(self, room):
        """
        This returns the name of a room given the board coordinates
        """
        name = ""
        if room[0] == 0:
            if room[1] == 0:
                name = "Kitchen"
            elif room[1] == 5:
                name = "Dining Room"
            else:
                name = "Lounge"
        elif room[0] == 5:
            if room[1] == 0:
                name = "Ball Room"
            else:
                name = "Hall"
        else:
            if room[1] == 0:
                name = "Conservatory"
            elif room[1] == 5:
                name = "Billiard Room"
            elif room[1] == 7:
                name = "Library"
            else:
                name = "Study"
                
        return name
        
    def currentRoom(self):
        """
        This returns the current room of the player
        """
        room = ""
        if (self.locX >= 0 and self.locX <= 4 ):
            if (self.locY <= 4):
                return "Kitchen"
            if(self.locY <= 9):
                return "Dining Room"
            else:
                return "Lounge"
        if (self.locX > 4 and self.locX < 10 ):
            if (self.locY <= 4):
                return "Ball Room"
            if(self.locY <= 9):
                return 'X'
            else:
                return "Hall"
            
        if (self.locX > 9 and self.locX <= 14 ):
            if (self.locY <= 4):
                return "Conservatory"
            if(self.locY <= 6):
                return "Billiard Room"
            if(self.locY <= 9):
                return "Library"
            else:
                return "Study"
        else:
            return 'X'
        
        return room
    
    def adjacentR(self, room):
        """
        This returns a list of the rooms adjacent to the given room
        """
        adjacent = []
        if room == "Kitchen":
            adjacent = ["Dining Room", "Ball Room", "Study"]
        elif room == "Ball Room":
            adjacent = ["Kitchen", "Conservatory"]
        elif room == "Conservatory":
            adjacent = ["Ball Room", "Billiard Room", "Lounge"]
        elif room == "Billiard Room":
            adjacent = ["Conservatory", "Library"]
        elif room == "Library":
            adjacent = ["Billiard Room", "Study"]
        elif room == "Study":
            adjacent = ["Library", "Hall", "Kitchen"]
        elif room == "Hall":
            adjacent = ["Study", "Lounge"]
        elif room == "Lounge":
            adjacent = ["Hall", "Dining Room", "Conservatory"]
        elif room == "Dining Room":
            adjacent = ["Kitchen", "Lounge"]
            
        return adjacent
    
    def isNear(self, adjacent):
        """
        This returns a list of the rooms adjacent to the adjacent rooms of the
        player's current room
        """
        near = []
        for i in range(len(adjacent)):
            near += ([[adjacent[i]] + 
                     [self.adjacentR(adjacent[i])]])
        
        if self.currentR in near:
            near.remove(self.currentR)
        return near
    
    def chooseRoom(self, posLoc, adjacent):
        """
        This method picks a room for the player to attempt to move to
        """
        room = ""
        if posLoc:
            if self.currentR in posLoc:
                posLoc.remove(self.currentR)
            choiceR = []
            for i in range(len(adjacent)):
                if adjacent[i] in posLoc:
                    choiceR += [adjacent[i]]
            if choiceR:
                room = choiceR[0]
            else:
                choiceR = self.isNear(adjacent)
                i = 0
                while(i < len(choiceR)):
                    if choiceR[i] not in posLoc:
                        choiceR.remove(choiceR[i])
                    i += 1
                if choiceR:
                    room = choiceR[0][0]
                else:
                    room = adjacent[0]
        else:
            room = adjacent[0]
              
        return room
    
    def canMove(self, roll):
        if roll > 2:
            return True
        return False
        
    def myTurn(self, posX, posY, roll):
        """
        This method makes a decision on what action to take on the player's
        turn
        """
        case = self.kb.caseCheck()
        self.updateLoc(posX, posY)
        self.currentR = self.currentRoom()
        self.updateKnownR()
        posLoc = self.knownR
        adjacent = self.adjacentR(self.currentR)
        print(adjacent)
        cMove = self.canMove(roll)
            
        suspect = ""
        s = list(self.kb.getSuspect())
        weapon = ""
        w = list(self.kb.getWeapon())
        room = ""
        
        if case:
            if len(case) == 3:
                case = self.kb.getCase()
                move = ["Accuse"] + [case]
            else:
                if "suspect" in case:
                    suspect = CONST_SUSPECT[random.randint(0, len(CONST_SUSPECT) - 1)]
                else:
                    suspect = s[random.randint(0, len(s) - 1)]
                    
                if "weapon" in case:
                    weapon = CONST_WEAPON[random.randint(0, len(CONST_WEAPON) - 1)]
                else:
                    weapon = w[random.randint(0, len(w) - 1)]
                
                if "room" in case:
                    room = adjacent[random.randint(0, len(adjacent) - 1)]
                else:
                    room = self.chooseRoom(posLoc, adjacent)
                if not cMove:
                    if self.currentR in self.secretPass:
                        room = self.superSecret()
            
                suggest = [suspect, weapon, room]
                
            
                move = ["Move"] + [suggest]
        else:
            room = self.chooseRoom(posLoc, adjacent)
            
            suspect = s[random.randint(0, len(s) - 1)]
            weapon = w[random.randint(0, len(w) - 1)]
        
            if not cMove:
                if self.currentR in self.secretPass:
                    room = self.superSecret()
            
            suggest = [suspect, weapon, room]
            
            move = ["Move"] + [suggest]
        
        return move
            
    def superSecret(self):
        room = ""
        if self.currentR == self.secretPass[0]:
            room = self.secretPass[1]
        elif self.currentR == self.secretPass[1]:
            room = self.secretPass[0]
        elif self.currentR == self.secretPass[2]:
            room = self.secretPass[3]
        elif self.currentR == self.secretPass[3]:
            room = self.secretPass[2]
            
        return room
    
    def notMyTurn(self, turn, suggest, knowItAll):
        """
        Adds the suggestion and refution of the other players on a turn to the
        player's knowledge base and returns the updated knowledge base.
        """
        self.kb.fullOfSecrets(turn, suggest, knowItAll)
    
    def canRefute(self, suggestion):
        cards = []
        hand = self.kb.getHand()
        for i in range(len(suggestion)):
            if suggestion[i] in hand:
                cards += [suggestion[i]]
        print(cards)
        return cards
    
    def myRefute(self, player, refute):
        card = ""
        if self.kb.haveRefute(player):
            for i in range(len(refute)):
                if self.kb.inRefute(player, refute[i]):
                    card = refute[i]
        else:
            card = refute[random.randint(0, len(refute) - 1)]
        
        self.kb.updateRefute(player, card)
        
        return card

class KB:
    """
    A class that builds the knowledge base. It builds a different knowledge base
    depending on if the owner is a computer or not.
    """
    def __init__(self, hand, handSize, num, isHuman):
        self.isHuman = isHuman
        self.know = list(hand)
        self.handSize = list(handSize)
        self.player = num
        
        self.suspect = []
        self.weapon = []
        self.room = []
        
        if self.isHuman:
            self.file =[]
            #if the player is human we don't need that fancy stuff
            for i in range(len(self.know)):
                #go through the hand and add the cards into the different cat
                if self.know[i] in CONST_SUSPECT:
                    self.suspect += [self.know[i]]
                elif self.know[i] in CONST_WEAPON:
                    self.weapon += [self.know[i]]
                elif self.know[i] in CONST_ROOM:
                    self.room += [self.know[i]]
            
            #put all the categories of cards together in the knowledge base
            self.kb = [self.suspect, self.weapon, self.room]
        else:
            #if the player is a computer, stuff gets complicated
            self.kb = list(self.know)
            self.myRefutes = []
            
            #create a list containing the player's hands
            self.others = []
            for i in range(len(self.handSize)):
                self.myRefutes += [[]]
                
                #check to see if that index is us
                if not i == self.player:
                    #the first is what we know the player has, the second is 
                    #what we know the player does not have and the third is
                    #what suggestions they've disproved
                    self.others += [[[],[list(self.know)],[]]]
                else:
                    self.others += [list(self.know)]
            
            
            self.suspect = list(CONST_SUSPECT)
            self.weapon = list(CONST_WEAPON)
            self.room = list(CONST_ROOM)
            #take the possiblities and remove the ones we know
            for i in range((len(self.know))):
                if self.know[i] in self.suspect:
                    self.suspect.remove(self.know[i])
                elif self.know[i] in self.weapon:
                    self.weapon.remove(self.know[i])
                else:
                    self.room.remove(self.know[i])
            
            #the possible case file
            self.case = [self.suspect, self.weapon, self.room]
            #the actual case file
            self.file = []
        
            #lists of suggestions and shown cards of other players
            self.suggest = []           
            self.shown = []
            
    def getHand(self):
        return self.know
            
    def updateRefute(self, player, card):
        self.myRefutes[player] += [card]
        
    def inRefute(self, player, card):
        if card in self.myRefutes[player]:
            return True
        return False
        
    def haveRefute(self, player):
        if self.myRefutes[player]:
            return True
        return False
    
    def inCat(self, card):
        """
        This returns a string of the category of a given card
        """
        if card in CONST_SUSPECT:
            return "suspect"
        elif card in CONST_WEAPON:
            return "weapon"
        else:
            return "room"
    
    def removeCat(self, card):
        """
        This removes a card from it the possibilities of its category
        """
        if card in self.suspect:
            self.suspect.remove(card)
        elif card in self.weapon:
            self.weapon.remove(card)
        elif card in self.room:
            self.room.remove(card)
         
    def getSuspect(self):
        """
        Returns the list of possible suspects
        """
        return self.suspect
    
    def getWeapon(self):
        """
        Returns the list of possible weapons
        """
        return self.weapon
    
    def getRoom(self):
        """
        Returns the list of possible rooms
        """
        return self.room
    
    def byDefault(self):
        """
        If we know all but one card is not in the case file, then we know that
        card must be in the case file
        """
        for i in range(len(self.case)):
            if len(self.case[i]) == 1:
                if self.case[i][0] not in self.file:
                    self.file.append(self.case[i][0])
    
    def caseCheck(self):
        """
        Checks what we know is in the case file
        """
        #just in case a human tries to access this
        if self.isHuman:
            complete = "Don't poke your nose where it don't belong."
        else:
            complete = []
        
            #check what we know is in the casefile
            if self.file:
                for i in range(len(self.file)):
                    if self.file[i] not in complete:
                        complete += [self.inCat(self.file[i])]
            
        return complete
    
    def getCase(self):
        return self.file
    
    def fullOfSecrets(self, player, suggest, disproof):
        """
        This attempts to figure out what cards other players have by what
        suggestions are disproved
        """
        #just in case a human tries to access this
        if not self.isHuman:
            count = 0
            pos = list(suggest)
        
            #add the suggestion to the list with the player who made it and the
            #player who disproved it
            self.suggest += [[player, disproof, [suggest]]]
            #add the suggestion list to the list of things a player has disproved
            for i in range(len(suggest)):
                self.others[disproof][2] += suggest[i]
        
            #adds the suggestion to the list of cards we know a player doesn't
            #have to the players between the player making the suggestion and 
            #the player refuting it who couldn't disprove it
            for i in range(player, disproof):
                for j in range(len(suggest)):
                    self.others[i][1] += suggest[j]
        
            #check to see if we know all of the cards of the player who refuted
            if len(self.others[player][0]) != self.handSize[player]:
                #check how many cards we know the other player doesn't have
                i = 0
                while i < len(pos):
                    if pos[0] in self.others[disproof][0]:
                        pos.remove(pos[0])
                        count += 1
                    i += 1
                
                #if we know they don't have two of the cards they must have the
                #third
                if count == 2 and not pos[0] in self.others[disproof][0]:
                    self.others[disproof][0] += pos
                    self.kb += list(pos)
                    
                    #remove it from the list of possiblities
                    for i in range(len(self.case)):
                        if suggest:
                            for j in range(len(self.suggest)):
                                if self.case[i]:
                                    if suggest[j] in self.case[i]:
                                        self.case[i].remove(suggest[j])
                    
                    self.shown += [[disproof] + suggest]
                
                #check if we now know all of a player's cards
                self.allPlay(disproof)
    
    def humanRefute(self, card, suggestion):
        """
        This updates the knowledge base of a human player given a refute card
        """
        if card not in self.kb:
            if card == []:
                for i in range(len(suggestion)):
                    if suggestion[i] not in self.know:
                        self.file += suggestion[i]
            if card in CONST_SUSPECT:
                self.kb[0] += [card]
            elif card in CONST_WEAPON:
                self.kb[1] += [card]
            elif card in CONST_ROOM:
                self.kb[2] += [card]
        
        return self.kb
        
    def compRefute(self, card, player, suggestion):
        """
        This updates the knowledge base of a computer player given a refute
        card
        """
        if not self.isHuman:
            if card not in self.kb:
                if card == []:
                    for i in range(len(suggestion)):
                        if suggestion[i] not in self.know:
                            self.file += [suggestion[i]]
                            self.kb += [suggestion[i]]
                else:
                    self.kb += [card]
                    self.removeCat(card)
                    self.others[player][0] += card
                    self.shown += [[player], [card]]
            
        return self.kb
    
    def allPlay(self, player):
        """
        This checks to see if we know all of a player's cards and if so adds
        the rest of the deck to what we know the player doesn't have
        """
        if len(self.others[player][0]) == self.handSize[player]:
            for i in range(len(CONST_DECK)):
                if (not CONST_DECK[i] in self.others[player][0] and 
                    not CONST_DECK[i] in self.others[player][1]):
                    self.others[player][1] += CONST_DECK[i]
                    
    def showKb(self):
        print(self.kb)
        if self.file:
            print("Case File: ")
            print(self.file)