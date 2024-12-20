import matplotlib.pyplot as plt

#PRE: Takes in the medium temperature in °C at a pressure of 15MPa
#POST: Returns the medium ethalpy in J/kg
def hl15mpa(t_hl):
    return 1000*(4.983*(10**(-5))*(t_hl**3)-0.032525*(t_hl**2)+11.607*t_hl-561.75)

#PRE: Takes in the medium temperature in °C at a pressure of 15MPa
#POST: Returns the medium density in kg/m^3
def rl15mpa(t_hl): 
    return -3.9161*(10**(-5))*(t_hl**3)+0.024953*(t_hl**2)-(6.5364*t_hl)+1497.6

qth=3.2e9                                       # thermal ractor power
p_prim=15e6                                     # primary pressure
kf=1771                                         # pressure drop factor for the primary circuit
t_hotleg=320                                    # nominal coolant hot leg temperature
dt_sg=10                                        # temperature difference in steam generator
t_cond=40                                       # temperature in turbine condenser
eta_pump=0.9                                    # pump efficiency
abs_zero=273.15                                 # absolute zero temp 

n_net_opt=0
n_pump_el_opt=0
t_cl_opt=0
h_hl=hl15mpa(t_hotleg)
different_primary_massflows = []                # different massflows of primary depending on temp in kg/sec
different_primary_volume_flow_rates = []        # different volumeflow rate of primary depending on temp in m^3/sec
different_thermal_energy_outputs = []           # different gross thermal energy outputs in MW
different_net_energy_outputs = []               # different net energy outputs in MW
different_pump_energy_consumption = []          # different net energy outputs in MW
different_temperatures = []                     # different temperatures of the primary in °C 


for i in range(260,300,1):
    t_coldleg=i
    massflowrate_primary = qth/((hl15mpa(t_hotleg)-hl15mpa(t_coldleg)))
    Volume_flow_rate_core = massflowrate_primary/rl15mpa(t_coldleg)
    different_primary_volume_flow_rates.append(Volume_flow_rate_core)
    Pressure_drop_across_core = kf*(Volume_flow_rate_core**2)
    Power_consumed_by_ideal_pump = Pressure_drop_across_core*Volume_flow_rate_core
    Power_consumed_by_pump = Power_consumed_by_ideal_pump/eta_pump
    
    eta_carnot_secondary_side = 1-(t_cond+abs_zero)/(t_coldleg-dt_sg+abs_zero)              # The idea is here that we assume the average temperature across a steam generator is equal to the cold leg temperature (worst case scenario) and then there is an additonal heat transfer penatly subtracted of the cold leg temperature which is due to non-ideal nature of the heatexchanger
    gross_thermal_energy_output = eta_carnot_secondary_side*qth                             # Net energy available to the turbine assuming carnot efficency (which is not the case)

    net_thermal_energy=gross_thermal_energy_output-Power_consumed_by_ideal_pump

    
    different_primary_massflows.append(massflowrate_primary)
    different_temperatures.append(t_coldleg)
    different_thermal_energy_outputs.append(gross_thermal_energy_output/1000000000)         #conversion to GW
    different_net_energy_outputs.append(net_thermal_energy/1000000000)                      #conversion to GW
    different_pump_energy_consumption.append(Power_consumed_by_pump/1000000000)             #conversion to GW

n_net_opt = max(different_net_energy_outputs)
idx_opt = different_net_energy_outputs.index(n_net_opt)




plt.plot(different_temperatures,different_net_energy_outputs,label="Net thermal energy available for turbine")
plt.plot(different_temperatures,different_thermal_energy_outputs,label="Gross thermal energy")
plt.scatter(different_temperatures[idx_opt],n_net_opt,label="Process optimum",marker="o",color="r")
plt.ylabel("Thermal energy output [GW]")
plt.xlabel("Cold leg temperature [°C]")
plt.title("Thermal energies")
plt.legend()
plt.show()
    
plt.plot(different_temperatures,different_primary_massflows,label="Primary massflowrate")
plt.scatter(different_temperatures[idx_opt],different_primary_massflows[idx_opt],label="Process optimum",marker="o",color="r")
plt.ylabel("Massflowrate [kg/sec]")
plt.xlabel("Cold leg temperature [°C]")
plt.title("Massflowrates across core (primary massflowrates)")
plt.legend()
plt.show()

plt.plot(different_temperatures,different_pump_energy_consumption,label="Pump energy consumption")
plt.scatter(different_temperatures[idx_opt],different_pump_energy_consumption[idx_opt],label="Process optimum",marker="o",color="r")
plt.ylabel("Energy consumption of the RCP [GW]")
plt.xlabel("Cold leg temperature [°C]")
plt.title("Energy consumption of pump depending on cold leg temperature")
plt.legend()
plt.show()





