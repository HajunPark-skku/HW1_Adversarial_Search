import random
import time

class RandomAgent:
    # agent가 O인지 X인지 저장하는 함수
    def __init__(self, player):
        self.player = player
    
    # 현재게임을 인자로 받아 어떤 수를 놓을지 결정하는 함수
    def action(self, game):
        possible_moves = game.get_possible_moves()
        if len(possible_moves) == 0:
            return None
        
        move = random.choice(possible_moves)
        return move
    
class NoisyHeuristicAgent:
    def __init__(self, player, epsilon=0.2):
        self.player = player
        self.epsilon = epsilon
        
    def get_opponent(self):
        if self.player == 'X':
            return 'O'
        else:
            return 'X'

    # 즉시 이기는 수를 찾는 함수
    def find_winning_move(self, game, player):
        for move in game.get_possible_moves():
            copied_game = game.copy()
            copied_game.make_move(move, player)

            if copied_game.checking_winner() == player:
                return move
        return None

    def center_preferred_move(self, game):
        possible_moves = game.get_possible_moves()
        if (2, 2) in possible_moves:
            return (2, 2)

        best_move = None
        best_distance = 999

        for move in possible_moves:
            row, col = move
            distance = abs(row - 2) + abs(col - 2)

            if distance < best_distance:
                best_distance = distance
                best_move = move
        return best_move
    
    def action(self, game):
        possible_moves = game.get_possible_moves()
        if len(possible_moves) == 0:
            return None
        
        # 20%의 확률로 랜덤
        if random.random() <= self.epsilon:
            return random.choice(possible_moves)
        
        winning_move = self.find_winning_move(game, self.player)
        if winning_move is not None:
            return winning_move
        
        opponent = self.get_opponent()
        blocking_move = self.find_winning_move(game, opponent)
        if blocking_move is not None:
            return blocking_move
        return self.center_preferred_move(game)

class AlphaBetaAgent:
    def __init__(self, player, depth_limit=3, time_limit=3.0):
        self.player = player
        self.depth_limit = depth_limit
        self.time_limit = time_limit
        self.expanded_nodes = 0

    def get_opponent(self):
        if self.player == 'X':
            return 'O'
        else:
            return 'X'

    def terminal_score(self, game):
        winner = game.checking_winner()

        if winner == self.player:
            return 100000
        elif winner == self.get_opponent():
            return -100000
        else:
            return 0

    def score_line(self, line):
        my_count = line.count(self.player)
        opp_count = line.count(self.get_opponent())
        empty_count = line.count('.')

        # 둘 다 포함된 줄은 위협성이 낮으므로 0점
        if my_count > 0 and opp_count > 0:
            return 0

        # 내 쪽 점수
        if my_count == 4:
            return 10000
        elif my_count == 3 and empty_count == 1:
            return 200
        elif my_count == 2 and empty_count == 2:
            return 30
        elif my_count == 1 and empty_count == 3:
            return 5

        # 상대 쪽 점수
        if opp_count == 4:
            return -10000
        elif opp_count == 3 and empty_count == 1:
            return -250
        elif opp_count == 2 and empty_count == 2:
            return -35
        elif opp_count == 1 and empty_count == 3:
            return -5

        return 0

    def evaluate(self, game):
        board = game.board
        score = 0
        opponent = self.get_opponent()

        # 중심 선호
        center_positions = [(2, 2), (2, 1), (2, 3), (1, 2), (3, 2)]
        for row, col in center_positions:
            if board[row][col] == self.player:
                score += 8
            elif board[row][col] == opponent:
                score -= 8

        # 가로 검사
        for row in range(5):
            for col in range(2):
                line = [
                    board[row][col],
                    board[row][col + 1],
                    board[row][col + 2],
                    board[row][col + 3]
                ]
                score += self.score_line(line)

        # 세로 검사
        for row in range(2):
            for col in range(5):
                line = [
                    board[row][col],
                    board[row + 1][col],
                    board[row + 2][col],
                    board[row + 3][col]
                ]
                score += self.score_line(line)

        # 대각선 (\) 검사
        for row in range(2):
            for col in range(2):
                line = [
                    board[row][col],
                    board[row + 1][col + 1],
                    board[row + 2][col + 2],
                    board[row + 3][col + 3]
                ]
                score += self.score_line(line)

        # 대각선 (/) 검사
        for row in range(2):
            for col in range(3, 5):
                line = [
                    board[row][col],
                    board[row + 1][col - 1],
                    board[row + 2][col - 2],
                    board[row + 3][col - 3]
                ]
                score += self.score_line(line)

        return score

    def alphabeta(self, game, depth, alpha, beta, maximizing, start_time):
        # 시간 초과 시 현재 상태 평가값 반환
        if time.time() - start_time > self.time_limit:
            return self.evaluate(game)

        # 게임 종료 상태
        if game.is_terminated():
            return self.terminal_score(game)

        # 깊이 제한 도달
        if depth == 0:
            return self.evaluate(game)

        self.expanded_nodes += 1
        possible_moves = game.get_possible_moves()

        if maximizing:
            value = float('-inf')

            for move in possible_moves:
                copied_game = game.copy()
                copied_game.make_move(move, self.player)

                score = self.alphabeta(
                    copied_game,
                    depth - 1,
                    alpha,
                    beta,
                    False,
                    start_time
                )

                if score > value:
                    value = score

                if value > alpha:
                    alpha = value

                if alpha >= beta:
                    break

            return value

        else:
            value = float('inf')
            opponent = self.get_opponent()

            for move in possible_moves:
                copied_game = game.copy()
                copied_game.make_move(move, opponent)

                score = self.alphabeta(
                    copied_game,
                    depth - 1,
                    alpha,
                    beta,
                    True,
                    start_time
                )

                if score < value:
                    value = score

                if value < beta:
                    beta = value

                if alpha >= beta:
                    break

            return value

    def action(self, game):
        possible_moves = game.get_possible_moves()

        if len(possible_moves) == 0:
            return None

        start_time = time.time()
        self.expanded_nodes = 0

        best_move = None
        best_score = float('-inf')

        for move in possible_moves:
            # 시간 초과 시 랜덤 fallback
            if time.time() - start_time > self.time_limit:
                return random.choice(possible_moves)

            copied_game = game.copy()
            copied_game.make_move(move, self.player)

            score = self.alphabeta(
                copied_game,
                self.depth_limit - 1,
                float('-inf'),
                float('inf'),
                False,
                start_time
            )

            if score > best_score:
                best_score = score
                best_move = move

        if best_move is None:
            return random.choice(possible_moves)

        return best_move
