import pandas as pd
import numpy as np
manufacturers = ["GMD","EMD","GE"]
All_models = pd.DataFrame(np.zeros(shape=(0,4)),columns = ["Model","Build Year","Total Produced","Power Output"])
for manufacturer in manufacturers:
    model_list = manufacturer + " Locomotives.csv"
    models = pd.read_csv(model_list)
    models = models[["Model","Build Year","Total Produced","Power Output"]]
    All_models = pd.concat([All_models,models],axis=0)
    print(All_models)
All_models = All_models.reset_index()
print(All_models)
All_models.to_csv("Locomotive HP Reference.csv")
file_name = "AEX.csv"
raw_data = pd.read_csv(file_name)
raw_data = raw_data[1:]
df = raw_data.set_axis(['Road No.', 'Model', 'Build Date'], axis=1)
df = df.reset_index()
df['Horsepower'] = pd.DataFrame(np.zeros(shape=(len(df),1)), index=df.index)
print(df)
for i in range(len(df)):
    if df.loc[i,"Model"] in All_models["Model"].values:
        print("True")
        row = All_models.loc[(All_models["Model"] == df.loc[i,"Model"])].index[0]
        df.loc[i,"Horsepower"] = All_models.loc[row,"Power Output"]
print(df)