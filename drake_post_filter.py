import pandas as pd
import numpy as np

def drake_score(prediction, historical_draws):
    main_numbers = set(prediction[:7])
    powerball = prediction[7]
    overlaps = []
    power_hits = []
    for row in historical_draws:
        draw = list(row)
        if len(draw) < 9:
            continue
        past_main = set(draw[1:8])
        past_pball = draw[8]
        overlap_count = len(main_numbers.intersection(past_main))
        overlaps.append(overlap_count)
        power_hits.append(1 if powerball == past_pball else 0)
    if not overlaps:
        return 0.0
    p_div1 = sum(1 for o in overlaps if o >= 5) / len(overlaps)
    p_cluster = sum(overlaps) / (len(overlaps) * 7)
    p_powerball = sum(power_hits) / len(power_hits)
    last_draw = set(historical_draws[-1][1:8]) if len(historical_draws[-1]) >= 8 else set()
    redundancy = len(main_numbers.intersection(last_draw)) / 7
    score = (0.5 * p_div1) + (0.3 * p_cluster) + (0.2 * p_powerball) - (0.1 * redundancy)
    return round(score, 4)

def apply_drake_filter(predictions_path, history_path, output_path='scored_predictions.csv'):
    predictions = pd.read_csv(predictions_path)
    historical = pd.read_csv(history_path).values.tolist()
    scored = []
    for i, row in predictions.iterrows():
        pred = list(row[:8])
        score = drake_score(pred, historical)
        scored.append(score)
    predictions['DrakeScore'] = scored
    predictions.sort_values(by='DrakeScore', ascending=False, inplace=True)
    predictions.to_csv(output_path, index=False)
