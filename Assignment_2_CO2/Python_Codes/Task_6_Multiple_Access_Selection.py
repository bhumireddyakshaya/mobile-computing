# TASK 6: Choosing Multiple-Access Techniques for Real Deployments
# Weighted decision matrix with a +/-20% weight sensitivity check

techniques = ["SDMA", "TDMA", "FDMA", "CDMA", "OFDMA"]
criteria = ["Capacity", "Mobility", "Interference handling", "Low complexity", "Burst data"]
weights = [0.25, 0.20, 0.20, 0.15, 0.20]

# Ratings are illustrative engineering judgements from 1 (poor) to 5 (excellent).
ratings = {
    "Wide-area cellular voice": {
        "SDMA": [4, 4, 3, 3, 3], "TDMA": [3, 4, 3, 4, 2],
        "FDMA": [2, 4, 3, 4, 1], "CDMA": [4, 4, 4, 2, 3], "OFDMA": [5, 4, 4, 3, 5]},
    "Jam-resistant tactical link": {
        "SDMA": [3, 3, 3, 3, 2], "TDMA": [2, 3, 2, 4, 2],
        "FDMA": [2, 3, 2, 4, 1], "CDMA": [4, 3, 5, 2, 3], "OFDMA": [4, 3, 3, 3, 4]},
    "High-rate stadium downlink": {
        "SDMA": [4, 3, 4, 2, 3], "TDMA": [2, 3, 2, 4, 2],
        "FDMA": [2, 3, 2, 4, 2], "CDMA": [3, 3, 3, 2, 3], "OFDMA": [5, 4, 4, 3, 5]},
    "5000 low-rate sensors": {
        "SDMA": [3, 2, 3, 2, 2], "TDMA": [4, 3, 3, 4, 4],
        "FDMA": [2, 3, 3, 4, 1], "CDMA": [3, 3, 3, 2, 3], "OFDMA": [4, 3, 4, 2, 4]}
}

def scores(weight_values, deployment):
    return {tech: sum(weight_values[i] * ratings[deployment][tech][i]
                      for i in range(len(criteria))) for tech in techniques}

print("TASK 6 - WEIGHTED MULTIPLE-ACCESS DECISION")
print("Criteria and weights:")
for c, w in zip(criteria, weights):
    print(c, ":", w)

for deployment in ratings:
    base = scores(weights, deployment)
    winner = max(base, key=base.get)
    plus = [w * 1.2 for w in weights]
    minus = [w * 0.8 for w in weights]
    plus = [w / sum(plus) for w in plus]
    minus = [w / sum(minus) for w in minus]
    winner_plus = max(scores(plus, deployment), key=scores(plus, deployment).get)
    winner_minus = max(scores(minus, deployment), key=scores(minus, deployment).get)
    print("\\nDeployment:", deployment)
    print("Scores:", {k: round(v, 2) for k, v in base.items()})
    print("Primary choice:", winner)
    print("Winner with all weights +20%:", winner_plus)
    print("Winner with all weights -20%:", winner_minus)

print("\\nNote: Ratings and weights are stated design assumptions, not standards data.")
print("Real networks commonly combine access methods to balance their strengths.")
