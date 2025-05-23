import pandas as pd
import numpy as np
import regex as re
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
def company_abbr_fetcher(string):
    pattern = r"([A-Za-z]+)\s*\d"
    match = re.search(pattern, string)
    if match:
        output = match.group(1)
        index_val = ArchiveList[ArchiveList['Reporting Marks'] == output].index
        index_val = index_val[0]
        company_name = ArchiveList.loc[index_val,"Railroad name"]
        output = company_name
    else:
        output = ""
    return output
RR_Archives_list = "RR Picture Archives List.xlsx"
ArchiveList = pd.read_excel("RR Picture Archives List.xlsx")
Consolidated = pd.DataFrame(np.zeros(shape=(0,4)),columns=['Unit Number', 'Notes', 'Model','Serial Number'])
Companies = ArchiveList["Reporting Marks"].to_list()
for company in Companies:
    filename = "RR Pictures Archive/" + company + ".csv"
    company_data = pd.read_csv(filename)
    Consolidated = pd.concat([Consolidated,company_data],axis=0)
Consolidated = Consolidated.reset_index()
print(Consolidated)

HP_reference = pd.read_csv("Locomotive HP Reference.csv",encoding='cp1252')
# file_name = "AEX.csv"
# raw_data = pd.read_csv(file_name)
# raw_data = raw_data[1:]
# df = raw_data.set_axis(['Road No.', 'Model', 'Build Date'], axis=1)
# df = df.reset_index()
# df['Horsepower'] = pd.DataFrame(np.zeros(shape=(len(df),1)), index=df.index)
# print(df)
Company_name = np.zeros(len(Consolidated))
Consolidated.insert(loc=0, column='Company Name', value=Company_name)

for i in range(len(Consolidated)):
    loco_model = Consolidated.loc[i,"Model"].rsplit(";",1)[0]
    Consolidated.loc[i,"Model"] = loco_model
    if Consolidated.loc[i,"Model"] in HP_reference["Model"].values:
        print(str(i) + "True")
        row = HP_reference.loc[(HP_reference["Model"] == Consolidated.loc[i,"Model"])].index[0]
        Consolidated.loc[i,"HP"] = HP_reference.loc[row,"Power Output"]
print(Consolidated)
Consolidated['Unit Number'] = Consolidated['Unit Number'].str.upper()
Consolidated.to_csv("HP Assigned RR Archive Data.csv")
Consolidated = pd.read_csv("HP Assigned RR Archive Data.csv")
for i in range(len(Consolidated)):
    print(Consolidated.loc[i,"Unit Number"])
    Consolidated.loc[i,"Company Name"] = company_abbr_fetcher(Consolidated.loc[i,"Unit Number"])
Consolidated.to_csv("HP Assigned RR Archive Data.csv")