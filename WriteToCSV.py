import os

def writeToCSV(data, base_path):

    file_name = 'PitchRoll_Data.csv'
    file_path = os.path.join(base_path, file_name)
    data.to_csv(file_path, index=False, encoding='utf-8')