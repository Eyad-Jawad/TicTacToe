#XOproject: VERY Updated
class Players:
    def __init__(self, AI: str, player: str) -> None:
        self.ai: str = AI
        self.player: str = player

    def checkWin(self, player: str, board: list[list[str | None]]) -> bool:
        for i in range(3):
            if all([board[i][j] == player for j in range(3)]): return True # horizontal positions
            if all([board[j][i] == player for j in range(3)]): return True # vertical positions
        if all([board[i][i]     == player for i in range(3)]): return True # diagonal from left positions
        if all([board[i][2 - i] == player for i in range(3)]): return True # diagonal from right positions
        
        return False
    
    def checkTie(self, board: list[list[str | None]]) -> bool:
        for i in range(3):
            for j in range(3):
                if not board[i][j]: return False
        return True
    
    # TODO: I dont like how this works
    def getAvailableMoves(self, board: list[list[str | None]]) -> list[tuple[int, int]]:
        availableMoves = []
        for i in range(3):
            for j in range(3):
                if not board[i][j]:
                    availableMoves.append((i, j))
        return availableMoves


class Ai(Players):
    def __init__(self, AI, player):
        super().__init__(AI, player)
        self.turn: str = player

    def aiPlay(self, board: list[list[str | None]]) -> tuple[int, int]:
        availableMoves = self.getAvailableMoves(board)

        bestScore = float('-inf')
        bestMove = None
        
        for move in availableMoves:
            board[move[0]][move[1]] = self.ai
            score = self.minmax(0, board)
            if score > bestScore:
                bestScore = score
                bestMove = (move[0], move[1])
            board[move[0]][move[1]] = None

        return bestMove

    def minmax(self, depth, board: list[list[str | None]]) -> int | float:
        if self.checkWin(self.player, board):
            return depth - 10
        elif self.checkWin(self.ai, board):
            return 10 - depth
        elif self.checkTie(board):
            return 0
        
        best = float('-inf') if self.turn == self.ai else float('inf')

        for move in self.getAvailableMoves(board):
            board[move[0]][move[1]] = self.turn
            
            if self.turn == self.ai:
                self.turn = self.player
                best = max(best, self.minmax(depth + 1, board))
                self.turn = self.ai
            else:
                self.turn = self.ai
                best = min(best, self.minmax(depth + 1, board))
                self.turn = self.player
            
            board[move[0]][move[1]] = None

        return best
    
def printBoard(board: list[list[str | None]]) -> None:
    print(f"{"=" * 50}")
    for i in range(3):
        for j in range(3):
            if board[i][j]: print(f" {board[i][j]} ", end="")
            else: print(f" {i * 3 + j + 1} ", end="")
            print("|", end="")

        if i < 2:
            print("\n---+---+---")
        else:
            print()

def getMove(board: list[list[str | None]]) -> tuple[int, int]:
    while True:
        try:
            move = int(input("Choose a square: ")) - 1

            if not (0 <= move <= 8):
                raise ValueError
            
            i = move // 3
            j = move %  3

            if board[i][j]: raise ValueError

            return (i, j)

        except ValueError:
            printBoard(board)
            print("Please choose a valid square!")

def getChar() -> str:
    while True:
        try:
            char = input("Choose X or O: ")
            if char.upper() not in ("X", "O"):
                raise ValueError
            
            return char.upper()
        
        except ValueError:
            print("Please choose X or O!")

def main():
    playerChar = getChar()
    aiChar     = "X" if playerChar == "O" else "O"

    player = Players(aiChar, playerChar)
    ai = Ai(aiChar, playerChar)

    board = [[None for _ in range(3)] for _ in range(3)]

    for i in range(6):
        printBoard(board)

        if player.checkWin(player.player, board):
            print("You Won!")
            break
        elif ai.checkWin(ai.ai, board):
            print("You lost.")
            break
        elif player.checkTie(board):
            print("Tie.")
            break

        playerMove = getMove(board)
        board[playerMove[0]][playerMove[1]] = player.player

        if i == 4: continue

        aiMove = ai.aiPlay(board)
        board[aiMove[0]][aiMove[1]] = ai.ai

main()