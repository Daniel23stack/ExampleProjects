## Main Method of Clue
## Jonathan Rogers, Kate Kielkopf
## 4/26/2018

import baseGame

print("Welcome to Clue")
print("Number of Players Allowed: 3-6")
totalPlayers = 0

while(not 3 <= totalPlayers <= 6):
    stringTotalPlayers = input("How many players are playing today?: ")
    try:
        totalPlayers = int(stringTotalPlayers)
        if(totalPlayers > 6):
            print("That's too many players, please choose a number between 3 and 6")
        if(totalPlayers < 3):
            print("That's too few players, please choose a number between 3 and 6")
    except Exception as e:
        print("That's not even a number, please choose a number between 3 and 6")

game = baseGame.BaseGame(totalPlayers)
game.start()
