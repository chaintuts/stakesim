# This file contains driver code for conducting the Proof of Stake simulatioin
#
# Author: Josh McIntyre
#

import stakesimlib

# Module constants
DISPLAY_INTERVAL = 10

# Format function for the entropy
def format_entropy(result):

    res = "Id  Cmt    Rvl V\n"
    for node_id in result.node_ids:
        valid = "T" if result.validated[node_id] else "F"
        res += f"N{node_id}: {result.committed[node_id]:03d} -> {result.revealed[node_id]:03d} {valid}\n"

    return res

# Format function for stakes
def format_stake(result):

    res = "Id  Stk Wgt\n"
    for node_id in result.node_ids:
        valid = "T" if result.validated[node_id] else "F"
        res += f"N{node_id}: {result.staked[node_id]:03d} {result.weights[node_id]*100:02.0f}%\n"

    return res

# Format function for node selection
def format_selection(result):

    res = f"Entropy: {result.combined_entropy}\n"
    res += f"Node Selected: {result.selected_node}\n"

    return res

# Display the simulation data on a screen
def display_screen(entropy_slide, stake_slide, selection_slide):

    import busio
    import board
    import time
    import adafruit_character_lcd.character_lcd_i2c as character_lcd

    # Initialize the board
    i2c = busio.I2C(board.SCL, board.SDA)
    cols = 20
    rows = 4
    lcd = character_lcd.Character_LCD_I2C(i2c, cols, rows)
    lcd.backlight = True

    # Rotate through the formatted slides one-by-one
    # Based on what data will fit on the screen
    while True:
        lcd.clear()
        lcd.message = entropy_slide
        time.sleep(DISPLAY_INTERVAL)

        lcd.clear()
        lcd.message = stake_slide
        time.sleep(DISPLAY_INTERVAL)

        lcd.clear()
        lcd.message = selection_slide
        time.sleep(DISPLAY_INTERVAL)

# Display the simulation data via serial_connected
def display_serial(entropy_slide, stake_slide, selection_slide):

    print()
    print(entropy_slide)
    print(stake_slide)
    print(selection_slide)


# The main entropy point for the program
def main():

    ssn = stakesimlib.StakeSimNode(3)
    result = ssn.simulate()

    entropy_slide = format_entropy(result)
    stake_slide = format_stake(result)
    selection_slide = format_selection(result)

    display_serial(entropy_slide, stake_slide, selection_slide)
    display_screen(entropy_slide, stake_slide, selection_slide)

if __name__ == "__main__":
	main()
