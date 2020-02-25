import pymatgen.apps.battery.analyzer as ans
import pymatgen.apps.battery.battery_abc as bat
import pymatgen.apps.battery.insertion_battery as ins

import pandas as pd

from pymatgen import MPRester
#if __name__ == "__main__":
MAPI_KEY = 'T6m6yGppfgtTxpT1'
mpr = MPRester(MAPI_KEY)


def get_battery_data(self, formula_or_batt_id):
    """Returns batteries from a batt id or formula.

    Examples:
        get_battery("mp-300585433")
        get_battery("LiFePO4")
    """
    return mpr._make_request('/battery/%s' % formula_or_batt_id)

MPRester.get_battery_data = get_battery_data

def get_bat_dat():
    """Returns a dataframe of all battery materials and their properties

    This function returns a dataframe of all the battery materials (battery/all_ids)
    """

    #making a list of all the battery IDs
    all_bat_ids_list = (mpr._make_request('/battery/all_ids'))
    #making an empty dataframe to hold all of the battery data
    all_battery_dataframe = pd.DataFrame([])

    #looping through every id in the list of all battery IDs
    for batt_id in all_bat_ids_list:
        #Gets all the data for one battery id
        result_bat_id = pd.DataFrame(mpr.get_battery_data(batt_id))

        #this block of code goes into the adj_pairs element of the dataframe, makes it a list, and extracts something from that list
        adj_pairs = result_bat_id['adj_pairs']
        adj_pairs_list = list(adj_pairs)
        in_list = pd.DataFrame(list(adj_pairs_list[0]))
        max_d_vol = pd.DataFrame(in_list['max_delta_volume'])
        result_bat_id['Max Delta Volume'] = max_d_vol
        #here we can do the same as the above line with any element in adj pairs and append it to our dataframe

        #appending the results to the dataframe
        all_battery_dataframe = all_battery_dataframe.append(result_bat_id)

    #this part simply cleans the dataframe with headings and makes the index the battery ID
    all_battery_dataframe.rename(columns = {'battid':'Battery ID', 'reduced_cell_formula':'Reduced Cell Formula', 'average_voltage':'Average Voltage (V)', 'min_voltage':'Min Voltage (V)', 'max_voltage':'Max Voltage (V)', 'nsteps':'Number of Steps', 'min_instability':'Min Instability', 'capacity_grav':'Gravimetric Capacity (units)', 'capacity_vol':'Volumetric Capacity', 'working_ion':'Working Ion', 'min_frac':'Min Fraction', 'max_frac':'Max Fraction', 'reduced_cell_composition':'Reduced Cell Composition', 'framework':'Framework', 'adj_pairs':'Adjacent Pairs', 'spacegroup':'Spacegroup', 'energy_grav':'Gravemetric Energy (units)', 'energy_vol':'Volumetric Energy', 'numsites':'Number of Sites', 'type':'Type'}, inplace = True)
    clean_battery_df = all_battery_dataframe.set_index('Battery ID')

    #returns the cleaned dataframe
    return clean_battery_df
