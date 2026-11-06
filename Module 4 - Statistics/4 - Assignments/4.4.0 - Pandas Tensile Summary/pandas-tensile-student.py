import numpy as np
import pandas as pd

"""
Pandas Tensile Summary

The tensile data from the previous module was written to a single CSV file with one row per
sample and these columns:

    Sample_Name, Material_Type, Tensile_Strength, Fracture_Strain, Elastic_Modulus, Yield_Strength

Complete the six functions below using Pandas. Each function is graded separately, so you can
work on them in any order. Your functions will be tested on tensile files with different
materials, a different number of samples, and rows in a different order than the course file,
so do not write code that only works for 1045CR, 2024 and PMMA.

Submit this file to Gradescope.
"""


def load_tensile_data(_path: str):
    """
    Load a tensile data CSV file into a Pandas DataFrame.
    :param _path: Path to the CSV file
    :return: A DataFrame with one row per sample
    """

    df = pd.read_csv(_path)

    return df


def select_material(_df, _material: str):
    """
    Select all of the samples that were made of one material.
    :param _df: DataFrame of tensile data
    :param _material: Material to keep, as it appears in the Material_Type column (e.g. 'PMMA')
    :return: A DataFrame that only contains the rows for that material. All columns are kept.
    """

    df = _df[_df['Material_Type'] == _material]

    return df


def select_strong(_df, _material: str, _min_yield: float):
    """
    Select the samples of one material that have a yield strength ABOVE a minimum value.
    Hint: two conditions are needed. Remember the parentheses and use & (not 'and').
    :param _df: DataFrame of tensile data
    :param _material: Material to keep, as it appears in the Material_Type column
    :param _min_yield: Minimum yield strength. Samples exactly equal to this value are not kept
    :return: A DataFrame with the rows that meet both conditions. All columns are kept.
    """

    # YOUR CODE HERE #
    df = _df[(_df['Material_Type'] == _material) & (_df['Yield_Strength'] > _min_yield)]

    return df


def get_values(_df, _material: str, _column: str):
    """
    Pull the values of one column for one material out as a Numpy array.
    :param _df: DataFrame of tensile data
    :param _material: Material to keep, as it appears in the Material_Type column
    :param _column: Name of the column to extract (e.g. 'Elastic_Modulus')
    :return: A Numpy array (not a Pandas Series) of the values, in the same order as the DataFrame
    """

    # YOUR CODE HERE #

    df = _df[_df['Material_Type'] == _material]
    values = df[_column].values

    return values


def material_statistics(_df, _material: str, _column: str):
    """
    Calculate the mean and standard deviation of one column for one material.
    Use the sample standard deviation, which is what Pandas .std() gives you.
    :param _df: DataFrame of tensile data
    :param _material: Material to keep, as it appears in the Material_Type column
    :param _column: Name of the column to analyze (e.g. 'Yield_Strength')
    :return: A tuple of (mean, standard deviation)
    """

    # YOUR CODE HERE #

    df = _df[_df['Material_Type'] == _material]
    mean = df[_column].mean()
    std = df[_column].std()

    return (mean, std)


def summary_table(_df, _columns: list):
    """
    Calculate the mean and standard deviation of several columns for every material in the data.
    Do not type in the material names. Use .unique() so the function works for any data file.
    :param _df: DataFrame of tensile data
    :param _columns: List of column names to analyze (e.g. ['Elastic_Modulus', 'Yield_Strength'])
    :return: A dictionary of dictionaries. The first key is the material name, the second key is the
             column name, and the value is a tuple of (mean, standard deviation). For example:
             {'PMMA': {'Elastic_Modulus': (3.09, 0.2), 'Yield_Strength': (49.41, 3.04)}, ...}
    """

    # YOUR CODE HERE #

    summary = {}
    materials = _df['Material_Type'].unique()

    for material in materials:
        summary[material] = {}
        for column in _columns:
            mean, std = material_statistics(_df, material, column)
            summary[material][column] = (mean, std)

    return summary


if __name__ == '__main__':
    # Use this section to check your work. It is not graded and is not run by Gradescope.
    # When it is working you should see (rounded):
    #   Material   Elastic_Modulus        Yield_Strength
    #   1045CR     199.19 +/- 10.69       606.03 +/- 17.53
    #   2024       74.61 +/- 15.63        342.71 +/- 24.2
    #   PMMA       3.09 +/- 0.2           49.41 +/- 3.04
    path_to_file = '../../../data/tensile/tensile_data.csv'

    data = load_tensile_data(path_to_file)
    if data is None:
        print('load_tensile_data() is not complete yet')
    else:
        print(data)

        table = summary_table(data, ['Elastic_Modulus', 'Yield_Strength'])
        if table is None:
            print('summary_table() is not complete yet')
        else:
            for material in table:
                print(material, end='\t')
                for column in table[material]:
                    (avg, std) = table[material][column]
                    print(column, round(avg, 2), '+/-', round(std, 2), end='\t')
                print()
