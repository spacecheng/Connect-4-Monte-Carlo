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

def choose_bot():
    bots = [bot.rand_bot]
    while True:
        print("Select a bot:")
        print(*(f"{b.name}({i})" for i,b in enumerate(bots)))
        sel = int(input())
        if(sel >= 0 and sel < len(bots)):
            break
        else:
            print("Not a valid option")
    sel_bot = bots[sel]
    return sel_bot

def play(pvp = False): #default play is against bot
    end = False
    game,cur_state = setup()
    board, heights, last_move, who_turn = cur_state
    if pvp: #local vs
        print("Player 1 is mark 1 player 2 is mark -1")
        while not end:
            moveset = game.valid_moves(heights)
            game.display_board(board)
            print(f"Player {1 if who_turn == 1 else -1}'s turn.\n Valid moves:{moveset}")
            choice = int(input())
            while choice not in moveset:
                print(f"Invalid move, Valid moves:{moveset}")
                choice = int(input())
            board, heights, move_idx, col_height = game.move(board,heights,who_turn,choice)
            end = game.check_win(board,who_turn,choice,move_idx,col_height)
            if end:
                game.display_board(board)
                print(f"Player {1 if who_turn == 1 else -1} Wins (with move on col {choice})")
                return
            who_turn = -who_turn
    else: #play against bot
        print("You are mark 1 and the bot is mark -1")
        sel_bot = choose_bot()
        while True:
            print("Do you want to go first? (y/n)")
            choice = input()
            if choice == 'y':
                player_first = True
                break
            elif choice == 'n':
                player_first = False
                break
            else:
                print("Not a valid option")
        moveset = game.valid_moves(heights)
        if player_first is True:
            game.display_board(board)
            print(f"Your turn.\n Valid moves:{moveset}")
            while True:
                choice = int(input())
                if choice in moveset:
                    break
                print(f"Invalid move, Valid moves:{moveset}")
            board, heights, move_idx, col_height = game.move(board,heights,1,choice)
        while not end:
            #bot move
            moveset = game.valid_moves(heights)
            choice = sel_bot.act(board, heights, moveset)
            print(f"Bot choice: {choice}")
            board, heights, move_idx, col_height = game.move(board,heights,-1,choice)
            end = game.check_win(board,-1,choice,move_idx,col_height)
            if end:
                game.display_board(board)
                print(f"The bot Wins (with move on col {choice})")
                return
            moveset = game.valid_moves(heights)
            game.display_board(board)
            print(f"Your turn.\n Valid moves:{moveset}")
            while True:
                choice = int(input())
                if choice in moveset:
                    break
                print(f"Invalid move, Valid moves:{moveset}")
            board, heights, move_idx, col_height = game.move(board,heights,1,choice)
            end = game.check_win(board,1,choice,move_idx,col_height)
            if end:
                game.display_board(board)
                print(f"You Win (with move on col {choice})")
                return



            
            


                


play(False)
