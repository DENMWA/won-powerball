import random
import pandas as pd

def generate_mode_a_predictions(entries=100):
    predictions = []
    for _ in range(entries):
        main_numbers = sorted(random.sample(range(1, 36), 7))
        powerball = random.randint(1, 20)
        predictions.append(main_numbers + [powerball])
    columns = [f'N{i+1}' for i in range(7)] + ['Powerball']
    return pd.DataFrame(predictions, columns=columns)
