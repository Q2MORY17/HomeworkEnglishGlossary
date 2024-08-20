import pandas as pd
import random
from colorama import init, Fore
from datetime import datetime
import time
import os

#TODO: clear on all os + make the path available on all os
# Clearing the screen - Windows
os.system('cls')

def NewPlayer(name = 'Théodore'):
    newName = input(f'Tryck "Enter" om du är {name} annars, skriv ditt namn här och sen tryck "Enter": ')
    if newName == "":
        return name
    else:
        return newName.capitalize()

# Who is playing
playerName = NewPlayer()

# Start timer
start = time.time()

# Colorama initialize to work on Command line
init()

# Import .csv data to a Pandas dataframe 
df = pd.read_csv(r'C:/Users/kent1/Documents/ThéodoresHomeworkEnglish/SvenskaBegrepp.csv')

# Declare variables
resultTracker = 0
wordMemory = []
possibleAnswers = []
lottery = 0
lengthOfSvenskaGlossary = 20

def answerHint(lottery): # Say lottery = 3
    possibleNumberGenerator= [lottery]
    for i in range(3):
        entryNonEqualToLottery = random.randint(df.shape[0]-lengthOfSvenskaGlossary, df.shape[0]-1)
        while entryNonEqualToLottery == lottery:
            entryNonEqualToLottery = random.randint(df.shape[0]-lengthOfSvenskaGlossary, df.shape[0]-1)
        if i == 0:
            possibleNumberGenerator.append(entryNonEqualToLottery)
        else:
            while entryNonEqualToLottery in possibleNumberGenerator:
                entryNonEqualToLottery = random.randint(df.shape[0]-lengthOfSvenskaGlossary, df.shape[0]-1)
            possibleNumberGenerator.append(entryNonEqualToLottery)
        random.shuffle(possibleNumberGenerator)
    return [df.iat[possibleNumberGenerator[0], 0], df.iat[possibleNumberGenerator[1], 0], df.iat[possibleNumberGenerator[2], 0], df.iat[possibleNumberGenerator[3], 0]]

def wordFinder(lottery):
    """
    wordFinder looks to the dataframe and issues an index for a unique word to the game. it avoids repeat words
    by recursively re-running the algorithm until a unique entry is found.

    Parameters
    ----------
    lottery : int
        random selection in the swedish column

    Returns
    -------
    lottery
        which would not have been previously used in game
    """
    for i in wordMemory:
        if df.iat[lottery, 1] == i:
            lottery = random.randint(df.shape[0]-lengthOfSvenskaGlossary, df.shape[0]-1)
            return(wordFinder(lottery))
    return lottery

for i in range(lengthOfSvenskaGlossary):
    possibleAnswers.clear()
    lottery = wordFinder(random.randint(df.shape[0]-lengthOfSvenskaGlossary, df.shape[0]-1))
    wordMemory.append(df.iat[lottery, 1])
    print("")
    print(Fore.MAGENTA + df.iat[lottery, 1] + Fore.RESET)
    possibleAnswers = answerHint(lottery)
    print("Förslag: "+ Fore.YELLOW + f"{possibleAnswers[0]} | {possibleAnswers[1]} | {possibleAnswers[2]} | {possibleAnswers[3]}" + Fore.RESET)
    userInput = str(input("Skriv den korrekta orden som matchar bergreppet ovan: "))
    if userInput.capitalize() == df.iat[lottery, 0]:
        print("Bra gjort, " + Fore.GREEN + df.iat[lottery, 0] + Fore.RESET + " är korrekt. Forsätt så!")
        resultTracker += 1
    else:
        print("Orden förväntad är " + Fore.CYAN + df.iat[lottery, 0] + Fore.RESET + " , du skrev " + Fore.RED + userInput + Fore.RESET)

if resultTracker == lengthOfSvenskaGlossary:
    print(f"Hej, du fick {resultTracker}/{lengthOfSvenskaGlossary}! Du är BÄST!\n")
elif resultTracker > lengthOfSvenskaGlossary-4:
    print(f"Hej, du fick {resultTracker}/{lengthOfSvenskaGlossary}! Bra jobbat!\n")
else:
    print(f"Hej, du fick {resultTracker}/{lengthOfSvenskaGlossary}! Försök igen, du kommer att lyckas :)\n")

# Stop timer
end = time.time()
timeOfPlay = end - start
today = datetime.now()

# Appending to file
with open("SvenskaBegreppResult.txt", 'a') as file1:
    file1.write(playerName + "," + today.strftime('%Y-%m-%d,%H:%M:%S') + "," + str(resultTracker) + "," + str(round(timeOfPlay, 2)) + '\n')