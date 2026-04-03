class Ai {
    constructor(ai, player, game) {
        this.ai = ai;
        this.player = player;
        this.game = game;
    }

    getAvailableMoves(board) {
        let availableMoves = [];
        for (let i = 0; i < 9; i++) {
            if (!(board[i])) {
                availableMoves.push(i);
            }
        }
        return availableMoves;
    }

    aiPlay(board) {
        let availableMoves = this.getAvailableMoves(board);
        let bestScore = Number.NEGATIVE_INFINITY;
        let bestMove = availableMoves[0];

        for (const move of availableMoves) {
            board[move] = this.ai;
            let score = this.minmax(0, board, this.player);
            if (score > bestScore) {
                bestScore = score;
                bestMove = move;
            }
            board[move] = null;
        }

        return bestMove;
    }

    minmax(depth, board, turn) {
        if (this.game.checkWin(this.player)) {
            return depth - 10;
        } else if (this.game.checkWin(this.ai)) {
            return 10 - depth;
        } else if (this.game.checkTie()) {
            return 0;
        }

        let best = turn === this.ai ? Number.NEGATIVE_INFINITY : Number.POSITIVE_INFINITY;

        let availableMoves = this.getAvailableMoves(board);
        for (const move of availableMoves) {
            board[move] = turn;

            if (turn === this.ai) {
                best = Math.max(best, this.minmax(depth + 1, board, this.player));
            } else {
                best = Math.min(best, this.minmax(depth + 1, board, this.ai));
            }

            board[move] = null;
        }

        return best;
    }
};

class Game {
    constructor() {
        this.board = Array(9).fill(null);
        this.winningPositions = [
            [0, 1, 2], 
            [3, 4, 5], 
            [6, 7, 8], 
            [0, 3, 6], 
            [1, 4, 7], 
            [2, 5, 8], 
            [0, 4, 8], 
            [2, 4, 6]  
        ];
    }

    checkWin(player) {
        return this.winningPositions.some(winningPosition => winningPosition.every(i => this.board[i] === player));
    }
    
    checkTie() {
        return this.board.every(square => square !== null);
    }

    checkEndGame(ai) {
        if (this.checkWin("O")) {
            this.printBoard(ai);
            alert("You lost.");
            return;
        } else if (this.checkWin("X")) {
            this.printBoard(ai);
            alert("You won!");
            return;
        } else if (this.checkTie()) {
            this.printBoard(ai);
            alert("Tie.");
            return;
        }
    }
    
    printBoard(ai) {    
        const gameBox = document.getElementById("game");
        gameBox.innerHTML = "";
        for (let i = 0; i < 9; i++) {
    
                let div = document.createElement("div");
                div.classList.add("square");

                if (this.board[i]) {
                    div.textContent = this.board[i];
                } else {
                    div.textContent = i + 1;
                }
    
                gameBox.appendChild(div);
    
            if (i % 3 === 2 && i < 6) {
                let hr = document.createElement("hr");
                gameBox.appendChild(hr);
            }

            div.addEventListener("click", () => {
                if (this.checkWin("X") || this.checkWin("O") || this.checkTie()) {
                    this.printBoard(ai);
                    return;
                }

                if (this.board[i] !== null) return;

                this.board[i] = "X";

                if (this.checkWin("X") || this.checkWin("O") || this.checkTie()) {
                    this.printBoard(ai);
                    this.checkEndGame(ai);
                    return;
                }

                let move;

                if (randInt(1, 3) !== 2) {
                    move = ai.aiPlay(this.board);
                } else {
                    let availableMoves = ai.getAvailableMoves(this.board);
                    if (availableMoves.length === 0) return;

                    let randomInt = randInt(0, availableMoves.length - 1);
                    move = availableMoves[randomInt];
                }
                if (move !== undefined) {
                    this.board[move] = "O";
                }

                this.printBoard(ai);
            });
        }
    }
}

function randInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

let game = new Game();
let ai = new Ai("O", "X", game);

game.printBoard(ai);