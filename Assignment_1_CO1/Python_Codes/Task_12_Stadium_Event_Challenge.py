"""Task 12 - Stadium event surge evaluation and temporary adaptation.
Erlang-B based illustrative calculation; standard library only.
Run: python Task_12_Stadium_Event_Challenge.py
"""
import math

def erlang_b(m,a):
    b=1.0
    for k in range(1,m+1): b=a*b/(k+a*b)
    return b

def capacity_at_blocking(channels,target=.02):
    lo,hi=0.0,max(1.0,channels*5.0)
    for _ in range(70):
        mid=(lo+hi)/2
        if erlang_b(channels,mid)<=target: lo=mid
        else: hi=mid
    return lo

def main():
    attendees=25000; traffic_each=.05; stadium_area=1.0
    surge=attendees*traffic_each
    baseline_users=10000; base_traffic=baseline_users*.025
    print('TASK 12 - STADIUM EVENT DESIGN CHALLENGE')
    print('Event attendees:',attendees,'| traffic per attendee:',traffic_each,'Erlang')
    print('Event offered traffic: %.1f Erlangs in %.1f km^2 (%.1f Erlang/km^2)' % (surge,stadium_area,surge/stadium_area))
    print('For comparison, 10,000 township subscribers offer %.1f Erlangs over 12 km^2 (%.2f Erlang/km^2).' % (base_traffic,base_traffic/12.0))
    print('\nIllustrative local stadium capacity using N=7, 336 total channels:')
    channels=336//7
    baseline_cap=capacity_at_blocking(channels)
    print('Fixed reuse channels per cell:',channels,'| capacity at 2%% blocking: %.2f Erlangs/cell' % baseline_cap)
    # One stadium cell at N=7 is grossly overloaded. Three temporary small cells share the local load.
    print('Unchanged single-cell blocking at event load: %.4f' % erlang_b(channels,surge))
    temp_cells=3
    # Assume 3 temporary microcells, each receives one third of the event traffic and 48 channels
    # from temporary/local channel pool; this is an explicit planning assumption, not extra spectrum.
    temp_channels=48
    per_cell=surge/temp_cells
    print('\nTemporary redesign: 3 microcells in stadium zone, 48 channels per microcell from borrowed/replanned local pool.')
    print('Traffic per microcell: %.2f Erlangs | Erlang-B blocking: %.4f' % (per_cell,erlang_b(temp_channels,per_cell)))
    print('Aggregate 2%%-blocking capacity of 3 microcells: %.2f Erlangs' % (temp_cells*capacity_at_blocking(temp_channels)))
    print('Capacity shortfall vs event traffic: %.2f Erlangs' % max(0,surge-temp_cells*capacity_at_blocking(temp_channels)))
    print('\nRecommendation: MODIFY temporarily with pre-planned microcells/COW and sectoring; avoid permanent township-wide densification.')
    print('Important: borrowed channels must be taken from lightly loaded neighbouring cells; total licensed spectrum remains 336.')
    print('Assumptions: equal load split, no inter-cell interference penalty in Erlang-B, and 48 channels/cell is a planning scenario.')
if __name__=='__main__': main()
