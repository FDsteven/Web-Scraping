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
    pattern = r"^([^\s]+)"
    match = re.search(pattern, string)
    num_pattern = r"\s+(.*)"
    reporting_number_match = re.search(num_pattern, string)
    full_name = ""
    if match:
        output = match.group(1)
        index_val = ArchiveList[ArchiveList['Reporting Marks'] == output].index
        index_val_1 = Private_list[Private_list['Reporting Marks'] == output].index
        if len(index_val) > 0:
            val = index_val[0]
            company_name = ArchiveList.loc[val,"Railroad name"]
        if len(index_val_1) > 0:
            val = index_val_1[0]
            company_name = Private_list.loc[val,"Railroad name"]
        full_name = company_name
        reporting_mark = output
    else:
        output = ""
        reporting_mark = ""
    if reporting_number_match:
        reporting_number = reporting_number_match.group(1)
    else:
        reporting_number = ""
    return full_name, reporting_mark, reporting_number
RR_Archives_list = "RR Picture Archives List.xlsx"
ArchiveList = pd.read_excel("RR Picture Archives List.xlsx")
Consolidated = pd.DataFrame(np.zeros(shape=(0,4)),columns=['Unit Number', 'Notes', 'Model','Serial Number'])
Companies = ArchiveList["Reporting Marks"].to_list()
Private_list = pd.read_excel("RR Private Owners.xlsx")
Consolidated_Private = pd.DataFrame(np.zeros(shape=(0,4)),columns=['Unit Number', 'Notes', 'Model','Serial Number'])
Companies = Private_list["Reporting Marks"].to_list()
RR_Archive_df = pd.read_csv("HP Assigned RR Archive Data-sorted-TD.csv")
for company in Companies:
    filename = "RR Pictures Archive/" + company + ".csv"
    company_data = pd.read_csv(filename)
    Consolidated_Private = pd.concat([Consolidated_Private,company_data],axis=0)
    
print(Consolidated_Private)
Consolidated_Private = Consolidated_Private.reset_index()
Consolidated_Private.to_csv("HP Assigned RR Private Data.csv")
HP_reference = pd.read_csv("Locomotive HP Reference.csv",encoding='cp1252')
# file_name = "AEX.csv"
# raw_data = pd.read_csv(file_name)
# raw_data = raw_data[1:]
# df = raw_data.set_axis(['Road No.', 'Model', 'Build Date'], axis=1)
# df = df.reset_index()
# df['Horsepower'] = pd.DataFrame(np.zeros(shape=(len(df),1)), index=df.index)
# print(df)
Company_name = np.zeros(len(Consolidated_Private))
Consolidated_Private.insert(loc=0, column='Company Name', value=Company_name)
Consolidated_Private.insert(loc=1, column='Reporting Mark', value=Company_name)
Consolidated_Private.insert(loc=2, column='Reporting Number', value=Company_name)
for i in range(len(Consolidated_Private)):
    loco_model = Consolidated_Private.loc[i,"Model"]
    Consolidated_Private.loc[i,"Model"] = loco_model
    if Consolidated_Private.loc[i,"Model"] in HP_reference["Model"].values:
        print(str(i) + "True")
        row = HP_reference.loc[(HP_reference["Model"] == Consolidated_Private.loc[i,"Model"])].index[0]
        Consolidated_Private.loc[i,"HP"] = HP_reference.loc[row,"Power Output"]
print(Consolidated_Private)
Consolidated_Private['Unit Number'] = Consolidated_Private['Unit Number'].str.upper()
Consolidated_Private.to_csv("HP Assigned RR Private Data.csv")
Consolidated_Private = pd.read_csv("HP Assigned RR Private Data.csv")
for i in range(len(Consolidated_Private)):
    print(Consolidated_Private.loc[i,"Unit Number"])
    full_name, reporting_mark, reporting_number = company_abbr_fetcher(Consolidated_Private.loc[i,"Unit Number"])
    Consolidated_Private.loc[i,"Company Name"] = full_name
    Consolidated_Private.loc[i,"Reporting Mark"] = reporting_mark
    Consolidated_Private.loc[i,"Reporting Number"] = reporting_number
Consolidated = pd.concat([RR_Archive_df,Consolidated_Private],axis=0)
Consolidated = Consolidated.reset_index()
Consolidated.to_csv("HP Assigned RR Archive Data_extended.csv")