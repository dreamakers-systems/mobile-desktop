""" Load informations to analysis """

from typing import (
    Dict,
    List, 
    Any,
    Tuple, 
    Type,
    )

import locale

import pandas as pd
from pandas import DataFrame

from .data_analyse import DataAnalyse

locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")

class DataExtructure(DataAnalyse):
    """ object to load, analyse and export data """

    def __init__(self, data_list: List, porcents: Dict) -> None:
        """Receave data from a sql search
        :data_frame = [[dd-mm-yy, int, (- or +)], ...]

        The class receave tree parameters in a json to
        calculate all rown in the dataframe 
        :dict_ = {
            "10":(10, -90),
            "12":(12, -85),
            "23":(23, -80)
        }
        """
    

        self.data_list = data_list
        self.porcents = porcents
        
    def get_result(self) -> List:
        """ set a data with faturation """
        collumns = ["Valor", "Quantidade", "Recebido", "A Pagar"]
        data = self.analyse_faturation()
        df_data = pd.DataFrame(data, columns=collumns, index=None)
        df_data["Valor"] = df_data["Valor"].map(locale.currency)
        df_data["Recebido"] = df_data["Recebido"].map(locale.currency)
        df_data["A Pagar"] = df_data["A Pagar"].map(locale.currency)
        return df_data.values.tolist()


    def get_faturation(self):
        """Get Result Faturation"""
        return self.analyse_faturation()