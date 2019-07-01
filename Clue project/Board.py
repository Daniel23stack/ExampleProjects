'''
Created on Apr 16, 2018

@author: Daniel Jennings
'''


class Board(object):
    '''
    classdocs
    '''

    '''
     constructs a board labeling each of the rooms with a
     specified letter
    '''
    displayBoard = [[" "] * 31 for i in range(31)]
    
    def __init__(self, board = 0):
        '''
        Constructor
        '''
        
        if (board==0):
            self.board = [[0] * 15 for i in range(15)]
            for y in range(0,4):
                for x in range (0,4):
                    if (x == 0 and y == 0):
                        self.board[x][y] = 'S'
                    else:
                        self.board[x][y] = 'K'
                        
                for y in range (0, 4):
                    for x in range (5,9):
                        self.board[x][y] = 'B'
                
                for y in range (0, 4):
                    for x in range (10, 14):
                        if(x == 14 and y == 0):
                            self.board[x][y] = 'S'
                        else:
                            self.board[x][y] = 'C'
                        
                for y in range (5,9):
                    for x in range(0,4):
                        self.board[x][y] = 'D'
                for y in range (5,9):
                    for x in range(5,9):
                        self.board[x][y] = 'X'
                for y in range (5,6):
                    for x in range(10,14):
                        self.board[x][y] = 'BR'
                for y in range (7,9):
                    for x in range(10,14):
                        self.board[x][y] = 'L'
                        
                for y in range (10,14):
                    for x in range(0,4):
                        if (x == 0 and y == 14):
                            self.board[x][y] = 'S'
                        else:
                            self.board[x][y] = 'O'
                for y in range (10,14):
                    for x in range(5,9):
                        self.board[x][y] = 'H'
                for y in range (10,14):
                    for x in range(10,14):
                        self.board[x][y] = 'T'
                        
                        
                self.set_display_outline()
                self.set_rooms_display()
                self.update_board()
        else:
            self.board = board;
        
        
        
    

    '''    
    returns the room the player is in based on 
    their x and y coordinates
    '''
    def getLocation(self, playerX, playerY):
        if (playerX >= 0 and playerX <= 4 ):
            if (playerY <= 4):
                return 'K'
            if(playerY <= 9):
                return 'D'
            else:
                return 'O'
        if (playerX > 4 and playerX < 10 ):
            if (playerY <= 4):
                return 'B'
            if(playerY <= 9):
                return 'X'
            else:
                return 'H'
            
        if (playerX > 9 and playerX <= 14 ):
            if (playerY <= 4):
                return 'C'
            if(playerY <= 6):
                return 'BR'
            if(playerY <= 9):
                return 'L'
            else:
                return 'T'
        else:
            return 'X'
        
    def getRoom(self, room):
        if room == "Kitchen":
            return 'K'
        elif room == "Dining Room":
            return 'D'
        elif room == "Lounge":
            return 'L'
        elif room == "Ball Room":
            return 'B'
        elif room == "Hall":
            return 'H'
        elif room == "Conservatory":
            return 'C'
        elif room == "Billiard Room":
            return 'BR'
        elif room == "Library":
            return 'L'
        elif room == "Study":
            return 'T'
        else:
            return 'X'
    
    '''
    Sets the location given by the player's name onto the board
    replacing the normal placement with their name.
    Returns a lcation in the form [x,y]
    '''
    def setLocation (self,playerX, playerY, playerName):
        self.original_name(playerX,playerY)
        if (self.getLocation(playerX, playerY) == 'K'):
            return self.location_setter(playerName, 1, 1, 'K')
        if (self.getLocation(playerX, playerY) == 'D'):
            return self.location_setter(playerName, 1, 6, 'D')
        if (self.getLocation(playerX, playerY) == 'O'):
            return self.location_setter(playerName, 1, 10, 'O')
        if (self.getLocation(playerX, playerY) == 'B'):
            return self.location_setter(playerName, 5, 1, 'B')
        if (self.getLocation(playerX, playerY) == 'X'):
            return [5, 8]
        if (self.getLocation(playerX, playerY) == 'H'):
            return self.location_setter(playerName, 5, 10, 'H')
        if (self.getLocation(playerX, playerY) == 'C'):
            return self.location_setter(playerName, 10, 1, 'C')
        if (self.getLocation(playerX, playerY) == 'BR'):
            return self.location_setter(playerName, 10, 5, 'BR')
        if (self.getLocation(playerX, playerY) == 'L'):
            return self.location_setter(playerName, 10, 7, 'L')
        if (self.getLocation(playerX, playerY) == 'T'):
            return self.location_setter(playerName, 10, 10, 'T')
        else:
            return [5,8]
        
        
        
        

    '''
    Private method that allows for the setting the name of the player
    on the board. use the set location.
    '''
    def location_setter(self, playerName, locationX, locationY, locationName):
        count = locationX
        done = 0
        while (done != 0):
                if (self.board[count][locationY] == locationName):
                    self.board[count][locationY] = playerName
                    done = 1
                    self.displayBoard[count*2][locationY *2] = playerName
                    self.update_board()
                    return [count, locationY]
                elif (count > 4):
                    if (count == 5):
                        self.board[locationX, locationY + 1] = playerName
                        self.displayBoard[locationX*2][(locationY +1) *2] = playerName
                        self.update_board()
                        return [locationX, locationY + 1]
                    if (count == 6):
                        self.board[locationX + 1][locationY + 1] = playerName
                        self.displayBoard[(locationX + 1) * 2][(locationY + 1) * 2] = playerName
                        self.update_board()
                        return [locationX + 1, locationY + 1]
                    else:
                        count = count + 1
    
    
    '''
    determines whether a a players location is allowed
    '''
    def is_legal(self, playerX, playerY):
        if (self.getLocation(playerX, playerY) == 'X'):
            return False
        else:
            return True
    
    '''
     this is a method that if given the player's location will
     return their movement through a secret passage way
     if there is not a secret passage way it will put them at
     [6,6] whose location is illegal
    '''
    def secretPassage(self, playerX, playerY, playerName):
        if (self.getLocation(playerX, playerY) == 'K'):
            return self.setLocation(11, 11, playerName)
        if (self.getLocation(playerX, playerY) == 'S'):
            return self.setLocation(1, 1, playerName)
        if (self.getLocation(playerX, playerY) == 'C'):
            return self.setLocation(1, 11, playerName)
        if (self.getLocation(playerX, playerY) == 'O'):
            return self.setLocation(11, 1, playerName)
        else:
            return [6, 6]
    
    
    def get_min_x(self, location):
        for i in range(0,15):
            for j in range(0,15):
                if self.getLocation(i, j) == location:
                    return i
        return -1
    
    def get_min_y(self, location):
        for i in range(0,15):
            for j in range(0,15):
                if self.getLocation(i, j) == location:
                    return j
        return -1
    
    def get_max_x(self, location):
        maxX = 0
        for i in range(0,15):
            for j in range(0,15):
                if self.getLocation(i, j) == location:
                    maxX = i
        return maxX

    def get_max_y(self, location):
        maxY = 0
        for i in range(0,15):
            for j in range(0,15):
                if self.getLocation(i, j) == location:
                    maxY = j
        return maxY

    
    '''
    resets the playerX and playerY name on the board to the room name
    '''
    def original_name (self, playerX, playerY):
        self.board[playerX][playerY] = self.getLocation(playerX, playerY)
        self.displayBoard[playerX * 2][playerY * 2] = " "
        
        
    def update_board(self):
        for y in range(0, 31):
            for x in range(0, 31):
                print(self.displayBoard[x][y], end =" ")
            print("")
            
    def set_display_outline(self):
        self.displayBoard[0][0] = "_"
        self.displayBoard[0][30] = "|"
        self.displayBoard[30][30] = "|"
        self.displayBoard[30][0] = "_"

        for i in range(1, 30):
            self.displayBoard[i][0] = '_'
            self.displayBoard[0][i] = '|'
            self.displayBoard[30][i] = '|'
            self.displayBoard[i][30] = '_'
    
        for i in range(1,31):
            self.displayBoard[10][i] = '|'
            self.displayBoard[20][i] = '|'
            if (i != 10 and i != 20 and i != 30):
                self.displayBoard[i][10] = '_'
                self.displayBoard[i][20] = '_'
        for  x in range (21, 30):
            self.displayBoard[x][14] = '_'
            
    def set_rooms_display(self):
        self.displayBoard[2][3] = "K"
        self.displayBoard[3][3] = "I"
        self.displayBoard[4][3] = "T"
        self.displayBoard[5][3] = "C"
        self.displayBoard[6][3] = "H"
        self.displayBoard[7][3] = "E"
        self.displayBoard[8][3] = "N"
        
        self.displayBoard[11][3] = "B"
        self.displayBoard[12][3] = "A"
        self.displayBoard[13][3] = "L"
        self.displayBoard[14][3] = "L"
        self.displayBoard[15][3] = "R"
        self.displayBoard[16][3] = "O"
        self.displayBoard[17][3] = "O"
        self.displayBoard[18][3] = "M"
        
        self.displayBoard[22][3] = "C"
        self.displayBoard[23][3] = "O"
        self.displayBoard[24][3] = "N"
        self.displayBoard[25][3] = "V"
        self.displayBoard[26][3] = "O"
        
        self.displayBoard[2][12] = "D"
        self.displayBoard[3][12] = "I"
        self.displayBoard[4][12] = "N"
        self.displayBoard[5][12] = "I"
        self.displayBoard[6][12] = "N"
        self.displayBoard[7][12] = "G"
        
        self.displayBoard[11][12] = "C"
        self.displayBoard[12][12] = "E"
        self.displayBoard[13][12] = "L"
        self.displayBoard[14][12] = "L"
        self.displayBoard[15][12] = "A"
        self.displayBoard[16][12] = "R"
        
        self.displayBoard[22][12] = "B"
        self.displayBoard[23][12] = "I"
        self.displayBoard[24][12] = "L"
        self.displayBoard[25][12] = "L"
        self.displayBoard[26][12] = "A"
        self.displayBoard[27][12] = "R"
        self.displayBoard[28][12] = "D"
        
        
        self.displayBoard[22][16] = "L"
        self.displayBoard[23][16] = "I"
        self.displayBoard[24][16] = "B"
        self.displayBoard[25][16] = "R"
        self.displayBoard[26][16] = "A"
        self.displayBoard[27][16] = "R"
        self.displayBoard[28][16] = "Y"
        
        self.displayBoard[2][22] = "L"
        self.displayBoard[3][22] = "O"
        self.displayBoard[4][22] = "U"
        self.displayBoard[5][22] = "N"
        self.displayBoard[6][22] = "G"
        self.displayBoard[7][22] = "E"
        
        self.displayBoard[11][22] = "H"
        self.displayBoard[12][22] = "A"
        self.displayBoard[13][22] = "L"
        self.displayBoard[14][22] = "L"
        
        self.displayBoard[22][22] = "S"
        self.displayBoard[23][22] = "T"
        self.displayBoard[24][22] = "U"
        self.displayBoard[25][22] = "D"
        self.displayBoard[26][22] = "Y"
        
        self.displayBoard[1][1] = "S"
        self.displayBoard[2][1] = "T"
        
        self.displayBoard[1][29] = "S"
        self.displayBoard[2][29] = "C"
        
        self.displayBoard[28][1] = "S"
        self.displayBoard[29][1] = "L"
        
        self.displayBoard[28][29] = "S"
        self.displayBoard[29][29] = "K"
        
        
        
    def get_adjacent_rooms(self, playerX, playerY):
        if (self.getLocation(playerX, playerY) == 'K'):
            return["Ballroom", "Dining"]
        if (self.getLocation(playerX, playerY) == 'D'):
            return["Kitchen", "Lounge"]
        if (self.getLocation(playerX, playerY) == 'O'):
            return["Dining", "Hall"]
        if (self.getLocation(playerX, playerY) == 'H'):
            return["Lounge", "Study"]
        if (self.getLocation(playerX, playerY) == 'T'):
            return["Hall", "Library"]
        if (self.getLocation(playerX, playerY) == 'L'):
            return["Study", "Billard"]
        if (self.getLocation(playerX, playerY) == 'BR'):
            return["Library", "Conservatory"]
        if (self.getLocation(playerX, playerY) == 'C'):
            return["Billard", "Ballroom"]
        if (self.getLocation(playerX, playerY) == 'B'):
            return["Conservatory", "Kitchen"]
            
    def inSecret(self, playerX, playerY):
        if (self.getLocation(playerX, playerY) == 'K' or 
            self.getLocation(playerX, playerY) == 'T' or 
            self.getLocation(playerX, playerY) == 'C' or 
            self.getLocation(playerX, playerY) == 'O'):
            return True
        
        return False
    
    def secret(self, playerX, playerY):
        if self.getLocation(playerX, playerY) == 'K':
            return "Study"
        elif self.getLocation(playerX, playerY) == 'T':
            return "Kitchen"
        elif self.getLocation(playerX, playerY) == 'C':
            return "Lounge"
        else:
            return "Conservatory"