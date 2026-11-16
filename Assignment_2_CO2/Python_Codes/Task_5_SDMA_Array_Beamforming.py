# TASK 5: SDMA - Reusing the Same Channel in Different Directions
# Uniform linear array (ULA) beam-pattern simulation

import math

def array_gain(n, steer_deg, user_deg):
    # Half-wavelength element spacing; normalized array factor.
    psi = math.pi * (math.sin(math.radians(user_deg)) -
                     math.sin(math.radians(steer_deg)))
    if abs(math.sin(psi / 2)) < 1e-10:
        return 1.0
    value = math.sin(n * psi / 2) / (n * math.sin(psi / 2))
    return value * value

print("TASK 5 - SDMA ARRAY PATTERN")
print("Assumption: half-wavelength spacing; SIR threshold = 10 dB.")
threshold = 10
for n in [2, 4, 8, 16]:
    print("\\nNumber of antenna elements:", n)
    # Evaluate a user B at increasing angular separation from beam-steered user A.
    minimum = None
    for separation in range(5, 61, 5):
        desired = 1.0
        interference = array_gain(n, 0, separation)
        sir = 10 * math.log10(desired / max(interference, 1e-12))
        print("Separation", separation, "degrees -> SIR", round(sir, 2), "dB")
        if sir >= threshold and minimum is None:
            minimum = separation
    print("Minimum tested separation meeting threshold:", minimum, "degrees")

print("\\nLarger arrays form narrower beams, improving angular separation.")
print("Users in nearly the same direction are difficult to separate.")
print("At a toll plaza, clustered vehicle directions limit SDMA effectiveness.")
