#WrdGuessr
import csv
from random import randint


class wordGuessr():  #wordGuessr game class

  def __init__(self):  #instantiate important variables
    """
    Init function for wrdguessr class
    """

    self.currentName = ''
    self.totalScore = 0

    self.attainedScore = 0

    self.words = []
    self.currentWord = ''

    self.roundInProgress = False
    self.gameInProgress = False

    self.scoreboard = []

    self.setName()

  def readScoreboardFile(self, path):
    """
    Open CSV file, update the self.scorefboard dictionary using values from the CSV
    Arguments:
        path: path to scoreboard file
    """

    try: #Using try to catch any errors
      with open(path, 'r') as sc:
        scoreboard = csv.DictReader(sc)

        for score in scoreboard:
          self.scoreboard.append(score)
          if score['name'] == self.currentName:
            self.totalScore = int(score['score'])
        sc.close()

    except FileNotFoundError:
      print('Could not find scoreboard')

  def updateLocalBoard(self):
    """
    Updates the local scoreboard dictionary with the current users score
    """
    found = False
    for index, score in enumerate(self.scoreboard):
      if score['name'] == self.currentName:
        self.scoreboard[index]['score'] = self.totalScore
        found = True
    if found == False:
      self.scoreboard.append({
        'name': self.currentName,
        'score': str(self.totalScore)
      })

  def saveScoreboardFile(self, path):  
    """
    Export the self.scoreboard dict into a CSV file
    Arguments:
        path: path to scoreboard file
    """
    
    self.updateLocalBoard()
    self.SortScoreboard()
    with open(path, 'w') as scw:
      scw.writelines('name,score\n')
      for score in self.scoreboard:
        scw.writelines(score['name'] + ',' + str(score['score']) + '\n')
      scw.close()

  def SortScoreboard(self):
    """
    Sort the scoreboard array.
    uses bubble sort for the scoreboard, as its might not be loaded in order.
    """
    
    sorted = False

    while (sorted == False):
      swaps = 0
      for index in range(0, len(self.scoreboard) - 1):

        if int(self.scoreboard[index]['score']) < int(
            self.scoreboard[index + 1]['score']):
          print(
            str(self.scoreboard[index]['score']) + '<' +
            str(self.scoreboard[index + 1]['score']))
          #swap items
          temp = self.scoreboard[index]
          self.scoreboard[index] = self.scoreboard[index + 1]
          self.scoreboard[index + 1] = temp
          swaps += 1

      if swaps == 0:
        sorted = True

  def printScoreboardTop5(self):  
    """
    Print the top 5 key-value pairs in the self.scoreboard dict
    """
    
    self.updateLocalBoard()
    self.SortScoreboard()

    print('----- SCOREBOARD -----'
          )  #below is the format that the scoreboard is printed in
    if len(self.scoreboard) < 5:
      for x in range(0, len(self.scoreboard)):
        print(
          ('{}. {} [{} Points]').format(str(x + 1), self.scoreboard[x]['name'],
                                        self.scoreboard[x]['score']))
    else:
      for x in range(0, 4):
        print(
          ('{}. {} [{} Points]').format(str(x + 1), self.scoreboard[x]['name'],
                                        self.scoreboard[x]['score']))
    print('----------------------')

  def printLogo(self):
    """
    Print game logo using ascii art
    """
    usrString = ''
    #code below prints the ASCII art of the games name to act as a title screen/landing page
    if self.currentName != '':
      usrString = ('Playing as: ' + self.currentName + ' - All time Score: ' +
                   str(self.totalScore))

    print("""

░██╗░░░░░░░██╗██████╗░██████╗░░██████╗░██╗░░░██╗███████╗░██████╗░██████╗██████╗░
░██║░░██╗░░██║██╔══██╗██╔══██╗██╔════╝░██║░░░██║██╔════╝██╔════╝██╔════╝██╔══██╗
░╚██╗████╗██╔╝██████╔╝██║░░██║██║░░██╗░██║░░░██║█████╗░░╚█████╗░╚█████╗░██████╔╝
░░████╔═████║░██╔══██╗██║░░██║██║░░╚██╗██║░░░██║██╔══╝░░░╚═══██╗░╚═══██╗██╔══██╗
░░╚██╔╝░╚██╔╝░██║░░██║██████╔╝╚██████╔╝╚██████╔╝███████╗██████╔╝██████╔╝██║░░██║
░░░╚═╝░░░╚═╝░░╚═╝░░╚═╝╚═════╝░░╚═════╝░░╚═════╝░╚══════╝╚═════╝░╚═════╝░╚═╝░░╚═╝
{}
                    """.format(usrString))

  def cls(self):
    """
    Clear the console screen
    """
    for x in range(0, 100):
      print('')

  def endGame(self):
    """
    End the game session and save scoreboard to file
    """
    self.saveScoreboardFile('scoreboard.txt')
    self.gameInProgress = False

  def startRound(self):
    """
    Start a round for the guessing game
    """
    self.setRandomWord() #Set a random word for the round
    self.roundInProgress = True #Condition the while loop wil use later on to stay in the round
    word_array = list(self.currentWord[0]) #Split the current word into a array of letters
    guessedWord = []#list ofusers currently guessed letters
    hint = False #Boolean of whether to show the hint
    self.attainedScore = 5 #user score. Start off at 5 to allow for 5 initial guesses

    for x in range(0, len(word_array)):  #replaces the word chosen with '_' #fills the users guessed letters list with underscores
      guessedWord.append('_')

    while (self.roundInProgress == True): #Actual loop for the round

      self.cls()
      self.printLogo()

      #---------------------------------- Beginning of round Checks ----------------------------------#

      if (''.join(guessedWord)) == self.currentWord[0]:  #Check if we've won yet before beginning another guess round. The users guessWord array would be equal to the current word
        print('You have won the round!')
        print('The word was {}'.format(self.currentWord[0]))
        self.totalScore += self.attainedScore
        input('Press enter to continue...')
        self.cls()
        self.roundInProgress = False

      elif (self.attainedScore <= 0): #Check if the score has dipped below 0, in this case, end the round and notify the user.
        print('You have lost the game, Better luck next time')
        print('The word was {}'.format(self.currentWord))
        input('Press enter to continue...')
        self.cls()
        self.roundInProgress = False
      else:
        for letter in guessedWord:
          print(letter, end='')

    #---------------------------------- Beginning of rounds user input ----------------------------------#

        print('\n')
        print('Current Score: {}'.format(self.attainedScore))
        print('Length of word: {}'.format(len(self.currentWord[0])))

        if hint:
          print('Hint: {}'.format(self.currentWord[1]))

        print("Enter # to return to main menu or * to show the hint.")
        print("Alternatively, you can attempt to guess the entire word")
        usr_input = input('Please make a guess > ')

    #---------------------------------- Beginning of user input Checks ----------------------------------#

        if (len(usr_input) > 1) and (usr_input == self.currentWord[0]): #if the guess is a word, ie length is more than 1, then check if the word matches the currentword. If so, end the game
          self.cls()
          self.printLogo()
          print('You have won the round!')
          print('The word was {}'.format(self.currentWord[0]))
          self.attainedScore = (len(self.currentWord) * 10) + 5
          self.totalScore += self.attainedScore
          input('Press enter to continue...')
          self.cls()
          self.roundInProgress = False

        elif usr_input.lower() in word_array:  #General check to see if the guess is in the curent word
          guessScore = 0
          dup = True  #check if we've checked all occurances of that particular word in the word

          while dup == True:  #We need a loop here in case the input word appears more than once in the array.
            if usr_input.lower() in word_array:
              guessedWord[word_array.index(
                usr_input.lower())] = usr_input.lower()
              word_array[word_array.index(usr_input.lower())] = '-'
              guessScore += 10
            else:
              dup = False

          self.attainedScore += guessScore

        elif usr_input == '#':
          self.roundInProgress = False

        elif usr_input == '*':
          hint = True

        else:
          self.cls()
          self.attainedScore -= 1
          print('Incorrect guess. Try again!')
          input('Press enter to continue...')

    #---------------------------------- end of round loop ----------------------------------#

  def gameMainMenu(self):
    """
    Main menu routine
    """
    validOptionChosen = False
    availableChoices = { #dictionary that holds referances to the relevent menu funcitons, and a string to attach them to user input
      '1': self.startRound, #If option 1 selected then it starts the game
      '2': self.printHelp,  #Choosing option 2 runs a function that prints a small guide on how to use the program
      '3': self.endGame     #Terminates current session
    }

    while (validOptionChosen != True and self.gameInProgress):  #This while loop runs the options menu on the home screen
      self.cls()
      self.printLogo()  #Prints ASCII art
      self.printScoreboardTop5( )  #If populated, the top 5 scores in the scoreboard file will be printed on the home screen


      #Displays the menu for the user to then make a decision
      usr_input = input(""" 
Select one of the following options:
1) Start a new round
2) How to play
3) Exit Game
> """)  

      if usr_input not in availableChoices.keys():  #Makes a check to ensure that the user chose a valid input
        self.cls()
        print('Invalid Option!')  #If the user input is found to be invalid an error message
        input('Press enter to continue...')

      elif usr_input in availableChoices.keys():#If its a valid selection, call the function that is referanced by the string
        availableChoices[usr_input]()
        validOptionChosen = False

  def loadFile(self, path):
    """
    Load wordlist into memory
    Arguments:
        path: path to wordlist file
    """
    with open(path, 'r') as file:  #Open a csv file as read only
      open_CSV = csv.reader(
        file)  #Parse the opened file instance into a CSVReader object
      for row in open_CSV:  #iterate through all rows
        self.words.append(row)  #and append the row into thw words array
      print(self.words)
      file.close()  #Close the file once its in memory
#chooses a random word from the words.txt file

  def setRandomWord(self):
    """
    Pick a random word and set internal currentWord variable
    """
    print('Picking a random word')
    picked_word = self.words[randint(0, len(self.words) - 1)]
    self.currentWord = picked_word
    self.currentWord[0] = self.currentWord[0].lower()


#User inputs their username here, also checks if the username is valid (more than 3 characters long)

  def setName(self):
    """
    Sets user name for leaderboard.
    """
    validName = False
    while validName != True:
      self.cls()
      self.printLogo()
      print('\n\n')
      user_input = input(
        'Enter a username for the scoreboard: ')  #username input
      if len(user_input) < 4:  #username validity checked here
        print(
          'Invalid username. Please input a name more than 3 characters long.')
      else:
        self.currentName = user_input
        validName = True

  def startGame(self, path):
    """
    Start the emain game loop
    """
    self.loadFile(path)  #Load the specified file into memory
    self.gameInProgress = True  #Overall variable to set game as in progress
    while self.gameInProgress:  #While the game is running
      self.gameMainMenu()

  def printHelp(self):  #This function prints a guide on how to play the game and interact with the program
    """
    Print help for the game
    """

    self.cls()
    self.printLogo()
    print('''

    Welcome to WRDGUESSR.

    When you start a round, you will be presented with the length of a random word as
    well as underscores to show the words you will guess.

    You begin the round with 5 points. For every correct guess, you will be awarded
    with 10 points, but beware if you make an incorrect guess, you will lose a point.
    If the socre ever falls below zero in a round, the round will be over.

    At the end of the round, your score will be added to you all time score, and if you
    are good at the game, you will be lsited as a champion on the leaderboard.
    
    Good Luck. We hope you enjoy playing WRDGUESSR.
    ''')  # <--

    input('Press enter to continue...')


if __name__ == "__main__":
    print('Error: You have tried to excecute the wrdguessr library directly. Please use the main.py wrapper to instanciate and launch the game.')