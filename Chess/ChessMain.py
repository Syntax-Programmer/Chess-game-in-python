from ChessEngine import Main
import keyboard

GAME = Main()
print(
    """
    
    Press y/Y to start.
    
    """
)
if keyboard.read_key().lower() != "y":
    exit(code=1)
else:
    # Removing the "y" from the input screen
    keyboard.press("backspace")
    GAME.GameLoop()
