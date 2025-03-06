# Description: This file contains the variables used in the code.

# ******************************************************************************
# ----> INPUTS: thermodynamics inputs @ 30km altitude <-----
# ******************************************************************************

M_in                        = 6.8                # Mach regime
rho_in                      = 0.01841            # Freestream air density
p_in                        = 1197.0             # Freestream pressure
T_in                        = 226.5              # Freestream temperature
a                           = 301.7              # Speed of sound in 
gamma                       = 1.4                # Specific Heat Ratio
R                           = 287.0              # Ideal gas constant

# ******************************************************************************
# ----> INPUTS: ramp geometry <-----
# ******************************************************************************

gapHeight                   = 0.01841              # Gap height in m 

# ******************************************************************************
# ----> INPUTS: combustion chamber <-----
# ******************************************************************************
fuelEnthalpy                = 142.0     # hydrogen enthalpy at 25 ºC in kJ/Kg
referenceTemperature        = 25.0      # reference temperature for fuel -> 25ºC
desiredMachOutCombustion    = 1.1      # Desired Mach number after the combustion chamber

# ******************************************************************************
# ----> INPUTS: exhaust  <-----
# ******************************************************************************

initStepFinalArea           = 0.075
finalStepFinalArea          = 1.500
incrementFinalArea          = 0.050