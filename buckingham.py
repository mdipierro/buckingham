#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This module implement:

- dimensional analysis
- formula validation
- units conversion
- error propagation

Developed by Massimo Di Pierro

Projects gets it name from
http://en.wikipedia.org/wiki/Buckingham_%CF%80_theorem Buckingham

Should work with 2.4,..,2.7 and (almost) 3.x
"""

import re
import math

__all__ = ['Number', 'allunits', 'pm', 'exp', 'log', 'sin', 'cos']

class Fraction:
    @staticmethod
    def gcd(x, y):
        g = y
        while x > 0:
            g = x
            x = y % x
            y = g
        return g
    def __init__(self,x,y='1'):
        z=(str(x)+'/'+str(y)).split('/')[:2]
        self.n,self.d = int(float(z[0])),int(float(z[1]))
        if self.d<0:
            self.n,self.d = -self.n,-self.d
        m = self.n and self.gcd(abs(self.n),abs(self.d)) or 1
        self.n, self.d = self.n/m, self.d/m
    def __add__(self,other):
        if not isinstance(other,Fraction):
            other=Fraction(other)
        return Fraction(self.n*other.d+other.n*self.d,self.d*other.d)
    def __radd__(self,other):
        return self+other
    def __sub__(self,other):
        if not isinstance(other,Fraction):
            other=Fraction(other)
        return Fraction(self.n*other.d-other.n*self.d,self.d*other.d)
    def __mul__(self,other):
        if not isinstance(other,Fraction):
            other=Fraction(other)
        return Fraction(self.n*other.n,self.d*other.d)
    def __rmul__(self,other):
        return self*other
    def __div__(self,other):
        if not isinstance(other,Fraction):
            other=Fraction(other)
        return Fraction(self.n/other.d,self.d/other.n)
    def __eq__(self,other):
        if not isinstance(other,Fraction):
            other=Fraction(other)
        return self.n*other.d==self.d*other.n
    def __str__(self):
        if self.d==0:
            return '0'
        if self.d==1:
            return str(self.n)
        return '%s/%s' % (self.n,self.d)
    def __float__(self):
        if self.n==0: return 0.0
        return float(self.n)/self.d
    

UNITS = {
    'N': (1.0,0,0,0,0,0,0), # none
    'L': (1.0,1,0,0,0,0,0), # meter
    'T': (1.0,0,1,0,0,0,0), # second
    'M': (1.0,0,0,1,0,0,0), # gram
    'A': (1.0,0,0,0,1,0,0), # ampere
    'K': (1.0,0,0,0,0,1,0), # kelvin
    'D': (1.0,0,0,0,0,0,1), # dollar
    'none': (1.0,0,0,0,0,0,0), # none
    'pure': (1.0,0,0,0,0,0,0), # none
    'meter':  (1.0,1,0,0,0,0,0), # meter
    'second': (1.0,0,1,0,0,0,0), # second
    'gram':   (1.0,0,0,1,0,0,0), # gram
    'ampere': (1.0,0,0,0,1,0,0), # ampere
    'kelvin': (1.0,0,0,0,0,1,0), # kelvin
    'dollar': (1.0,0,0,0,0,0,1), # dollar
    'currency': (1.0,0,0,0,0,0,1), # currency
    'coulomb': (1.0,0,1,0,1,0,0), # one ampere x 1 second
    'angstrom': (10**-10,1,0,0,0,0,0),
    'atm': (101325000.0,-1,-2,1,0,0,0),
    'au':  (149597870691.0,1,0,0,0,0,0),
    'bar': (100000000.0,-1,-2,1,0,0,0),
    'coulomb':(1.0,0,1,0,1,0,0),
    'day':(86400.0,0,1,0,0,0,0),
    'ev':(1.602176487e-16,2,-2,1,0,0,0),
    'eV':(1.602176487e-16,2,-2,1,0,0,0),
    'farad':(1000.0,-2,4,-1,2,0,0),
    'faraday':(9.64853399e4,0,1,0,1,0,0),    
    'foot':(381./1250,1,0,0,0,0,0),
    'hour':(3600.0,0,1,0,0,0,0),
    'henry':(1000.0,2,-2,1,-2,0,0),
    'hz':(1.0,0,-1,0,0,0,0),
    'inch':(127./5000.,1,0,0,0,0,0),
    'point':(127./360000,1,0,0,0,0,0),
    'joule':(1000.0,2,-2,1,0,0,0),
    'calorie':(4186.8,2,-2,1,0,0,0),
    'lightyear':(9460730472580800.0,1,0,0,0,0,0),
    'liter':(0.001,3,0,0,0,0,0),
    'mho':(0.001,-2,3,-1,2,0,0),
    'mile':(201168./125,1,0,0,0,0,0),
    'minute':(60.0,0,1,0,0,0,0),
    'mmhg':(133322.387415,-1,-2,1,0,0,0),
    'newton':(1000.0,1,-2,1,0,0,0),
    'ohm':(1000.0,2,-3,1,-2,0,0),
    'pascal':(1000.0,-1,-2,1,0,0,0),
    'pound':(4448.2216152605,1,-2,1,0,0,0),
    'psi':(6894757.29316836,-1,-2,1,0,0,0),
    'quart':(473176473./125000000000,3,0,0,0,0,0),
    'siemens':(0.001,-2,3,-1,2,0,0),
    'volt':(1000.0,2,-3,1,-1,0,0),
    'watt':(1000.0,2,-3,1,0,0,0),
    'weber':(1000.0,2,-2,1,-2,0,0),
    'yard':(1143./1250,1,0,0,0,0,0),
    'year':(3944615652./125,0,1,0,0,0,0),
    'fermi':(10.0**-15,1,0,0,0,0,0),
}

def extend_units(units):
    scales =  [
        ('yocto',10.0**-24),
        ('zepto',10.0**-21),
        ('atto',10.0**-18),
        ('femto',10.0**-15),
        ('pico',10.0**-12),
        ('nano',10.0**-9),
        ('micro',10.0**-6),
        ('milli',10.0**-3),
        ('centi',10.0**-2),
        ('deci',0.1),
        ('deka',10.0),
        ('hencto',10.0**2),
        ('kilo',10.0**3),
        ('mega',10.0**6),
        ('giga',10.0**9),
        ('tera',10.0**12),
        ('peta',10.0**15),
        ('exa',10.0**18),
        ('zetta',10.0**21),
        ('votta',10.0**24),
        ]
    keys = [key for key in units]
    for name, conversion in scales:
        for key in keys:
            if not key in ('N','M','T','M','A','K','D','none','None'):
                v = units[key]
                units[name+key] = (v[0]*conversion,v[1],v[2],v[3],v[4],v[5],v[6])
extend_units(UNITS)

def buckingham(units,d):
    items = units.split('/')
    numerator = items[0].split('*')
    denominator = items[1:]
    power = Fraction(0)
    for item in numerator:
        x = item.split('^')
        if not x[0] in d:
            raise RuntimeError("Unknown units")
        if len(x) == 1:
            power=power+d[x[0]]
        else:
            power=power+d[x[0]]*Fraction(x[1])
    for item in denominator:
        x = item.split('^')
        if not x[0] in d:
            raise RuntimeError("Unknown units")
        if len(x) == 1:
            power = power-d[x[0]]
        else:
            power = power-d[x[0]]*Fraction(x[1])
    return power

def int_safe(x):
    if not x:
        return 0
    x = math.log10(x)
    i = int(x)
    if x == i or x>0:
        return i
    return i-1

class Number:
    """
    Example of dimensional analysis and conversions

    >>> a = Number(10,dims = 'meter/second')
    >>> b = Number(2,dims = 'yard/minute')
    >>> c = a + b
    >>> print(c.convert('kilometer/hour'))
    (36.109728 ± 0)

    >>> Number(1,dims = 'joule').convert('eV').value
    6.2415096471204178e+18

    >>> print("%s %s %s" % (c.value, c.error, c.units()))
    10.03048 0.0 meter*second^-1

    Without conversion results are always in:
      meters, seconds, grams, ampere, kelvin, currency (and combination)

    The error is the standard deviation assuming the true value
    is Normal distributed

    Error propagation assumes independence

    >>> a = Number(1,dims = 'decimeter^3')
    >>> b = Number(2,dims = 'liter')
    >>> c = Number(5,dims = 'gram/centimeter^3')
    >>> d = (a + b)*c
    >>> print(d.convert('kilogram'))
    (15.000000 ± 0)

    Simplified syntax

    >>> globals().update(allunits())
    >>> length = (4 + pm(0.5)) * meter # (4±0.5)m
    >>> velocity = 5 * meter/second
    >>> time = length/velocity
    >>> print(time)
    (8.00 ± 1.00)/10

    Example of formula validation

    >>> a = Number(10,dims = 'meter/second')
    >>> b = Number(2,dims = 'yard^3')
    >>> c = a + b
    Traceback (most recent call last):
    ...
    RuntimeError: Incompatible Dimensions

    Examples of error propagation:

    >>> a = Number(10,error = 2,dims = 'meter/second') # (10±2)m/s
    >>> b = Number(5,error = 1,dims = 'hour')          # (5±1)h
    >>> c = a*b
    >>> print(c.convert('kilometer'))
    (1.800 ± 0.509)x10^2
    >>> print(c.convert('lightyear'))
    (1.903 ± 0.538)/10^11
    >>> print(c.convert('kilometer').value)
    180.0
    >>> print(c.convert('kilometer').error)
    50.9116882454

    Examples of more complex formulas

    >>> c = a**4/(7*b)
    >>> print('%s %s' % (c, c.units()))
    (7.94 ± 6.54)/10^2 meter^4*second^-5

    For pure numbers sin, cos, exp, log are also defined
    You can use a.is_pure() to check if a number is pure.

    (last result is implicitly in meter**4/second**5)

    Financial application example

    >>> coupon = Number(200,error = 1,dims = "dollar/day")
    >>> expiration = Number(1,error = 0,dims = "year")
    >>> payoff = coupon*expiration
    >>> print(payoff.convert('dollar'))
    (7.3048 ± 0.0365)x10^4

    I.e. $73048 dollars with $365 dollars of one sigma uncertainty

    Latex Output

    >>> print(payoff.as_latex())
    (7.3048 \\pm 0.0365)\\times 10^{4}

    """
    regex = re.compile('([a-zA-Z]+)(\^\-?\d+(/\d+)?)?(\*([a-zA-Z]+)(\^\-?\d+(/\d+)?)?)*(\/([a-zA-Z]+)(\^\-?\d+(/\d+)?)?)*')
    c_n = dict((key,value[0]) for key,value in UNITS.items())
    c_l = dict((key,value[1]) for key,value in UNITS.items())
    c_t = dict((key,value[2]) for key,value in UNITS.items())
    c_m = dict((key,value[3]) for key,value in UNITS.items())
    c_a = dict((key,value[4]) for key,value in UNITS.items())
    c_k = dict((key,value[5]) for key,value in UNITS.items())
    c_d = dict((key,value[6]) for key,value in UNITS.items())

    def __init__(self,value,error = 0.0,dims = 'N'):
        if not isinstance(error,(int,float)):
            raise RuntimeError("second argument must be the error")
        if isinstance(dims,tuple):
            dims = 'N*L^%s*T^%s*M^%s*A^%s*K^%s*D^%s' % dims
        dims = dims.replace(' ','')
        if not self.regex.match(dims):
            raise SyntaxError('Invalid Dims')
        n = eval(dims.replace('^','**'),self.c_n) or 1        
        l = buckingham(dims,self.c_l)
        t = buckingham(dims,self.c_t)
        m = buckingham(dims,self.c_m)
        a = buckingham(dims,self.c_a)
        k = buckingham(dims,self.c_k)
        d = buckingham(dims,self.c_d)
        self.value = float(value) * n
        self.error = float(error) * n
        self.dims = (l,t,m,a,k,d)


    def __add__(self,other):
        """
        >>> a = Number(2,1)
        >>> b = Number(3,2)
        >>> print(a+b)
        5.00 ± 2.24
        """
        if not isinstance(other,Number):
            other=Number(other,0,self.dims)
        elif self.dims != other.dims:
            raise RuntimeError("Incompatible Dimensions")
        a,da = self.value,self.error
        b,db = other.value,other.error
        c = a+b
        if not self is other:
            dc = math.sqrt(da**2+db**2)
        else:
            dc = 2.*da
        return Number(c,dc,self.dims)

    def __radd__(self,other):
        return self+other

    def __sub__(self,other):
        """
        >>> a = Number(2,1)
        >>> b = Number(3,2)
        >>> print(a-b)
        -1.00 ± 2.24
        """
        if not isinstance(other,Number):
            other=Number(other,0,self.dims)
        elif self.dims != other.dims:
            raise RuntimeError("Incompatible Dimentions")
        a,da = self.value,self.error
        b,db = other.value,other.error
        c = a-b
        if not self is other:
            dc = math.sqrt(da**2+db**2)
        else:
            dc = 0
        return Number(c,dc,self.dims)

    def __rsub__(self,other):
        x = self - other
        x.value*=-1
        return x

    def __mul__(self,other):
        """
        >>> print(Number(2,1) * 1)
        2.00 ± 1.00

        >>> print(Number(4,2) * Number(7,3))
        (2.80 ± 1.84)x10
        """
        if not isinstance(other,Number):
            other = Number(other)
        a,da = self.value,self.error
        b,db = other.value,other.error
        c = a*b
        if not self is other:
            dc = math.sqrt((da*b)**2+(db*a)**2)
        else:
            dc = 2.0*da*a
        dims = tuple(self.dims[i]+other.dims[i] for i in range(6))
        return Number(c,dc,dims)

    def __rmul__(self,other):
        """
        >>> print(1 * Number(2,1))
        2.00 ± 1.00
        """
        return self*other

    def __div__(self,other):
        """
        >>> print(Number(2,1) / 1)
        2.00 ± 1.00

        >>> print(Number(4,2) / Number(7,3))
        (5.71 ± 3.76)/10
        """
        if not isinstance(other,Number):
            other = Number(other)
        a,da = self.value,self.error
        b,db = other.value,other.error
        c = a/b
        if not self is other:
            dc = math.sqrt((da/b)**2+((a*db)/(b*b))**2)
        else:
            dc = 0.0
        dims = tuple(self.dims[i]-other.dims[i] for i in range(6))
        return Number(c,dc,dims)

    def __rdiv__(self,other):
        """
        >>> print(1 / Number(2,1))
        (5.00 ± 2.50)/10
        """
        if not isinstance(other,Number):
            other = Number(other)
        return other/self

    def __pow__(self,other):
        if not isinstance(other,Number):
            other = Number(other)
        elif not other.is_pure():
            raise RuntimeError("Incompatible Dimentions")
        a,da = self.value,self.error
        b,db = other.value,other.error
        dims = tuple(self.dims[i]*other.value for i in range(6))
        c = a**b
        if not self is other:
            dc = abs(c)*math.sqrt((da*b/a)**2+(db*math.log(a))**2)
        else:
            dc = abs(c)*(da*abs(b/a)+db*math.log(a))
        return Number(c,dc,dims)

    def convert(self,dims):
        """
        >>> print(Number(0, dims="meter/second").convert('kilometer/hour'))
        (0.000000 ± 0)
        """
        other = Number(1.0,0,dims)
        if self.dims != other.dims:
            raise RuntimeError("Incompatible Dimensions")
        return self/other

    def as_string(self,decimals = 2):
        value,error,dims = self.value,self.error,self.dims
        if error:
            n = int_safe(abs(value))
            m = int_safe(error)
            value = value/(10**n)
            error = error/(10**n)
            i = str(max(n-m+2,decimals))
        else:
            return ("(%f ± 0)") % (value)
        if n>1:
            a = ("(%."+i+"f ± %."+i+"f)x10^%i") % (value,error,n)
        elif n>0:
            a = ("(%."+i+"f ± %."+i+"f)x10") % (value,error)
        elif n<-1:
            a = ("(%."+i+"f ± %."+i+"f)/10^%i") % (value,error,-n)
        elif n<0:
            a = ("(%."+i+"f ± %."+i+"f)/10") % (value,error)
        else:
            a = ("%."+i+"f ± %."+i+"f") % (value,error)
        return a

    def as_latex(self,decimals = 2):
        value,error,dims = self.value,self.error,self.dims
        if error:
            n = int_safe(abs(value))
            m = int_safe(error)
            value = value/(10**n)
            error = error/(10**n)
            i = str(max(n-m+2,decimals))
        else:
            return ("(%f \\pm 0)") % (value)
        if n>1:
            a = ("(%."+i+"f \\pm %."+i+"f)\\times 10^{%i}") % (value,error,n)
        elif n>0:
            a = ("(%."+i+"f \\pm %."+i+"f)\\times 10") % (value,error)
        elif n<-1:
            a = ("(%."+i+"f \\pm %."+i+"f)\\times 10^{%i}") % (value,error,-n)
        elif n<0:
            a = ("(%."+i+"f \\pm %."+i+"f)\\times 10^{-1}") % (value,error,-n)
        else:
            a = ("%."+i+"f \\pm %."+i+"f") % (value,error)
        return a

    def __str__(self):
        return self.as_string()

    def is_pure(self):
        return sum(x*x for x in self.dims) == 0

    def purify(self,force = False):
        if not force and not self.is_pure():
            raise RuntimeError("Try purify(force = True)")
        return Number(self.value,self.error,(0,0,0,0,0))

    def units(self):
        if self.is_pure():
            return 'none'
        def f(a,n):
            if float(n) == 0:
                return ''
            if float(n) == 1:
                return '*%s' % a
            if float(n)>0:
                return '*%s^%s'%(a,n)
            if float(n)<0:
                return '*%s^%s' %(a,n)
        r = ''
        r+=f('meter',self.dims[0])
        r+=f('second',self.dims[1])
        r+=f('gram',self.dims[2])
        r+=f('ampere',self.dims[3])
        r+=f('kelvin',self.dims[4])
        r+=f('currency',self.dims[5])
        return r[1:]


    def guess(self):
        raise RuntimeError("this function is a work in progress...")
        if self.is_pure():
            return 'pure'
        options={
            'length': (1,0,0,0,0,0),
            'area': (2,0,0,0,0,0),
            'volume': (3,0,0,0,0,0),
            'speed': (1,-1,0,0,0,0),
            'time': (0,1,0,0,0,0),
            'mass': (0,0,1,0,0,0),
            'current': (0,0,0,1,0,0),
            'charge': (0,0,1,1,0,0),
            'temperature': (0,0,0,0,1,0),
            'currency': (0,0,0,0,0,1),
            'pressure': (-1,-2,1,0,0,0),
            'energy':(2,-2,1,0,0,0),
            'frequency':(0,-1,0,0,0,0),
            'resistance':(2,-3,1,-2,0,0),
            'acceptance':(-2,4,-1,2,0,0),
            'conductance':(-2,3,-1,2,0,0),
            'voltage':(2,-3,1,-1,0,0),
            'power':(1,-3,1,0,0,0),
            'magnetic_flux':(2,-2,1,-2,0,0)}
        dims=self.dims
        r=''
        while True:            
            n=1
            #### fix this... compute n
            y = [i/n for i in dims]
            if not sum(y): break
            def d1(u,w):
                return sum((u[i]-float(j))*(u[i]-float(j)) for i,j in enumerate(w))
            def d2(u,w):
                return sum((u[i]+float(j))*(u[i]+float(j)) for i,j in enumerate(w))
            matches = [(d1(x,y),key,+1) for key,x in options.items()]
            matches += [(d2(x,y),key,-1) for key,x in options.items()]
            matches.sort()
            key,sign=matches[0][1],matches[0][2]
            r += '*%s' % key
            if n*sign!=1: r+='^%s' % (n*sign)
            if matches[0]==0: break
            dims = [(y[i]-j*sign) for i,j in enumerate(options[key])]
        return r[1:]

def sin(x):
    if not isinstance(x,Number):
        return math.sin(x)
    if not x.is_pure():
        raise RuntimeError("Incompatible Dimensions")
    return Number(sin(x.value),abs(cos(x.value))*x.error,x.dims)

def cos(x):
    if not isinstance(x,Number):
        return math.cos(x)
    if not x.is_pure():
        raise RuntimeError("Incompatible Dimensions")
    return Number(cos(x.value),abs(sin(x.value))*x.error,x.dims)

def exp(x):
    if not isinstance(x,Number):
        return math.exp(x)
    if not x.is_pure():
        raise RuntimeError("Incompatible Dimensions")
    c = exp(x.value)
    return Number(c,abs(c)*x.error,x.dims)

def log(x):
    if not isinstance(x,Number):
        return math.log(x)
    if not x.is_pure():
        raise RuntimeError("Incompatible Dimensions")
    c = log(x.value)
    return Number(c,abs(x.error/x.value),x.dims)

def allunits():
    return dict((key,Number(1,0,key)) for key in UNITS.keys())

def pm(error):
    return Number(0,error)

if __name__ == '__main__':
    import doctest
    doctest.testmod()
