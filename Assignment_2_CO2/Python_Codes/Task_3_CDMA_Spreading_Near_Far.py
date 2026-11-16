# TASK 3: CDMA - Spreading, Despreading and Near-Far Problem
# Simplified synchronous DS-CDMA correlation model

import random

def walsh_codes(length):
    codes = [[1]]
    while len(codes) < length:
        old = codes
        codes = []
        for row in old:
            codes.append(row + row)
        for row in old:
            codes.append(row + [-x for x in row])
    return codes[:length]

def correlation(a, b):
    return sum(x * y for x, y in zip(a, b)) / len(a)

random.seed(7)
print("TASK 3 - CDMA SIMULATION")
for length in [8, 16, 64]:
    codes = walsh_codes(length)
    print("\\nSpreading length:", length, "| Processing gain:", length, "=", round(10 * __import__('math').log10(length), 2), "dB")
    print("Correlation of first two Walsh codes:", round(correlation(codes[0], codes[1]), 3))

    # Use one desired user and add interference from other users.
    # A simple threshold detector illustrates how correlation and power affect errors.
    for condition in ["Orthogonal synchronous", "Random non-orthogonal", "Orthogonal with 10x near-far user"]:
        errors = 0
        total_bits = 200
        users = min(6, length)
        for _ in range(total_bits):
            desired_bit = random.choice([-1, 1])
            if condition == "Orthogonal synchronous":
                interference = 0
            elif condition == "Random non-orthogonal":
                interference = random.uniform(-0.9, 0.9) * (users - 1) / max(1, length / 8)
            else:
                interference = random.choice([-1, 1]) * 0.35
            received = desired_bit + interference
            detected = 1 if received >= 0 else -1
            if detected != desired_bit:
                errors += 1
        print(condition + ":", "users =", users, "bits =", total_bits,
              "bit errors =", errors, "BER =", round(errors / total_bits, 3))

print("\\nNote: This is a teaching model, not a full RF channel simulator.")
print("Power control reduces near-far interference; synchronisation preserves code orthogonality.")
