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

def choose_bot(game, bot_num = None):
    bots = [bot.rand_bot(game), bot.smart_rand(game)]
    print("Autoselected bot:", bot_num)
    if bot_num is not None:
        print("Apple")
        return bots[bot_num]
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

def play(pvp = 1, debug_skip = False): #default play is against bot
    end = 0
    game,cur_state = setup()
    board, heights, last_move, who_turn = cur_state
    marks = ["0","X","O"]
    if pvp == 0: #local vs
        print("Player 1 is mark X player 2 is mark O")
        while not end == 1:
            moveset = game.valid_moves(heights)
            game.display_board(board)
            print(f"Player {1 if who_turn == 1 else 2}'s turn ({marks[who_turn]}).\n Valid moves:{moveset}")
            choice = int(input())
            while choice not in moveset:
                print(f"Invalid move, Valid moves:{moveset}")
                choice = int(input())
            board, heights, move_idx, col_height = game.move(board,heights,who_turn,choice)
            end = game.check_win(board,moveset,who_turn,choice,move_idx,col_height)
            if end == 1:
                game.display_board(board)
                print(f"Player {1 if who_turn == 1 else 2} Wins (with move on col {choice})")
                return
            who_turn = -who_turn
    elif pvp == 1: #play against bot
        print("You are mark X and the bot is mark O")
        sel_bot = choose_bot(game)
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

            cur_state = game.move(board,heights,1,choice)
            board, heights, move_idx, col_height = cur_state
        while not end == 1:
            #bot move
            moveset = game.valid_moves(heights)
            cur_state = (board, heights, move_idx, col_height)
            choice = sel_bot.act(cur_state, heights, moveset)
            print(f"Bot choice: {choice}")
            board, heights, move_idx, col_height = game.move(board,heights,-1,choice)
            end = game.check_win(board,moveset,-1,choice,move_idx,col_height)
            if end == 1:
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
            end = game.check_win(board,moveset,1,choice,move_idx,col_height)
            if end == 1:
                game.display_board(board)
                print(f"You Win (with move on col {choice})")
                return
            
    elif pvp == 2: #bot vs bot
        #Option for delay or not debug reasons
        if debug_skip:
            print("Skipping selection")
            bot1 = choose_bot(game,0)
            bot2 = choose_bot(game,0)
        else:
            bot1 = choose_bot(game)
            bot2 = choose_bot(game)
        bot_menu = [bot1, bot2]
        bot_idx = 0
        sel_bot = bot_menu[bot_idx]
        print("Bot 1 is mark X Bot 2 is mark O")
        who_turn = 1
        while True:
            moveset = game.valid_moves(heights)
            choice = sel_bot.act(cur_state, heights, moveset)
            print(f"Bot {bot_idx + 1} choice: {choice}")
            board, heights, move_idx, col_height = game.move(board,heights,who_turn,choice)
            end = game.check_win(board,moveset,who_turn,choice,move_idx,col_height)
            if end == 1:
                game.display_board(board)
                print(f"Bot {bot_idx + 1} Wins (with move on col {choice})")
                return
            game.display_board(board)
            bot_idx = 1 - bot_idx
            who_turn = -who_turn
            if not debug_skip:
                input("Press enter to continue")

play()