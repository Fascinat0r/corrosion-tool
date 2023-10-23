import json

from Tube_point import Tube_point
import pandas as pd


def start_point(point: Tube_point, path: str):  # initialization of start point, done by hand

    fill_variables_from_json(path, point)
    point.update_point_state()
    return point

df = pd.read_excel('Imput_data.xlsm')
_ = df['Unnamed: 1']
Tube_point.temperature = _[0]
Tube_point.pressure = _[2]
Tube_point.molar_composition = [_[6], _[11]]
Tube_point.components_density = [_[7], _[12]]
Tube_point.liquid_viscosities = _[13]
Tube_point.vapor_viscosities = _[8]
Tube_point.length = _[18]
Tube_point.roughness = _[19]
Tube_point.diameter = _[20]



def fill_variables_from_json(json_file, point):
    df = pd.read_excel('Imput_data.xlsm')
    _ = df['Unnamed: 1']
    with open(json_file, 'r') as file:
        data = json.load(file)

    point.temperature = _[0]
    point.pressure = _[2]
    point.molar_composition = [_[6], _[11]]
    point.molar_masses = data.get('molar_masses', point.molar_masses)
    point.velocity = data.get('velocity', point.velocity)
    point.diameter = _[20]
    point.length = _[18]
    point.vapor_viscosities = _[8]
    point.liquid_viscosities = _[8]
    point.components_density = [_[7], _[12]]
    point.roughness = _[19]
    point.mass = _[1]
