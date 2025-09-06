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
    newName = input(f'Press Enter if you are {name} otherwise, please enter you name and Press Enter: ')
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
df = pd.read_csv(r'C:/Users/kent1/Documents/ThéodoresHomeworkEnglish/listeDeMotFrancais.csv')

# Declare variables
resultTracker = 0   # Initialize
wordMemory = []     # Initialize
lottery = 0         # Initialize
lengthOfThisWeeksEnglishGlossary = 20  # Enter count of words for the week's glossary

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
            lottery = random.randint(df.shape[0]-lengthOfThisWeeksEnglishGlossary, df.shape[0]-1)
            return(wordFinder(lottery))
    return lottery

for i in range(lengthOfThisWeeksEnglishGlossary):
    lottery = wordFinder(random.randint(df.shape[0]-lengthOfThisWeeksEnglishGlossary, df.shape[0]-1))
    wordMemory.append(df.iat[lottery, 1])
    print("")
    print(Fore.MAGENTA + df.iat[lottery, 1] + Fore.RESET)
    userInput = str(input("Type the english translation of the above word: "))
    if userInput.lower() == df.iat[lottery, 0]:
        print("Well done! You spelt " + Fore.GREEN + df.iat[lottery, 0] + Fore.RESET + " correctly. Keep it up!")
        resultTracker += 1
    else:
        print("The spelling I am looking for is " + Fore.CYAN + df.iat[lottery, 0] + Fore.RESET + ", you keyed in " + Fore.RED + userInput + Fore.RESET)

if resultTracker == lengthOfThisWeeksEnglishGlossary:
    print(f"Hey, you scored {resultTracker}/{lengthOfThisWeeksEnglishGlossary}! You are the BEST!")
elif resultTracker >= lengthOfThisWeeksEnglishGlossary-3:
    print(f"Hey, you scored {resultTracker}/{lengthOfThisWeeksEnglishGlossary}! Well done!")
else:
    print(f"Hey, you scored {resultTracker}/{lengthOfThisWeeksEnglishGlossary}! Keep trying, you will get there :)")

# Stop timer
end = time.time()
timeOfPlay = end - start
today = datetime.now()

# Appending to file
with open("commentCaVa.txt", 'a') as file1:
    file1.write(playerName + "," + today.strftime('%Y-%m-%d,%H:%M:%S') + "," + str(resultTracker) + "," + str(round(timeOfPlay, 2)) + '\n')