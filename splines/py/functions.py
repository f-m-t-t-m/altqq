import math

functions = [lambda x: 2*x**3 + 3*x**2,
             lambda x: 1-(math.e**(100*x)-math.e**(-100*x))/(math.e**100 - math.e**(-100)),
             lambda x: 2 - math.sqrt(2*x-x*x),
             lambda x: math.e**(-500*x**2)/(math.sqrt(2*math.pi)*0.1),
             lambda x: x**4 + x**3]
derives = [lambda x: 6*x**2 + 6*x,
           lambda x: -(100*math.e**(100*x)+100*math.e**(-100*x))/(math.e**100 - math.e**(-100)),
           lambda x: (x-1)/(math.sqrt(2*x-x*x)),
           lambda x: -1000*x*math.e**(-500*x**2)/(math.sqrt(2*math.pi)*0.1),
           lambda x: 4*x**3 + 3*x**2]
derives2 = [lambda x: 12*x + 6,
            lambda x: -(10000*math.e**(100*x)-10000*math.e**(-100*x))/(math.e**100 - math.e**(-100)),
            lambda x: math.sqrt(2*x-x*x)/(x**4-4*x**3+4*x**2+0.0000001),
            lambda x: ((1000*x)**2-1000)*math.e**(-500*x**2)/(math.sqrt(2*math.pi)*0.1),
            lambda x: 13*x**2 + 6*x]
