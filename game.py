# 게임 자체 규칙

# 보드 생성, 가능한 수 찾기, 수 두기, 승리 판정, 무승부 판정, 현재상태 복사
class Game:
    # 보드판 및 현재 플레이어 생성
    def __init__(self):
        self.board = [['.' for _ in range(5)] for _ in range(5)]
        self.current_player = 'X'
    
    # 중간 결과 출력 및 디버깅을 위해 보드판 출력
    def print_board(self):
        for row in self.board:
            print(' '.join(row))
        print()
    
    # 놓을수 있는 칸 검사(이중반복문을 통해 순회)-> 반환
    def get_possible_moves(self):
        moves = []
        for i in range(5):
            for j in range(5):
                if self.board[i][j] == '.':
                    moves.append((i,j))
        return moves
    
    # 플레이어가 놓은 말을 보드판에 반영, 이미 놓아져있는경우 False 반환
    def make_move(self, move, player):
        row, col = move
        if not (0 <= row < 5 and 0 <= col < 5):
            return False
        
        if self.board[row][col] != '.':
            return False
        
        self.board[row][col] = player
        
        return True
    
    # 플레이터 턴 변경
    def switching_player(self):
        if self.current_player == 'X':
            self.current_player = 'O'
        else:
            self.current_player = 'X'
    
    # 승자 체크
    def checking_winner(self):
        # 가로, 세로, 대각선(\, /) 연속 4칸이 동일한지 체크 -> 5x5판의 규격 이용
        
        # 가로줄 검사
        for row in range(5):
            for col in range(2):
                cell = self.board[row][col]
            
                if cell != '.' and \
                cell == self.board[row][col+1] and \
                cell == self.board[row][col+2] and \
                cell == self.board[row][col+3]:
                    return cell
        
        # 세로줄 검사
        for row in range(2):
            for col in range(5):
                cell = self.board[row][col]
            
                if cell != '.' and \
                cell == self.board[row+1][col] and \
                cell == self.board[row+2][col] and \
                cell == self.board[row+3][col]:
                    return cell
        
        # 대각선(\방향) 검사
        for row in range(2):
            for col in range(2):
                cell = self.board[row][col]
            
                if cell != '.' and \
                cell == self.board[row+1][col+1] and \
                cell == self.board[row+2][col+2] and \
                cell == self.board[row+3][col+3]:
                    return cell
        
        # 대각선(/방향) 검사
        for row in range(2):
            for col in range(3,5):
                cell = self.board[row][col]
            
                if cell != '.' and \
                cell == self.board[row+1][col-1] and \
                cell == self.board[row+2][col-2] and \
                cell == self.board[row+3][col-3]:
                    return cell
        
        # 승부가 나지 않으면 None return
        return None 
    
    # 승패가 나뉘지 않은 경우 True 반환
    def draw(self):
        if self.checking_winner() is not None:
            return False

        for row in self.board:
             if '.' in row:
                return False

        return True
    
    # 종료되었는지 확인
    def is_terminated(self):
        # 무승부거나 승/패가 나뉜경우->게임이 종료됐으므로 True 반환()
        if self.checking_winner() is not None or self.draw():
            return True 
        return False
    
    def copy(self):
        new_game = Game()
        for i, row in enumerate(self.board):
            new_game.board[i] = row[:]
        new_game.current_player = self.current_player
        return new_game
