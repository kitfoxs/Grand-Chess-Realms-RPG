# Chessnut Pro Setup Guide for macOS

## Step 1: Prepare Your Chessnut Pro

1. **Turn on** your Chessnut Pro board
2. Put it in **pairing/discoverable mode**:
   - Check your Chessnut Pro manual for exact steps
   - Usually: Hold power button for a few seconds until LED blinks
   - Some models: There's a dedicated Bluetooth button
3. Make sure board is **charged** or plugged in
4. Keep it **close** to your Mac (within 1-2 meters)

## Step 2: Check macOS Bluetooth

1. Open **System Settings** → **Bluetooth**
2. Make sure Bluetooth is **ON**
3. Look for "Chessnut" or "Smart Chess" in available devices
4. **DON'T** pair it through Settings yet - we'll do it programmatically

## Step 3: Install Python Dependencies

```bash
# Make sure you're in the project directory
cd ~/Desktop/Grand-Chess-Realms-RPG

# Install required packages
pip3 install -r requirements-board.txt

# Or install individually:
pip3 install bleak python-chess
```

## Step 4: Run Connection Test

```bash
# Make the test script executable
chmod +x test_chessnut_connection.py

# Run the test
python3 test_chessnut_connection.py
```

## What the Test Does

1. **Scans** for all Bluetooth devices
2. **Identifies** potential Chessnut devices
3. **Connects** to each one and tests communication
4. **Reads** board position
5. **Confirms** everything is working

## Expected Output (Success)

```
============================================================
  CHESSNUT PRO CONNECTION TEST
  macOS Silicon Edition
============================================================

🔍 Scanning for ALL Bluetooth devices...

Found 12 Bluetooth devices:

  ⭐ 1. Chessnut Pro
      Address: XX:XX:XX:XX:XX:XX

✅ Found 1 potential Chessnut device(s)!

🔌 Attempting to connect to: Chessnut Pro

✅ Connected successfully!

🎮 Attempting to initialize board...
✅ Initialization code sent!

👂 Listening for board changes...
   (Move a piece on the board to test)

♟️  Board position received!

   a b c d e f g h
  ┌─────────────────┐
8 │ r n b q k b n r │ 8
7 │ p p p p p p p p │ 7
6 │ . . . . . . . . │ 6
5 │ . . . . . . . . │ 5
4 │ . . . . . . . . │ 4
3 │ . . . . . . . . │ 3
2 │ P P P P P P P P │ 2
1 │ R N B Q K B N R │ 1
  └─────────────────┘
   a b c d e f g h

✅ Board communication working!

🎉 SUCCESS! Your Chessnut Pro is connected!
```

## Troubleshooting

### Issue: "No Chessnut devices found"

**Solutions:**
1. Make sure board is turned ON
2. Check if board is in pairing mode (LED should be blinking)
3. Try turning board off and on again
4. Move board closer to your Mac
5. Restart Bluetooth on your Mac:
   ```bash
   # Restart Bluetooth service (requires sudo)
   sudo killall bluetoothd
   ```

### Issue: "Failed to connect"

**Solutions:**
1. Board might be connected to another device (phone/tablet)
   - Disconnect it from other devices first
2. Board might need to be unpaired:
   - Go to macOS System Settings → Bluetooth
   - If "Chessnut" is listed, click (i) and "Forget Device"
   - Try again
3. Try pairing manually first:
   - System Settings → Bluetooth
   - Click "Connect" on Chessnut device
   - Then run test script again

### Issue: "Permission denied" or "Access restricted"

**Solutions:**
1. Grant Bluetooth permissions to Terminal:
   - System Settings → Privacy & Security → Bluetooth
   - Enable for "Terminal" or your Python IDE
2. Try running with sudo (not recommended but may help diagnose):
   ```bash
   sudo python3 test_chessnut_connection.py
   ```

### Issue: Board shows in scan but won't connect

**Possible causes:**
1. **Wrong device model**: The UUIDs might be different for Pro vs Air
   - We may need to use ChessnutPy or EasyLinkSDK instead
2. **Firmware version**: Check if board firmware is up to date
3. **macOS security**: May need to grant additional permissions

### Issue: Connection works but no board data

**Try:**
1. Reset the pieces to starting position
2. Move a piece deliberately
3. Check if LED lights respond
4. Board might need calibration (check manual)

## Next Steps After Success

Once the test succeeds, we'll:
1. Create a reusable board interface class
2. Integrate with chess engine
3. Build the RPG game logic on top

## Alternative: Try ChessnutPy

If the simple driver doesn't work, we can try the more full-featured ChessnutPy:

```bash
cd chessnut-pro-drivers/ChessnutPy-main
pip3 install -r requirements.txt
python3 main.py
```

ChessnutPy includes:
- More robust connection handling
- Web interface
- Engine support
- Better error handling

## Need Help?

If you encounter issues:
1. Take a screenshot of the error
2. Note your Chessnut Pro model/version
3. Check if board works with official Chessnut app
4. We can try alternative connection methods
