import pandas as pd
import numpy as np
# manufacturers = ["GMD","EMD","GE"]
# All_models = pd.DataFrame(np.zeros(shape=(0,4)),columns = ["Model","Build Year","Total Produced","Power Output"])
# for manufacturer in manufacturers:
#     model_list = manufacturer + " Locomotives.csv"
#     models = pd.read_csv(model_list)
#     models = models[["Model","Build Year","Total Produced","Power Output"]]
#     All_models = pd.concat([All_models,models],axis=0)
#     print(All_models)
# All_models = All_models.reset_index()
# print(All_models)
# All_models.to_csv("Locomotive HP Reference.csv")

HP_reference = pd.read_csv("Locomotive HP Reference.csv",encoding='cp1252')
# file_name = "AEX.csv"
# raw_data = pd.read_csv(file_name)
# raw_data = raw_data[1:]
# df = raw_data.set_axis(['Road No.', 'Model', 'Build Date'], axis=1)
# df = df.reset_index()
# df['Horsepower'] = pd.DataFrame(np.zeros(shape=(len(df),1)), index=df.index)
# print(df)
df_raw = pd.read_csv("Expanded_CGData.csv",encoding='cp1252')
for i in range(len(df_raw)):
    loco_model = df_raw.loc[i,"locomotive model"]
    df_raw.loc[i,"locomotive model"] = loco_model
    if df_raw.loc[i,"locomotive model"] in HP_reference["Model"].values:
        print(str(i) + "True")
        print(i)
        row = HP_reference.loc[(HP_reference["Model"] == df_raw.loc[i,"locomotive model"])].index[0]
        df_raw.loc[i,"HP"] = HP_reference.loc[row,"Power Output"]
print(df_raw)
df_raw.to_csv("HP Assigned CGData.csv")