from api.models.models import LAWMYearResult


def map_series_to_year_result_creation_kwargs(series):
    creation_kwargs = {k : from_fortran_dict[k](series) for k in from_fortran_dict}
    return creation_kwargs


from_fortran_dict = {
    'year'  : lambda series: series['YEAR'],
    '_0_5'  : lambda df: df['0-5_perc'],
    '_11_70': lambda df: df['11-70_perc'],
    '_6_17' : lambda df: df['6-17_perc'],
    'al'    : lambda df: df['AL'],
    'birthr': lambda df: df['BIRTHR'],
    'calor' : lambda df: df['CALOR'],
    'capd_1': lambda df: df['CAPD(1)'],
    'capd_2': lambda df: df['CAPD(2)'],
    'capd_3': lambda df: df['CAPD(3)'],
    'capd_4': lambda df: df['CAPD(4)'],
    'capd_5': lambda df: df['CAPD(5)'],
    'capt'  : lambda df: df['CAPT'],
    'chmor' : lambda df: df['CHMOR'],
    'eapopr': lambda df: df['EAPOPR'],
    'educr' : lambda df: df['EDUCR'],
    'enrol' : lambda df: df['ENROL'],
    'excal' : lambda df: df['EXCAL'],
    'exlife': lambda df: df['EXLIFE'],
    'falu'  : lambda df: df['FALU'],
    'fert'  : lambda df: df['FERT'],
    'gnp'   : lambda df: df['GNP'],
    'gnpd_1': lambda df: df['GNPD(1)'],
    'gnpd_2': lambda df: df['GNPD(2)'],
    'gnpd_3': lambda df: df['GNPD(3)'],
    'gnpd_4': lambda df: df['GNPD(4)'],
    'gnpd_5': lambda df: df['GNPD(5)'],
    'gnpxc' : lambda df: df['GNPXC'],
    'grmor' : lambda df: df['GRMOR'],
    'houser': lambda df: df['HOUSER'],
    'hsexfl': lambda df: df['HSEXFL'],
    'perxfl': lambda df: df['PERXFL'],
    'pop'   : lambda df: df['POP'],
    'popr'  : lambda df: df['POPR'],
    'prot'  : lambda df: df['PROT'],
    'rend'  : lambda df: df['REND'],
    'rlfd_1': lambda df: df['RLFD(1)'],
    'rlfd_2': lambda df: df['RLFD(2)'],
    'rlfd_3': lambda df: df['RLFD(3)'],
    'rlfd_4': lambda df: df['RLFD(4)'],
    'rlfd_5': lambda df: df['RLFD(5)'],
    'sepopr': lambda df: df['SEPOPR'],
    'tlf'   : lambda df: df['TLF'],
    'turbh' : lambda df: df['TURBH'],
    'urbanr': lambda df: df['URBANR'],
}