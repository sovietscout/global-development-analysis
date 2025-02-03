import pandas as pd
from enum import Enum
from pathlib import Path
from typing import Optional


PROCD_P = Path('../data/procd/')
RAW_P = Path('../data/raw/')


class DF(Enum):
    WDI = {'file_name': 'wb-wdi.xlsx', 'sheet_name': 'Data'}
    PIP = {'file_name': 'wb-pip.csv', 'sep': ','}
    WIID = {'file_name': 'un-wiid.csv', 'sep': ';'}
    HDR = {'file_name': 'undp-hdr.csv', 'sep': ','}
    WEO = {'file_name': 'imf-weo.xlsx', 'sheet_name': 'Data'}
    COUNTRIES = {'file_name': 'countries-{}.csv', 'sep': ','}


def Load(dataset: DF, raw: Optional[bool] = False) -> pd.DataFrame:
    conf = dataset.value

    file_name = conf.get('file_name')
    sep = conf.get('sep', ',')

    if not raw:
        # Processed files are always saved in csv format
        file_name = file_name.replace('xlsx', 'csv')
        sep = ','

    if dataset == DF.COUNTRIES:
        v = 'all' if raw else 'selected'
        file_name = file_name.format(v)

    dir_path = RAW_P if raw else PROCD_P
    file_path = dir_path / file_name

    if not file_path.is_file():
        raise FileNotFoundError(f"File not found: {file_path}")

    if file_path.suffix == '.xlsx':
        return pd.read_excel(file_path, sheet_name=conf.get('sheet_name'))
    return pd.read_csv(file_path, sep=sep)

def Save(dataset: DF, df: pd.DataFrame) -> None:
    conf = dataset.value

    file_name = conf['file_name']
    file_name = file_name.replace('xlsx', 'csv')

    if dataset == DF.COUNTRIES:
        file_name = file_name.format('selected')

    file_path = PROCD_P / file_name

    df.to_csv(file_path, index=False, header=True)
