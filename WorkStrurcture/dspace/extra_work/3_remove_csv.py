# removing existing csv file from mentioned filepath
import os
def remove_csv():
    for folder, subfolders, files in os.walk('C:/Users/irfan/Documents/DSPACE_CSV_SCRAPPING/'):
        for file in files:
            if file.endswith('.csv'):
                path = os.path.join(folder, file)
                print('csv file deleted : ', path)
                os.remove(path)
remove_csv()
