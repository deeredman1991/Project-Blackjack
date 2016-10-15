import random
import time
import json
from ctypes import windll
import sys

#Console Attributes
FOREGROUND_BLACK     = 0x0000
FOREGROUND_BLUE      = 0x0001
FOREGROUND_GREEN     = 0x0002
FOREGROUND_CYAN      = 0x0003
FOREGROUND_RED       = 0x0004
FOREGROUND_MAGENTA   = 0x0005
FOREGROUND_YELLOW    = 0x0006
FOREGROUND_GREY      = 0x0007
FOREGROUND_LIGHT     = 0x0008 #Light Colors

BACKGROUND_BLACK     = 0x0000
BACKGROUND_BLUE      = 0x0010
BACKGROUND_GREEN     = 0x0020
BACKGROUND_CYAN      = 0x0030
BACKGROUND_RED       = 0x0040
BACKGROUND_MAGENTA   = 0x0050
BACKGROUND_YELLOW    = 0x0060
BACKGROUND_GREY      = 0x0070
BACKGROUND_LIGHT     = 0x0080 #Light Colors

STD_OUTPUT_HANDLE = -11
stdout_handle = windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
SetConsoleTextAttribute = windll.kernel32.SetConsoleTextAttribute

def setTextColor(*args):
    color = 0
    for i in args:
        color += i
    SetConsoleTextAttribute(stdout_handle, color)
    
def Print(msg, end='\n'):
    sys.stdout.write('{}{}'.format(msg, end))
    sys.stdout.flush()

#Init Default Console Colors
DEFAULT_BACKGROUND   = BACKGROUND_BLACK
DEFAULT_FOREGROUND   = FOREGROUND_LIGHT+FOREGROUND_GREY

setTextColor(DEFAULT_BACKGROUND+DEFAULT_FOREGROUND)
    
#Define betting functions
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

#Define general init function
def initGame():
    global gamesPlayed, redBet, blackBet, evenBet, oddBet, lowBet, highBet, money, minBet, maxBet, highestBalance, maxRoll
    
    gamesPlayed = 0
    
    redBet = 0
    blackBet = 0
    evenBet = 0
    oddBet = 0
    lowBet = 0
    highBet = 0
    
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
            print("Generating Options.json.")
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
    
    #Output initial bets
    Print ("~Initial Bet~" )
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
    
####################
###SCORE KEEPING####
####################
    gamesPlayed += 1
    if money > highestBalance:
        highestBalance = money
        
####################
###BETTING LOGIC####
####################
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
            
####################
#######OUTPUT#######
####################
    #--------------------
    #-----Full Roll------
    #--------------------
    setTextColor(DEFAULT_BACKGROUND+DEFAULT_FOREGROUND)
    Print( "Ball ", end="" )
    
    if roll != 0 and roll != 37:
        if roll % 2 == 0:
            setTextColor(DEFAULT_BACKGROUND+FOREGROUND_LIGHT+FOREGROUND_CYAN)
        else:
            setTextColor(DEFAULT_BACKGROUND+FOREGROUND_LIGHT+FOREGROUND_YELLOW)
    else:
        setTextColor(DEFAULT_BACKGROUND+FOREGROUND_LIGHT+FOREGROUND_GREEN)
    Print( "landed", end="" )
    
    setTextColor(DEFAULT_BACKGROUND+DEFAULT_FOREGROUND)
    Print( " on ", end="" )
    
    if roll >= 1 and roll <= 18:
        setTextColor(DEFAULT_BACKGROUND+FOREGROUND_MAGENTA)
    elif roll >= 19 and roll <= 36:
        setTextColor(DEFAULT_BACKGROUND+FOREGROUND_LIGHT+FOREGROUND_MAGENTA)
    else:
        setTextColor(DEFAULT_BACKGROUND+FOREGROUND_LIGHT+FOREGROUND_GREEN)
    
    Print( "{} ".format(roll if roll != 37 else '00'), end="" )
    
    if table[roll] == 'red':
        setTextColor(DEFAULT_BACKGROUND+FOREGROUND_LIGHT+FOREGROUND_RED)
    elif table[roll] == 'black':
        setTextColor(DEFAULT_BACKGROUND+FOREGROUND_LIGHT+FOREGROUND_BLACK)
    else:
        setTextColor(DEFAULT_BACKGROUND+FOREGROUND_LIGHT+FOREGROUND_GREEN)
    Print( table[roll].capitalize(), end="" )
    setTextColor(DEFAULT_BACKGROUND+DEFAULT_FOREGROUND)
    Print( ".")
    
    Print("")
    
    #--------------------
    #---Red and Black----
    #--------------------
    #Red
    setTextColor(DEFAULT_BACKGROUND+DEFAULT_FOREGROUND)
    Print( "${number:.<{padding}} on ".format( number = redBet, padding = len(str(highestBalance)) ), end="" )
    setTextColor(DEFAULT_BACKGROUND+FOREGROUND_LIGHT+FOREGROUND_RED)
    Print( "Red", end="" )
    setTextColor(DEFAULT_BACKGROUND+DEFAULT_FOREGROUND)
    Print( ".")
    
    #Black
    setTextColor(DEFAULT_BACKGROUND+DEFAULT_FOREGROUND)
    Print( "${number:.<{padding}} on ".format( number = blackBet, padding = len(str(highestBalance)) ), end="" )
    setTextColor(DEFAULT_BACKGROUND+FOREGROUND_LIGHT+FOREGROUND_BLACK)
    Print( "Black", end="" )
    setTextColor(DEFAULT_BACKGROUND+DEFAULT_FOREGROUND)
    Print( ".")
    
    #--------------------
    #----Odd and Even----
    #--------------------
    #Odd
    setTextColor(DEFAULT_BACKGROUND+DEFAULT_FOREGROUND)
    Print( "${number:.<{padding}} on ".format( number = oddBet, padding = len(str(highestBalance)) ), end="" )
    setTextColor(DEFAULT_BACKGROUND+FOREGROUND_LIGHT+FOREGROUND_YELLOW)
    Print( "Odd", end="" )
    setTextColor(DEFAULT_BACKGROUND+DEFAULT_FOREGROUND)
    Print( ".")
    
    #Even
    setTextColor(DEFAULT_BACKGROUND+DEFAULT_FOREGROUND)
    Print( "${number:.<{padding}} on ".format( number = evenBet, padding = len(str(highestBalance)) ), end="" )
    setTextColor(DEFAULT_BACKGROUND+FOREGROUND_LIGHT+FOREGROUND_CYAN)
    Print( "Even", end="" )
    setTextColor(DEFAULT_BACKGROUND+DEFAULT_FOREGROUND)
    Print( ".")
    
    #--------------------
    #----Low and High----
    #--------------------
    #Low
    setTextColor(DEFAULT_BACKGROUND+DEFAULT_FOREGROUND)
    Print( "${number:.<{padding}} on ".format( number = lowBet, padding = len(str(highestBalance)) ), end="" )
    setTextColor(DEFAULT_BACKGROUND+FOREGROUND_MAGENTA)
    Print( "Low", end="" )
    setTextColor(DEFAULT_BACKGROUND+DEFAULT_FOREGROUND)
    Print( ".")
    
    #High
    setTextColor(DEFAULT_BACKGROUND+DEFAULT_FOREGROUND)
    Print( "${number:.<{padding}} on ".format( number = highBet, padding = len(str(highestBalance)) ), end="" )
    setTextColor(DEFAULT_BACKGROUND+FOREGROUND_LIGHT+FOREGROUND_MAGENTA)
    Print( "High", end="" )
    setTextColor(DEFAULT_BACKGROUND+DEFAULT_FOREGROUND)
    Print( ".")
    
    #--------------------
    #-------Pocket-------
    #--------------------
    if money > 0:
        setTextColor(DEFAULT_BACKGROUND+FOREGROUND_LIGHT+FOREGROUND_GREEN)
    else:
        setTextColor(DEFAULT_BACKGROUND+FOREGROUND_LIGHT+FOREGROUND_RED)
    Print( "$" + str(money), end="" )
    setTextColor(DEFAULT_BACKGROUND+DEFAULT_FOREGROUND)
    Print( " in our pocket.")
    
####################
###STOP CONDITION###
####################
    if money <= 0:
        Print( "" )
        setTextColor(DEFAULT_BACKGROUND+FOREGROUND_CYAN)
        Print( "Games Played: ", end="" )
        setTextColor(DEFAULT_BACKGROUND+DEFAULT_FOREGROUND)
        Print( gamesPlayed )
        setTextColor(DEFAULT_BACKGROUND+FOREGROUND_LIGHT+FOREGROUND_GREEN)
        Print( "$" + str(highestBalance), end="" )
        setTextColor(DEFAULT_BACKGROUND+FOREGROUND_CYAN)
        Print( " was your biggest pocket." )
        input = raw_input("Type 'quit' to end program. Press 'return'(enter) to play again. : ")
        if "q" in input.lower():
            break
        else:
            Print( "" )
            initGame()
    #time.sleep(10)