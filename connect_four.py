import sys
def gravity_decorator(insert_method):
    """Decorator to apply gravity to the game board after piece is placed.
    Makes pieces fall into the lowest available position after bomb or teleport.
    Args:
        insert_method: the original method for placing piece on board
    Returns:
        A wrapper function that does the original insertion then applies gravity.
    """
    def wrapper(self, board, column):
        insertion = insert_method(self, board, column)
        moved = True
        while moved == True:
            moved = False
            # Iterate through board column by column and row from second last to the top
            for column in range(board.columns):
                for row in range(board.rows - 2, -1, -1):
                    if (
                        board.grid[row][column] != " "
                        and board.grid[row + 1][column] == " "
                    ):
                        # Move the piece down as the row below was empty and empty the space
                        board.grid[row + 1][column] = board.grid[row][column]
                        board.grid[row][column] = " "
                        moved = True
        return insertion

    return wrapper


class Board:
    """Make a connect-four game board with a given number of rows and columns.
    This class manages the grid structure and its display
    """

    def __init__(self, rows: int, columns: int):
        """Initialise a new game board.
        Args:
            rows: number of rows
            columns: number of columns
        """
        self.rows = rows
        self.columns = columns
        self.grid = []

        # Creating the grid as a list of lists, by going row by row.
        for row in range(self.rows):
            row = []
            for column in range(self.columns):
                row.append(" ")
            self.grid.append(row)

    def __str__(self) -> str:
        """Returns the string representation of the board for display.

        Includes number of columns at the top and a grid structure below.
        """

        # Construct column header with numbers, with proper alignment.
        numbered_column = " "
        column_num_space = 3
        for column_num in range(1, self.columns + 1):
            centered_string = str(column_num).center(column_num_space)
            numbered_column += centered_string
            if column_num < self.columns:
                numbered_column += " "
        
        # Remove trailing characters and add newline for formatting.
        numbered_column = numbered_column.rstrip()
        numbered_column += "\n"

        horizontal_border = "+"
        for i in range(self.columns):
            horizontal_border += "---+"
        horizontal_border += "\n"

        # Assemble grid, building it row by row.
        display = ""
        for row in self.grid:
            display += horizontal_border

            middle_line = "|"
            for space in row:
                middle_line += f" {space} |"
            middle_line += "\n"

            display += middle_line

        display += horizontal_border

        output = numbered_column + display

        return output


class Piece:
    """Represents a piece with a symbol.
    This class handles the logic for inserting a piece onto the game board.
    """

    def __init__(self, symbol: str):
        """Initialise a new piece with given symbol
        Args:
            symbol: character representing the piece.
        """
        self.symbol = symbol

    def insert(self, board, column: int):
        """Places the piece into the specified column of the board.
        The piece is placed in the lowest available row.
        Args:
            board: the board the piece needs to be inserted in.
            column: the column the piece needs to be inserted in.
        Returns:
            True if piece was successfully inserted or false if not
            (columns is out of bounds or full).
        """

        column_i0 = column - 1

        if not (0 <= column_i0 < board.columns):
            return False

        # Iterate from bottom to top, to find the first empty slot (whitespace).
        for row in range(board.rows - 1, -1, -1):
            if board.grid[row][column_i0] == " ":
                board.grid[row][column_i0] = self.symbol
                return True
        return False


class Player:
    """Stores information about user playing the game with a name, symbol and collection of pieces.

    This class manages a player's pieces and their selection during gameplay.
    """
    def __init__(self, name: str, symbol: str):
        """Initialises a new player.
        Args:
            name: the name of the player.
            symbol: the symbol the player wants to use for their pieces.
        """

        self.name = name
        self.symbol = symbol
        self.pieces = []

    def add_piece(self, symbol, quantity):
        """Adds new piece objects to player's collection.
        Args:
            symbol: The symbol of the pieces to be added to the collection.
            quantity: the number of piece objects to create and add.
        """
        for x in range(quantity):
            if symbol == "B":
                piece = BombPiece()
            elif symbol == "T":
                piece = TeleportPiece()
            else:
                piece = Piece(symbol)
            self.pieces.append(piece)

    def __str__(self):
        """Return a string representation of the player's hand.

        The string groups pieces by their symbol and reflects the count for each.
        """

        # Count the number of each unique piece symbol in player's hand.
        counter = {}
        for piece in self.pieces:
            symbol = piece.symbol
            if symbol in counter:
                counter[symbol] += 1
            else:
                counter[symbol] = 1
        
        # Format counter into a list of strings
        strings = []
        for key in sorted(counter.keys()):
            strings.append(f"{key}: {counter[key]}")

        output_str = f"{self.name}'s pieces -> "
        output_str += ", ".join(strings)

        return output_str

    def choose_piece(self):
        """Prompts the user to choose a piece and a column to play.
        Returns:
            A list containing the removed piece object(the chosen piece) and the column,
            or None is the input was invalid or the piece was not found.
        """
        print(Player.__str__(self))
        user_input = input("Choose a piece to play (symbol and column): ")

        split = user_input.split(" ")
        if len(split) != 2:
            return None

        chosen = split[0]
        try:
            column = int(split[1])
        except:
            return None

        # Search for player's chosen piece in their collection and remove it.
        for i in range(len(self.pieces)):
            if self.pieces[i].symbol == chosen:
                removed_piece = self.pieces.pop(i)
                return [removed_piece, column]
        return None


class Game:
    """Manages overall game flow for a connect four game, including setup,
    piece placement, turn management and win/draw checking.
    """

    def __init__(self, rows, columns):
        """Initialises a new game.
        Args:
            rows: the number of rows for game board.
            columns: the number of columns for game board.
        """
        self.rows = rows
        self.columns = columns
        self.board = Board(self.rows, self.columns)
        self.players = []
        self.current_player = None

    def setup(self):
        """Sets up the game by creating player objects and distributing pieces.
        Prompt players for their name and the unique symbol they want to play with,
        then calculates and assigns the starting number of pieces for each.
        """
        
        # Validate user input until we get the proper format
        inputting = True
        parts1 = []
        while inputting:
            player1 = input("Enter player one's name and symbol: ")
            current = player1.split(" ")
            if len(current) == 2 and len(current[1]) == 1:
                parts1 = current
                break
        
        while inputting:
            player2 = input("Enter player two's name and symbol: ")
            parts2 = player2.split(" ")
            if (
                len(parts2) == 2
                and parts2[1] != parts1[1]
                and len(parts2[1]) == 1
            ):
                break

        # Create player objects using user input
        splitp1 = player1.split(" ")
        splitp2 = player2.split(" ")
        player1 = Player(splitp1[0], splitp1[1])
        player2 = Player(splitp2[0], splitp2[1])

        self.players.append(player1)
        self.players.append(player2)

        # Distribute pieces based on total slots
        total = self.rows * self.columns
        teleport_total = total // 10
        bomb_total = total // 20
        quantityp2 = total // 2
        quantityp1 = total // 2
        if total % 2 != 0:
            quantityp1 += 1

        player1.add_piece(splitp1[1], quantityp1)
        player1.add_piece("T", teleport_total)
        player1.add_piece("B", bomb_total)
        
        player2.add_piece(splitp2[1], quantityp2)
        player2.add_piece("T", teleport_total)
        player2.add_piece("B", bomb_total)

        # Set player 1 as starting
        self.current_player = self.players[0]

    def begin(self):
        """Starts and manages the main game loop."""

        self.setup()
        print(self.board)
        playing = True

        while playing:
            
            # Determine other player for simulatenous win checks.
            otherplayer = None
            if self.players[0] == self.current_player:
                otherplayer = self.players[1]
            else:
                otherplayer = self.players[0]
            otherplayer_symbol = otherplayer.symbol

            # If one player runs out of pieces before game end we let the ohter player play on
            if len(self.current_player.pieces) == 0:
                print(f"{self.current_player.name} out of pieces")
                self.current_player = otherplayer
                print(self.board)
                continue
            
            # Get the current player's chosen piece and column
            userlist = self.current_player.choose_piece()
            if userlist == None:
                continue

            piece = userlist[0]
            column = userlist[1]
            column_i0 = column - 1

            insert_success = piece.insert(self.board, int(column))
            if insert_success == False:
                continue

            # Determine the exact row the piece was inserted into.
            inserted_row = -1
            for row in range(self.board.rows):
                if self.board.grid[row][column_i0] == piece.symbol:
                    inserted_row = row
                    break
                else:
                    continue


            # ----- Win conditions -----
            current_player_wins = None
            # Check for horizontal win by connecting consecutive pieces in left or right order.
            counter_h = 1
            
            column_index = column_i0 + -1
            while (
                column_index >= 0
                and self.board.grid[inserted_row][column_index] == piece.symbol
            ):
                counter_h += 1
                column_index -= 1

            column_index = column_i0 + 1
            while (
                column_index < self.board.columns
                and self.board.grid[inserted_row][column_index] == piece.symbol
            ):
                counter_h += 1
                column_index += 1

            if counter_h >= 4:
                current_player_wins = True

            # Check for win condition in "\" direction (top left or bottom right)
            counter_d_backslash = 1

            check_row = inserted_row - 1
            check_column = column_i0 - 1
            while (
                check_row >= 0
                and check_column >= 0
                and self.board.grid[check_row][check_column] == piece.symbol
            ):
                check_row -= 1
                check_column -= 1
                counter_d_backslash += 1

            check_row = inserted_row + 1
            check_column = column_i0 + 1
            while (
                check_row < self.board.rows
                and check_column < self.board.columns
                and self.board.grid[check_row][check_column] == piece.symbol
            ):
                check_row += 1
                check_column += 1
                counter_d_backslash += 1

            # Check for win condition in "/" direction (top right or bottom left)
            counter_d_slash = 1

            check_row = inserted_row - 1
            check_column = column_i0 + 1
            while (
                check_row >= 0
                and check_column < self.board.columns
                and self.board.grid[check_row][check_column] == piece.symbol
            ):
                check_row -= 1
                check_column += 1
                counter_d_slash += 1
            
            check_row = inserted_row + 1
            check_column = column_i0 - 1
            while (
                check_row < self.board.rows
                and check_column >= 0
                and self.board.grid[check_row][check_column] == piece.symbol
            ):
                check_row += 1
                check_column -= 1
                counter_d_slash += 1

            if counter_d_backslash >= 4:
                current_player_wins = True

            if counter_d_slash >= 4:
                current_player_wins = True

            # Check for vertical win by consecutive pieces in up or down direction.
            counter_v = 1
            
            vertical_row = inserted_row - 1
            while (
                vertical_row >= 0
                and self.board.grid[vertical_row][column_i0] == piece.symbol
            ):
                vertical_row -= 1
                counter_v += 1

            Down_row = inserted_row + 1
            while (
                Down_row < self.board.rows
                and self.board.grid[Down_row][column_i0] == piece.symbol
            ):
                Down_row += 1
                counter_v += 1

            if counter_v >= 4:
                current_player_wins = True

            # Detect simulatenous wins (draw) in case of flow-on effects.
            otherplayer_wins = None
            for row in range(self.board.rows):
                for column in range(self.board.columns):
                    if self.board.grid[row][column] == otherplayer_symbol:

                        # Check for horizontal win for other player
                        horizontal_count = 1
                        for x in range(1, 4):
                            if (
                                column + x < self.board.columns
                                and self.board.grid[row][column + x]
                                == otherplayer_symbol
                            ):
                                horizontal_count += 1
                            else:
                                break
                        if horizontal_count >= 4:
                            otherplayer_wins = True
                            break

                        # Check for vertical win for other player
                        vertical_count = 1
                        for x in range(1, 4):
                            if (
                                row + x < self.board.rows
                                and self.board.grid[row + x][column]
                                == otherplayer_symbol
                            ):
                                vertical_count += 1
                            else:
                                break
                        if vertical_count >= 4:
                            otherplayer_wins = True
                            break

                        # Check for diagonal (bottom right) win for other player
                        bottom_right = 1
                        for x in range(1, 4):
                            if (
                                row + x < self.board.rows
                                and column + x < self.board.columns
                                and self.board.grid[row + x][column + x]
                                == otherplayer_symbol
                            ):
                                bottom_right += 1
                            else:
                                break
                        if bottom_right >= 4:
                            otherplayer_wins = True
                            break

                        # Check for diagonal (bottom left) win for other player
                        bottom_left = 1
                        for x in range(1, 4):
                            if (
                                row + x < self.board.rows
                                and column - x >= 0
                                and self.board.grid[row + x][column - x]
                                == otherplayer_symbol
                            ):
                                bottom_left += 1
                            else:
                                break
                        if bottom_left >= 4:
                            otherplayer_wins = True
                            break
                if otherplayer_wins == True:
                    break

            # Determine game outcome based on detected wins.
            if current_player_wins == True and otherplayer_wins == True:
                print("It was a draw!")
                print(self.board)
                playing = False
                continue
            
            elif current_player_wins == True:
                print(f"{self.current_player.name} wins!")
                print(self.board)
                playing = False
                continue
            
            elif otherplayer_wins == True:
                print(f"{self.current_player.name} wins!")
                print(self.board)
                playing = False
                continue
            
            # Draw if board is completely full (no whitespace slots).
            board_is_full = True
            for row in self.board.grid:
                for slot in row:
                    if slot == " ":
                        board_is_full = False
                        break

            # Draw if players out of pieces
            no_more_pieces = False
            if len(self.players[0].pieces) == 0 and len(self.players[1].pieces) == 0:
                no_more_pieces = True

            if board_is_full == True or no_more_pieces == True:
                print("It was a draw!")
                print(self.board)
                playing = False
                continue
            

            print(self.board)
            
            # Switch players for next turn
            self.current_player = otherplayer


class BombPiece(Piece):
    """Represents the logic for the bomb piece "B".
    When the bomb piece is inserted it removes everything around it in each direction by one slot.
    """
    def __init__(self):
        """Initialise the base Piece class with the "B" symbol"""
        super().__init__("B")

    @gravity_decorator
    def insert(self, board, column):
        """Insert bomb piece and detonate it.
        Args:
            board: The board the piece is inserted in.
            column: The column the piece is inserted in.
        Returns:
            boolean value: True or False if bomb detonated or not
        """
        
        inserted = super().insert(board, column)
        if inserted == False:
            return False
        inserted_row = -1
        column_i0 = column - 1
        
        # Find exact row the bomb was placed in to center the explosion
        for row in range(board.rows - 1, -1, -1):
            if board.grid[row][column_i0] == self.symbol:
                inserted_row = row
                break
        
        # Clear each cell in the radius and ignore out of bounds cells
        for row in range(-1, 2):
            for column in range(-1, 2):
                target_row = inserted_row + row
                target_column = column_i0 + column

                if 0 <= target_row < board.rows and 0 <= target_column < board.columns:
                    board.grid[target_row][target_column] = " "
        return True


class TeleportPiece(Piece):
    """Represents the logic for the teleport piece "T".
    When inserted, it moves a piece from a mirrored board position to the lowest
    available spot in the original column.
    """
    def __init__(self):
        """Initialise the base Piece class with "T" symbol."""
        super().__init__("T")

    @gravity_decorator
    def insert(self, board, column):
        """Insert the teleport piece, move the mirrored piece and apply gravity.
        Args:
            board: The board the piece is inserted in.
            column: The column the piece is inserted in.
        Returns:
            boolean value: True or False if teleported or not
        """
        
        inserted = super().insert(board, column)

        if inserted == False:
            return False

        #Find the exact row where the "T" piece landed
        inserted_row = -1
        column_i0 = column - 1
        for row in range(board.rows - 1, -1, -1):
            if board.grid[row][column_i0] == self.symbol:
                inserted_row = row
                break
        
        # Remove the "T"
        board.grid[inserted_row][column_i0] = " "
        
        # Calculate mirrored row and column based on the board's center
        center_row = (board.rows - 1) / 2
        mirrored_row = int(2 * center_row - inserted_row)
        
        center_column = (board.columns - 1) / 2
        mirrored_column = int(2 * center_column - column_i0)

        symbol_to_teleport = None
        
        if 0 <= mirrored_row < board.rows and 0 <= mirrored_column < board.columns:
            # If within bounds get symbol from mirrored position
            targetted_symbol_mirroredposition = board.grid[mirrored_row][mirrored_column]

            # If there is a piece at mirrored position, move it and remove from original slot.
            if targetted_symbol_mirroredposition != " ":
                symbol_to_teleport = targetted_symbol_mirroredposition
                board.grid[mirrored_row][mirrored_column] = " "

        # If piece was found and removed, find the lowest spot and place teleported symbol
        if symbol_to_teleport != None:
            for row in range(board.rows - 1, -1, -1):
                if board.grid[row][column_i0] == " ":
                    board.grid[row][column_i0] = symbol_to_teleport
                    break
        
        return True

def main():
    "Command-line interface for players"
    if len(sys.argv) != 3:
        print("Usage: python connect_four.py <rows> <columns>")
        sys.exit(1)
    
    try:
        rows = int(sys.argv[1])
        columns = int(sys.argv[2])
    except ValueError:
        print("Please enter rows and columns as integers.")
        sys.exit(1)
    print(f"Starting connect four game with {rows}x{columns}")
    print(f"Please enter the username and symbol you want to use, symbol can be either O or X.\n")
    game = Game(rows,columns)
    game.begin()
if __name__ == "__main__":
    main()