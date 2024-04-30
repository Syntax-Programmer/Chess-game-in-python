from typing import Literal
from os import system
from time import sleep


def AddressFilter(address_to_filter: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """Filters the provided address to only have valid usable entries."""
    return [
        indices
        for indices in address_to_filter
        if 0 <= indices[0] <= 7 and 0 <= indices[1] <= 7
    ]


def PawnAddress(
    side: Literal["W", "B"], use: Literal["FM", "NM", "C"], sq_index: tuple[int, int]
) -> list[tuple[int, int]]:
    """
    Gives the addresses form which a pawn can attack from, can move to.
    "W": White, "B": Black
    "FM": First move, "NM": Normal move, "C": Capture move
    """
    sign_convention = -1 if side == "B" else 1
    if use == "FM":
        address = [
            (sq_index[0] + (forward_step * sign_convention), sq_index[1])
            for forward_step in (1, 2)
        ]
    elif use == "NM":
        address = [(sq_index[0] + (1 * sign_convention), sq_index[1])]
    elif use == "C":
        address = [
            (sq_index[0] + (1 * sign_convention), sq_index[1] + sideways_step)
            for sideways_step in (1, -1)
        ]
    else:
        return []
    return AddressFilter(address_to_filter=address)


def KnightAddress(sq_index: tuple[int, int]) -> list[tuple[int, int]]:
    """Gives  the addresses form which a knight can attack from, can move to."""
    address = [
        (sq_index[0] + 2, sq_index[1] + 1),
        (sq_index[0] + 2, sq_index[1] - 1),
        (sq_index[0] - 2, sq_index[1] + 1),
        (sq_index[0] - 2, sq_index[1] - 1),
        (sq_index[0] + 1, sq_index[1] + 2),
        (sq_index[0] - 1, sq_index[1] + 2),
        (sq_index[0] + 1, sq_index[1] - 2),
        (sq_index[0] - 1, sq_index[1] - 2),
    ]
    return AddressFilter(address_to_filter=address)


def KingAddress(sq_index: tuple[int, int]) -> list[tuple[int, int]]:
    """Gives  the addresses form which a king can attack from, can move to."""
    address = [
        (sq_index[0], sq_index[1] + 1),
        (sq_index[0], sq_index[1] - 1),
        (sq_index[0] - 1, sq_index[1]),
        (sq_index[0] + 1, sq_index[1]),
        (sq_index[0] - 1, sq_index[1] + 1),
        (sq_index[0] - 1, sq_index[1] - 1),
        (sq_index[0] + 1, sq_index[1] - 1),
        (sq_index[0] + 1, sq_index[1] + 1),
    ]
    return AddressFilter(address_to_filter=address)


def AxialAddress(sq_index: tuple[int, int]) -> list[tuple[int, int]]:
    """Gives  the addresses form which a rook/queen can attack from, can move to.

    address[0]: +x - axis
    address[1]: -x - axis
    address[2]: +y - axis
    address[3]: -y - axis
    From the provided sq_index.
    """
    address = [
        [(sq_index[0], sq_index[1] + right_step) for right_step in range(1, 8)],
        [(sq_index[0], sq_index[1] - left_step) for left_step in range(1, 8)],
        [(sq_index[0] - up_step, sq_index[1]) for up_step in range(1, 8)],
        [(sq_index[0] + down_step, sq_index[1]) for down_step in range(1, 8)],
    ]
    for place, sub_address in enumerate(address):
        address[place] = AddressFilter(address_to_filter=sub_address)
    return address


def QuadrantalAddress(sq_index: tuple[int, int]) -> list[tuple[int, int]]:
    """Gives  the addresses form which a rook/queen can attack from, can move to.

    address[0]: Quad-1
    address[1]: Quad-2
    address[2]: Quad-3
    address[3]: Quad-4
    From the provided sq_index."""
    address = [
        [(sq_index[0] - step, sq_index[1] + step) for step in range(1, 8)],
        [(sq_index[0] - step, sq_index[1] - step) for step in range(1, 8)],
        [(sq_index[0] + step, sq_index[1] - step) for step in range(1, 8)],
        [(sq_index[0] + step, sq_index[1] + step) for step in range(1, 8)],
    ]
    for place, sub_address in enumerate(address):
        address[place] = AddressFilter(address_to_filter=sub_address)
    return address


def ValidSquaresToMoveTo(side: Literal["W", "B"]) -> list[str]:
    """Gives what all squares a piece can move to."""
    return (
        ["♟", "♜", "♞", "♝", "♛", " "]
        if side == "B"
        else ["♙", "♖", "♘", "♗", "♕", " "]
    )


def SameSidePieces(side: Literal["W", "B"]) -> list[str]:
    """GIves pieces of the same side."""
    return (
        ["♟", "♚", "♞", "♝", "♛", "♜"]
        if side == "W"
        else ["♙", "♘", "♔", "♗", "♕", "♖"]
    )


class Attacked:
    """Checks if a square/king is attacked by an opponent piece."""

    """Returns True if the provided squares is attacked by the piece in the scope of the function."""

    # Defining the king function separate from the pawns and knights function as king can't attack kings.
    def __init__(self, board: list[list[str]]) -> None:
        self.board = board
        self.white_king_location = (0, 4)
        self.black_king_location = (7, 4)

    def AttackedByPawnsKnights(
        self, side: Literal["W", "B"], sq_index: tuple[int, int]
    ) -> bool:
        "Check if the provided sq_index is attacked by piece specified by the function."
        from_knight_attacking = KnightAddress(sq_index=sq_index)
        from_pawn_attacking = PawnAddress(side=side, use="C", sq_index=sq_index)
        pieces_to_check_for = (
            ["♙", "♘"] if side == "W" else ["♟", "♞"]
        )  # Pieces that can attack.
        # Returns boolean for attacked or not.
        return any(
            self.board[indices[0]][indices[1]] == pieces_to_check_for[0]
            for indices in from_pawn_attacking
        ) or any(
            self.board[indices[0]][indices[1]] == pieces_to_check_for[1]
            for indices in from_knight_attacking
        )

    def AttackedByKing(
        self, side: Literal["W", "B"], sq_index: tuple[int, int]
    ) -> bool:
        "Check if the provided sq_index is attacked by piece specified by the function."
        from_king_attacking = KingAddress(sq_index=sq_index)
        piece_to_check_for = "♔" if side == "W" else "♚"  # Pieces that can attack.
        # Returns boolean for attacked or not.
        return any(
            self.board[indices[0]][indices[1]] == piece_to_check_for
            for indices in from_king_attacking
        )

    def AttackedBySlidingPieces(
        self, side: Literal["W", "B"], sq_index: tuple[int, int]
    ) -> bool:
        "Check if the provided sq_index is attacked by piece specified by the function."

        def FirstPieceGrabber(
            address_to_parse: list[list[tuple[int, int]]]
        ) -> list[tuple[int, int]]:
            """Grabs the first pieces form the 4 sub addresses of sliding pieces."""
            parsed_address = []
            for sub_address in address_to_parse:
                for indices in sub_address:
                    if self.board[indices[0]][indices[1]] not in ["♔", "♚", " "]:
                        parsed_address.append(indices)
                        break
            return parsed_address

        # Grabbing the first pieces from all 4 directions and diagonals to check for attacking pieces within them.
        axial_address = FirstPieceGrabber(
            address_to_parse=AxialAddress(sq_index=sq_index)
        )
        quadrantal_address = FirstPieceGrabber(
            address_to_parse=QuadrantalAddress(sq_index=sq_index)
        )
        pieces_to_check_for = (
            ["♖", "♕", "♗"] if side == "W" else ["♜", "♛", "♝"]
        )  # Pieces that can attack.
        # Returns boolean for attacked or not.
        return any(
            self.board[indices[0]][indices[1]] in pieces_to_check_for[:2]
            for indices in axial_address
        ) or any(
            self.board[indices[0]][indices[1]] in pieces_to_check_for[1:]
            for indices in quadrantal_address
        )

    def IsKingAttacked(self, side: Literal["W", "B"]) -> bool:
        """Checks if the king of the provided side is attacked by a piece or not."""
        king_location = (
            self.white_king_location if side == "W" else self.black_king_location
        )
        return self.AttackedByPawnsKnights(
            side=side, sq_index=king_location
        ) or self.AttackedBySlidingPieces(side=side, sq_index=king_location)


class MoveAddress(Attacked):
    def __init__(self, board: list[list[str]]) -> None:
        super().__init__(board)

    def PawnsKnightsKingsMoveAddress(
        self, side: Literal["W", "B"], start: tuple[int, int], end: tuple[int, int]
    ) -> list[tuple[int, int]]:
        """Creates addresses for a move of pawn/knight/king."""

        def PawnMoveUseFinder(
            start: tuple[int, int], end: tuple[int, int]
        ) -> Literal["FM", "NM", "C"]:
            """Finds the use parameter for the PawnAddress function to be used."""
            sign_convention = -1 if side == "B" else 1
            use = ""
            if (start[0] == 1 and end[0] == 3) or (start[0] == 6 and end[0] == 4):
                use = "FM"
            elif (
                start[0] + (1 * sign_convention) == end[0]
                and start[1] + 1 != end[1]
                and start[1] - 1 != end[1]
            ):
                use = "NM"
            elif start[0] + (1 * sign_convention) == end[0] and (
                start[1] + 1 == end[1] or start[1] - 1 == end[1]
            ):
                use = "C"
            return use

        move_address = []
        if self.board[start[0]][start[1]] in ["♟", "♙"]:
            move_address = PawnAddress(
                side=side, use=PawnMoveUseFinder(start=start, end=end), sq_index=start
            )
        elif self.board[start[0]][start[1]] in ["♞", "♘"]:
            move_address = KnightAddress(sq_index=start)
        elif self.board[start[0]][start[1]] in ["♚", "♔"]:
            move_address = KingAddress(sq_index=start)
            for indices in move_address[:]:
                if (
                    self.AttackedByKing(side=side, sq_index=indices)
                    or self.AttackedByPawnsKnights(side=side, sq_index=indices)
                    or self.AttackedBySlidingPieces(side=side, sq_index=indices)
                ):
                    move_address.remove(indices)
        return move_address

    def SlidingPiecesMoveAddress(
        self, start: tuple[int, int], end: tuple[int, int]
    ) -> list[tuple[int, int]]:
        """Creates addresses for a move of sliding pieces."""
        move_address = []
        if self.board[start[0]][start[1]] in ["♜", "♖"]:
            move_address = AxialAddress(sq_index=start)
        elif self.board[start[0]][start[1]] in ["♝", "♗"]:
            move_address = QuadrantalAddress(sq_index=start)
        elif self.board[start[0]][start[1]] in ["♛", "♕"]:
            move_address = QuadrantalAddress(sq_index=start)
            move_address.extend(AxialAddress(sq_index=start))
        for sub_address in move_address:
            if end in sub_address:
                index_of_end = sub_address.index(end)
                move_address = sub_address[: index_of_end + 1]
        return move_address


class Moving:
    def __init__(self, board: list[list[str]]) -> None:
        self.board = board
        self.start = ()
        self.end = ()
        self.performed_move_cache = ()

    def InputToMove(self, input_move: str) -> None:
        """Converts the user input into indices referenced to the board."""
        if input_move == "ooo":
            self.start = self.end = -1
            return
        elif input_move == "oo":
            self.start = self.end = -2
            return
        start = input_move[:2]
        end = input_move[2:]
        self.start = int(start[1]) - 1, ord(start[0]) - ord("a")
        self.end = int(end[1]) - 1, ord(end[0]) - ord("a")

    def MovePerformer(self) -> None:
        """Moves the pieces on the board."""
        self.performed_move_cache = (
            self.board[self.start[0]][self.start[1]],
            self.board[self.end[0]][self.end[1]],
        )  # Caches the squares changed during the move.
        self.board[self.end[0]][self.end[1]] = self.board[self.start[0]][self.start[1]]
        self.board[self.start[0]][self.start[1]] = " "

    def CastlePerformer(self, sq_to_modify: list[tuple[int, int]]) -> None:
        """Performs the castling move."""
        king_initial, king_final, rook_initial, rook_final = sq_to_modify
        self.board[king_final[0]][king_final[1]] = self.board[king_initial[0]][
            king_initial[1]
        ]
        self.board[king_initial[0]][king_initial[1]] = " "
        self.board[rook_final[0]][rook_final[1]] = self.board[rook_initial[0]][
            rook_initial[1]
        ]
        self.board[rook_initial[0]][rook_initial[1]] = " "

    def MoveReverser(self) -> None:
        """Reverses the already performed move."""
        # Unpack the cache into the board.
        (
            self.board[self.start[0]][self.start[1]],
            self.board[self.end[0]][self.end[1]],
        ) = self.performed_move_cache


class Pieces(MoveAddress, Moving):
    def __init__(self, board: list[list[str]]) -> None:
        self.white_short_castle = True
        self.white_long_castle = True
        self.black_short_castle = True
        self.black_long_castle = True
        # Data consist of [[squares to check], [squares to modify]].
        self.CASTLING_DATA = {
            "W": {
                "-1": [[(0, 3), (0, 2)], [(0, 4), (0, 2), (0, 0), (0, 3)]],
                "-2": [[(0, 5), (0, 6)], [(0, 4), (0, 6), (0, 7), (0, 5)]],
            },
            "B": {
                "-1": [[(7, 3), (7, 2)], [(7, 4), (7, 2), (7, 0), (7, 3)]],
                "-2": [[(7, 5), (7, 6)], [(7, 4), (7, 6), (7, 7), (7, 5)]],
            },
        }
        super().__init__(board)

    def CastlingRightsManager(self, side: Literal["W", "B"]) -> None:
        """Sets rights to false if a king/rook is moved."""
        if side == "W":
            if self.start in [-1, -2] or (
                self.start == (0, 4) and self.board[self.end[0]][self.end[1]] == "♚"
            ):
                self.white_long_castle = self.white_short_castle = False
            elif self.start == (0, 0) and self.board[self.end[0]][self.end[1]] == "♜":
                self.white_long_castle = False
            elif self.start == (0, 7) and self.board[self.end[0]][self.end[1]] == "♜":
                self.white_short_castle = False
        if side == "B":
            if self.start in [-1, -2] or (
                self.start == (7, 4) and self.board[self.end[0]][self.end[1]] == "♔"
            ):
                self.black_long_castle = self.black_short_castle = False
            elif self.start == (7, 0) and self.board[self.end[0]][self.end[1]] == "♖":
                self.black_long_castle = False
            elif self.start == (7, 7) and self.board[self.end[0]][self.end[1]] == "♖":
                self.black_short_castle = False

    def PawnsKnightsKings(self, side: Literal["W", "B"]) -> bool:
        """Handles everything related to pawns/knights/kings."""

        def KingLocationUpdater(
            side: Literal["W", "B"], location_to_set_to: tuple[int, int]
        ) -> None:
            if self.board[self.start[0]][self.start[1]] not in ["♔", "♚"]:
                return
            if side == "W":
                self.white_king_location = location_to_set_to
            elif side == "B":
                self.black_king_location = location_to_set_to

        def Promotion(side: Literal["W", "B"]) -> None:
            """Check for and performs the promotion of a pawn"""
            same_side_pieces = SameSidePieces(side=side)
            piece_dict = {"n": 2, "b": 3, "q": 4, "r": 5}
            if self.end[0] in [7, 0] and self.board[self.end[0]][self.end[1]] in [
                "♟",
                "♙",
            ]:
                while True:
                    what_to_promote_to = input("What to promote to n/b/q/r : ").lower()
                    if (
                        not what_to_promote_to
                        or len(what_to_promote_to) != 1
                        or what_to_promote_to not in "qrbn"
                    ):
                        print("Please enter valid input for promotion.")
                        continue
                    else:
                        self.board[self.end[0]][self.end[1]] = same_side_pieces[
                            piece_dict.get(what_to_promote_to)
                        ]
                        break

        move_address = self.PawnsKnightsKingsMoveAddress(
            side=side, start=self.start, end=self.end
        )
        if (
            self.board[self.start[0]][self.start[1]]
            not in SameSidePieces(side=side)[:3]
        ):
            print("Select a valid piece to move")
            return False
        if self.end not in move_address:
            print("The entered move is not possible.")
            return False
        if (
            self.start[1] == self.end[1]
            and self.board[self.start[0]][self.start[1]] in ["♟", "♙"]
            and any(
                self.board[indices[0]][indices[1]] != " " for indices in move_address
            )
        ):
            print("Pawn's way is blocked.")
            return False
        if self.board[self.end[0]][self.end[1]] not in ValidSquaresToMoveTo(side=side):
            print("Friendly fire is not permitted under SOVIET LAW.")
            return False
        KingLocationUpdater(side=side, location_to_set_to=self.end)
        self.MovePerformer()
        if self.IsKingAttacked(side=side):
            print("Check after you king.")
            self.MoveReverser()
            return False
        self.CastlingRightsManager(side=side)
        Promotion(side=side)
        return True

    def SlidingPieces(self, side: Literal["W", "B"]) -> bool:
        """Handles everything related to sliding pieces."""
        move_address = self.SlidingPiecesMoveAddress(start=self.start, end=self.end)
        if (
            self.board[self.start[0]][self.start[1]]
            not in SameSidePieces(side=side)[3:]
        ):
            print("Select a valid piece to move")
            return False
        if self.end not in move_address:
            print("The entered move is not possible.")
            return False
        if self.board[self.end[0]][self.end[1]] not in ValidSquaresToMoveTo(side=side):
            print("Friendly fire is not permitted under SOVIET LAW.")
            return False
        if any(
            self.board[indices[0]][indices[1]] != " " for indices in move_address[:-1]
        ):
            print("Piece's path is blocked.")
            return False
        self.MovePerformer()
        if self.IsKingAttacked(side=side):
            print("Check after you king.")
            self.MoveReverser()
            return False
        self.CastlingRightsManager(side=side)
        return True

    def Castling(self, side: Literal["W", "B"]) -> bool:
        """Handles everything related to castling."""

        def CastlingRightsChecker(side: Literal["W", "B"]) -> bool:
            """Returns the castling rights referenced for that particular castle."""
            if side == "W":
                if self.start == -1:
                    return self.white_long_castle
                elif self.start == -2:
                    return self.white_short_castle
            if side == "B":
                if self.start == -1:
                    return self.black_long_castle
                elif self.start == -2:
                    return self.black_short_castle

        if self.IsKingAttacked(side=side):
            print("Can't castle if your king is attacked.")
            return False
        sq_to_check, sq_to_modify = self.CASTLING_DATA.get(side).get(str(self.start))
        if any(self.board[indices[0]][indices[1]] != " " for indices in sq_to_check):
            print("Way toward castling is blocked.")
            return False
        for indices in sq_to_check:
            if (
                self.AttackedByKing(side=side, sq_index=indices)
                or self.AttackedByPawnsKnights(side=side, sq_index=indices)
                or self.AttackedBySlidingPieces(side=side, sq_index=indices)
            ):
                print("Can't castle if the squares in between are attacked.")
                return False
        if not CastlingRightsChecker(side=side):
            print("The king/ rook have been moved before the castling move.")
            return False
        self.CastlePerformer(sq_to_modify=sq_to_modify)
        self.CastlingRightsManager(side=side)
        return True


class Main(Pieces):
    def __init__(self) -> None:
        self.board = [
            ["♜", "♞", "♝", "♛", "♚", "♝", "♞", "♜"],
            ["♟", "♟", "♟", "♟", "♟", "♟", "♟", "♟"],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            ["♙", "♙", "♙", "♙", "♙", "♙", "♙", "♙"],
            ["♖", "♘", "♗", "♕", "♔", "♗", "♘", "♖"],
        ]
        super().__init__(board=self.board)

    def DrawBoard(self) -> None:
        """Draws and updates the chess board."""
        sleep(0.05)
        system("cls")
        print("   a   b   c   d   e   f   g   h")
        print("  +---+---+---+---+---+---+---+---+")
        for row_index in range(8):
            row = f"{row_index+1} |"
            for piece_index in range(8):
                row += f" {self.board[row_index][piece_index]} |"
            print(row)
            print("  +---+---+---+---+---+---+---+---+")

    def PieceCalling(self, side: Literal["W", "B"], input_move: str) -> bool:
        """Calls the appropriate pieces according to the user request."""

        def FormatValidityChecker(input_move: str) -> bool:
            """Checks if the user inputted move is valid."""
            if (not input_move or len(input_move) != 4) and input_move not in [
                "ooo",
                "oo",
            ]:
                return False
            return (
                input_move[0] in "abcdefgh"
                and input_move[1] in "12345678"
                and input_move[2] in "abcdefgh"
                and input_move[3] in "12345678"
                and input_move[:2] != input_move[2:]
            ) or input_move in ["ooo", "oo"]

        if not FormatValidityChecker(input_move=input_move):
            print("Consider feeding us the in the right format?")
            return False
        self.InputToMove(input_move=input_move)
        if self.start == self.end in [-1, -2]:
            return self.Castling(side=side)
        elif self.board[self.start[0]][self.start[1]] in ["♟", "♙", "♞", "♘", "♚", "♔"]:
            return self.PawnsKnightsKings(side=side)
        elif self.board[self.start[0]][self.start[1]] in ["♜", "♖", "♝", "♗", "♛", "♕"]:
            return self.SlidingPieces(side=side)

    def GameLoop(self) -> None:
        """The main game loop."""
        self.DrawBoard()
        running = True
        while running:
            white_move = input("White's move: ").lower()
            while not self.PieceCalling(side="W", input_move=white_move):
                white_move = input("White's move: ").lower()
            self.DrawBoard()
            black_move = input("Black's move: ").lower()
            while not self.PieceCalling(side="B", input_move=black_move):
                black_move = input("Black's move: ").lower()
            self.DrawBoard()
