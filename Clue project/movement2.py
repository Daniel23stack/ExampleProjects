class Movement():
    
    '''
    Constructor
    '''
    def __init__(self, board, player):
        self.player = player
        self.board = board
        self.numMoves = 0
        
    

    '''
    Calculates the shortest distance between the room the player is in and the 
    room they want to go to 1 added for door
    '''
    def distance(self,loc, dest):
        if (abs(self.board.get_max_x(loc) - self.board.get_max_x(dest)) 
        <= abs(self.board.get_min_x(loc) - self.board.get_max_x(dest))):
            xDist = abs(self.board.get_max_x(loc) - self.board.get_max_x(dest))
        else:
            xDist = abs(self.board.get_min_x(loc) - self.board.get_max_x(dest))
        if (abs(self.board.get_max_y(loc) - self.board.get_max_y(dest)) 
        <= abs(self.board.get_min_y(loc) - self.board.get_max_y(dest))):
            yDist = abs(self.board.get_max_y(loc) - self.board.get_max_y(dest))
        else:
            yDist = abs(self.board.get_min_y(loc) - self.board.get_max_y(dest))
        return xDist+yDist+2
       
    '''
    Moves the player to their desired destination if they rolled high enough 
    and returns their new location
    '''
    def moveTo(self, room, dieRoll):
        destination = self.board.getRoom(room)
        if destination != 'X' and destination != "Cellar" and destination != "cellar":
            passageDest = (self.board.secretPassage(self.player.get_positionX(), 
                                                    self.player.get_positionY(), 
                                                    self.player.get_name))
            if passageDest:
                if (passageDest[0] <= self.board.get_max_x(destination) and 
                    passageDest[0] >=self.board.get_min_x(destination)):
                    if (passageDest[1] <= self.board.get_max_y(destination) and 
                        passageDest[1] >= self.board.get_min_y(destination)):
                        self.player.update_position[self.board.get_min_x(destination),
                                                    self.board.get_min_y(destination)]
            self.numMoves += dieRoll
            if (self.distance(self.board.getLocation(self.player.get_positionX(), 
                                                       self.player.get_positionY()), 
                        destination) <= self.numMoves):
                self.numMoves = 0
                self.player.update_position([self.board.get_min_x(destination), 
                                             self.board.get_min_y(destination)])
            self.player.update_position([self.board.get_min_x(destination), 
                                             self.board.get_min_y(destination)])
            return self.board.setLocation(self.player.get_positionX(), 
                                          self.player.get_positionY(), 
                                          self.player.get_name())
        return [5,5]#illegal location