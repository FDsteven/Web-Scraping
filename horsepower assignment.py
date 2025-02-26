import pandas as pd
import numpy as np
manufacturers = ["GMD","EMD","GE"]
All_models = pd.DataFrame(np.zeros(shape=(0,4)),columns = ["Model","Build Year","Total Produced","Power Output"])
for manufacturer in manufacturers:
    model_list = manufacturer + " Locomotives.csv"
    models = pd.read_csv(model_list)
    pd.concat([All_models,models],axis=1)
    print(All_models)
file_name = "AEX.csv"
raw_data = pd.read_csv(file_name)
raw_data = raw_data[1:]
df = raw_data.set_axis(['Road No.', 'Model', 'Builder No.', 'Build Date', 'Notes'], axis=1)
print(df)
# for i in range(len(df)):
#     if df.loc[i,"Model"] in
#     df.loc[i,"Horsepower"] = 