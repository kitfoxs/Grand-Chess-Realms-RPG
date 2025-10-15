#!/usr/bin/env python3
"""
Test script to connect to Chessnut Pro board on macOS
"""

import asyncio
from bleak import BleakScanner, BleakClient
import sys

# UUIDs for Chessnut boards (from the driver code)
WRITE_CHAR = '1B7E8272-2877-41C3-B46E-CF057C562023'
READ_DATA = '1B7E8262-2877-41C3-B46E-CF057C562023'
INIT_CODE = b'\x21\x01\x00'

# Piece representation
PIECE_DICT = {
    0: ".", 1: "q", 2: "k", 3: "b", 4: "p", 5: "n",
    6: "R", 7: "P", 8: "r", 9: "B", 10: "N", 11: "Q", 12: "K"
}


def print_board(data):
    """Print chess board in human-readable format"""
    print("\n   a b c d e f g h")
    print("  ┌─────────────────┐")
    for row_idx in range(8):
        print(f"{8-row_idx} │ ", end="")
        row = reversed(data[row_idx*4:row_idx*4+4])
        for byte in row:
            piece1 = PIECE_DICT.get(byte >> 4, "?")
            piece2 = PIECE_DICT.get(byte & 0x0F, "?")
            print(f"{piece1} {piece2} ", end="")
        print(f"│ {8-row_idx}")
    print("  └─────────────────┘")
    print("   a b c d e f g h\n")


async def scan_all_devices():
    """Scan for all Bluetooth devices to find Chessnut"""
    print("🔍 Scanning for ALL Bluetooth devices...")
    print("   (Looking for your Chessnut Pro)\n")

    devices = await BleakScanner.discover(timeout=10.0)

    chessnut_devices = []
    print(f"Found {len(devices)} Bluetooth devices:\n")

    for i, device in enumerate(devices, 1):
        name = device.name or "Unknown"
        # Highlight potential Chessnut devices
        if any(word in name.lower() for word in ['chess', 'chessnut', 'smart']):
            print(f"  ⭐ {i}. {name}")
            print(f"      Address: {device.address}")
            chessnut_devices.append(device)
        else:
            print(f"  {i}. {name} ({device.address})")

    print("\n" + "="*60)
    if chessnut_devices:
        print(f"\n✅ Found {len(chessnut_devices)} potential Chessnut device(s)!")
        return chessnut_devices
    else:
        print("\n⚠️  No obvious Chessnut devices found.")
        print("   Make sure your Chessnut Pro is:")
        print("   1. Turned ON")
        print("   2. In pairing mode (check manual)")
        print("   3. Not already connected to another device")
        return []


async def test_connection(device):
    """Test connection to a specific device"""
    print(f"\n🔌 Attempting to connect to: {device.name}")
    print(f"   Address: {device.address}\n")

    try:
        async with BleakClient(device) as client:
            if not client.is_connected:
                print("❌ Failed to connect")
                return False

            print("✅ Connected successfully!")

            # List available services
            print("\n📋 Available services:")
            for service in client.services:
                print(f"   Service: {service.uuid}")
                for char in service.characteristics:
                    props = ','.join(char.properties)
                    print(f"      └─ Char: {char.uuid} ({props})")

            # Try to initialize the board
            print("\n🎮 Attempting to initialize board...")
            try:
                await client.write_gatt_char(WRITE_CHAR, INIT_CODE)
                print("✅ Initialization code sent!")

                # Set up notification handler
                board_data = None

                def notification_handler(characteristic, data):
                    nonlocal board_data
                    if len(data) >= 34:
                        board_data = data[2:34]
                        print("\n♟️  Board position received!")
                        print_board(board_data)

                # Start listening for board updates
                await client.start_notify(READ_DATA, notification_handler)
                print("👂 Listening for board changes...")
                print("   (Move a piece on the board to test)\n")

                # Wait for some data
                await asyncio.sleep(10)

                await client.stop_notify(READ_DATA)

                if board_data:
                    print("\n✅ Board communication working!")
                    return True
                else:
                    print("\n⚠️  No board data received")
                    return False

            except Exception as e:
                print(f"⚠️  Error during initialization: {e}")
                print("   (This might not be a Chessnut device)")
                return False

    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False


async def main():
    """Main test function"""
    print("="*60)
    print("  CHESSNUT PRO CONNECTION TEST")
    print("  macOS Silicon Edition")
    print("="*60)
    print()

    # First, make sure board is ready
    print("📝 Pre-flight checklist:")
    print("   1. Is your Chessnut Pro turned ON? ✓")
    print("   2. Is it in pairing/discoverable mode? ✓")
    print("   3. Is it close to your Mac? ✓")
    input("\nPress ENTER when ready...")

    # Scan for devices
    chessnut_devices = await scan_all_devices()

    if not chessnut_devices:
        print("\n💡 Troubleshooting tips:")
        print("   - Check if Bluetooth is enabled on your Mac")
        print("   - Try turning the board off and on again")
        print("   - Make sure it's not paired with another device")
        print("   - Check if board has battery/is charging")
        return

    # Test each potential device
    print("\n" + "="*60)
    print("Testing connections...\n")

    for i, device in enumerate(chessnut_devices, 1):
        print(f"\nTest {i}/{len(chessnut_devices)}")
        print("-" * 60)
        success = await test_connection(device)

        if success:
            print("\n" + "="*60)
            print("🎉 SUCCESS! Your Chessnut Pro is connected!")
            print("="*60)
            print(f"\nDevice details:")
            print(f"  Name: {device.name}")
            print(f"  Address: {device.address}")
            print(f"\nYou can now use this device for your Chess RPG!")
            return

    print("\n" + "="*60)
    print("❌ Could not establish working connection")
    print("="*60)
    print("\n💡 Next steps:")
    print("   1. Check Chessnut Pro manual for pairing mode")
    print("   2. Try pairing via macOS Bluetooth settings first")
    print("   3. Contact Chessnut support if issues persist")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
