from functions import *
from variables import *
import pandas as pd
import math
from matplotlib import pyplot as plt

# Code By Felipe Diogo Moura Silva 

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

# Columns for the dataframe and a empty list to store the data
columns = ["Theta", "Beta", "Mach", "Pressure Ratio", "Rho Ratio", "Temperature Ratio", "Rho Out", "P Out", "T Out", "a", "u"]
data = []



# ****************************************************************************************************
# ----> RAMPS: calculations of flow deviation with user defined ramp angles <-----

#        LOGIC:  [action --> result]   
#       1. given number of ramps --> value of each ramp theta
#       2. with thetas and Newton-Raphson --> Betas
#       3. with betas and thetas and initial thermo properties --> after compressions properties
# ****************************************************************************************************

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
    a = soundSpeedInAir(T_in, gamma, R)
    u = mach * a
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
        round(T_in, 2), 
        round(a, 2),
        round(u, 2)
    ])
    M_in = mach


# Creating thedataframe with the created list for the ramps data
allData = pd.DataFrame(data, columns=columns)




# **************************************************************************************************
# ----> NECESSARY EVIL: special calculations for the REFLETION stage <-----
#
#        LOGIC:  [action --> result]   
#       1. given the sum of betas and thetas as input --> thermo properties.
#
# **************************************************************************************************

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
a = soundSpeedInAir(TOutputReflection, gamma, R)
u = machOutputReflection * a

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
    "T Out": round(TOutputReflection, 2), 
    "a": round(a, 2),
    "u": round(u, 2)
}])

# Adding the reflection data to the main dataframe
allData = pd.concat([allData, new_row], ignore_index=True)

# Writing the final values with reflection to a file
with open("output.txt", "w") as file:
    file.write("Data in compression and reflection:\n")
    file.write(allData.to_string(index=False))
    file.write("\n------------------------------------------------------------------------------------------------------\n")


# **************************************************************************************************
# ----> COMBUSTION: Heat addition in the flow by Rayleigh theory <-----
#
#        LOGIC:  [action --> result]   
#       1. given mach post compression/reflection and desired mach pior to exhaust --> thermo properties.
#       2. with thermo properties ratios --> required heat per mass unit to add in flow and heat ratio
#          out
#
# **************************************************************************************************

columnsCombustion = ["Pressure Ratio", "Rho Ratio", "Temperature Ratio", "Total Temperature Ratio",\
                     "Required Heat to add","Heat ratio Out"]
dataCombustion = []

machInputCombustion     = allData["Mach"].iloc[-1]
rhoInputCombustion      = allData["Rho Out"].iloc[-1]
vInputCombustion        = allData["u"].iloc[-1]

combustionPressureRatio, combustionRhoRatio, combustionTemperatureRatio, combustionTotalTemperatureRatio = \
combustionThermoProperties(machInputCombustion, desiredMachOutCombustion, gamma)

# stating to calculate the heat transfer properties
if allData["T Out"].iloc[-1]  <= 725.0:
    Cp = 14.3 # KJ/*k
elif allData["T Out"].iloc[-1] > 725.0:
    Cp = 13   # # KJ/kg*k
else: 
    ValueError
    print("Invalid temperature.")

# target temperature given combustion properties 
combustionPreviousTemperature = allData["T Out"].iloc[-1]
combustionCurrentTemperature  = combustionTemperatureRatio*combustionPreviousTemperature

requiredQ               = expectedHeat(Cp, combustionCurrentTemperature, combustionPreviousTemperature)
h                       = specificEnthalpy(fuelEnthalpy, Cp, combustionCurrentTemperature, referenceTemperature)
releasedQRatio          = heatRatioOut(rhoInputCombustion, vInputCombustion, gapHeight, h)

# managing the final combustion data 
dataCombustion.append([round(combustionPressureRatio, 2), round(combustionRhoRatio, 2),\
                       round(combustionTemperatureRatio, 2), round(combustionTotalTemperatureRatio, 2), \
                       round(requiredQ, 2) ,round(releasedQRatio, 2)])

combustionData = pd.DataFrame(dataCombustion, columns=columnsCombustion)


# Writing the final values with combustion to a file
with open("output.txt", "a") as file:
    file.write("Data in combustion chamber:\n")
    file.write(combustionData.to_string(index=False))
    file.write("\n------------------------------------------------------------------------------------------------------\n")


# **************************************************************************************************
# ----> EXHAUST: Exhaust calculations w/ Prandtl-Meyer equations <-----

#       LOGIC:   [action --> result]
#                1. guessing final areas and using prandt-Meyer --> list with values and result measures 

# **************************************************************************************************

# Exhaust area calculation
columnsExhaust = ["Final Area", "Mach", "Prandtl-Meyer Angle", "Exhaust Lenght"]
dataExhaust = []

finalArea = float(initStepFinalArea)
finalArea = float(finalArea)

throatArea = (allData["Rho Out"].iloc[0]*(allData["Mach"].iloc[0] * a)) / allData["Mach"].iloc[-1]

while finalArea <= finalStepFinalArea:
    # Prandtl-Meyer function call
    exhaustMach         = prandtlMeyerMach(gamma, throatArea=(0.01841), finalArea=finalArea)
    exhaustAngle        = prandtlMeyerAngle(exhaustMach, gamma)
    exhaustLength       = (finalArea/2) / math.tan(math.radians(exhaustAngle))
    dataExhaust.append([round(finalArea, 2), round(exhaustMach, 2), round(exhaustAngle, 2), round(exhaustLength, 2)])
    finalArea += incrementFinalArea
    

# Creating the dataframe for the exhaust data
exhaustData = pd.DataFrame(dataExhaust, columns=columnsExhaust)
print("\nData in exhaust:\n")
print(exhaustData)

with open("output.txt", "a") as file:
    file.write("Exhaust data:\n")
    file.write(exhaustData.to_string(index=False))
    file.write("\n------------------------------------------------------------------------------------------------------\n")
