from time import sleep
from os import system

"""
NOTE: If at any place there is a boolean True return anywhere,
where the boolean is not specified by a var name. Means the move is invalid else it is false.
"""


def MoveCorrectFormatChecker(input_move: str) -> bool:
    """Checks if the user entered move is in the correct format."""
    if not input_move or len(input_move) != 5:
        return False
    else:
        return (
            input_move[0] in "pnrbqk"
            and input_move[1] in "abcdefgh"
            and input_move[2] in "12345678"
            and input_move[3] in "abcdefgh"
            and input_move[4] in "12345678"
            and input_move[1:3] != input_move[3:5]
        )


def IsMovingToValidPlace(
    side: str,
    move_package: list[str, tuple[int, int], tuple[int, int]],
    gameboard: list[list[str]],
) -> bool:
    """Checks if the user is capturing a valid piece."""
    is_capturing_valid_piece = True
    _, _, end = move_package
    if side == "black":
        is_capturing_valid_piece = gameboard[end[0]][end[1]] in [
            "♟",
            "♞",
            "♜",
            "♝",
            "♛",
            " ",
        ]
    elif side == "white":
        is_capturing_valid_piece = gameboard[end[0]][end[1]] in [
            "♙",
            "♘",
            "♖",
            "♗",
            "♕",
            " ",
        ]
    return is_capturing_valid_piece


def FirstPieceGrabber(
    address: list[list[tuple[int, int]]], gameboard: list[list[str]]
) -> list[tuple[int, int]]:
    """Grabs the first piece form all 4 direction of axial/quadrantal address."""
    grabbed_pieces = []
    for sub_address in address:
        for index in sub_address:
            if gameboard[index[0]][index[1]] not in [" ", "♚", "♔"]:
                grabbed_pieces.append(index)
                break
    return grabbed_pieces


def PiecesHash() -> dict[dict[str]]:
    """General hash used by Moving class."""
    return {
        "p": {"white": "♟", "black": "♙"},
        "n": {"white": "♞", "black": "♘"},
        "r": {"white": "♜", "black": "♖"},
        "b": {"white": "♝", "black": "♗"},
        "q": {"white": "♛", "black": "♕"},
        "k": {"white": "♚", "black": "♔"},
    }


def CastlingHash() -> dict[dict[list[list[tuple[int, int]]]]]:
    """Castling hash used by Pieces class"""
    # The hash gives [(squares_to_check), (squares_to_modify)]
    return {
        "white": {
            "oo": [
                [(0, 5), (0, 6)],
                [(0, 4), (0, 6), (0, 7), (0, 5)],
            ],
            "ooo": [
                [(0, 3), (0, 2), (0, 1)],
                [(0, 4), (0, 2), (0, 0), (0, 3)],
            ],
        },
        "black": {
            "oo": [
                [(7, 5), (7, 6)],
                [(7, 4), (7, 6), (7, 7), (7, 5)],
            ],
            "ooo": [
                [(7, 3), (7, 2), (7, 1)],
                [(7, 4), (7, 2), (7, 0), (7, 3)],
            ],
        },
    }


class Boards:
    def __init__(self, gameboard: list[list[str]]) -> None:
        self.gameboard = gameboard

    def DrawBoard(self) -> None:
        """Updates the board by erasing the old one and printing a new one."""
        sleep(0.05)
        system("cls")
        print("    a   b   c   d   e   f   g   h")
        print("  +---+---+---+---+---+---+---+---+")
        for row_index in range(8):
            row = f"{row_index+1} |"
            for piece_index in range(8):
                row += f" {self.gameboard[row_index][piece_index]} |"
            print(row)
            print("  +---+---+---+---+---+---+---+---+")


class Address:
    def __init__(self, GAMEBOARD_ADDRESS: list[tuple[int, int]]) -> None:
        self.GAMEBOARD_ADDRESS = GAMEBOARD_ADDRESS

    def AddressFilter(
        self, address_to_filter: list[tuple[int, int]]
    ) -> list[tuple[int, int]]:
        """Filters the generally created address to only have addresses that are on the board."""
        return [
            elements
            for elements in address_to_filter
            if elements in self.GAMEBOARD_ADDRESS
        ]

    def PawnAddress(
        self, side: str, use: str, sq_index: tuple[int, int]
    ) -> list[tuple[int, int]]:
        """Crates addresses that a pawn can move to or attack from."""
        address = []
        if side == "black":
            if use == "capture":
                address = [
                    (sq_index[0] - 1, sq_index[1] - 1),
                    (sq_index[0] - 1, sq_index[1] + 1),
                ]
            elif use == "first_move":
                address = [
                    (sq_index[0] - 1, sq_index[1]),
                    (sq_index[0] - 2, sq_index[1]),
                ]
            elif use == "normal_move":
                address = [(sq_index[0] - 1, sq_index[1])]
        elif side == "white":
            if use == "capture":
                address = [
                    (sq_index[0] + 1, sq_index[1] - 1),
                    (sq_index[0] + 1, sq_index[1] + 1),
                ]
            elif use == "first_move":
                address = [
                    (sq_index[0] + 1, sq_index[1]),
                    (sq_index[0] + 2, sq_index[1]),
                ]
            elif use == "normal_move":
                address = [(sq_index[0] + 1, sq_index[1])]
        return self.AddressFilter(address_to_filter=address)

    def KnightAddress(self, sq_index: tuple[int, int]) -> list[tuple[int, int]]:
        """Crates addresses that a knight can move to or attack from."""
        address = [
            (sq_index[0] - 2, sq_index[1] - 1),
            (sq_index[0] - 2, sq_index[1] + 1),
            (sq_index[0] + 2, sq_index[1] - 1),
            (sq_index[0] + 2, sq_index[1] + 1),
            (sq_index[0] - 1, sq_index[1] - 2),
            (sq_index[0] + 1, sq_index[1] - 2),
            (sq_index[0] - 1, sq_index[1] + 2),
            (sq_index[0] + 1, sq_index[1] + 2),
        ]
        return self.AddressFilter(address_to_filter=address)

    def AxialAddress(self, sq_index: tuple[int, int]) -> list[list[tuple[int, int]]]:
        """Crates addresses that a rook/queen can move to or attack from."""
        # address[0]: Positive x-axis form provided sq_index.
        # address[1]: Negative x-axis form provided sq_index.
        # address[2]: Positive y-axis form provided sq_index.
        # address[3]: Negative y-axis form provided sq_index.
        address = [
            [(sq_index[0], sq_index[1] + move_right) for move_right in range(1, 8)],
            [(sq_index[0], sq_index[1] - move_left) for move_left in range(1, 8)],
            [(sq_index[0] - move_up, sq_index[1]) for move_up in range(1, 8)],
            [(sq_index[0] + move_down, sq_index[1]) for move_down in range(1, 8)],
        ]
        for index, sub_address in enumerate(address):
            address[index] = self.AddressFilter(address_to_filter=sub_address)
        return address

    def QuadrantalAddress(
        self, sq_index: tuple[int, int]
    ) -> list[list[tuple[int, int]]]:
        """Crates addresses that a bishop/queen can move to or attack from."""
        # address[0]: Quadrant-1 form provided sq_index.
        # address[1]: Quadrant-2 form provided sq_index.
        # address[2]: Quadrant-3 form provided sq_index.
        # address[3]: Quadrant-4 form provided sq_index.
        address = [
            [(sq_index[0] - step, sq_index[1] + step) for step in range(1, 8)],
            [(sq_index[0] - step, sq_index[1] - step) for step in range(1, 8)],
            [(sq_index[0] + step, sq_index[1] - step) for step in range(1, 8)],
            [(sq_index[0] + step, sq_index[1] + step) for step in range(1, 8)],
        ]
        for index, sub_address in enumerate(address):
            address[index] = self.AddressFilter(address_to_filter=sub_address)
        return address

    def KingAddress(self, sq_index: tuple[int, int]) -> list[tuple[int, int]]:
        """Crates addresses that a king can move to or attack from."""
        address = [
            (sq_index[0], sq_index[1] - 1),
            (sq_index[0], sq_index[1] + 1),
            (sq_index[0] - 1, sq_index[1]),
            (sq_index[0] + 1, sq_index[1]),
            (sq_index[0] - 1, sq_index[1] + 1),
            (sq_index[0] - 1, sq_index[1] - 1),
            (sq_index[0] + 1, sq_index[1] - 1),
            (sq_index[0] + 1, sq_index[1] + 1),
        ]
        return self.AddressFilter(address_to_filter=address)


class Attacked(Address):
    def __init__(
        self, gameboard: list[list[str]], GAMEBOARD_ADDRESS: list[tuple[int, int]]
    ) -> None:
        super().__init__(GAMEBOARD_ADDRESS)
        self.gameboard = gameboard
        self.white_king_location: tuple[int, int] = (0, 4)
        self.black_king_location: tuple[int, int] = (7, 4)

    def PawnOrKnightAttacking(self, side: str, sq_index: tuple[int, int]) -> bool:
        """Checks if the provided sq_index is attacked by pawn or knight."""
        is_attacked = False
        pawn_address = self.PawnAddress(side=side, use="capture", sq_index=sq_index)
        knight_address = self.KnightAddress(sq_index=sq_index)
        if side == "white":
            if any(
                self.gameboard[gameboard_index[0]][gameboard_index[1]] == "♙"
                for gameboard_index in pawn_address
            ) or any(
                self.gameboard[gameboard_index[0]][gameboard_index[1]] == "♘"
                for gameboard_index in knight_address
            ):
                is_attacked = True
        elif side == "black":
            if any(
                self.gameboard[gameboard_index[0]][gameboard_index[1]] == "♟"
                for gameboard_index in pawn_address
            ) or any(
                self.gameboard[gameboard_index[0]][gameboard_index[1]] == "♞"
                for gameboard_index in knight_address
            ):
                is_attacked = True
        return is_attacked

    def KingAttacking(self, side: str, sq_index: tuple[int, int]) -> bool:
        """Checks if the provided sq_index is attacked by king."""
        is_attacked = False
        king_address = self.KingAddress(sq_index=sq_index)
        if side == "white":
            if any(
                self.gameboard[gameboard_index[0]][gameboard_index[1]] == "♔"
                for gameboard_index in king_address
            ):
                is_attacked = True
        elif side == "black":
            if any(
                self.gameboard[gameboard_index[0]][gameboard_index[1]] == "♚"
                for gameboard_index in king_address
            ):
                is_attacked = True
        return is_attacked

    def SlidingPieceAttacking(self, side: str, sq_index: tuple[int, int]) -> bool:
        """Checks if the provided sq_index is attacked by rook or queen or bishop."""
        is_attacked = False
        axial_address = self.AxialAddress(sq_index=sq_index)
        quadrantal_address = self.QuadrantalAddress(sq_index=sq_index)
        axial_address = FirstPieceGrabber(
            address=axial_address, gameboard=self.gameboard
        )
        quadrantal_address = FirstPieceGrabber(
            address=quadrantal_address, gameboard=self.gameboard
        )
        if side == "white":
            if any(
                self.gameboard[gameboard_index[0]][gameboard_index[1]] in ["♕", "♖"]
                for gameboard_index in axial_address
            ) or any(
                self.gameboard[gameboard_index[0]][gameboard_index[1]] in ["♕", "♗"]
                for gameboard_index in quadrantal_address
            ):
                is_attacked = True
        elif side == "black":
            if any(
                self.gameboard[gameboard_index[0]][gameboard_index[1]] in ["♛", "♜"]
                for gameboard_index in axial_address
            ) or any(
                self.gameboard[gameboard_index[0]][gameboard_index[1]] in ["♛", "♝"]
                for gameboard_index in quadrantal_address
            ):
                is_attacked = True
        return is_attacked

    def IsKingAttacked(self, side: str) -> bool:
        """Checks if the king of the respective side is in check or not."""
        if side == "black":
            king_location = self.black_king_location
        elif side == "white":
            king_location = self.white_king_location
        return self.PawnOrKnightAttacking(
            side=side, sq_index=king_location
        ) or self.SlidingPieceAttacking(side=side, sq_index=king_location)


class PossibleMovesCreator(Attacked):
    def __init__(
        self, gameboard: list[list[str]], GAMEBOARD_ADDRESS: list[tuple[int, int]]
    ) -> None:
        super().__init__(gameboard, GAMEBOARD_ADDRESS)

    def UseCaseFinder(
        self, move_package: list[str, tuple[int, int], tuple[int, int]]
    ) -> str:
        """Finds the use case of a pawn move."""
        _, start, end = move_package
        use = None
        if (start[0] == 1 and end[0] == 3) or (start[0] == 6 and end[0] == 4):
            use = "first_move"
        elif (start[0] + 1 == end[0] or start[0] - 1 == end[0]) and (
            start[1] - 1 != end[1] and start[1] + 1 != end[1]
        ):
            use = "normal_move"
        elif start[0] + 1 == end[0] or start[0] - 1 == end[0]:
            use = "capture"
        return use

    def PawnsOrKnightsOrKingsMoveAddress(
        self, side: str, move_package: list[str, tuple[int, int], tuple[int, int]]
    ) -> list[tuple[int, int]]:
        """Makes move_address for pawns or knights or kings."""
        piece_notation, start, _ = move_package
        move_address = []
        if piece_notation == "p":
            use = self.UseCaseFinder(move_package=move_package)
            move_address = self.PawnAddress(side=side, use=use, sq_index=start)
        elif piece_notation == "n":
            move_address = self.KnightAddress(sq_index=start)
        elif piece_notation == "k":
            move_address = self.KingAddress(sq_index=start)
            for indices in move_address[:]:
                if (
                    self.PawnOrKnightAttacking(side=side, sq_index=indices)
                    or self.KingAttacking(side=side, sq_index=indices)
                    or self.SlidingPieceAttacking(side=side, sq_index=indices)
                ):
                    move_address.remove(indices)
        return move_address

    def SlidingPieceMoveAddress(
        self, move_package: list[str, tuple[int, int], tuple[int, int]]
    ) -> list[tuple[int, int]]:
        """Makes move_address for rook or bishop or queen."""
        piece_notation, start, end = move_package
        move_address = []
        if piece_notation == "r":
            move_address = self.AxialAddress(sq_index=start)
        elif piece_notation == "b":
            move_address = self.QuadrantalAddress(sq_index=start)
        elif piece_notation == "q":
            move_address = self.AxialAddress(sq_index=start)
            move_address.extend(self.QuadrantalAddress(sq_index=start))
        for sub_address in move_address:
            if end in sub_address:
                end_index = sub_address.index(end)
                move_address = sub_address[: end_index + 1]
                break
        return move_address


class Moving:
    def __init__(self, gameboard: list[list[str]]) -> None:
        """Initialization of variables."""
        self.gameboard = gameboard
        # Note: self.move_cache stores the data of the performed move [piece_moving, piece_captured/blank_square]
        self.move_cache: list[str, str] = []
        self.move_package: list[str, tuple[int, int], tuple[int, int]] = []
        self.piece_notation: str = ""
        self.start: str = ""
        self.end: str = ""

    def InputToMove(self, input_move: str) -> bool:
        """Converts the given input move into processable chunks.
        Returns True if move is invalid."""
        if not MoveCorrectFormatChecker(input_move=input_move):
            return True
        self.piece_notation = input_move[0]
        start = input_move[1:3]
        end = input_move[3:5]
        self.start = int(start[1]) - 1, ord(start[0]) - ord("a")
        self.end = int(end[1]) - 1, ord(end[0]) - ord("a")
        self.move_package = self.piece_notation, self.start, self.end
        return False

    def MovePiece(self, side: str) -> bool:
        # sourcery skip: class-extract-method
        """Moves the piece that user wants.
        Returns True if move is invalid."""
        PIECES_HASH = PiecesHash()
        piece_to_move = PIECES_HASH[self.piece_notation][side]
        if self.gameboard[self.start[0]][self.start[1]] != piece_to_move:
            return True
        self.move_cache = [piece_to_move, self.gameboard[self.end[0]][self.end[1]]]
        (
            self.gameboard[self.end[0]][self.end[1]],
            self.gameboard[self.start[0]][self.start[1]],
        ) = (piece_to_move, " ")
        return False

    def ReverseMove(self) -> bool:
        """Reverses the move for specific cases."""
        """Returns True as this indicates the move is invalid."""
        piece_moved, piece_moved_to = self.move_cache
        (
            self.gameboard[self.end[0]][self.end[1]],
            self.gameboard[self.start[0]][self.start[1]],
        ) = (piece_moved_to, piece_moved)
        return True

    def CastleMoving(self, squares_to_modify: list[tuple[int, int]]) -> None:
        """Performs the castling move."""
        king_initial, king_final, rook_initial, rook_final = squares_to_modify
        (
            self.gameboard[king_final[0]][king_final[1]],
            self.gameboard[king_initial[0]][king_initial[1]],
        ) = (self.gameboard[king_initial[0]][king_initial[1]], " ")
        (
            self.gameboard[rook_final[0]][rook_final[1]],
            self.gameboard[rook_initial[0]][rook_initial[1]],
        ) = (self.gameboard[rook_initial[0]][rook_initial[1]], " ")


class Pieces(PossibleMovesCreator, Moving):
    def __init__(
        self, gameboard: list[list[str]], GAMEBOARD_ADDRESS: list[tuple[int, int]]
    ) -> None:
        super().__init__(gameboard, GAMEBOARD_ADDRESS)
        self.white_short_castle: bool = True
        self.white_long_castle: bool = True
        self.black_short_castle: bool = True
        self.black_long_castle: bool = True

    def CastlingRightsCanceller(self, side: str) -> None:
        """Makes the castling invalid if either king or rook moves."""
        if side == "black":
            if self.piece_notation == "k":
                self.black_long_castle, self.black_short_castle = False, False
            elif self.piece_notation == "r":
                if self.start == (7, 0):
                    self.black_long_castle = False
                elif self.start == (7, 7):
                    self.black_short_castle = False
        elif side == "white":
            if self.piece_notation == "k":
                self.white_long_castle, self.white_short_castle = False, False
            elif self.piece_notation == "r":
                if self.start == (0, 0):
                    self.white_long_castle = False
                elif self.start == (0, 7):
                    self.white_short_castle = False

    def KingLocationUpdater(self, side: str, location_to_set: tuple[int, int]) -> None:
        """Updates the king location if the king is moved."""
        if self.piece_notation == "k":
            if side == "white":
                self.white_king_location = location_to_set
            elif side == "black":
                self.black_king_location = location_to_set

    def Promotion(self, side: str) -> None:
        """For promotion of a pawn."""
        PIECES_HASH = PiecesHash()
        if self.end[0] in [0, 7] and self.piece_notation == "p":
            what_to_promote_to = (
                input("What do you want to promote to: r/ n/ b/ q: ").strip().lower()
            )
            while what_to_promote_to not in ["r", "n", "b", "q"]:
                what_to_promote_to = (
                    input("Invalid selection: r/ n/ b/ q: ").strip().lower()
                )
            self.gameboard[self.end[0]][self.end[1]] = PIECES_HASH[what_to_promote_to][
                side
            ]

    def SingleSquareMovingPieces(self, side: str, input_move: str) -> bool:
        """Controls everything related to pawns or knights or kings."""
        """Returns True if the move is invalid in some way."""
        if self.InputToMove(input_move=input_move):
            return True
        move_address = self.PawnsOrKnightsOrKingsMoveAddress(
            side=side, move_package=self.move_package
        )
        if self.end not in move_address:
            return True
        if (
            self.piece_notation == "p"
            and self.gameboard[self.end[0]][self.end[1]] == " "
        ):
            for iterator in move_address:
                if self.gameboard[iterator[0]][iterator[1]] != " ":
                    return True
        if not (
            IsMovingToValidPlace(
                side=side, move_package=self.move_package, gameboard=self.gameboard
            )
        ):
            return True
        if self.MovePiece(side=side):
            return True
        self.KingLocationUpdater(side=side, location_to_set=self.end)
        if self.IsKingAttacked(side=side):
            self.KingLocationUpdater(side=side, location_to_set=self.start)
            return self.ReverseMove()
        self.Promotion(side=side)
        self.CastlingRightsCanceller(side=side)
        return False

    def SlidingPieces(self, side: str, input_move: str) -> bool:
        """Controls everything related to rooks or bishops or queens."""
        """Returns True if the move is invalid in some way."""
        if self.InputToMove(input_move=input_move):
            return True
        move_address = self.SlidingPieceMoveAddress(move_package=self.move_package)
        if self.end not in move_address:
            return True
        if self.gameboard[self.end[0]][self.end[1]] == " ":
            for iterator in move_address:
                if self.gameboard[iterator[0]][iterator[1]] != " ":
                    return True
        else:
            if not IsMovingToValidPlace(
                side=side, move_package=self.move_package, gameboard=self.gameboard
            ):
                return True
            for iterator in move_address[:-1]:
                if self.gameboard[iterator[0]][iterator[1]] != " ":
                    return True
        if self.MovePiece(side=side):
            return True
        if self.IsKingAttacked(side=side):
            return self.ReverseMove()
        self.CastlingRightsCanceller(side=side)
        return False

    def Castling(self, side: str, input_move: str) -> bool:
        """Controls everything related to castling."""
        """Returns True if the move is invalid in some way."""
        if not self.IsKingAttacked(side=side):
            return True
        CASTLING_RIGHTS_HASH = {
            "white": {"oo": "white_short_castle", "ooo": "white_long_castle"},
            "black": {"oo": "black_short_castle", "ooo": "black_long_castle"},
        }
        if not getattr(self, CASTLING_RIGHTS_HASH[side][input_move]):
            return True
        CASTLING_HASH = CastlingHash()
        squares_to_check, squares_to_modify = CASTLING_HASH[side][input_move]
        for iterator in squares_to_check:
            if (
                self.PawnOrKnightAttacking(side=side, sq_index=iterator)
                or self.SlidingPieceAttacking(side=side, sq_index=iterator)
                or self.KingAttacking(side=side, sq_index=iterator)
                or self.gameboard[iterator[0]][iterator[1]] != " "
            ):
                return True
        self.CastleMoving(squares_to_modify=squares_to_modify)
        if side == "black":
            self.black_long_castle, self.black_short_castle = False, False
        elif side == "white":
            self.white_long_castle, self.white_short_castle = False, False
        return False

    def PiecesCalling(self, side: str, input_move: str) -> bool:
        if (
            not input_move
            or input_move[0] not in "pnk"
            and input_move[0] not in "rbq"
            and input_move not in ["ooo", "oo"]
        ):
            return True
        elif input_move[0] in "pnk":
            return self.SingleSquareMovingPieces(side=side, input_move=input_move)
        elif input_move[0] in "rbq":
            return self.SlidingPieces(side=side, input_move=input_move)
        else:
            return self.Castling(side=side, input_move=input_move)


class Main(Pieces, Boards):
    def __init__(self) -> None:
        self.gameboard = [
            ["♜", "♞", "♝", "♛", "♚", "♝", "♞", "♜"],
            ["♟", "♟", "♟", "♟", "♟", "♟", "♟", "♟"],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            ["♙", "♙", "♙", "♙", "♙", "♙", "♙", "♙"],
            ["♖", "♘", "♗", "♕", "♔", "♗", "♘", "♖"],
        ]
        self.GAMEBOARD_ADDRESS = [(row, col) for row in range(8) for col in range(8)]
        super().__init__(self.gameboard, self.GAMEBOARD_ADDRESS)

    def GameLoop(self) -> None:
        self.DrawBoard()
        while True:
            white_move = input("White's move: ").strip().lower()
            terminator = self.PiecesCalling(side="white", input_move=white_move)
            while terminator is True:
                white_move = input("Invalid move, Try Again: ").strip().lower()
                terminator = self.PiecesCalling(side="white", input_move=white_move)
            self.DrawBoard()
            black_move = input("Black's move: ").strip().lower()
            terminator = self.PiecesCalling(side="black", input_move=black_move)
            while terminator is True:
                black_move = input("Invalid move, Try Again: ").strip().lower()
                terminator = self.PiecesCalling(side="black", input_move=black_move)
            self.DrawBoard()
