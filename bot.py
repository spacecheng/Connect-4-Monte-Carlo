'''
This is where all the bot stuff like the 
tables and choosing action will be defined
'''
import environment
import random
import math
from environment import help_check_win as check_win

EXPLORE_WEIGHT = math.sqrt(2)


class Node:
    __slots__ = ('board', 'heights', 'mark', 'move', 'parent',
                 'children', 'untried_moves', 'wins', 'visits', 'terminal')

    def __init__(self, board, heights, mark, move=None, parent=None):
        self.board = board
        self.heights = heights
        self.mark = mark
        self.move = move
        self.parent = parent
        self.children = []
        self.untried_moves = None
        self.wins = 0.0
        self.visits = 0
        self.terminal = None

    def uct(self, c=EXPLORE_WEIGHT):
        if self.visits == 0:
            return float('inf')
        return (self.wins / self.visits) + c * math.sqrt(
            math.log(self.parent.visits) / self.visits
        )

    def best_child(self, c=EXPLORE_WEIGHT):
        return max(self.children, key=lambda n: n.uct(c))


class mcts_bot:
    def __init__(self, game, iterations = 1000):
        self.game = game
        self.iterations = iterations
        self._cols = game.cols
        self._rows = game.rows
        self._wc = game.win_cond
        self.name = f"MCTS({iterations})"

    def _check_win(self, board, mark, col, move_idx, col_height):
        """Fast win check without debug prints, used during rollouts."""
        row = col_height - 1
        cols, rows, wc = self._cols, self._rows, self._wc
        for dr, dc in ((0, 1), (1, 0), (1, 1), (1, -1)):
            count = 1
            for sign in (1, -1):
                r, c = row + dr * sign, col + dc * sign
                while 0 <= r < rows and 0 <= c < cols and board[r * cols + c] == mark:
                    count += 1
                    r += dr * sign
                    c += dc * sign
            if count >= wc:
                return True
        return False

    def _rollout(self, board, heights, mark):
        """Random playout from given state. Returns winner mark or 0 for draw."""
        game = self.game
        check = self._check_win
        while True:
            moveset = game.valid_moves(heights)
            if not moveset:
                return 0
            col = random.choice(moveset)
            board, heights, move_idx, col_height = game.move(
                board, heights, mark, col
            )
            if check(board, mark, col, move_idx, col_height):
                return mark
            mark = -mark

    def act(self, state, heights, moveset):
        """Select best move via Monte Carlo Tree Search."""
        board = state[0]
        game = self.game
        check = self._check_win

        ones = sum(1 for x in board if x == 1)
        neg_ones = sum(1 for x in board if x == -1)
        mark = 1 if ones == neg_ones else -1

        if len(moveset) == 1:
            return moveset[0]

        root = Node(board, heights, mark)
        root.untried_moves = list(moveset)

        for _ in range(self.iterations):
            node = root

            # --- Selection: walk down tree via UCT ---
            while (node.untried_moves is not None
                   and len(node.untried_moves) == 0
                   and node.children):
                node = node.best_child()

            # --- Terminal node reached: reuse known result ---
            if node.terminal is not None:
                result = node.terminal

            # --- Expansion: add one child for a random untried move ---
            elif node.untried_moves and len(node.untried_moves) > 0:
                col = random.choice(node.untried_moves)
                node.untried_moves.remove(col)

                new_board, new_heights, move_idx, col_height = game.move(
                    node.board, node.heights, node.mark, col
                )
                child = Node(
                    new_board, new_heights, -node.mark,
                    move=col, parent=node
                )
                node.children.append(child)

                if check(new_board, node.mark, col, move_idx, col_height):
                    child.terminal = node.mark
                    child.untried_moves = []
                    result = node.mark
                else:
                    child_moves = game.valid_moves(new_heights)
                    if not child_moves:
                        child.terminal = 0
                        child.untried_moves = []
                        result = 0
                    else:
                        child.untried_moves = child_moves
                        # --- Simulation: random rollout ---
                        result = self._rollout(
                            new_board, new_heights, -node.mark
                        )

                node = child
            else:
                result = 0

            # --- Backpropagation ---
            while node is not None:
                node.visits += 1
                if result == -node.mark:
                    node.wins += 1.0
                elif result == 0:
                    node.wins += 0.5
                node = node.parent

        return max(root.children, key=lambda n: n.visits).move


class rand_bot:
    name = "random"
    def __init__(self,game):
        self.game = game
    def act(self,state,heights,moveset):
        r = random.random
        move = moveset[int(r() * len(moveset))]
        return move
    
class smart_rand:
    name = "random+check"
    def __init__(self,game):
        self.game = game
    def act(self,state,heights,moveset):
        board, _, move_idx, _ = state
        win_cond = self.game.win_cond
        h = self.game.rows
        w = self.game.cols
        r = random.random
        for move in moveset:
            print(f"checking {move}")
            print(heights)
            new_height =heights[move]
            move_idx = new_height*w + move
            print(f"mvidx = {move_idx}")
            print("Given board")
            self.game.display_board(board)
            print(f"params: {win_cond} {w} {h} {move} {move_idx} {new_height}")
            res = check_win(win_cond,w,h,board,moveset,1,move,move_idx,new_height+1)
            print(f"result{res}")
            if res == 1:
                print("found win")
                return move
            res = check_win(win_cond,w,h,board,moveset,-1,move,move_idx,new_height+1)
            print(res)
            if res == 1:
                print("found loss")
                return move
        move = moveset[int(r() * len(moveset))]
        return move
class smart_rand_stack:
    name = "random+stackcheck"
    def __init__(self,game):
        self.game = game
    def act(self,state,heights,moveset):
        game = self.game
        board, _, move_idx, _ = state
        win_cond = self.game.win_cond
        h = game.rows
        w = game.cols
        r = random.random
        for move in moveset:
            print(f"checking {move}")
            print(heights)
            new_height =heights[move]
            move_idx = new_height*w + move
            print(f"mvidx = {move_idx}")
            print("Given board")
            game.display_board(board)
            #slightly different new_height
            new_height+= 1
            res = check_win(win_cond,w,h,board,moveset,1,move,move_idx,new_height)
            print(f"result{res}")
            if res == 1:
                print("found win")
                return move
            res = check_win(win_cond,w,h,board,moveset,-1,move,move_idx,new_height)
            print(res)
            if res == 1:
                print("found loss")
                return move
            print("No surface win/loss found")
            #new stack check
            if new_height < h:
                board, heights, _, col_height = game.move(board,heights,1,move)
                res = 0
                print("Checking stack")
                temp_move_idx = new_height*w + move
                new_height += 1
                temp_moveset = game.valid_moves(temp_heights)
                res = check_win(win_cond, w, h, temp_board, temp_moveset, -1, move, temp_move_idx, new_height)
                
            
        move = moveset[int(r() * len(moveset))]
        return move