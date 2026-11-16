# TASK 2: Sharing the Channel - FDMA vs TDMA
# Illustrative dedicated-channel allocation simulation

TOTAL_CHANNELS = 80
FDMA_GUARD_OVERHEAD = 0.10
TDMA_CONTROL_OVERHEAD = 0.10
fdma_usable = int(TOTAL_CHANNELS * (1 - FDMA_GUARD_OVERHEAD))
tdma_usable = int(TOTAL_CHANNELS * (1 - TDMA_CONTROL_OVERHEAD))

print("TASK 2 - FDMA vs TDMA CAPACITY")
print("Nominal channels:", TOTAL_CHANNELS)
print("FDMA usable after 10% guard-band allowance:", fdma_usable)
print("TDMA usable after 10% slot/control allowance:", tdma_usable)

# Each traffic list represents simultaneous channel requests in a time interval.
traffic_sets = {
    "Continuous voice": [50, 60, 70, 75, 65, 55],
    "Bursty data (10% duty)": [8, 4, 12, 5, 10, 3],
    "70/30 voice-data mix": [55, 62, 68, 74, 70, 60],
    "Edge case: short synchronised bursts": [10, 10, 10, 80, 10, 10]
}

for name, demand_values in traffic_sets.items():
    print("\\nTraffic:", name)
    for scheme, capacity in [("FDMA", fdma_usable), ("TDMA", tdma_usable)]:
        requested = sum(demand_values)
        served = sum(min(demand, capacity) for demand in demand_values)
        blocked = sum(max(0, demand - capacity) for demand in demand_values)
        allocated_capacity = capacity * len(demand_values)
        utilisation = served / allocated_capacity * 100
        wasted = allocated_capacity - served
        print(scheme, "served =", served, "blocked =", blocked,
              "utilisation =", round(utilisation, 1), "%",
              "wasted channel-slots =", wasted)

print("\\nDecision: For tiny periodic sensor reports, shared or scheduled access")
print("is usually more efficient than reserving a dedicated channel per device.")
print("Assumption: both schemes have equal illustrative 10% overhead.")
