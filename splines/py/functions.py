import math

functions = [lambda x: 2*x**3 + 3*x**2,
             lambda x: 1-(math.e**(100*x)-math.e**(-100*x))/(math.e**100 - math.e**(-100)),
             lambda x: math.cos(10*x),
             lambda x: math.fabs(math.cos(3*x)),
             lambda x: 2 - math.sqrt(2*x-x**2)]
derives = [lambda x: 6*x**2 + 6*x,
           lambda x: -(100*math.e**(100*x)+100*math.e**(-100*x))/(math.e**100 - math.e**(-100)),
           lambda x: -10*math.sin(10*x),
           lambda x: 3*math.sin(3*x) if math.cos(3*x) < 0 else -3*math.sin(3*x),
           lambda x: (x-1)/math.sqrt(2*x - x**2)]
derives2 = [lambda x: 12*x + 6,
            lambda x: -(10000*math.e**(100*x)-10000*math.e**(-100*x))/(math.e**100 - math.e**(-100)),
            lambda x: -100*math.cos(10*x),
            lambda x: -9*math.cos(3*x) if math.cos(3*x) < 0 else 9*math.cos(3*x),
            lambda x: math.sqrt(2*x - x**2) / (x**4 - 4*x**3 + 4*x**2)]
