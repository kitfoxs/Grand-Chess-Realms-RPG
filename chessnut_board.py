#!/usr/bin/env python3
"""
ChessnutBoard - Clean interface for Chessnut Pro board
Handles Bluetooth connection, position detection, and LED control
"""

import asyncio
from bleak import BleakScanner, BleakClient
import chess

# Bluetooth UUIDs for Chessnut boards
WRITE_CHAR = '1B7E8272-2877-41C3-B46E-CF057C562023'
READ_DATA = '1B7E8262-2877-41C3-B46E-CF057C562023'
INIT_CODE = b'\x21\x01\x00'

# Piece encoding from board
PIECE_DICT = {
    0: None, 1: "q", 2: "k", 3: "b", 4: "p", 5: "n",
    6: "R", 7: "P", 8: "r", 9: "B", 10: "N", 11: "Q", 12: "K"
}


class ChessnutBoard:
    """Interface to Chessnut Pro electronic chess board"""

    def __init__(self):
        self.client = None
        self.device = None
        self.current_position = None
        self.on_position_change = None  # Callback for position changes
        self.on_move = None  # Callback for detected moves
        self._running = False

    async def connect(self, device_name="Chessnut Pro", timeout=10.0):
        """Connect to the Chessnut board"""
        print(f"🔍 Scanning for {device_name}...")

        # Scan for the device
        devices = await BleakScanner.discover(timeout=timeout)

        for device in devices:
            if device.name and device_name.lower() in device.name.lower():
                self.device = device
                break

        if not self.device:
            raise Exception(f"Could not find {device_name}")

        print(f"✅ Found: {self.device.name}")
        print(f"🔌 Connecting...")

        # Connect
        self.client = BleakClient(self.device)
        await self.client.connect()

        if not self.client.is_connected:
            raise Exception("Failed to connect")

        print(f"✅ Connected to {self.device.name}")

        # Initialize board
        await self.client.write_gatt_char(WRITE_CHAR, INIT_CODE)
        print("✅ Board initialized")

        return True

    def _parse_board_data(self, data):
        """Parse raw board data into piece positions"""
        if len(data) < 34:
            return None

        # Extract the 32 bytes of position data (skip first 2 header bytes)
        position_data = data[2:34]

        # Convert to 8x8 board
        board = [[None for _ in range(8)] for _ in range(8)]

        for row_idx in range(8):
            row_bytes = position_data[row_idx*4:row_idx*4+4]
            col = 7  # Start from h-file, moving left

            for byte in row_bytes:
                # Each byte contains 2 pieces (4 bits each)
                piece1 = PIECE_DICT.get(byte >> 4)
                piece2 = PIECE_DICT.get(byte & 0x0F)

                if col >= 0:
                    board[row_idx][col] = piece1
                    col -= 1
                if col >= 0:
                    board[row_idx][col] = piece2
                    col -= 1

        return board

    def _board_to_fen(self, board):
        """Convert board array to FEN string"""
        if not board:
            return None

        fen_rows = []
        for row in board:
            fen_row = ""
            empty_count = 0

            for piece in row:
                if piece is None:
                    empty_count += 1
                else:
                    if empty_count > 0:
                        fen_row += str(empty_count)
                        empty_count = 0
                    fen_row += piece

            if empty_count > 0:
                fen_row += str(empty_count)

            fen_rows.append(fen_row)

        # Join rows with / and add default turn info
        return "/".join(fen_rows) + " w - - 0 1"

    def _boards_equal(self, board1, board2):
        """Check if two board positions are identical"""
        if board1 is None or board2 is None:
            return False

        for i in range(8):
            for j in range(8):
                if board1[i][j] != board2[i][j]:
                    return False
        return True

    def _find_move(self, old_board, new_board):
        """Detect what move was made between two positions"""
        if not old_board or not new_board:
            return None

        # Find differences
        differences = []
        for row in range(8):
            for col in range(8):
                if old_board[row][col] != new_board[row][col]:
                    square = chess.square_name(chess.square(col, 7 - row))
                    differences.append({
                        'square': square,
                        'old': old_board[row][col],
                        'new': new_board[row][col]
                    })

        # Simple move detection: one piece removed, one piece added
        if len(differences) == 2:
            if differences[0]['new'] is None and differences[1]['old'] is None:
                # Piece moved from differences[0] to differences[1]
                return {
                    'from': differences[0]['square'],
                    'to': differences[1]['square'],
                    'piece': differences[0]['old']
                }
            elif differences[1]['new'] is None and differences[0]['old'] is None:
                # Piece moved from differences[1] to differences[0]
                return {
                    'from': differences[1]['square'],
                    'to': differences[0]['square'],
                    'piece': differences[1]['old']
                }

        # Capture: one square changed piece, one square emptied
        elif len(differences) == 2:
            from_square = None
            to_square = None

            for diff in differences:
                if diff['new'] is None:  # Square was emptied
                    from_square = diff
                elif diff['old'] is not None:  # Square had piece that was replaced
                    to_square = diff

            if from_square and to_square:
                return {
                    'from': from_square['square'],
                    'to': to_square['square'],
                    'piece': from_square['old'],
                    'captured': to_square['old']
                }

        return None

    async def start_listening(self):
        """Start listening for board changes"""
        if not self.client or not self.client.is_connected:
            raise Exception("Not connected to board")

        self._running = True
        last_board = None

        def notification_handler(characteristic, data):
            nonlocal last_board

            # Parse the board position
            board = self._parse_board_data(data)

            if board and not self._boards_equal(board, last_board):
                # Position changed!
                fen = self._board_to_fen(board)

                # Detect move if we have a previous position
                move = None
                if last_board:
                    move = self._find_move(last_board, board)

                # Call callbacks
                if self.on_position_change:
                    self.on_position_change(board, fen)

                if move and self.on_move:
                    self.on_move(move)

                last_board = board
                self.current_position = board

        # Start notifications
        await self.client.start_notify(READ_DATA, notification_handler)
        print("👂 Listening for moves...")

        # Keep running
        while self._running and self.client.is_connected:
            await asyncio.sleep(0.1)

    async def set_leds(self, squares):
        """
        Set LED lights on specific squares

        Args:
            squares: List of square names (e.g., ['e2', 'e4']) or 'all' or 'none'
        """
        if not self.client or not self.client.is_connected:
            raise Exception("Not connected to board")

        # Initialize LED array (10 bytes: 2 control + 8 rows)
        led_data = bytearray([0x0A, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])

        if squares == 'all':
            # Turn on all LEDs
            for i in range(2, 10):
                led_data[i] = 0xFF
        elif squares == 'none':
            # All LEDs off (already initialized to 0)
            pass
        else:
            # Set specific squares
            for square_name in squares:
                try:
                    square = chess.parse_square(square_name)
                    file = chess.square_file(square)
                    rank = chess.square_rank(square)

                    # Convert to LED array indices
                    row_idx = 2 + (7 - rank)  # Rows are flipped in LED array
                    bit_position = file

                    # Set the bit
                    led_data[row_idx] |= (1 << bit_position)
                except:
                    print(f"⚠️  Invalid square: {square_name}")

        # Send LED command
        await self.client.write_gatt_char(WRITE_CHAR, led_data)

    async def highlight_move(self, from_square, to_square, duration=2.0):
        """Highlight a move on the board with LEDs"""
        await self.set_leds([from_square, to_square])
        await asyncio.sleep(duration)
        await self.set_leds('none')

    def stop_listening(self):
        """Stop listening for board changes"""
        self._running = False

    async def disconnect(self):
        """Disconnect from the board"""
        if self.client and self.client.is_connected:
            self._running = False
            await self.client.disconnect()
            print("🔌 Disconnected")

    def print_board(self, board=None):
        """Print the current board position"""
        if board is None:
            board = self.current_position

        if not board:
            print("No board position available")
            return

        print("\n   a b c d e f g h")
        print("  ┌─────────────────┐")

        for row_idx in range(8):
            rank = 8 - row_idx
            print(f"{rank} │ ", end="")

            for col_idx in range(8):
                piece = board[row_idx][col_idx]
                display = piece if piece else "."
                print(f"{display} ", end="")

            print(f"│ {rank}")

        print("  └─────────────────┘")
        print("   a b c d e f g h\n")


# Example usage
if __name__ == "__main__":
    async def main():
        board = ChessnutBoard()

        # Callback when position changes
        def on_position_change(position, fen):
            print("\n" + "="*60)
            print("♟️  POSITION CHANGED")
            print("="*60)
            board.print_board(position)
            print(f"FEN: {fen}\n")

        # Callback when move detected
        def on_move(move):
            print(f"\n🎯 MOVE: {move['piece']} from {move['from']} to {move['to']}")
            if 'captured' in move:
                print(f"   💥 Captured: {move['captured']}")

        # Set callbacks
        board.on_position_change = on_position_change
        board.on_move = on_move

        try:
            # Connect
            await board.connect()

            # Flash all LEDs to confirm connection
            print("\n💡 Testing LEDs...")
            await board.set_leds('all')
            await asyncio.sleep(0.5)
            await board.set_leds('none')
            await asyncio.sleep(0.5)
            await board.set_leds('all')
            await asyncio.sleep(0.5)
            await board.set_leds('none')

            print("\n✅ Ready! Make moves on the board...")
            print("   (Press Ctrl+C to exit)\n")

            # Listen for moves
            await board.start_listening()

        except KeyboardInterrupt:
            print("\n\n⚠️  Stopping...")
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()
        finally:
            await board.disconnect()

    asyncio.run(main())
