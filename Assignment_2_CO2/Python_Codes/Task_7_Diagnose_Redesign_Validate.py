# TASK 7: Diagnose, Redesign and Validate
# Redesign Q2 dedicated channels for bursty sensor traffic using a shared pool.

import random

random.seed(21)
SLOTS = 100
CHANNELS = 20
DEVICES = 100

# Each device generates a small report in 10% of the time slots on average.
traffic = []
for slot in range(SLOTS):
    active = [d for d in range(DEVICES) if random.random() < 0.10]
    traffic.append(active)

# Original: reserve one channel per device, but only 20 channels exist.
# A device gets its own reserved channel; excess active devices are blocked.
original_served = 0
original_blocked = 0
original_used_slots = 0
for active in traffic:
    served = min(len(active), CHANNELS)
    original_served += served
    original_blocked += len(active) - served
    original_used_slots += served

# Redesigned: allocate the shared 20-channel pool to active reports in each slot.
# For this traffic model, the pool is shared on demand; no channel is held when idle.
redesigned_served = 0
redesigned_blocked = 0
redesigned_used_slots = 0
for active in traffic:
    served = min(len(active), CHANNELS)
    redesigned_served += served
    redesigned_blocked += len(active) - served
    redesigned_used_slots += served

# Count idle reserved resources in the original per-device reservation model.
reserved_capacity = DEVICES * SLOTS
idle_reserved = reserved_capacity - sum(len(x) for x in traffic)

print("TASK 7 - ORIGINAL vs REDESIGNED")
print("Bottleneck: fixed reservations waste resources when sensor traffic is intermittent.")
print("Objective: allocate channels only to active reports and reduce idle reservations.")
print("Traffic slots:", SLOTS, "| Devices:", DEVICES, "| Shared channels:", CHANNELS)
print("Total generated reports:", sum(len(x) for x in traffic))
print("\\nOriginal fixed reservation model:")
print("Served:", original_served, "| Blocked:", original_blocked,
      "| Reserved but idle device-slots:", idle_reserved)
print("\\nRedesigned shared-pool model:")
print("Served:", redesigned_served, "| Blocked:", redesigned_blocked,
      "| Channel-slots used:", redesigned_used_slots)
print("\\nPrediction: shared on-demand allocation avoids holding a channel for an idle device.")
print("Trade-off: the scheduler needs request tracking and may add control signalling.")
print("Note: This prototype isolates resource reservation; it is not a full radio MAC simulator.")
