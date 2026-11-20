MOBILE COMPUTING - ASSIGNMENT 1 (CO1)
Separate Python programs and output reference images

CONTENTS
Python_Codes/
  Task_8_Cell_Planning_Simulator.py
  Task_9_Experimental_Metrics_and_Plots.py
  Task_10_Theory_vs_Simulation.py
  Task_12_Stadium_Event_Challenge.py
Output_Images/
  Matching program-output images
  Task_9_Blocking_vs_Load.png
  Task_9_Capacity_vs_Cluster.png
Task_9_metrics.csv and matching .txt output files are also included.

HOW TO RUN
1. Extract this ZIP.
2. Open one .py file at a time in Programiz Online Python Compiler.
3. Copy the complete code and click Run.
4. Each program is independent and uses only the Python standard library.

TASK COVERAGE
- Task 8: hexagonal cell-area/site estimate, valid cluster-size enumeration, Erlang-B, subscriber scaling, Monte-Carlo first-tier SIR, sectoring comparison, dynamic channel-borrowing demonstration and the required N=7,n=4 sanity check.
- Task 9: comparable blocking/capacity metrics and a CSV file (created in the current working folder when run). SIR mean/5th-percentile/outage measurements are printed by Task 8. Two supporting plots are included.
- Task 10: analytical six-interferer SIR compared with Monte-Carlo user-position results.
- Task 12: event traffic calculation and a temporary stadium microcell adaptation scenario, including the capacity shortfall under the fixed spectrum constraint.

IMPORTANT ASSIGNMENT NOTE
Tasks 1-7 and Task 11 mainly require written derivations, design explanations and language-independent pseudocode. They are not converted into Python because the assignment asks for analytical evidence. Task 8 is the main implementation task; Tasks 9, 10 and 12 use the simulator's evidence.

MODEL ASSUMPTIONS / LIMITATIONS
These are educational, reproducible models, not a production radio-planning tool. The SIR model uses six first-tier co-channel sites and idealised geometry; it does not model terrain, detailed shadowing, fading or real channel maps. Sectoring uses a simplified 120-degree angular filter. Erlang-B assumes Poisson arrivals and an ideal loss system. The Task 12 three-microcell scenario assumes equal load split and a 48-channel local allocation per microcell; borrowed channels are reallocated from lightly loaded cells, not added to the licensed 336-channel total. The event's 1,250 Erlangs greatly exceeds the illustrative 2%-blocking capacity, so the script explicitly reports the shortfall and recommends prioritisation/admission control and Wi-Fi/data offload rather than claiming the full event load can be served. State these assumptions in your report and validate/adjust them with your own chosen design parameters.

The PNGs are reference renderings of the programs' terminal output and supporting charts, not screenshots from Programiz.
