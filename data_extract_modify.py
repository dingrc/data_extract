import pymatgen.apps.battery.analyzer as ans
import pymatgen.apps.battery.battery_abc as bat
import pymatgen.apps.battery.insertion_battery as ins
import magpie

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

        
        # this block of code goes into the adj_pairs element of the dataframe, makes it a list, and extracts something from that list
        # here we add Charge Formula & DisCharge Formular
        adj_pairs = result_bat_id['adj_pairs']
        adj_pairs_list = list(adj_pairs)
        in_list = pd.DataFrame(list(adj_pairs_list[0]))
        max_d_vol = pd.DataFrame(in_list['max_delta_volume'])
        formula_charge=pd.DataFrame(in_list['formula_charge'])
        formula_discharge=pd.DataFrame(in_list['formula_discharge'])
        result_bat_id['Max Delta Volume'] = max_d_vol
        result_bat_id['Charge Formula'] = formula_charge
        result_bat_id['Discharge Formula'] = formula_discharge
        #here we can do the same as the above line with any element in adj pairs and append it to our dataframe

        # here we add spacegroup number as a parameter in outcome
        space_list=list(result_bat_id['spacegroup'])
        df_space=pd.DataFrame(space_list)
        spacegroup=df_space["number"]
        result_bat_id['Spacegroup']=spacegroup

        #appending the results to the dataframe
        all_battery_dataframe = all_battery_dataframe.append(result_bat_id)

    #this part simply cleans the dataframe with headings and makes the index the battery ID
    all_battery_dataframe.rename(columns = {'battid':'Battery ID', 'reduced_cell_formula':'Reduced Cell Formula', 'average_voltage':'Average Voltage (V)', 'min_voltage':'Min Voltage (V)', 'max_voltage':'Max Voltage (V)', 'nsteps':'Number of Steps', 'min_instability':'Min Instability', 'capacity_grav':'Gravimetric Capacity (units)', 'capacity_vol':'Volumetric Capacity', 'working_ion':'Working Ion', 'min_frac':'Min Fraction', 'max_frac':'Max Fraction', 'reduced_cell_composition':'Reduced Cell Composition', 'framework':'Framework', 'adj_pairs':'Adjacent Pairs', 'spacegroup':'Spacegroup', 'energy_grav':'Gravemetric Energy (units)', 'energy_vol':'Volumetric Energy', 'numsites':'Number of Sites', 'type':'Type'}, inplace = True)
    clean_battery_df = all_battery_dataframe.set_index('Battery ID')

    #returns the cleaned dataframe
    return clean_battery_df

    def get_elementProperty(clean_battery_df):

        # here we import a API called The Materials Agnostic Platform for Informatics and Exploration (Magpie)
        # this API can let us use formula of a conpound to get its  elemental properties from statistics of 
        # atomic constituents attributes. 

        #  Details are in this paper:
        #  Ward, L.; Agrawal, A.; Choudhary, A.; Wolverton, C. A General-Purpose Machine Learning Framework for Predicting Properties of 
        #  Inorganic Materials. npj Comput. Mater. 2016, 2, No. 16028.
        from magpie import MagpieServer
        m = MagpieServer()
        
        # here we can get Mean and Deviation of Element Property for Charge_Formula
        charge_formula=clean_battery_df['Charge Formula']
        df_Mean_Charge=m.generate_attributes("oqmd-Eg",charge_formula).iloc[:,6:-7:6]
        df_Dev_Charge=m.generate_attributes("oqmd-Eg",charge_formula).iloc[:,8:-7:6]
        df_Mean_Charge.rename(columns={'mean_Nuber':'Char_mean_Number','mean_MendeleevNumber':'Char_mean_MendeleevNumber','mean_AtomicWeight':'Char_mean_AtomicWeight','mean_MeltingT':'Char_mean_MeltingTemp','mean_Column':'Char_mean_Column','mean_Row':'Char_mean_Row',
        'mean_CovalentRadius':'Char_mean_CovalentRadius','mean_Electronegativity':'Char_mean_Electronegativity','mean_NsValence':'Char_mean_NsValence','mean_NpValence':'Char_mean_NpValence','mean_NdValence':'Char_mean_NdValence','mean_NfValence':'Char_mean_NfValence',
        'mean_NValance':'Char_mean_NValance','mean_NsUnfilled':'Char_mean_NsUnfilled','mean_NpUnfilled':'Char_mean_NpUnfilled','mean_NdUnfilled':'Char_mean_NdUnfilled','mean_NfUnfilled':'Char_mean_NfUnfilled','mean_NUnfilled':'Char_mean_NUnfilled','mean_GSvolume_pa':'Char_mean_GSvolume_pa',
        'mean_GSbandgap':'Char_mean_GSbandgap','mean_GSmagmom':'Char_mean_GSmagmom','mean_SpaceGroupNumber':'Char_mean_SpaceGroupNumber'})
        df_Dev_Charge.rename(columns={'dev_Nuber':'Char_dev_Number','dev_MendeleevNumber':'Char_dev_MendeleevNumber','dev_AtomicWeight':'Char_dev_AtomicWeight','dev_MeltingT':'Char_dev_MeltingTemp','dev_Column':'Char_dev_Column','dev_Row':'Char_dev_Row',
        'dev_CovalentRadius':'Char_dev_CovalentRadius','dev_Electronegativity':'Char_dev_Electronegativity','dev_NsValence':'Char_dev_NsValence','dev_NpValence':'Char_dev_NpValence','dev_NdValence':'Char_dev_NdValence','dev_NfValence':'Char_dev_NfValence',
        'dev_NValance':'Char_dev_NValance','dev_NsUnfilled':'Char_dev_NsUnfilled','dev_NpUnfilled':'Char_dev_NpUnfilled','dev_NdUnfilled':'Char_dev_NdUnfilled','dev_NfUnfilled':'Char_dev_NfUnfilled','dev_NUnfilled':'Char_dev_NUnfilled','dev_GSvolume_pa':'Char_dev_GSvolume_pa',
        'dev_GSbandgap':'Char_dev_GSbandgap','dev_GSmagmom':'Char_dev_GSmagmom','dev_SpaceGroupNumber':'Char_dev_SpaceGroupNumber'})
        
        
        # here we can get Mean and Deviation of Element Property for Discharge_Formula
        discharge_formula=clean_battery_df['Discharge Formula']
        df_Mean_Discharge=m.generate_attributes("oqmd-Eg",discharge_formula).iloc[:,6:-7:6]
        df_Dev_Discharge=m.generate_attributes("oqmd-Eg",discharge_formula).iloc[:,8:-7:6]
        df_Mean_Discharge.rename(columns={'mean_Nuber':'Dis_mean_Number','mean_MendeleevNumber':'Dis_mean_MendeleevNumber','mean_AtomicWeight':'Dis_mean_AtomicWeight','mean_MeltingT':'Dis_mean_MeltingTemp','mean_Column':'Dis_mean_Column','mean_Row':'Dis_mean_Row',
        'mean_CovalentRadius':'Dis_mean_CovalentRadius','mean_Electronegativity':'Dis_mean_Electronegativity','mean_NsValence':'Dis_mean_NsValence','mean_NpValence':'Dis_mean_NpValence','mean_NdValence':'Dis_mean_NdValence','mean_NfValence':'Dis_mean_NfValence',
        'mean_NValance':'Dis_mean_NValance','mean_NsUnfilled':'Dis_mean_NsUnfilled','mean_NpUnfilled':'Dis_mean_NpUnfilled','mean_NdUnfilled':'Dis_mean_NdUnfilled','mean_NfUnfilled':'Dis_mean_NfUnfilled','mean_NUnfilled':'Dis_mean_NUnfilled','mean_GSvolume_pa':'Dis_mean_GSvolume_pa',
        'mean_GSbandgap':'Dis_mean_GSbandgap','mean_GSmagmom':'Dis_mean_GSmagmom','mean_SpaceGroupNumber':'Dis_mean_SpaceGroupNumber'})
        df_Dev_Discharge.rename(columns={'dev_Nuber':'Dis_dev_Number','dev_MendeleevNumber':'Dis_dev_MendeleevNumber','dev_AtomicWeight':'Dis_dev_AtomicWeight','dev_MeltingT':'Dis_dev_MeltingTemp','dev_Column':'Dis_dev_Column','dev_Row':'Dis_dev_Row',
        'dev_CovalentRadius':'Dis_dev_CovalentRadius','dev_Electronegativity':'Dis_dev_Electronegativity','dev_NsValence':'Dis_dev_NsValence','dev_NpValence':'Dis_dev_NpValence','dev_NdValence':'Dis_dev_NdValence','dev_NfValence':'Dis_dev_NfValence',
        'dev_NValance':'Dis_dev_NValance','dev_NsUnfilled':'Dis_dev_NsUnfilled','dev_NpUnfilled':'Dis_dev_NpUnfilled','dev_NdUnfilled':'Dis_dev_NdUnfilled','dev_NfUnfilled':'Dis_dev_NfUnfilled','dev_NUnfilled':'Dis_dev_NUnfilled','dev_GSvolume_pa':'Dis_dev_GSvolume_pa',
        'dev_GSbandgap':'Dis_dev_GSbandgap','dev_GSmagmom':'Dis_dev_GSmagmom','dev_SpaceGroupNumber':'Dis_dev_SpaceGroupNumber'})
        
        # use concat to merge all data in one DataFrame
        element_attributes=pd.concat(objs=[df_Mean_Charge,df_Dev_Charge,df_Mean_Discharge,df_Dev_Discharge],axis=1)
        return element_attributes


        def get_all_variable(clean_battery_df,element_attributes):
            
            #features(predictor) we are to use: 'Working Ion','Crystal Lattice','Spacegroup', 'element_attribute for charge formula', 'element attributes for discharge fromula'
            # lable to be predict: 'Gravimetric Capacity (units)','Volumetric Capacity','Max Delta Volume'


            # select features we need in training our model
            train_set=clean_battery_df[['Working Ion','Crystal Lattice','Spacegroup','Gravimetric Capacity (units)','Volumetric Capacity','Max Delta Volume']]
            # concat the element attributes which represent the property of charge/dis electrode in our features
            train_set.reset_index(drop=False, inplace=True)
            train_set=pd.concat(objs=[train_set,element_attributes],axis=1)
            # make a .csv file to our working directory.
            train_set.to_csv(path_or_buf='./TrainingData.csv')
            return train_set