import random
import os
from wordleWords import word_list, dictionary
theWord = ''
gameRunning = True

def clear():
    if os.name == 'nt':
        os.system('cls')
    elif os.name == 'posix':
        os.system('clear')

def printLogo():
    prGreen('W O R D L E')
    print()

def prRed(text): print(u"\u001b[41;1m {} \u001b[0m".format(text).center(41))

def prYellow(text): print(u"\u001b[43;1m {} \u001b[0m".format(text).center(41))

def prGreen(text): print(u"\u001b[42;1m {} \u001b[0m".format(text).center(41))

def randomWord():
    global theWord
    theWord = random.choice(word_list)

def customWord():
    global theWord
    while len(theWord) != 6:
        theWord = input("Choose a word for the other player to guess! ")

def showKeyboard():
    keyboard = (u"\u001b[47;1m {} \u001b[0m".format(' Q  W  E  R  T  Y  U  I  O  P '.center(30))
     + '\n' + u"\u001b[47;1m {} \u001b[0m".format(' A  S  D  F  G  H  J  K  L '.center(30))
      + '\n' + u"\u001b[47;1m {} \u001b[0m".format(' Z  X  C  V  B  N  M '.center(30)))
    return keyboard

def blankBoard():
    for i in range(6):
        print(((u"\u001b[47;1m[ ][ ][ ][ ][ ]\u001b[0m")).center(41))
    print()

def printBoard(*rows):
    global lives
    global board
    blanks = ''
    for row in rows:
        board += row + '\n'
    for i in range(lives):
        blanks += ((u"\u001b[47;1m[ ][ ][ ][ ][ ]\u001b[0m").center(41) + '\n')
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
            for letter in greens:
                row = row.replace(u"\u001b[43;1m {} \u001b[0m".format(letter),u"\u001b[47;1m {} \u001b[0m".format(letter),guess.count(letter)-theWord.count(letter))
                mapping = [(' {} '.format(letter),u"\u001b[42;1m {} \u001b[47;1m".format(letter))]
                for k,v in mapping:
                    currentKB = currentKB.replace(k,v)
            for letter in yellows:
                mapping = [(' {} '.format(letter),u"\u001b[43;1m {} \u001b[47;1m".format(letter))]
                for k,v in mapping:
                    currentKB = currentKB.replace(k,v)
            for letter in blacks:
                mapping = [(' {} '.format(letter),u"\u001b[40;1m {} \u001b[47;1m".format(letter))]
                for k,v in mapping:
                    currentKB = currentKB.replace(k,v)
            return guess, row

def checkWin(guess,lives):
    if guess == theWord:
        if lives == 5:
            prGreen("Genius.")
        elif lives == 4:
            prGreen("Magnificent.")
        elif lives == 3:
            prGreen("Impressive.")
        elif lives == 2:
            prGreen("Splendid.")
        elif lives == 1:
            prGreen("Great.")
        elif lives == 0:
            prGreen("Phew.")
        return True
    else:
        if lives == 0:
            prYellow("The word was"+' '+theWord)
        return False

def replay():
    global gameRunning
    replay = ''
    while replay != 'Y' and replay != 'N':
        replay = input("Do you want to play again? Y/N ").upper()
    if replay == 'Y':
        gameRunning = True
        clear()
    else:
        prYellow("Goodbye.")
        gameRunning = False

#gameLogic
while gameRunning:
    clear()
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
    while lives>0:
        # print(f"Test purposes: word is {theWord} ")
        guesses,rows = takeGuess(row)
        printLogo()
        printBoard(rows.center(86))
        print()
        print(currentKB)
        print()
        if checkWin(guesses,lives) == True:
            break
    replay()