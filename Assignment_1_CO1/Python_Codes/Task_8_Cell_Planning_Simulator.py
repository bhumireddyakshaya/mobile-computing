"""Task 8 - Hexagonal cellular planning simulator (standard-library only).
Illustrative first-tier model; assumptions are printed with the results.
Run: python Task_8_Cell_Planning_Simulator.py
"""
import math, random

AREA_KM2 = 12.0
TOTAL_CHANNELS = 336
SUBSCRIBER_LEVELS = [1000, 10000, 20000, 100000]
CLUSTER_SIZES = [3, 4, 7, 12]
PATH_LOSS_EXPONENTS = [2.5, 3.0, 4.0]
CELL_RADIUS_KM = 0.75
TRAFFIC_PER_SUBSCRIBER = 0.025
BLOCKING_TARGET = 0.02
SIR_THRESHOLD_DB = 12.0
MONTE_CARLO_SAMPLES = 2500
SEED = 2026

def erlang_b(channels, traffic):
    """Recursive Erlang-B formula, numerically stable for integer channels."""
    b = 1.0
    for m in range(1, max(0, channels) + 1):
        b = (traffic * b) / (m + traffic * b)
    return b

def max_traffic(channels, target=BLOCKING_TARGET):
    if channels <= 0: return 0.0
    lo, hi = 0.0, max(1.0, float(channels) * 4.0)
    for _ in range(70):
        mid = (lo + hi) / 2.0
        if erlang_b(channels, mid) <= target: lo = mid
        else: hi = mid
    return lo

def hex_cell_count(area, radius):
    cell_area = (3.0 * math.sqrt(3.0) / 2.0) * radius * radius
    return math.ceil(area / cell_area), cell_area

def valid_cluster_sizes(limit=12):
    return sorted({i*i + i*j + j*j for i in range(0, limit+1)
                   for j in range(0, limit+1)
                   if i*i + i*j + j*j > 0 and i*i + i*j + j*j <= limit})

def monte_carlo_sir(cluster_n, exponent, sectored=False, samples=MONTE_CARLO_SAMPLES, seed=SEED):
    """Six first-tier co-channel sites at D=R*sqrt(3N); sectoring keeps in-beam sites."""
    rng = random.Random(seed + int(cluster_n*100) + int(exponent*10))
    reuse_distance = math.sqrt(3.0 * cluster_n)  # normalised by R
    interferers = [(reuse_distance*math.cos(k*math.pi/3), reuse_distance*math.sin(k*math.pi/3)) for k in range(6)]
    values=[]
    for _ in range(samples):
        radius = math.sqrt(rng.random()) * 0.95
        angle = rng.random() * 2.0 * math.pi
        ux, uy = radius*math.cos(angle), radius*math.sin(angle)
        desired = max(math.hypot(ux,uy), 0.05)
        total_i = 0.0
        for bx, by in interferers:
            dx, dy = bx-ux, by-uy
            bearing = math.atan2(dy,dx)
            # A 120-degree receive/transmit sector centred on the serving direction.
            rel = (bearing-angle+math.pi) % (2*math.pi) - math.pi
            if not sectored or abs(rel) <= math.pi/3:
                dist=max(math.hypot(dx,dy),0.05)
                total_i += (desired/dist)**exponent
        sir_db = 10.0*math.log10(1.0/max(total_i,1e-15))
        values.append(sir_db)
    values.sort()
    mean=sum(values)/len(values)
    p5=values[int(0.05*(len(values)-1))]
    outage=sum(v < SIR_THRESHOLD_DB for v in values)/len(values)
    return mean,p5,outage

def main():
    print('TASK 8 - CELLULAR PLANNING STRATEGY SIMULATOR')
    print('Township=12 km^2 | spectrum=336 duplex traffic channels | R=0.75 km')
    print('Traffic=0.025 Erlang/subscriber | Erlang-B target=2% | seed=2026')
    cells, cell_area=hex_cell_count(AREA_KM2,CELL_RADIUS_KM)
    print('Hexagonal cell area: %.3f km^2 | estimated sites: %d' % (cell_area,cells))
    print('Valid cluster sizes up to 12:', valid_cluster_sizes())
    print('\nSubscriber scaling (fixed reuse; channels/cell=floor(336/N))')
    print('%-8s %-5s %-8s %-12s %-12s' % ('Users','N','Ch/cell','Offered E/cell','Blocking'))
    for users in SUBSCRIBER_LEVELS:
        offered=users*TRAFFIC_PER_SUBSCRIBER/cells
        for n in [3,4,7,12]:
            ch=TOTAL_CHANNELS//n
            print('%-8d %-5d %-8d %-12.3f %-12.4f' % (users,n,ch,offered,erlang_b(ch,offered)))
    print('\nMonte-Carlo SIR comparison (same deterministic seed family)')
    print('%-5s %-5s %-12s %-12s %-10s %-12s' % ('N','n','Fixed mean dB','Fixed 5th dB','Fixed outage','120deg outage'))
    for n in CLUSTER_SIZES:
        for exp in PATH_LOSS_EXPONENTS:
            mean,p5,out=monte_carlo_sir(n,exp,False)
            _,_,sec_out=monte_carlo_sir(n,exp,True)
            print('%-5d %-5.1f %-12.2f %-12.2f %-10.3f %-12.3f' % (n,exp,mean,p5,out,sec_out))
    sanity=10*math.log10((math.sqrt(3*7)**4)/6)
    print('\nSanity check N=7, n=4, six equidistant interferers: %.2f dB (expected about 18.7 dB)' % sanity)
    print('\nDynamic channel-borrowing test (three-cell cluster; total remains 144 channels)')
    high_load, neighbour_load, borrowed = 60.0, 5.0, 15
    fixed_block = erlang_b(48, high_load)
    borrowed_block = erlang_b(48 + 2*borrowed, high_load)
    neighbour_block = erlang_b(48-borrowed, neighbour_load)
    print('High-demand cell: 60 E | neighbour cells: 5 E each | borrow 15 channels from each neighbour')
    print('High-cell blocking: fixed=%.4f, after borrowing=%.4f' % (fixed_block, borrowed_block))
    print('Each neighbour retains 33 channels; blocking at 5 E = %.6f' % neighbour_block)
    print('The 144-channel three-cell pool is conserved; borrowing helps only when neighbours have spare capacity.')
    print('Model limits: idealised first tier, no terrain/shadowing, illustrative uniform users.')

if __name__=='__main__': main()
