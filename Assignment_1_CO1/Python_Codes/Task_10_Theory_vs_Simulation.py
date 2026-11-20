"""Task 10 - Compare analytical SIR approximation with a Monte-Carlo first-tier model.
Standard-library only; deterministic seed. Run: python Task_10_Theory_vs_Simulation.py
"""
import math, random

def analytical_sir_db(n, exponent):
    # Six equidistant first-tier interferers; D/R=sqrt(3N).
    return 10*math.log10((math.sqrt(3*n)**exponent)/6.0)

def monte_carlo_sir_db(n, exponent, samples=4000, seed=2026):
    rng=random.Random(seed+n*17+int(exponent*10))
    d=math.sqrt(3*n)
    sites=[(d*math.cos(k*math.pi/3),d*math.sin(k*math.pi/3)) for k in range(6)]
    vals=[]
    for _ in range(samples):
        r=math.sqrt(rng.random())*0.95; a=rng.random()*2*math.pi
        x,y=r*math.cos(a),r*math.sin(a); desired=max(r,0.05); interference=0.0
        for sx,sy in sites:
            dist=max(math.hypot(sx-x,sy-y),0.05)
            interference+=(desired/dist)**exponent
        vals.append(10*math.log10(1/max(interference,1e-15)))
    vals.sort()
    return sum(vals)/len(vals), vals[int(.05*(len(vals)-1))]

def main():
    print('TASK 10 - THEORY VS SIMULATION')
    print('Theory: six equidistant interferers at D/R=sqrt(3N). Simulation: random mobile positions in serving cell.')
    print('%-5s %-5s %-13s %-13s %-13s %-13s' % ('N','n','Theory dB','Sim mean dB','Sim 5th dB','Mean gap dB'))
    for n in (3,4,7,12):
        for exp in (2.5,3.0,4.0):
            theory=analytical_sir_db(n,exp); mean,p5=monte_carlo_sir_db(n,exp)
            print('%-5d %-5.1f %-13.2f %-13.2f %-13.2f %-13.2f' % (n,exp,theory,mean,p5,mean-theory))
    print('\nInterpretation: the analytical value assumes six equal-distance interferers and a cell-edge reference geometry.')
    print('The Monte-Carlo mean changes with mobile position; the 5th percentile exposes vulnerable locations.')
    print('Differences are expected from user-position geometry and the finite first-tier model; shadowing is not included.')
    print('Known check: N=7, n=4 gives %.2f dB analytically (about 18.7 dB).' % analytical_sir_db(7,4))
if __name__=='__main__': main()
