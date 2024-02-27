from ChessEngine import Main

to_start = input("Start (Y/n): ").strip().lower()
if to_start != "y":
    exit()
Main = Main()
Main.GameLoop()
