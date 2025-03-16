import pandas as pd
import numpy as np
import glob
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
leasing_path = "Leasing Companies/*.csv"
HP_reference = pd.read_csv("Locomotive HP Reference.csv",encoding='cp1252')
# file_name = "AEX.csv"
# raw_data = pd.read_csv(file_name)
# raw_data = raw_data[1:]
# df = raw_data.set_axis(['Road No.', 'Model', 'Build Date'], axis=1)
# df = df.reset_index()
# df['Horsepower'] = pd.DataFrame(np.zeros(shape=(len(df),1)), index=df.index)
# print(df)
Leasing_df = pd.DataFrame(np.zeros(shape=(0,6)),columns=['Company','Abbr','Road No.', 'Model', 'Date','HP'])
for fname in glob.glob(leasing_path):
    print(fname)
    df_raw = pd.read_csv(fname)
    df = df_raw[['Company','Abbr','Road No.', 'Model', 'Date']]
    # df = df_raw.set_axis(['Company','Abbr','Road No.', 'Model', 'Build Date'], axis=1)
    Leasing_df = pd.concat([Leasing_df,df],axis=0)
    print(Leasing_df)
Leasing_df = Leasing_df.reset_index()

for i in range(len(Leasing_df)):
    if Leasing_df.loc[i,"Model"] in HP_reference["Model"].values:
        print(str(i) + "True")
        row = HP_reference.loc[(HP_reference["Model"] == Leasing_df.loc[i,"Model"])].index[0]
        Leasing_df.loc[i,"HP"] = HP_reference.loc[row,"Power Output"]
print(Leasing_df)
Leasing_df.to_csv("HP Assigned Leasing Company Master dataset.csv")