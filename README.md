Example of dimensional analysis and conversions
===============================================

Example:

    >>> a = Number(10,dims='meter/second')
    >>> b = Number(2,dims='yard/minute')
    >>> c = a + b
    >>> print c.convert('kilometer/hour')
    (36.109728 ± 0)

    >>> print c.value, c.error
    10.03048 0.0

Without conversion results are alwayws in:
  meters, seconds, grams, ampere, kelvin, dollar (and combination)

The error is the standard deviation assuming the true value
is Normal distributed

Error propagation assumes independence

    >>> a = Number(1,dims='decimeter^3')
    >>> b = Number(2,dims='liter')
    >>> c = Number(5,dims='gram/centimeter^3')
    >>> d = (a + b)*c
    >>> print d.convert('kilogram')
    (15.000000 ± 0)

Example of formula validation

    >>> a = Number(10,dims='meter/second')
    >>> b = Number(2,dims='yard^3')
    >>> c = a + b
    Traceback (most recent call last):
    ...
    RuntimeError: Incompatible Dimentions

Examples of error propagation:

    >>> a = Number(10,error=2,dims='meter/second') # (10±2)m/s
    >>> b = Number(5,error=1,dims='hour')  # (5±1)h
    >>> c = a*b
    >>> print c.convert('kilometer')
    (1.800 ± 0.509)x10^2
    >>> print c.convert('kilometer').value
    180.0
    >>> print c.convert('kilometer').error
    50.9116882454

Examples of more complex formulas

    >>> print a**4/(7*b)
    (7.94 ± 6.54)/10^2

(last result is implicitely in meter**4/second**5)

Financial application example:

    >>> coupon = Number(200,error=1,dims="dollar/day")
    >>> expiration = Number(1,error=0,dims="year")
    >>> payoff = coupon*expiration
    >>> print payoff.convert('dollar')
    (7.3048 ± 0.0365)x10^4

I.e. $73048 dollars with $365 dollas of one sigma uncertainly
    
