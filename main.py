from game import Game
from agents import RandomAgent, NoisyHeuristicAgent, AlphaBetaAgent
import random
import time


# 현재 플레이어에 맞는 agent에게 수를 받아오는 함수
def get_agent_move(agent, game):
        return agent.action(game)

# 한 판 진행하는 함수
def play_one_game(agent_x, agent_o, print_game=True, seed=None):
    if seed is not None:
        random.seed(seed)

    game = Game()

    # 시작 플레이어 랜덤
    if random.random() < 0.5:
        game.current_player = 'X'
    else:
        game.current_player = 'O'

    move_count = 0
    alpha_agent_total_time = 0.0
    alpha_agent_total_nodes = 0

    if print_game:
        print("===================================")
        print("Start Player:", game.current_player)
        game.print_board()

    while not game.is_terminated():
        if game.current_player == 'X':
            current_agent = agent_x
        else:
            current_agent = agent_o

        start_time = time.time()
        move = get_agent_move(current_agent, game)
        end_time = time.time()

        thinking_time = end_time - start_time

        if move is None:
            break

        result = game.make_move(move, game.current_player)

        if result is False:
            print("Invalid move:", move)
            break

        move_count += 1

        # AlphaBetaAgent의 시간 / 노드 수 측정
        if isinstance(current_agent, AlphaBetaAgent):
            alpha_agent_total_time += thinking_time
            alpha_agent_total_nodes += current_agent.expanded_nodes

        if print_game:
            print("Player", game.current_player, "moves:", move)
            game.print_board()

        if not game.is_terminated():
            game.switching_player()

    winner = game.checking_winner()

    if winner == 'X':
        result_text = 'X'
    elif winner == 'O':
        result_text = 'O'
    else:
        result_text = 'Draw'

    if print_game:
        print("Result:", result_text)
        print("Total Moves:", move_count)
        print("AlphaBeta Total Time:", round(alpha_agent_total_time, 4))
        print("AlphaBeta Expanded Nodes:", alpha_agent_total_nodes)
        print("===================================")

    return {
        'winner': result_text,
        'move_count': move_count,
        'alpha_time': alpha_agent_total_time,
        'alpha_nodes': alpha_agent_total_nodes
    }


# 여러 판 실험하는 함수
def run_games(agent_x, agent_o, num_games=20, print_each_game=False):
    results = []
    x_win = 0
    o_win = 0
    draw = 0

    total_alpha_time = 0.0
    total_alpha_nodes = 0
    total_moves = 0

    for i in range(num_games):
        result = play_one_game(agent_x, agent_o, print_game=print_each_game, seed=i)
        results.append(result)

        if result['winner'] == 'X':
            x_win += 1
        elif result['winner'] == 'O':
            o_win += 1
        else:
            draw += 1

        total_alpha_time += result['alpha_time']
        total_alpha_nodes += result['alpha_nodes']
        total_moves += result['move_count']

    print("========== Experiment Result ==========")
    print("Total Games:", num_games)
    print("X Wins:", x_win)
    print("O Wins:", o_win)
    print("Draws:", draw)
    print("Average Moves:", round(total_moves / num_games, 2))
    print("Average AlphaBeta Time:", round(total_alpha_time / num_games, 4))
    print("Average AlphaBeta Expanded Nodes:", round(total_alpha_nodes / num_games, 2))
    print("=======================================")

    return results


if __name__ == "__main__":
    # 1. 한 판만 테스트하고 싶을 때
    print("===== Single Game Test: AlphaBeta vs Random =====")
    agent_x = AlphaBetaAgent('X', depth_limit=4, time_limit=3.0)
    agent_o = RandomAgent('O')
    play_one_game(agent_x, agent_o, print_game=True)

    # 2. 여러 판 실험하고 싶을 때
    print("\n===== 20 Games: AlphaBeta vs Random =====")
    agent_x = AlphaBetaAgent('X', depth_limit=4, time_limit=3.0)
    agent_o = RandomAgent('O')
    run_games(agent_x, agent_o, num_games=20, print_each_game=False)

    print("\n===== 20 Games: AlphaBeta vs NoisyHeuristic =====")
    agent_x = AlphaBetaAgent('X', depth_limit=4, time_limit=3.0)
    agent_o = NoisyHeuristicAgent('O', epsilon=0.2)
    run_games(agent_x, agent_o, num_games=20, print_each_game=False)
