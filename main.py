'''
This is where the environment and bot are combined
to actualy train and test the bot
'''
import bot
import environment
def setup():
    game = environment.connect_4_game()
    state = game.init_state()
    game.display_board(state[0])

def play(pvp = False): #default play is against bot
    setup()
    if pvp: #local vs
        pass
    else: #play against bot
        pass

print("Welcome to our Connect 4 system")
choice_1 = int(input("Would you like to play against a bot(1) or a nearby friend(2)"))
if choice_1 == 1:
    mcts = bot.placeholder()
    choice_2 = int(input("Would you like to make the first move(1) or let the bot do so(2)?"))
    if choice_2 == 1:
        play()
    else:
        play(False,True)