import copy
import sys
import time

sys.path.insert(0, '../pycThermopack/')
from Tube_point import *
from start_point import start_point


def pvt_block(point: Tube_point, new_pressure, new_temperature):
    point.temperature = new_temperature
    point.pressure = new_pressure
    point.update_point_state()
    return point


def main(path: str):
    point = Tube_point()
    start_point(point, path)
    tube_diameters = [0.08, 0.08, 0.08, 0.09, 0.09, 0.09, 0.09, 0.08, 0.08, 0.1]
    tube_lengths = [1000, 200, 450, 1000, 200, 300, 200, 300, 1000, 0]
    tube_points = [point]

    re_nums = list()
    list_p1 = list()
    list_t1 = list()

    for i in range(1, len(tube_diameters)):
        xtt = tube_points[i - 1].calculate_xtt()
        # print ('i', i, ' xtt ', xtt)
        flow_mode = return_mode(xtt)
        print('Found ', flow_mode, ' flow_mode at', i, '! xtt= ', xtt)
        friction_factor = return_friction_factor(xtt)
        tube_points[i - 1].overall_viscosity = calculate_viscosity(tube_points[i - 1].liquid_viscosities[0],
                                                                   tube_points[i - 1].liquid_viscosities[1],
                                                                   friction_factor)
        tube_points[i - 1].reynolds_number = tube_points[i - 1].calculate_Re()
        re_nums.append(tube_points[i - 1].reynolds_number)
        print('Reynolds number for ', i, ' is ', tube_points[i - 1].reynolds_number, 'lambda is ',
              calculate_lambda(tube_points[i - 1].reynolds_number))
        diff = point.calculate_pressure_loss()
        P1 = tube_points[i - 1].pressure - diff
        T1 = tube_points[i - 1].temperature - i * 0.3
        list_p1.append(P1)
        list_t1.append(T1)
        dictf = {'Pressure': list_p1, 'Temperature': list_t1}
        df = pd.DataFrame(dictf)
        df.to_excel('output_data.xlsx', sheet_name='Output Info', index=False)
        print('P1: ', P1, ', T1: ', T1)
        next_point = copy.deepcopy(tube_points[i - 1])

        density = next_point.overall_density
        next_point = pvt_block(next_point, P1, T1)
        next_point = define_tube_params(next_point, tube_diameters[i], tube_lengths[i], density)

        tube_points.append(next_point)
        print()


# end of PVT block
# start of flow_mode part
# xtt = calculate_xtt(p)
# flow_mode = return_mode(xtt)
# print ('Found ', flow_mode, ' flow_mode!; xtt= ', xtt)
# end of flow_mode part
# start of friction part
# ff = return_friction_factor(xtt)

# p.overall_viscosity = calculate_visc(p.liquid_viscosities[0], p.liquid_viscosities[1], ff)

# p.Re = calculate_Re(p)

# print ('Reynolds number is ', p.Re)
# diff = return_pressure_loss(p.v,p.D,length, return_lambda(p.Re), p.overall_density)
# print (p.p, diff)
# P1 = p.p-diff
# T1 = p.T-20.0
# print ('New pressure is', P1)

# p2 = copy.deepcopy(p)
# pvt_block(p2, P1, T1)
# xtt2 = calculate_xtt(p2)
# mode2 = return_mode(xtt2)
# print ('New flow_mode is ', mode2, ' !; xtt= ', xtt2)
# pressure loss calculated, now time for calculating flow_mode again
# print ('dp', p.p, P1, 'D', p.D, 'length', length)
# wss = 0.25*(diff)*p.D/length
# print ('Average WSS is about', wss, 'Pa')

# tube = [p,p2]

# rho_1_1, =  rk_fluid.specific_volume(T1, P1, z, 1)
# rho_1_1= m_ethanol/rho_1_1
# rho_2_1, =  rk_fluid.specific_volume(T1, P1, z, 2)
# rho_2_1 = m_n2/rho_2_1
# rho_tot_1 = z[0]*rho_1+z[1]*rho_2


# xtt = calculate_xtt(rho_1_1, rho_2_1, mu_1, mu_2, v1, D)
# flow_mode = return_mode(xtt)
# print ('New flow_mode is ', flow_mode, ' !; xtt= ', xtt)
# wss = 0.25*(p-P1)*D/length
# print ('Average WSS is about', wss, 'Pa')

if __name__ == "__main__":
    start = time.time()
    main("jsons/default.json")
    end = time.time()
    print("The time of execution of above program is :", (end - start) * 10 ** 3, "ms")
