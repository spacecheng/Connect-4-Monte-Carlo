'''
This is where the environment and bot are combined
to actualy train and test the bot
'''
import bot
import environment
game = environment.connect_4_game()
state = game.init_state()
game.display_board(state[0])