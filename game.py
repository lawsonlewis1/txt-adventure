"""A small game to run in the shell."""


import os
from time import sleep


class Player():
    '''The playable character.
    
    When initiated, the restore() method is called which will check if a save
    data file exists. If it does the user can restore a previous instance of
    the Player class.

    If no save data file exists or the player chooses not to restore a previous 
    session's character a new Player is created. The user will be asked to enter
    a name for the Player, and the attributes will be set to defaults.

    Attributes: name, health, attack, defense, magic.
    '''
    def __init__(self):
        '''Create a new Player, or restore from a previous session.'''

        global SCENE
        global PLAY
        
        if self.restore() is False:
            print("Welcome to Lawson's game :)\n\n"
                  "Would you like to view the Tutorial?")
            while PLAY is True:
                choice = prompt()
                if choice is True:
                    print('Jolly good show, but first...')
                    break
                elif choice is False:
                    print('Very well then...')
                    SCENE = 4
                    break
            if PLAY is True:
                print('What is your name?')
                name = ''
                while name == '':
                    name = input('\n  > ')
                self.name = name
                self.health = 100
                self.attack = 10
                self.defense = 10
                self.magic = 10
    
    def __repr__(self):
        '''Return a nicely formatted table of the players attributes.'''

        return (
                '\n'
                '        {}\n\n'
                '        Health:        {}\n'
                '        Attack:        {}\n'
                '        Defense:       {}\n'
                '        Magic:         {}\n'
                ''.format(self.name.upper(), self.health, self.attack, self.defense, self.magic)
        )
    
    def restore(self):
        '''Restore data from a previous session, if available.
        
        Checks to see if the file 'save_data.txt' exists in the current
        directory. Initialises the player with the values found in this
        file. Returns false, if the file does not exist or if the player
        does not wish to restore. Returns true if restoration completes.

        Restore also sets the SCENE variable to reflect the current point
        in the dialogue from the previous session.
        '''

        global SCENE

        if os.path.isfile('./save_data.txt'):
            print('You have saved data from a previous session.'
                  '\nWould you like to continue from saved data?')
            while True:
                choice = prompt()
                if choice is True:
                    with open('save_data.txt', 'r') as file:
                        data = file.read()
                    data = data.split()
                    self.name = data[0]
                    self.health = int(data[1])
                    self.attack = int(data[2])
                    self.defense = int(data[3])
                    self.magic = int(data[4])
                    SCENE = int(data[5])
                    return True
                elif choice is False:
                    return False
        else:
            return False
    
    def modify(self, stat, up, amt):
        '''increase or decrease the players stats.
        
        Inputs
        stat: <str> the stat to modify.
        up: <str> direction to modify up/down.
        amt: <str> the amount to modify.
        '''

        amt = int(amt)

        if up == '+':
            if stat == 'health':
                self.health += amt
            elif stat == 'attack':
                self.attack += amt
            elif stat == 'defense':
                self.defense += amt
            elif stat == 'magic':
                self.magic += amt
        elif up == '-':
            if stat == 'health':
                self.health -= amt
            elif stat == 'attack':
                self.attack -= amt
            elif stat == 'defense':
                self.defense -= amt
            elif stat == 'magic':
                self.magic -= amt

            

    def death(self):
        '''Kill the player and finish the game.

        The game is harsh, if you die you cannot save.
        '''
        global ALIVE

        print("Oh no, You have died!")
        ALIVE = False
        quit()


def get_dialogue():
    '''Gets story dialogue from file.
    
    Dialogue is contained in the file 'Dialogue.txt' 
    in the current folder.
    '''

    with open('Dialogue.txt', 'r') as file:
        dialogue = file.readlines()
    
    dialogue = [x.strip() for x in dialogue if x[0] is not '#']
    cuts = [index for index, term in enumerate(dialogue) if term == '[CUT]']
    scenes = [[] for x in cuts]
    start = 0
    scene = 0
    for cut in cuts:
        for line in dialogue[start:cut]:
            scenes[scene].append(str(line))
        start = cut + 1
        scene += 1
    return scenes


def prompt():
    '''The in-game command line.
    
    Presents a command prompt. If the command is recognised the
    corresponding function will be called. If the command is not
    recognised the prompt will simply return the input as a
    lower case string. The return value can be used for context
    sensitive evaluation.
    '''
    global ALIVE
    global PLAY
    global PLAYER
    global SCENE

    while PLAY is True:
        command = input('\n  > ').lower()
        if command == '':
            return None
        elif command == 'help':
            print(
                "\n"
                "       Command         Action\n"
                "\n"
                "       <enter>         continue\n"
                "       help            view this help menu\n"
                "       stats           view the player stats screen\n"
                "       save            save the game\n"
                "       quit            exit the game\n"
            )
        elif command == 'stats':
            print(PLAYER)
        elif command == 'save':
            save(PLAYER, SCENE)
        elif command == 'quit':
            quit()
        elif command in ['yes', 'y']:
            return True
        elif command in ['no', 'n']:
            return False
        else:
            return command


def quit():
    '''Quit the game.
    
    Asks for confirmation. You can not save if you are dead.
    '''

    global PLAY
    global ALIVE
    global PLAYER
    global SCENE

    done = False

    if ALIVE is True:
        while done is False:
            print('Are you sure?')
            choice = input('\n  > ').lower()
            if choice in ['yes', 'y']:
                PLAY = False
                print('Do you wish to save your progress?')
                while True:
                    choice = input('\n  > ').lower()
                    if choice in ['yes', 'y']:
                        save(PLAYER, SCENE)
                        print('Goodbye...')
                        done = True
                        break
                    elif choice in ['no', 'n']:
                        print('Goodbye...')
                        done = True
                        break
                    else:
                        print('invalid option')
            elif choice in ['no', 'n']:
                break
            else:
                print('invalid option')
    else:
        print('Better luck next time.')
        PLAY = False


def save(player, scene):
    '''Saves the game.
    
    Writes the players attributes to 'save_data.txt'. The current
    scene is also written to the save file, so that a player can
    resume to the same scene they were at when they quit.
    '''

    with open('save_data.txt', 'w') as file:
        print('Saving...')
        data = [
            str(player.name), str(player.health), 
            str(player.attack), str(player.defense),
            str(player.magic), str(scene)
        ]
        for each in data:
            file.write(str(each + "\n"))
    sleep(.5)
    print('saved')


def print_scene(scene):
    for line in scene:
        try:
            stat, up, amt = line.split(' ', 2)
            if stat in ['health', 'attack', 'defense', 'magic']:
                PLAYER.modify(stat, up, amt)
        except ValueError:
            pass
    [print(line) for line in scene]


def play_choice_scene(scene):

    global PLAY

    del scene[0]
    yes = scene.index('yes>')
    no = scene.index('no>')
    [print(line) for line in scene[0:yes]]
    while PLAY is True:
        choice = prompt()
        if choice is True:
            print_scene(scene[yes+1:no])
            break
        elif choice is False:
            print_scene(scene[no+1:])
            break


def play_puzzle_scene(scene):

    global PLAY

    del scene[0]

    hint = scene.index('hint>')
    stop_hints = scene.index('answer>') - 1
    answer = scene[scene.index('answer>')+1]
    attempts = int(scene[scene.index('attempts>')+1])
    prize = scene.index('prize>')
    penalty = scene.index('penalty>')

    [print(line) for line in scene[0:hint]]
    while PLAY is True:
        if attempts < 1:
            print_scene(scene[penalty+1:])
            break
        print('    Attempts Remaining {}'.format(attempts))
        choice = prompt()
        if choice == answer:
            print_scene(scene[prize+1:penalty])
            break
        elif choice is None:
            if hint < stop_hints:
                hint += 1
                print(scene[hint])
            else:
                print('No more hints for you!')
        else:
            attempts -= 1


        



if __name__ == '__main__':
    PLAY = True
    ALIVE = True
    SCENE = 0
    DIALOGUE = get_dialogue()
    PLAYER = Player()
    while PLAY is True:
        try:
            scene = DIALOGUE[SCENE]
        except IndexError:
            PLAY = False
            print("To be continued...")
            break
        if '[CHOICE]' in scene:
            play_choice_scene(scene)
        elif '[PUZZLE]' in scene:
            play_puzzle_scene(scene)
        else:
            print_scene(scene)
        prompt()
        SCENE += 1
