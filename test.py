import requests
import pandas as pd
import datetime
import warnings
import openpyxl
warnings.simplefilter(action='ignore', category=FutureWarning)


today= datetime.date.today()
year = today.year

headers = {
        'Accept': 'application/json',
        'x-api-key': ''
    }
# def get_data(credit_hours,class_level,mode,session_time ):
pd.set_option('display.max_columns', None)

def get_courses(interests):
    headers = {
        'Accept': 'application/json',
        'x-api-key': ''
    }
    params = (
        {'subject_prefix':'{}'.format(interests)}
        )
    # print(params)
    response = requests.get('https://api.utdnebula.com/course/', headers=headers,params=params)

    json_response=response.json()
    # list1= pd.DataFrame(json_response['data']).iat[0,16]
    base_table=pd.DataFrame(json_response['data']) 
    df=base_table[["_id","class_level","course_number","credit_hours","description","school","sections","subject_prefix","title"]]
    # df.rename(columns={"_id":"course_reference"})
    
    return df

a=get_courses('MATH')
# print(a)
def get_sections(df,instruction_mode):
    df_fin = pd.DataFrame()
    for index,row in df.iterrows():
        course_reference=row['_id']
        # print(course_reference)
        params=({'course_reference':'{}'.format(course_reference),
        'instruction_mode':'{}'.format(instruction_mode)})
        response = requests.get('https://api.utdnebula.com/section/', headers=headers,params=params)
        json_response=response.json()
        # print(json_response)
        base_table=pd.DataFrame(json_response['data'])
        # base_table["professors"] = base_table["professors"].str[2:-2]
        df_new = base_table.astype({'meetings':'string'})
        df_new = df_new[df_new['meetings'].str.contains("{}".format(year))]
        # df_new=base_table[["_id","class_level","course_number","credit_hours","description","school","sections","subject_prefix","title"]]
        
        
        if not df_new.empty:
            # prof_test=df_new['professors']
            # if df_new['professors']:
            df_fin=df_fin.append(df_new,ignore_index=True)
        
        # df[df.astype(str)['professors'] != '[]']
    df_fin = df_fin.astype({'professors':'string'})
    for index,row in df_fin.iterrows(): 
        df = df_fin.drop(df_fin[df_fin.professors == '[]'].index)
    
    return(df)

def trimTables(originalTable):
    newTable = originalTable[['_id', 'academic_session', 'course_reference', 'section_number', 'instruction_mode', 'meetings','professors']]
    newTable['professors']=newTable['professors'].str[2:-2]
    # print(newTable)
    return newTable

b = get_sections(a,'Face-to-Face')
b=trimTables(b)

# print(b)
    
d = pd.merge(a, b , left_on='_id',right_on='course_reference' , how='inner')
# d = d.astype({'_id_y':'string'})

# print(d)

def get_prof(df):
    df_fin = pd.DataFrame()
    
    for index,row in df.iterrows():
        
        prof=row['professors']
               
        
        # print(prof)
        # params=({'_id':'{}'.format(sections)})
        # print(params)
        response = requests.get('https://api.utdnebula.com/professor/{}'.format(prof), headers=headers)
        json_response=response.json()
        # print(json_response)
        # base_table=pd.DataFrame(json_response) 
        base_table=pd.DataFrame(json_response)
        
        # base_table=base_table.reset_index(drop=True)
        second=pd.DataFrame(base_table['data'],index=['_id','first_name','last_name','titles'])
        # second.index.name = 'index_name'
        third=second.T
        df_fin=df_fin.append(third,ignore_index=True)
        # print(second.dtypes)
        # third=second.pivot(columns="index_name",values="data")
        # print(second)
        # new=pd.DataFrame(base_table['data'])
        # df_fin=df_fin.append(second,ignore_index=True)
        
        
        # second.to_excel("output2.xlsx", sheet_name='{}'.format(index))
        # print(str(base_table))
        # df_new = base_table.astype({'meetings':'string'})
        # df_new = df_new[df_new['meetings'].str.contains("{}".format(year))]
        # df_new=base_table[["_id","class_level","course_number","credit_hours","description","school","sections","subject_prefix","title"]]

    #     if not base_table.empty:
    #         df_fin=df_fin.append(base_table,ignore_index=True)
    # print(df_fin)
    return(df_fin)

    
c = get_prof(b)
# print(c)


# d = pd.merge(a, b , left_on='_id',right_on='course_reference' , how='inner')
df = pd.merge(d, c , left_on='professors',right_on='_id' , how='inner')

print(df)

df.to_excel("output.xlsx")
# response = requests.get('https://api.utdnebula.com/professor/6231081584ebaf3e8f1bbe48',headers=headers)
# json_response=response.json()
# print(json_response)
