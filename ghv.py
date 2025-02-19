from ghvFunctions import newtonRaphson, newMach, thermoProperties, prandtlMeyerAngle, prandtlMeyerMach
import pandas as pd
import math

# Code By Felipe Diogo Moura Silva :)

# ******************************************************************************
# ----> INPUTS: thermodynamics inputs @ 30km altitude <-----
# ******************************************************************************

M_in        = 6.8            # Mach regime
rho_in      = 0.01841        # Freestream air density
p_in        = 1197.0         # Freestream pressure
T_in        = 226.5          # Freestream temperature
a           = 301.7          # Speed of sound in air
gamma       = 1.4            # Specific Heat Ratio
R           = 287.0          # Ideal gas constant

# loop to get the number of ramps without errors
while True:
    try:
        rampNumber = int(input("Number of ramps: "))
        if rampNumber < 1:
            print("Number of ramps must be at least 1.")
            continue
        break
    except ValueError:
        print("Invalid input. Please enter an integer.")

# simple control variable
i=1

# creating the columns for the dataframe and a empty list to store the data
columns = ["Theta", "Beta", "Mach", "Pressure Ratio", "Rho Ratio", "Temperature Ratio", "Rho Out", "P Out", "T Out"]
data = []

# ********************************************************************************
# ----> RAMPS: calculations of flow deviation with user defined ramp angles <-----
# ********************************************************************************
for i in range(1, rampNumber + 1):
   
    
    # loop to get the angle of the ramp without errors
    while True:
        try:
            theta = float(input(f"Ramp {i} theta: "))
            break  # Se a entrada for válida, sai do loop
        except ValueError:
            print("Invalid input (probably using ',' instead of '.'). Please enter a valid number.")
            continue

    # Calculations         
    iterations, beta = newtonRaphson(M_in, gamma, theta, betaInit=20, step=0.0001, error=10e-5)
    mach = newMach(M_in, beta, gamma, theta)
    pressureRatio, rhoRatio, temperatureRatio = thermoProperties(M_in, gamma, beta)
    rho_in = rho_in * rhoRatio
    p_in = p_in * pressureRatio
    T_in = T_in * temperatureRatio


    # sToring the data in the created list
    data.append([
        round(theta, 2), 
        round(beta, 2), 
        round(mach, 2), 
        round(pressureRatio, 2), 
        round(rhoRatio, 2), 
        round(temperatureRatio, 2),
        round(rho_in, 2),
        round(p_in, 2),
        round(T_in, 2)
    ])
    M_in = mach


# Creating thedataframe with the created list for the ramps data
allData = pd.DataFrame(data, columns=columns)

# ******************************************************************************
# ----> NECESSARY EVIL: special calculations for the REFLETION stage <-----
# ******************************************************************************

# inputs for the reflection stage calculations
thetaInputReflection    = allData["Theta"].sum()
machInputReflection     = allData["Mach"].iloc[-1]
rhoInputReflection      = allData["Rho Out"].iloc[-1]
pInputReflection        = allData["P Out"].iloc[-1]
TInputReflection        = allData["T Out"].iloc[-1]

# function calls for the reflection stage calculations
iterations, betaReflection  = newtonRaphson(machInputReflection, gamma, thetaInputReflection, betaInit=20, step=0.0001, error=10e-6)
machOutputReflection        = newMach(machInputReflection, betaReflection, gamma, thetaInputReflection)
pressureRatioReflection, rhoRatioReflection, temperatureRatioReflection = thermoProperties(machInputReflection, gamma, betaReflection)

# thermodynamics output values for the reflection stage
rhoOutputReflection         = rhoInputReflection * rhoRatioReflection
pOutputReflection           = pInputReflection * pressureRatioReflection
TOutputReflection           = TInputReflection * temperatureRatioReflection

# Creating a new row for the reflection data
new_row = pd.DataFrame([{
    "Theta": round(thetaInputReflection, 2),
    "Beta": round(betaReflection, 2),
    "Mach": round(machOutputReflection, 2),
    "Pressure Ratio": round(pressureRatioReflection, 2),
    "Rho Ratio": round(rhoRatioReflection, 2),
    "Temperature Ratio": round(temperatureRatioReflection, 2),
    "Rho Out": round(rhoOutputReflection, 2),
    "P Out": round(pOutputReflection, 2),
    "T Out": round(TOutputReflection, 2)
}])

# Adding the reflection data to the main dataframe
allData = pd.concat([allData, new_row], ignore_index=True)

print("\nFinal values with reflection:\n")
print(allData)

# ******************************************************************************
# ----> EXHAUST: Exhaust calculations w/ Prandtl-Meyer equations <-----
# ******************************************************************************

# Exhaust area calculation
columnsExhaust = ["Final Area", "Mach", "Prandtl-Meyer Angle", "Exhaust Lenght"]
dataExhaust = []

# loop parameters
initStepFinalArea   = 0.100
finalStepFinalArea  = 1.500
incrementFinalArea  = 0.050

finalArea = float(initStepFinalArea)
finalArea = float(finalArea)

while finalArea <= finalStepFinalArea:
    # Prandtl-Meyer function call
    exhaustMach         = prandtlMeyerMach(gamma, throatArea=0.01841, finalArea=finalArea)
    exhaustAngle        = prandtlMeyerAngle(exhaustMach, gamma)
    exhaustLength       = finalArea / math.tan(math.radians(exhaustAngle))
    dataExhaust.append([round(finalArea, 2), round(exhaustMach, 2), round(exhaustAngle, 2), round(exhaustLength, 2)])
    finalArea += incrementFinalArea
    

# Creating the dataframe for the exhaust data
exhaustData = pd.DataFrame(dataExhaust, columns=columnsExhaust)
print("\nExhaust data:\n")
print(exhaustData)

