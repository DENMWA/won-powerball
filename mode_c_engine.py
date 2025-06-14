import numpy as np
import pandas as pd
import random
import hashlib

def entropy_score(freqs):
    probs = freqs / np.sum(freqs)
    return -np.sum(probs * np.log2(probs + 1e-9))

def frequency_decay(frequency, decay_factor=0.85):
    return frequency * decay_factor

def gap_score(draws, number):
    last_seen = next((i for i, draw in enumerate(reversed(draws)) if number in draw), len(draws))
    return last_seen

def bayesian_copair_score(draws, number, copairs):
    score = 0
    for draw in draws:
        if number in draw:
            score += sum([1 for n in draw if n in copairs])
    return score

def crypto_seeded_random():
    return int(hashlib.sha256(str(random.random()).encode()).hexdigest(), 16) % 100

def generate_candidate(draws, freq):
    all_numbers = list(range(1, 36))
    selected = []
    while len(selected) < 7:
        scores = {}
        for n in all_numbers:
            if n in selected:
                continue
            ent = entropy_score(freq)
            f_decay = frequency_decay(freq[n-1])
            gap = gap_score(draws, n)
            bayes = bayesian_copair_score(draws, n, selected)
            score = ent + f_decay + gap + bayes + crypto_seeded_random()
            scores[n] = score
        best = max(scores, key=scores.get)
        selected.append(best)
    return selected

def select_powerball(draws):
    powerballs = [row[-1] for row in draws if len(row) >= 8]
    freq = np.zeros(20)
    for n in powerballs:
        if 1 <= n <= 20:
            freq[int(n)-1] += 1
    def entropy_score_pb(freqs):
        probs = freqs / np.sum(freqs) if np.sum(freqs) > 0 else np.ones_like(freqs) / len(freqs)
        return -np.sum(probs * np.log2(probs + 1e-9))
    def gap_score_pb(powerballs, number):
        last_seen = next((i for i, p in enumerate(reversed(powerballs)) if p == number), len(powerballs))
        return last_seen
    candidates = list(range(1, 21))
    scores = {
        n: entropy_score_pb(freq) + gap_score_pb(powerballs, n) + crypto_seeded_random()
        for n in candidates
    }
    return max(scores, key=scores.get)

def generate_mode_c_predictions(history_path, entries=100):
    data = pd.read_csv(history_path)
    draws = data.iloc[:, 1:8].values.tolist()
    frequency = np.zeros(35)
    for draw in draws:
        for n in draw:
            frequency[n-1] += 1
    full_draws = data.values.tolist()
    predictions = []
    for _ in range(entries):
        main_set = generate_candidate(draws, frequency)
        pball = select_powerball(full_draws)
        predictions.append(main_set + [pball])
    columns = [f'N{i+1}' for i in range(7)] + ['Powerball']
    return pd.DataFrame(predictions, columns=columns)
