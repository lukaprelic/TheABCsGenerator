import pandas
import numpy as np

letterRarities = {
    'A': 0.084966,
    'B': 0.020720,
    'C': 0.045388,
    'D': 0.033844,
    'E': 0.111606,
    'F': 0.018121,
    'G': 0.024705,
    'H': 0.030034,
    'I': 0.075448,
    'J': 0.001965,
    'K': 0.011016,
    'L': 0.054893,
    'M': 0.030129,
    'N': 0.066544,
    'O': 0.071635,
    'P': 0.031671,
    'Q': 0.001962,
    'R': 0.075809,
    'S': 0.057351,
    'T': 0.069509,
    'U': 0.036308,
    'V': 0.010074,
    'W': 0.012899,
    'X': 0.002902,
    'Y': 0.017779,
    'Z': 0.002722,
}

backgroundRarities = {
    'Bubblegum': 0.11,
    'City': 0.11,
    'Cowboy': 0.11,
    'Desert': 0.11,
    'Heaven': 0.11,
    'Hell': 0.11,
    'Moon': 0.11,
    'Jungle': 0.11,
    'Ocean': 0.11,
    'Gold': 0.01,
}

hatRarity = {
    'None': 0.9,
    'Bubblegum': 0.0108,
    'City': 0.0108,
    'Cowboy': 0.0108,
    'Desert': 0.0108,
    'Heaven': 0.0108,
    'Hell': 0.0108,
    'Moon': 0.0108,
    'Nature': 0.0108,
    'Ocean': 0.0108,
    'Gold': 0.0028,
}

fontRarity = {
    'Sans Serif Amber': 0.3300,
    'Serif Amber': 0.1372,
    'Calligraphy Amber': 0.1072,
    'Sans Serif Red': 0.2022,
    'Serif Red': 0.0872,
    'Calligraphy Red': 0.0722,
    'Sans Serif Silver': 0.0250,
    'Serif Silver': 0.0150,
    'Calligraphy Silver': 0.0100,
    'Sans Serif Gold': 0.0080,
    'Serif Gold': 0.0040,
    'Calligraphy Gold': 0.0020,
}


def generateCombination():
    background = np.random.choice(list(backgroundRarities.keys()), p=list(backgroundRarities.values()))
    font = np.random.choice(list(fontRarity.keys()), p=list(fontRarity.values()))
    letter1 = np.random.choice(list(letterRarities.keys()), p=list(letterRarities.values()))
    letter2 = np.random.choice(list(letterRarities.keys()), p=list(letterRarities.values()))
    letter3 = np.random.choice(list(letterRarities.keys()), p=list(letterRarities.values()))
    hat = np.random.choice(list(hatRarity.keys()), p=list(hatRarity.values()))
    return background, letter1, letter2, letter3, font, hat


if __name__ == '__main__':
    rows = []
    for i in range(200):
        combination = generateCombination()
        row = list(combination)
        rows.append(row)
    cities = pandas.DataFrame(rows,
                              columns=
                              ['background', 'letter1', 'letter2', 'letter3', 'font', 'hat'])
    cities.to_csv('generated.csv')
