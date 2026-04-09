'''
This is where the environment and bot are combined
to actualy train and test the bot
'''
import bot
import environment
def setup(rows, cols, win_cond):
    game = environment.connect_4_game(rows, cols, win_cond)
    state = game.init_state()
    return game,state

def choose_bot(game, bot_num = None,cust_mcts = None):
    bots = [bot.rand_bot(game), bot.smart_rand(game), bot.mcts_bot(game,250),bot.mcts_bot(game)]
    print("Autoselected bot:", bot_num)
    if bot_num is not None:
        if cust_mcts is not None:
            return bot.mcts_bot(game,cust_mcts)
        print("Apple")
        return bots[bot_num]
    end_num = len(bots)
    while True:
        print("Select a bot:")
        print(*(f"{b.name}({i})" for i,b in enumerate(bots)),f"MCTS(custom)({end_num})")
        sel = int(input())
        if(sel >= 0 and sel < len(bots)):
            break
        elif sel == end_num:
            print("How much iterations?")
            its = int(input())
            return bot.mcts_bot(game,its)
        else:
            print("Not a valid option")
    sel_bot = bots[sel]
    return sel_bot

def play(bd_r = 6, bd_c = 7, bd_win_cd = 4,  pvp = 1, debug_skip = False): #default play is against bot
    end = 0
    game,cur_state = setup(bd_r, bd_c, bd_win_cd)
    board, heights, last_move, who_turn = cur_state
    marks = ["0","X","O"]
    if pvp == 0: #local vs
        print("Player 1 is mark X player 2 is mark O")
        while not end == 1 and not end == -1:
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
            elif end == -1:
                game.display_board(board)
                print("Game Ended in a Tie")
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
        move_idx = None
        col_height = None
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
        while not end == 1 and not end == -1:
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
            elif end == -1:
                game.display_board(board)
                print("Game Ended in a Tie")
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
            elif end == -1:
                game.display_board(board)
                print("Game Ended in a Tie")
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
        turns = 0
        while True:
            moveset = game.valid_moves(heights)
            cur_state = (board, heights, None, who_turn)
            choice = sel_bot.act(cur_state, heights, moveset)
            turns +=1
            print(f"Bot {bot_idx + 1} choice: {choice}")
            board, heights, move_idx, col_height = game.move(board,heights,who_turn,choice)
            end = game.check_win(board,moveset,who_turn,choice,move_idx,col_height)
            if end == 1:
                game.display_board(board)
                print(f"Bot {bot_idx + 1}({sel_bot.name}) Wins (on turn {turns} with move on col {choice}) against Bot {2 - bot_idx}")
                return
            elif end == -1:
                game.display_board(board)
                print("Game Ended in a Tie")
                return
            game.display_board(board)
            bot_idx = 1 - bot_idx
            sel_bot = bot_menu[bot_idx]
            who_turn = -who_turn
            if not debug_skip:
                input("Press enter to continue")
uniq_board_bin = None
while True:
    uniq_board_qry = input("Do you want a custom board? (y/n)")
    if uniq_board_qry == 'y':
        uniq_board_bin = True
        break
    elif uniq_board_qry == 'n':
        uniq_board_bin = False
        break
    else:
        print("Not a valid answer...")
        continue
if uniq_board_bin:
    bd_r = int(input("Enter board rows:"))
    bd_c = int(input("Enter board cols:"))
    bd_win_cd = int(input("Enter amout in a row to win:"))
while True:
    print("Which play would you like:")
    print("(0) Player vs Player")
    print("(1) Player vs Bot")
    print("(2) Bot vs Bot")
    pvp = int(input())
    if pvp in range(3):
        break
    else:
        print("Not a valid option...")
if uniq_board_bin:
    play(bd_r, bd_c, bd_win_cd, pvp)
else:
    play(pvp=pvp)


