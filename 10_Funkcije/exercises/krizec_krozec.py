"""Ustvarite program <b>Križci in Krožci.

Igralno polje lahko predstavite kot liste znotraj lista, kjer *E*
predstavlja prazno polje.

    board = [["X", "E", "E"],
             ["O", "E", "E"],
             ["E", "E", "E"]]

Od igralcev nato izmenično zahtevajte polje v katerega želijo
postaviti svoj znak. Privzememo lahko, da bodo igralci igrali
pravično in vpisovali samo prazna polja.
"""


def display_board(board):
    for row in board:
        print(row)


def make_move(on_turn, board):
    move = input(f"It's {on_turn}'s turn. Make a move (exp: 12): '")
    row = int(move[0])
    col = int(move[1])
    board[row][col] = on_turn


def is_game_over(board: list) -> bool:
    """Funkcija preveri, ali je igre konec."""
    # pregled po vrsticah
    for row in board:
        if row[0] != "E" and (row[0] == row[1] and row[0] == row[2]):
            return True
    # pregled po stolpcih
    for i in range(3):
        if board[0][i] != "E":
            if board[0][i] == board[1][i] and board[0][i] == board[2][i]:
                return True
    # pregled ene diagonale
    if board[0][0] != "E":
        if board[0][0] == board[1][1] and board[0][0] == board[2][2]:
            return True
    # pregled druge diagonale
    if board[0][2] != "E":
        if board[0][2] == board[1][1] and board[0][2] == board[2][0]:
            return True

    return False


def play():
    board = [["E", "E", "E"], ["E", "E", "E"], ["E", "E", "E"]]
    on_turn = "X"
    while True:
        display_board(board)
        make_move(on_turn, board)

        game_over = is_game_over(board)
        if game_over:
            print(f"{on_turn} je ZMAGOVALEC!")
            break
        else:
            if on_turn == "X":
                on_turn = "O"
            elif on_turn == "O":
                on_turn = "X"
        print()


if __name__ == "__main__":
    play()
