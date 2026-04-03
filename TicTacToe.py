#XOproject: VERY Updated
class Ai:
    def __init__(self, AI: str, player: str) -> None:
        self.ai: str = AI
        self.player: str = player
        self.turn: str = player

    # TODO: I dont like how this works
    def getAvailableMoves(self, board: list[str | None]) -> list[int]:
        availableMoves = []
        for i in range(3):
            for j in range(3):
                if not board[i * 3 + j]:
                    availableMoves.append(i * 3 + j)
        return availableMoves

    def aiPlay(self, board: list[str | None]) -> int:
        availableMoves = self.getAvailableMoves(board)

        bestScore = float('-inf')
        bestMove = None
        
        for move in availableMoves:
            board[move] = self.ai
            score = self.minmax(0, board)
            if score > bestScore:
                bestScore = score
                bestMove = move
            board[move] = None

        return bestMove

    def minmax(self, depth, board: list[str | None]) -> int | float:
        if checkWin(self.player, board):
            return depth - 10
        elif checkWin(self.ai, board):
            return 10 - depth
        elif checkTie(board):
            return 0
        
        best = float('-inf') if self.turn == self.ai else float('inf')

        for move in self.getAvailableMoves(board):
            board[move] = self.turn
            
            if self.turn == self.ai:
                self.turn = self.player
                best = max(best, self.minmax(depth + 1, board))
                self.turn = self.ai
            else:
                self.turn = self.ai
                best = min(best, self.minmax(depth + 1, board))
                self.turn = self.player
            
            board[move] = None

        return best
    
def checkWin(player: str, board: list[str | None]) -> bool:
    for i in range(3):
        if all([board[i * 3 + j] == player for j in range(3)]): return True # horizontal positions
        if all([board[j * 3 + i] == player for j in range(3)]): return True # vertical positions
    if all([board[i * 3 + i]     == player for i in range(3)]): return True # diagonal from left positions
    if all([board[i * 3 + 2 - i] == player for i in range(3)]): return True # diagonal from right positions
    
    return False

def checkTie(board: list[str | None]) -> bool:
    for i in range(3):
        for j in range(3):
            if not board[i * 3 + j]: return False
    return True
    
def printBoard(board: list[str | None]) -> None:
    print(f"{"=" * 50}")
    for i in range(3):
        for j in range(3):
            if board[i * 3 + j]: print(f" {board[i * 3 + j]} ", end="")
            else: print(f" {i * 3 + j + 1} ", end="")
            print("|", end="")

        if i < 2:
            print("\n---+---+---")
        else:
            print()

def getMove(board: list[str | None]) -> int:
    while True:
        try:
            move = int(input("Choose a square: ")) - 1

            if not (0 <= move <= 8):
                raise ValueError

            if board[move]: raise ValueError

            return move

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

    ai = Ai(aiChar, playerChar)

    board = [None for _ in range(9)]

    for i in range(6):
        printBoard(board)

        if checkWin(playerChar, board):
            print("You Won!")
            break
        elif checkWin(aiChar, board):
            print("You lost.")
            break
        elif checkTie(board):
            print("Tie.")
            break

        playerMove = getMove(board)
        board[playerMove] = playerChar

        if i == 4: continue

        aiMove = ai.aiPlay(board)
        board[aiMove] = aiChar
        print(f"The Ai chose square {aiMove}")

main()