import os

def writeToCSV(data, base_path, file_name):
    """
    This function writes data values to a csv files
    :param data: contains DM value, X location, Y location, Pitch Value, Roll Value
    :param base_path: contains file path where csv is saved to
    :param file_name: contains file name of csv
    """

    file_path = os.path.join(base_path, file_name)
    data.to_csv(file_path, index=False, encoding='utf-8')