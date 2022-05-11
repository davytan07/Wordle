import random
import os
import time
from wordleWords import word_list, dictionary
from termgraph import termgraph as tg
theWord = ''
gameRunning = True
gamesPlayed,gamesWon,currentStreak,maxStreak,first,second,third,fourth,fifth,sixth = 0,0,0,0,0,0,0,0,0,0
# pyinstaller wordleStandalone.py --onefile --target-arch universal2
def resetStats():
    f = open(f"{os.getcwd()}/wordleStats.dat", "w")
    f.write(f'''0
0
0
0
0
0
0
0
0
0''')
    f.close()

def recallStats():
    global gamesPlayed,gamesWon,currentStreak,maxStreak,first,second,third,fourth,fifth,sixth
    try:
        f = open(f"{os.getcwd()}/wordleStats.dat", "r")
        stats = f.readlines()
        gamesPlayed = int(stats[0])
        gamesWon = int(stats[1])
        currentStreak = int(stats[2])
        maxStreak = int(stats[3])
        first = int(stats[4])
        second = int(stats[5])
        third = int(stats[6])
        fourth = int(stats[7])
        fifth = int(stats[8])
        sixth = int(stats[9])
        f.close()
    except:
        prRed("No existing stats found, creating save file in your user folder...")
        time.sleep(2)
        resetStats()
        recallStats()

def updateStats():
    global gamesPlayed,gamesWon,currentStreak,maxStreak,first,second,third,fourth,fifth,sixth
    f = open(f"{os.getcwd()}/wordleStats.dat", "w")
    f.write(f'''{gamesPlayed}
{gamesWon}
{currentStreak}
{maxStreak}
{first}
{second}
{third}
{fourth}
{fifth}
{sixth}''')
    f.close()

def showStats():
    global gamesPlayed,gamesWon,currentStreak,maxStreak,first,second,third,fourth,fifth,sixth
    winRate = "%.1f" % (gamesWon/gamesPlayed*100)
    if currentStreak >= maxStreak:
        maxStreak = currentStreak
    print()
    prGreen("STATISTICS")
    print()
    statsTable = [[gamesPlayed,winRate,currentStreak,maxStreak],['Played', 'Win%', 'Current Streak', 'Max Streak']]
    for row in statsTable:
        print("{: ^20} {: ^20} {: ^20} {: ^20}".format(*row))
    print()
    prGreen("GUESS DISTRIBUTION")
    print()
    labels = ['1','2','3','4','5','6']
    data = [[first],[second],[third],[fourth],[fifth],[sixth]]
    normal_data = tg.normalize(data,72)
    len_categories = 1
    args = {'filename': 'filename', 'title': None, 'width': 72,
            'format': '{:.0f}', 'suffix': '', 'no_labels': False,
            'color': None, 'vertical': False, 'stacked': False,
            'different_scale': False, 'calendar': False,
            'start_dt': None, 'custom_tick': '', 'delim': '',
            'verbose': False, 'version': False}
    colors = [92]
    tg.stacked_graph(labels, data, normal_data, len_categories, args, colors)
    # os.system("termgraph %s/wordleDist.dat --color 'green' --format '{:.0f}'" % (os.getcwd()))

   
def clear():
    if os.name == 'nt':
        os.system('cls')
    elif os.name == 'posix':
        os.system('clear')

def printLogo():
    prGreen('W O R D L E')
    print()

def prRed(text): print(u"\u001b[41;1m {} \u001b[0m".format(text).center(90))

def prYellow(text): print(u"\u001b[43;1m {} \u001b[0m".format(text).center(90))

def prGreen(text): print(u"\u001b[42;1m {} \u001b[0m".format(text).center(90))

def prGrey(text): print(u"\u001b[47;1m {} \u001b[0m".format(text).center(90))

def randomWord():
    global theWord
    theWord = random.choice(word_list)

def customWord():
    global theWord
    while len(theWord) != 6:
        theWord = input("Choose a word for the other player to guess! ")

def showKeyboard():
    keyboard = ("".ljust(24,' ') + u"\u001b[47;1m {} \u001b[0m".format(' Q  W  E  R  T  Y  U  I  O  P '.center(30)) + "".rjust(24,' ')
     + '\n' + "".ljust(24,' ') + u"\u001b[47;1m {} \u001b[0m".format(' A  S  D  F  G  H  J  K  L '.center(30)) + "".rjust(24,' ')
      + '\n' + "".ljust(24,' ') + u"\u001b[47;1m {} \u001b[0m".format(' Z  X  C  V  B  N  M '.center(30))) + "".rjust(24,' ')
    return keyboard

def blankBoard():
    for i in range(6):
        print(((u"\u001b[47;1m[ ][ ][ ][ ][ ]\u001b[0m")).center(90))
    print()

def printBoard(*rows):
    global lives
    global board
    blanks = ''
    for row in rows:
        board += row + '\n'
    for i in range(lives):
        blanks += ((u"\u001b[47;1m[ ][ ][ ][ ][ ]\u001b[0m").center(90) + '\n')
    print(board,end='')
    print(blanks,end='')

def takeGuess(row):
    global lives
    global currentKB
    greens = set()
    yellows = set()
    blacks = set()
    while True:
        guess = input("").upper()
        if len(guess) != 5:
            prRed("Enter only 5-letter words!")
        elif guess not in dictionary:
            prRed("Not in word list.")
        else:
            clear()
            lives -= 1
            for i in range(len(guess)):           
                letter = guess[i]
                #in word, correct position -> green
                if letter == theWord[i]:
                    row += u"\u001b[42;1m {} \u001b[0m".format(letter)
                    greens.update(letter)
                else:
                    #in word, wrong position -> yellow
                    if letter in theWord:
                        if row.count(letter) < theWord.count(letter):
                            row += u"\u001b[43;1m {} \u001b[0m".format(letter)
                            yellows.update(letter)
                        #not in word -> black
                        else:
                            row += u"\u001b[47;1m {} \u001b[0m".format(letter)
                    #not in word -> black
                    else:
                        row += u"\u001b[47;1m {} \u001b[0m".format(letter)
                        blacks.update(letter)
            #updateKeyboard
            for letter in yellows:
                # if row.count(letter) < theWord.count(letter):
                mapping = [(' {} '.format(letter),u"\u001b[43;1m {} \u001b[47;1m".format(letter))]
                for k,v in mapping:
                    currentKB = currentKB.replace(k,v)
            for letter in greens:
                row = row.replace(u"\u001b[43;1m {} \u001b[0m".format(letter),u"\u001b[47;1m {} \u001b[0m".format(letter),guess.count(letter)-theWord.count(letter))
                mapping = [(' {} '.format(letter),u"\u001b[42;1m {} \u001b[47;1m".format(letter))]
                for k,v in mapping:
                    currentKB = currentKB.replace(k,v)
            for letter in blacks:
                mapping = [(' {} '.format(letter),u"\u001b[40;1m {} \u001b[47;1m".format(letter))]
                for k,v in mapping:
                    currentKB = currentKB.replace(k,v)
            return guess, row

def checkWin(guess,lives):
    global currentStreak,first,second,third,fourth,fifth,sixth
    if guess == theWord:
        if lives == 5:
            first += 1
            prGreen("Genius.")
        elif lives == 4:
            second += 1
            prGreen("Magnificent.")
        elif lives == 3:
            third += 1
            prGreen("Impressive.")
        elif lives == 2:
            fourth += 1
            prGreen("Splendid.")
        elif lives == 1:
            fifth += 1
            prGreen("Great.")
        elif lives == 0:
            sixth += 1
            prGreen("Phew.")
        return True
    else:
        if lives == 0:
            currentStreak = 0
            prYellow("The word was"+' '+theWord)
        return False

def replay():
    global gameRunning
    showStats()
    updateStats()
    replay = ' '
    while replay != '' and replay != 'Q' and replay != '/RESET':
        replay = input("Hit \U000023CE to play again, or enter Q to quit".center(80)).upper()
    if replay == '':
        gameRunning = True
        clear()
    elif replay == 'Q':
        prYellow("Stats saved!")
        gameRunning = False
    else:
        resetStats()
        prRed("Stats resetted!")
        time.sleep(2)
        gameRunning = True

#gameLogic
# resetStats()

while gameRunning:
    recallStats()
    clear()
    gamesPlayed += 1
    currentStreak += 1
    row = ''
    board = ''
    guessedLetters = ''
    lives = 6
    currentKB = showKeyboard()
    printLogo()
    blankBoard()
    randomWord()
    # theWord = 'HUBBY'
    # theWord = 'WINGS'
    # theWord = 'SHELF'
    # theWord = 'ACTOR'
    # theWord = 'VIDEO'
    while lives>0:
        # print(f"Test purposes: word is {theWord} ")
        guesses,rows = takeGuess(row)
        printLogo()
        printBoard(rows.center(134))
        print()
        print(currentKB)
        print()
        if checkWin(guesses,lives) == True:
            gamesWon += 1
            break
    time.sleep(1)
    clear()
    replay()