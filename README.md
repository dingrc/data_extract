
# data_extract
test2
test
origin/lester_branch

## This directory houses the functions that utilize ``pymatgen`` to get information from the Materials Project website for battery materials.

### Functions
`get_bat_dat()`
Extracts all data from materials project for materials with ID = battery.


I created a new .py file as a copy of data_extract writed by Mitch, and following are changes I made:

     1. add two columns as charge formula and discharge formula for a electrode in result of get_bat_dat() method, which will be used in next method

     2. As we known, it is impossible for us to simply utilize STRING type of charge&discharge formula as features in our training data. Therefore, Magpie API ( Ward, L.; Agrawal, A.; Choudhary, A.; Wolverton, C. AGeneral-Purpose Machine Learning Framework for PredictingProperties of Inorganic Materials. npj Comput. Mater. 2016, 2,No. 16028.) provides a strategy to use a bunch of statistics attributes of elements(atoms) involve in given a compound(formula) to represent the features of its properties.

     Thus, I create a method to obtain the elenments attributes for both dis/charge formula. In paper metioned above, 22 attributes are taken for elements, and we choose the mean value and deviation value for atoms in certain compound. Then we can get 4 columns as features to subtitute formula-name(string) of Dis/Charge compounds, including Mean_Charge , Dev_Charge, Mean_Discharge, Dev_Discharge. At the end, we concat these 4 columns in DataFrame as return value.

     3. Finally, I create a method to get all the dataset we need for model training and export as a .cvs file.
          (1)features(predictor) we are to use: 'Working Ion','Crystal Lattice','Spacegroup', 'element_attribute for charge formula', 'element attributes for discharge fromula'
          (2) lable to be predict: 'Gravimetric Capacity (units)','Volumetric Capacity','Max Delta Volume'

        ！！！！！！！！
        ！！！！！！！！
        HERE'S A BIG PROBLEM !!!!!
        I can't get value of 'Crystal Lattice' columns(eg. orthorhombic) from battery data we got from pymatgen.

        The only way to get this value is to use 'Reduced Cell Formula' in our data to search for 'Crystal System' in basic materials explorer in Materials Project database.

        I don't know how to achieve this, could you guys try to figure it out?
