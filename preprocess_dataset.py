"""
This is pre-process stage for our dataset.

The dataset we get from Feeding America only contains names of food banks but no addresses or any other
information regarding positions. So we first get addresses from their website and combine them into the
original dataset. Secondly, we match the zip code from external dataset to get their latitude and longitude.

We planned to use "requests" and "lxml" package to parse the website content at the beginning. However,
the javascript inside the HTML is beyond our current programming technique. Instead, we copy the content
into a text file and parse it line by line to get the addresses we need.

Source:
Food bank address in Feeding America
https://www.feedingamerica.org/find-your-local-foodbank)
Zip code with latitude and logitude
https://www.listendata.com/2020/11/zip-code-to-latitude-and-longitude.html

"""


import pandas as pd


def get_address(filename: str) -> pd.DataFrame:
    """
    Parse the text file into a dataframe with addresses.
    :param filename: the content from the web page
    :return: dataframe with food bank names as index
    """
    with open(filename, 'r') as f:
        # creat a dictionary to store all information of each food bank
        address = {}
        # initial a token to check the boundary between food banks
        now = None
        for line in f:
            row = line.strip()
            if 'logo' in row:
                row = row.replace('logo', '').strip()
                if row not in address.keys():
                    now = row
                    address[now] = []
                else:
                    continue
            else:
                if row:
                    address[now].append(row)
                else:
                    continue

    df_address = pd.DataFrame.from_dict(address, orient='index')
    # only return columns with address information
    return df_address[[0, 1, 2, 3]]

def parse_address_and_combine(df_address: pd.DataFrame, df_foodbank: pd.DataFrame) -> pd.DataFrame:
    """
    Split the address into separate columns of city, state, and zip code. Then combine to the original dataset.
    :param df_address: dataframe with address information
    :param df_foodbank: original dataset to combine with
    :return: a combined dataframe
    """

    for i in df_address.index:
        value = df_address.at[i, 2]
        if ',' in value:
            df_address.at[i, 'address_1'] = df_address.at[i, 1]
            df_address.at[i, 'address_2'] = df_address.at[i, 2]

        else:
            df_address.at[i, 'address_1'] = df_address.at[i, 1] + '|' + df_address.at[i, 2]
            df_address.at[i, 'address_2'] = df_address.at[i, 3]

    # split state and zip code then combine
    temp = df_address['address_2'].str.split(',', expand=True)
    temp.columns = ['city', 'address2']
    temp2 = temp['address2'].str.strip().str.split(expand=True)
    temp2.columns = ['state', 'zip_code']
    address_cleaned = df_address[['address_1']].join(temp[['city']].join(temp2))
    combined = df_foodbank.join(address_cleaned)

    # process unmatched rows
    col_process = ['address_1', 'city', 'state', 'zip_code']
    tocheck = combined[combined['zip_code'].isna()][col_process]
    address_cleaned.index = address_cleaned.index.str.replace(', Inc.', '').str.replace(' ', '').str.lower()
    for n in tocheck.index:
        name_tocheck = n.replace(', Inc.', '').replace('and', '&').replace(' ', '').lower()
        if name_tocheck in address_cleaned.index:
            combined.loc[n,col_process] = address_cleaned.loc[name_tocheck]

    # manually fill in values to the rows with slightly different name but no similar pattern to process together
    combined.loc['Feeding America West Michigan Food Bank', col_process] = ['864 West River Center Drive NE',
                                                                          'Comstock Park', 'MI', '49321']
    combined.loc['Connecticut Food Bank', col_process] = ['2 Research Parkway','Wallingford', 'CT', '06492']
    combined.loc['Foodbank of Southeastern Virginia', col_process] = ['800 Tidewater Drive|PO Box 1940',
                                                                     'Norfolk', 'VA', '23504']
    combined.loc['Westmoreland County Food Bank', col_process] = ['100 Devonshire Drive', 'Delmont', 'PA', '15626']

    return combined.reset_index()

if __name__ == '__main__':
    col = ['Food Bank', 'Total Population',
           '[Revised Projections – March 2021]\n2021 Food Insecurity  %',
           '[Revised Projections – March 2021]\n2021 Food Insecurity #']

    foodbank = pd.read_excel('data/Food Banks - 2021 Projections.xlsx', index_col=0, usecols=col)
    address = get_address('data/AllFoodBank.txt')
    foodbank_with_address = parse_address_and_combine(address,foodbank)

    # combining lat long values by zip codes
    df_zipcode = pd.read_csv('data/zip.csv')
    # change data type for merge
    foodbank_with_address['zip_code'] = foodbank_with_address['zip_code'].astype('float64')
    combine = pd.merge(foodbank_with_address.reset_index(),df_zipcode,
                       how='left',left_on='zip_code',right_on='postal code')
    # print(combine.set_index('Food Bank').columns)
    col2 = ['state_x', 'postal code', 'country code', 'Country']
    foodbank_with_latlon = combine.drop(columns=col2).dropna().set_index('Food Bank')
    foodbank_with_latlon.to_csv('foodbank_with_latlon.csv', index=True)

