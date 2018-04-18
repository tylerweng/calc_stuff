import argparse
import csv

FILEPATH = ''
# RELEVANT FIELDS
ORDER_ID = 'Order_ID'
TAX_EXCLUSIVE_SELLING_PRICE = 'TaxExclusive_Selling_Price'
TAX_LOCATION_CODE = 'Taxed_Location_Code'
JURISD_LEVEL = 'Jurisdiction_Level'
JURISD_NAME = 'Jurisdiction_Name'

# RELEVANT_FIELDS_IDX_MAP = {
#     'TaxExclusive_Selling_Price': 24,
#     'Taxed_Location_Code': 42,
#     'Jurisdiction_Level': 44,
#     'Jurisdiction_Name': 45
# }

NOT_APPLICABLE_CITY = 'NOT APPLICABLE'
COUNTY_SUFFIX = ' COUNTY'
CITY_PREFIX = 'City of '

# {COUNTY NAME: {Not Applicable, City of City
TAX_MAP = {}

def parse_args():
    parser = argparse.ArgumentParser(prog='calculate.py', description='Ingests csv, outputs summary report')
    parser.add_argument('--file', action='store', help='absolute file path used in request', required=True)
    return parser.parse_args().__dict__


def generate_summary():
    global TAX_MAP
    sum = 0
    with open(FILEPATH, 'r') as in_file:
        reader = csv.DictReader(in_file)
        # get fieldnames from DictReader object and store in list
        # headers = reader.fieldnames
        for line in reader:
            if line[ORDER_ID]:
                tesp = line[TAX_EXCLUSIVE_SELLING_PRICE]
                tloc = line[TAX_LOCATION_CODE]
            jl = line[JURISD_LEVEL]
            jn = line[JURISD_NAME]
            if jl == 'State':
                state = jn
            elif jl == 'City':
                city = jn
            elif jl == 'County':
                county = jn
                if state != 'CA':
                    continue
                if county not in TAX_MAP:
                    TAX_MAP[county] = {}
                sum += float(tesp)
                if city not in TAX_MAP[county]:
                    TAX_MAP[county][city] = float(tesp)
                else:
                    TAX_MAP[county][city] += float(tesp)
    for k, v in sorted(TAX_MAP.items()):
        print(k)
        print(v)
    print(f'sum: ${sum}')

def main():
    global FILEPATH
    try:
        args = parse_args()
    except Exception as ex:
        print(f'Failuree to parse args caused by: {ex}')
    FILEPATH = args['file']
    generate_summary()


main()
