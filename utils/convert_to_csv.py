import csv
import time

import pandas as pd


def pd_convert_csv(info, file_type):
    df = pd.DataFrame(info)
    timestr = time.strftime("%d%m%Y-%H%M%S")
    df.to_csv(r"output/"+file_type+"_csv_output_"+timestr+".csv", index=False)


def csv_convert(info, file_type):
    keys = info[0].keys()
    timestr = time.strftime("%d%m%Y-%H%M%S")
    with open(r"output/"+file_type+"_csv_output_"+timestr+".csv", "w", newline='') as file:
        csvwriter = csv.DictWriter(file, keys)
        csvwriter.writeheader()
        csvwriter.writerows(info)
