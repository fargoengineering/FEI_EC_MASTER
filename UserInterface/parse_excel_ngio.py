from global_vars import *
import pandas as pd
import os


class parse_excel:
    """
    This module is used to parse necessary data that has been configured in the Excel file: `Config_sheet.xlsx`

    Utilizes `pandas` python module to parse and read data from the CSV file, and converts said data into a pandas dataframe for manipulation.
    """

    global df, _pe

    def __init__(self, ob):
        path = os.path.dirname(__file__)
        path += "/config_sheet_ngio.xlsx"
        self.df = pd.read_excel(path, "Sheet1", header=1) # SET SHEET NAME
        self._pe = ob

    def parse_excel(self):
        for i in range(32): # number of total slot boards (could have more than 32)
    
            spn = i
            self._pe.spn_list.append(spn)
            # spn_data = self.df.loc[i, "UI_type"]
            # spn_type = str(spn_data)