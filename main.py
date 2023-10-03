import wrdguessr as wg

game = wg.wordGuessr()
game.readScoreboardFile('scoreboard.txt')
game.startGame('words.txt')