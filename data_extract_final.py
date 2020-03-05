"""
This module extracts battery material data from the materials project

The module includes function which extract data for all materials on the
materials project which are classified as a battery material. It mines the
data and exports a csv where each row is a different battery material.
"""
import pandas as pd
from pymatgen import MPRester


def get_battery_data(self, formula_or_batt_id):
    """Returns batteries from a batt id or formula.

    Examples:
        get_battery("mp-300585433")
        get_battery("LiFePO4")
    """
    return mpr._make_request('/battery/%s' % formula_or_batt_id)


def get_bat_dat_final(mapi_key):
    """
    Returns a dataframe of all battery materials and their properties

    This function returns a dataframe of all the battery materials by cycling
    through each battery ID
    """

    # MAPI_KEY is the API key obtained from the materials project
    mpr = MPRester(mapi_key)

    # import the crytsal system table from repository
    crystal = pd.read_csv('crystal_system_table.csv')

    #adding get_battery_data function to MPRester
    MPRester.get_battery_data = get_battery_data

    # making a list of all the battery IDs
    all_bat_ids_list = (mpr._make_request('/battery/all_ids'))

    # making an empty dataframe to hold all of the battery data
    all_battery_dataframe = pd.DataFrame([])

    # looping through every id in the list of all battery IDs
    for batt_id in all_bat_ids_list:
        # gets all the data for one battery id and stores it in a result df
        result_bat_id = pd.DataFrame(mpr.get_battery_data(batt_id))

        # this block of code goes into the adj_pairs element of the dataframe,
        # makes it a list, and extracts something from that list
        adj_pairs = result_bat_id['adj_pairs']
        adj_pairs_list = list(adj_pairs)
        in_list = pd.DataFrame(list(adj_pairs_list[0]))

        # volume change, charge and discharge properties of the materials
        max_d_vol = pd.DataFrame(in_list['max_delta_volume'])
        formula_charge = pd.DataFrame(in_list['formula_charge'])
        formula_discharge = pd.DataFrame(in_list['formula_discharge'])
        result_bat_id['Max Delta Volume'] = max_d_vol
        result_bat_id['Charge Formula'] = formula_charge
        result_bat_id['Discharge Formula'] = formula_discharge

        # go into spacegroup column and extract the crystal system number
        spacegroup_list = list(result_bat_id['spacegroup'])
        in_list_space = pd.DataFrame(spacegroup_list)
        crystal_number = in_list_space['number'][0]

        # use crystal dataframe to see what crystal system the number
        # corresponds to and store crystal system as system
        system = crystal.iloc[crystal_number-1]['Crystal']

        # append crystal system number and lattice to results
        result_bat_id['Spacegroup Number'] = crystal_number
        result_bat_id['Crystal Lattice'] = system

        # appending the results to the final dataframe
        all_battery_dataframe = all_battery_dataframe.append(result_bat_id)

    # cleaning the dataframe
    all_battery_dataframe.rename(
        columns={'battid': 'Battery ID', 'reduced_cell_formula':
                 'Reduced Cell Formula', 'average_voltage':
                 'Average Voltage (V)', 'min_voltage': 'Min Voltage (V)',
                 'max_voltage': 'Max Voltage (V)', 'nsteps': 'Number of Steps',
                 'min_instability': 'Min Instability', 'capacity_grav':
                 'Gravimetric Capacity (mAh/g)', 'capacity_vol':
                 'Volumetric Capacity (Ah/L)', 'working_ion': 'Working Ion',
                 'min_frac': 'Min Fraction', 'max_frac': 'Max Fraction',
                 'reduced_cell_composition': 'Reduced Cell Composition',
                 'framework': 'Framework', 'adj_pairs': 'Adjacent Pairs',
                 'spacegroup': 'Spacegroup', 'energy_grav':
                 'Specific Energy (Wh/kg)', 'energy_vol':
                 'Energy Density (Wh/L)', 'numsites': 'Number of Sites',
                 'type': 'Type'}, inplace=True)

    # setting index to the battery id
    clean_battery_df = all_battery_dataframe.set_index('Battery ID')

    # exports the clean dataframe as a csv to the repository
    # this ensures it does not need to be run each time
    clean_battery_df.to_csv(path_or_buf='./BatteryData.csv')

    # returns the cleaned dataframe
    return clean_battery_df
