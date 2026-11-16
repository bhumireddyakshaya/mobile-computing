# TASK 1: Mobile Communication or Mobile Computing?
# Simple classification and store-and-forward simulation
import random

cases = [
    ("Rugged tablet using cellular data", "mobile", "mobile communication + computing"),
    ("Laptop plugged into Ethernet at offices", "nomadic", "mainly mobile computing"),
    ("Fixed wireless router at substation", "fixed-wireless", "mainly mobile communication"),
    ("Push-to-talk handset", "mobile", "mainly mobile communication"),
    ("Offline meter-reading tablet", "mobile", "mainly mobile computing"),
    ("Own case: laptop in a moving train using Wi-Fi", "mobile", "both communication and computing")
]

print("TASK 1 - CLASSIFICATION")
for name, category, type_name in cases:
    print(name, "=>", category, "|", type_name)

# Simulate 100 meter updates. Immediate-send loses an update if disconnected.
# Store-and-forward keeps it until a connection returns.
print("\\nSTORE-AND-FORWARD SIMULATION (100 updates)")
for availability in [0.90, 0.60, 0.30]:
    random.seed(10)
    immediate_delivered = 0
    immediate_lost = 0
    queued_delivered = 0
    delayed = 0
    queue = []
    delays = []

    for minute in range(100):
        connected = random.random() < availability
        # One new meter reading is generated every minute.
        if connected:
            immediate_delivered += 1
            if queue:
                delayed += len(queue)
                delays.extend([minute - created for created in queue])
                queued_delivered += len(queue)
                queue = []
            queued_delivered += 1
            delays.append(0)
        else:
            immediate_lost += 1
            queue.append(minute)

    # Assume connectivity returns at the end so queued readings are delivered.
    if queue:
        delayed += len(queue)
        delays.extend([100 - created for created in queue])
        queued_delivered += len(queue)

    mean_delay = sum(delays) / len(delays) if delays else 0
    print("\\nLink availability:", int(availability * 100), "%")
    print("Immediate: delivered =", immediate_delivered, "lost =", immediate_lost)
    print("Queue: delivered =", queued_delivered, "delayed =", delayed,
          "lost = 0, mean delay =", round(mean_delay, 2), "minutes")

print("\\nConclusion: Offline storage protects data during disconnections.")
