import random
import time
import json

#Init Roulette Table
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

while True:
    try:
        with open('Options.json', 'r') as outfile:
            jsonData = json.load(outfile)
            money = jsonData["Starting Money"]
            minBet = jsonData["Minimum Bet"]
            maxBet = jsonData["Maximum Bet"]
            americanTable = jsonData["American Table"]
            break
    except IOError:
        print("Generating Options.json.")
        encoded_data = json.dumps({"Starting Money": 500, "Minimum Bet": 1, "Maximum Bet": 50, "American Table": True}, indent=4)
        with open('Options.json', 'w') as outfile:
            outfile.write(encoded_data + '\n')
            
highestBalance = money
maxRoll = 38 if americanTable else 37

games = 0

redBet = 0
blackBet = 0
evenBet = 0
oddBet = 0
lowBet = 0
highBet = 0

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

#Init Bet

betRed(minBet)
betBlack(minBet*2)
betOdd(minBet)
betEven(minBet*2)
betLow(minBet)
betHigh(minBet*2)

print "~Initial Bet~"
print "$" + str(redBet) + " On Red."
print "$" + str(blackBet) + " On Black."
print "$" + str(oddBet) + " On Odd."
print "$" + str(evenBet) + " On Even."
print "$" + str(lowBet) + " On Low."
print "$" + str(highBet) + " On High."
print "$" + str(money) + " in our pocket."

#Main Loop
while True:
    games += 1
    
    if money > highestBalance:
        highestBalance = money
        
    #Ball
    roll = random.randrange(0, maxRoll)
    
    #Handle Red and Black
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
    else: #Roll is Green
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
            
    #Handle Odd and Even
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
                
    else: #Roll is green
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
            
    #Handle low and high
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
    else: #Roll is green
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
            
    print "Ball Landed on {} {}. ".format( str(roll) if roll != 37 else '00' ,table[roll] )
    print ""
    print "$" + str(redBet) + " On Red."
    print "$" + str(blackBet) + " On Black."
    print "$" + str(oddBet) + " On Odd."
    print "$" + str(evenBet) + " On Even."
    print "$" + str(lowBet) + " On Low."
    print "$" + str(highBet) + " On High."
    print "$" + str(money) + " in our pocket."
    
    #raw_input("")
    if money <= 0:
        print "Games Played " + str(games)
        print "$" + str(highestBalance) + " was your biggest pocket."
        raw_input("")
        break
    #time.sleep(10)