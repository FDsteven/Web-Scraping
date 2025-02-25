import pandas as pd
manufacturers = ["GMD","EMD","GE"]
for i in manufacturers:
    file_name = i + " Locomotives.xlsx"
    raw_data = pd.read_excel(file_name)
    print(raw_data)
    print(type(raw_data.loc[0, "Power Output"]))
    raw_data['Power Output'] = raw_data['Power Output'].astype(float)
    raw_data.to_csv(i + " Locomotives.csv")
