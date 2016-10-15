import random
import time
import json
import sys

#Text Log
log = ''

#Custom Print function
def Print(msg, end='\n'):
    global log
    msg = '{}{}'.format(msg, end)
    log += msg
    sys.stdout.write(msg)
    sys.stdout.flush()

#Define Betting Functions
def betRed(bet):
    global redBet, money
    redBet = redBet + bet
    money = money - bet

def betBlack(bet):
    global blackBet, money
    blackBet = blackBet + bet
    money = money - bet

def betOdd(bet):
    global oddBet, money
    oddBet = oddBet + bet
    money = money - bet
    
def betEven(bet):
    global evenBet, money
    evenBet = evenBet + bet
    money = money - bet
    
def betLow(bet):
    global lowBet, money
    lowBet = lowBet + bet
    money = money - bet
    
def betHigh(bet):
    global highBet, money
    highBet = highBet + bet
    money = money - bet

#Create Roulette Table
table = [
    'green',
    'red', 'black', 'red',
    'black', 'red', 'black',
    'red', 'black', 'red',
    'black', 'black', 'red',
    'black', 'red', 'black',
    'red', 'black', 'red',
    'red', 'black', 'red',
    'black', 'red', 'black',
    'red', 'black', 'red',
    'black', 'black', 'red',
    'black', 'red', 'black',
    'red', 'black', 'red',
    'green' #00
    ]
    
#Declare global game variables
gamesPlayed = 0
redBet = 0
blackBet = 0
evenBet = 0
oddBet = 0
lowBet = 0
highBet = 0
money = 0
minBet = 0
maxBet = 0
maxRoll = 0
bestGame = 0

#Define general init function
def initGame():
    global gamesPlayed, redBet, blackBet, evenBet, oddBet, lowBet, highBet, money, minBet, maxBet, highestBalance, maxRoll, bestGame
    
    gamesPlayed = 0
    
    redBet = 0
    blackBet = 0
    evenBet = 0
    oddBet = 0
    lowBet = 0
    highBet = 0
    bestGame = 1
    
    #Generate and/or load Options.json
    while True:
        try:
            with open('Options.json', 'r') as outfile:
                jsonData = json.load(outfile)
                #Get money, minimum bet, maximum bet, and table type from Options.json.
                money = jsonData["Starting Money"]
                minBet = jsonData["Minimum Bet"]
                maxBet = jsonData["Maximum Bet"]
                americanTable = jsonData["American Table"]
                break
        except IOError:
            #If Options.json doesn't exist, create one with default values and try again.
            Print("Generating Options.json.")
            encoded_data = json.dumps({"Starting Money": 500, "Minimum Bet": 1, "Maximum Bet": 50, "American Table": True}, indent=4)
            with open('Options.json', 'w') as outfile:
                outfile.write(encoded_data + '\n')
                
    #Reset highest balance
    highestBalance = money
    #Set wheel/table type to either American or European.
    maxRoll = 38 if americanTable else 37
    
    #Initialize bets
    betRed(minBet)
    betBlack(minBet*2)
    betOdd(minBet)
    betEven(minBet*2)
    betLow(minBet)
    betHigh(minBet*2)
    betHigh(minBet*2)
    
    #Output initial bets
    Print( "~Initial Bet~" )
    Print( "$" + str(redBet) + " On Red." )
    Print( "$" + str(blackBet) + " On Black." )
    Print( "$" + str(oddBet) + " On Odd." )
    Print( "$" + str(evenBet) + " On Even." )
    Print( "$" + str(lowBet) + " On Low." )
    Print( "$" + str(highBet) + " On High." )
    Print( "$" + str(money) + " in our pocket." )
    
#First Init
initGame()

#Main Loop
while True:
    
    #Scorekeeping
    gamesPlayed += 1
    if money > highestBalance:
        bestGame = gamesPlayed
        highestBalance = money
        
    #Ball
    roll = random.randrange(0, maxRoll)
    
    #--------------------
    #Handle Red and Black
    #--------------------
    #Roll is Red
    if table[roll] == 'red':
        money += redBet*2
        redBet = 0
        betRed(minBet)
        if blackBet*2 > maxBet:
            blackBet = minBet*2
            money -= minBet*2
        else:
            blackBet = blackBet*2
            money -= blackBet
    #Roll is Black
    elif table[roll] == 'black':
        money += blackBet*2
        blackBet = 0
        betBlack(minBet)
        if redBet*2 > maxBet:
            redBet = minBet*2
            money -= minBet*2
        else:
            redBet = redBet*2
            money -= redBet
    #Roll is Green
    else:
        if redBet*2 > maxBet:
            redBet = minBet*2
            money -= minBet*2
        else:
            redBet = redBet*2
            money -= redBet
            
        if blackBet*2 > maxBet:
            blackBet = minBet*2
            money -= minBet*2
        else:
            blackBet = blackBet*2
            money -= blackBet
            
    #--------------------
    #Handle Odd and Even
    #--------------------
    if roll != 0 and roll != 37:
        #Roll is Even
        if roll % 2 == 0:
            money += evenBet*2
            evenBet = 0
            betEven(minBet)
            if oddBet*2 > maxBet:
                oddBet = minBet*2
                money -= minBet*2
            else:
                oddBet = oddBet*2
                money -= oddBet
        #Roll is Odd
        else:
            money += oddBet*2
            oddBet = 0
            betOdd(minBet)
            if evenBet*2 > maxBet:
                evenBet = minBet*2
                money -= minBet*2
            else:
                evenBet = evenBet*2
                money -= evenBet
    #Roll is Green
    else:
        if evenBet*2 > maxBet:
            evenBet = minBet*2
            money -= minBet*2
        else:
            evenBet = evenBet*2
            money -= evenBet
            
        if oddBet*2 > maxBet:
            oddBet = minBet*2
            money -= minBet*2
        else:
            oddBet = oddBet*2
            money -= oddBet
            
    #--------------------
    #Handle Low and High
    #--------------------
    #Roll is Low
    if roll >= 1 and roll <= 18:
        money += lowBet*2
        lowBet = 0
        betLow(minBet)
        
        if highBet*2 > maxBet:
            highBet = minBet*2
            money -= minBet*2
        else:
            highBet = highBet*2
            money -= highBet		
    #Roll is High
    elif roll >= 19 and roll <= 36:
        money += highBet*2
        highBet = 0
        betHigh(minBet)
        if lowBet*2 > maxBet:
            lowBet = minBet*2
            money -= minBet*2
        else:
            lowBet = lowBet*2
            money -= lowBet
    #Roll is Green
    else:
        if lowBet*2 > maxBet:
            lowBet = minBet*2
            money -= minBet*2
        else:
            lowBet = lowBet*2
            money -= lowBet
            
        if highBet*2 > maxBet:
            highBet = minBet*2
            money -= minBet*2
        else:
            highBet = highBet*2
            money -= highBet
            
    #Output Log
    Print( "Ball Landed on {} {}. ".format( str(roll) if roll != 37 else '00' ,table[roll] ) )
    Print( "" )
    Print( "Game Numer: " + str(gamesPlayed) )
    Print( "$" + str(redBet) + " On Red." )
    Print( "$" + str(blackBet) + " On Black." )
    Print( "$" + str(oddBet) + " On Odd." )
    Print( "$" + str(evenBet) + " On Even." )
    Print( "$" + str(lowBet) + " On Low." )
    Print( "$" + str(highBet) + " On High." )
    Print( "$" + str(money) + " in our pocket." )
    
    #Stop Condition
    if money <= 0:
        Print( "" )
        Print( "Total Games Played " + str(gamesPlayed) )
        Print( "Best Game: {}".format( bestGame-1 if bestGame > 1 else bestGame ) )
        Print( "$" + str(highestBalance) + " was your biggest pocket." )
        
        with open("log.txt", 'w') as outfile:
            outfile.write(log)
        
        input = raw_input("Type 'quit' to end program. Press 'return'(enter) to play again. : ")
        if "q" in input.lower():
            break
        else:
            initGame()
    #time.sleep(10)