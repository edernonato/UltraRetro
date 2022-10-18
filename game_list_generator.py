import os


class CreateGameList:

    def __init__(self):

        path = f"/usr/games/roms/snes/"
        roms = os.listdir(path)
        games_dict = {}

        for rom_index in range(len(roms)):
            games_dict[str(rom_index)] = roms[rom_index]

        print(games_dict)
        string_games = str(games_dict)

        with open('snes.txt', 'w') as snes_json:
            snes_json.write(str(string_games))

