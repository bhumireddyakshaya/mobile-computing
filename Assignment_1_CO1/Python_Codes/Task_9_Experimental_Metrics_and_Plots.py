"""Task 9 - Record comparable performance metrics and create CSV data.
Uses only the Python standard library. Run: python Task_9_Experimental_Metrics_and_Plots.py
"""
import math, csv

def erlang_b(m,a):
    b=1.0
    for k in range(1,m+1): b=a*b/(k+a*b)
    return b

def max_traffic(m,target=0.02):
    lo,hi=0.0,max(1.0,m*4.0)
    for _ in range(60):
        mid=(lo+hi)/2
        if erlang_b(m,mid)<=target: lo=mid
        else: hi=mid
    return lo

def main():
    rows=[]
    area=12.0; radius=0.75; cell_area=3*math.sqrt(3)*radius*radius/2
    sites=math.ceil(area/cell_area)
    for n in (3,4,7,12):
        channels=336//n
        capacity=max_traffic(channels)
        for users in (1000,10000,20000,100000):
            total_erlangs=users*0.025
            offered_per_cell=total_erlangs/sites
            blocking=erlang_b(channels,offered_per_cell)
            rows.append({'strategy':'Fixed reuse','cluster_N':n,'users':users,'sites':sites,
                         'channels_per_cell':channels,'offered_Erlang_per_cell':round(offered_per_cell,4),
                         'blocking_probability':round(blocking,6),'capacity_Erlang_per_cell_at_2pct':round(capacity,4),
                         'system_capacity_Erlang':round(capacity*sites,3)})
    with open('Task_9_metrics.csv','w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0].keys())); writer.writeheader(); writer.writerows(rows)
    print('TASK 9 - EXPERIMENTAL METRICS')
    print('Assumptions: 12 km^2, R=0.75 km, 336 channels, 0.025 Erlang/user, 2% blocking target')
    print('Estimated sites:',sites)
    print('%-5s %-9s %-8s %-10s %-12s %-12s' % ('N','Users','Ch/cell','Offered E','Blocking','Capacity E'))
    for r in rows:
        if r['users'] in (1000,100000):
            print('%-5d %-9d %-8d %-10.3f %-12.4f %-12.3f' % (r['cluster_N'],r['users'],r['channels_per_cell'],r['offered_Erlang_per_cell'],r['blocking_probability'],r['system_capacity_Erlang']))
    print('\nCSV saved as Task_9_metrics.csv in the current folder.')
    print('SIR mean/5th-percentile/outage are produced by Task 8; use those alongside this CSV.')
    print('Note: CSV blocking values assume uniform traffic across estimated sites.')
if __name__=='__main__': main()
