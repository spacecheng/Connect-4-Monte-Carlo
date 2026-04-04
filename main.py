'''
This is where the environment and bot are combined
to actualy train and test the bot
'''
import bot
import environment
def setup():
    game = environment.connect_4_game()
    state = game.init_state()
    return game,state

def play(pvp = False): #default play is against bot
    if pvp: #local vs
        end = False
        print("Player 1 is mark 1 player 2 is mark -1")
        game,cur_state = setup()
        board, heights, last_move, who_turn = cur_state
        moveset = game.valid_moves(heights)
        while not end:
            game.display_board(board)
            print(f"Player {1 if who_turn == 1 else -1}'s turn.\n Valid moves:{moveset}")
            choice = int(input())
            while choice not in moveset:
                print(f"Invalid move, Valid moves:{moveset}")
                choice = int(input())
            board, heights, move_idx, col_height = game.move(board,heights,who_turn,choice)
            end = game.check_win(board,heights,who_turn,choice,move_idx,col_height)
            if end:
                game.display_board(board)
                print(f"Player {1 if who_turn == 1 else -1} Wins (with move on col {choice})")
                return
            who_turn = -who_turn
    else: #play against bot
        pass

play(True)
