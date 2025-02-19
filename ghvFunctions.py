import math 

# ******************************************************************************
# ----> FUNCTIONS: Elegant functions used to calculate in main script <-----
# ******************************************************************************

def newtonRaphson(M, gamma, theta, betaInit, step, error):

    theta            = float(math.radians(theta))
    betaInit         = float(math.radians(betaInit))
    i=0

    while True:

        '''
            The absolute value in the fBeta is necessary to avoid negative values leading to a wrong result.
        '''    
        fBeta            =  abs(((((gamma-1) * M**2 * math.sin(betaInit)**2) + 2)/((gamma+1) * M**2 * math.sin(betaInit)**2)) - (math.tan(betaInit -\
                            theta))/(math.tan(betaInit)))

        ''' **SPECIAL ATTENTION TO THIS LINE**
            the absolute value in this line is necessary ONLY before f(beta + step) to avoid negative values when this
            function is subtracted by f(beta). 
            This is a common issue in the Newton-Raphson method, and it is not a problem with the method itself, dont worry!

            --> Newton-Raphson issues... XD

        '''
        fDerivativeBeta  = ((abs(((((gamma-1) * M**2 * math.sin(betaInit + step)**2) + 2)/((gamma+1) * M**2 * math.sin(betaInit + step)**2)) -\
                        (math.tan((betaInit + step) -theta))/(math.tan(betaInit + step))) - fBeta)/step)

        betaInit         = betaInit - (fBeta/fDerivativeBeta)
       
        if fBeta <= error:
            theta       = math.degrees(theta)
            betaInit    =  math.degrees(betaInit)

            break
       
        i=i+1

    return i, betaInit
def newMach(M, beta, gamma, theta):

    beta    =   math.radians(beta)
    theta   =   math.radians(theta)

    firstTerm = (M*math.sin(beta))**2   # M**2 * SIN(B)**2 


    return float((((firstTerm + (2/(gamma-1)))/((((2*gamma)/(gamma-1))*firstTerm) - 1))**0.5)/math.sin(beta-theta))
def thermoProperties(M, gamma, beta):




    ''' 
        The ratio is defined by post stage propertie over the pre stage propertie like: p2/p1 or p3/p2...
    '''
    
    beta    =   math.radians(beta)
    util1   =   (M**2 * math.sin(beta)**2)
    util2   =   (gamma+1) 
    util3   =   (gamma-1)


    pressureRatio       = float(1 + (2*gamma/util2)*(util1 - 1))
    rhoRatio            = float((util1 * util2)/(2 + util3*util1))
    temperatureRatio    = float((1 + ((2*gamma)/util2)*(util1 - 1))*((2 + util3*util1)/(util1*util2)))


    return pressureRatio, rhoRatio, temperatureRatio
def prandtlMeyerAngle(M, gamma):
    
    '''
        The Prandtl-Meyer function is a function that relates the Mach number with the deflection angle of a shock wave.
        This function is used to calculate the Mach number of the flow after the shock wave.
    '''
    gamma                   = float(gamma)  
    util1                   = (gamma+1)
    util2                   = (gamma-1)
    util3                   = M**2 - 1

    prandtlMeyerAngle = (((gamma+1)/(gamma-1))**0.5)*math.atan(((util2/util1)*util3)**0.5) - math.atan(util3**0.5)


    return float(math.degrees(prandtlMeyerAngle))
def prandtlMeyerMach(gamma, throatArea, finalArea):
    
    '''
        The Prandtl-Meyer function is a function that relates the Mach number with the deflection angle of a shock wave.
        This function is used to calculate the Mach number of the flow after the shock wave.
    '''
    gamma                   = float(gamma)  
    util1                   = (gamma+1)
    util2                   = (gamma-1)

    prandtlMeyerMach = ((2/util2)*((finalArea/throatArea)**((util2)/(util1)) - 1))**0.5 

    return float(prandtlMeyerMach)