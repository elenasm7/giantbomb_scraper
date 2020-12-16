import pandas as pd
from sqlalchemy import create_engine
import pickle
    
def save_pickle(file_name,obj):
    with open(file_name, 'wb') as handle:
        pickle.dump(obj, handle, protocol=pickle.HIGHEST_PROTOCOL)
    return file_name + ' is saved'

def open_pickle(file_name):
    with open(file_name, 'rb') as handle:
        obj = pickle.load(handle)
    return obj

def get_db_connection(log_in_credentials,SCHEMA,dbhost=None):
    f = open_pickle(log_in_credentials)
    if dbhost == None:
        dbhost = f['supreme']
    else:
        dbhost = f[dbhost]
        
    DB_CONNECTION = create_engine('mysql+mysqlconnector://' + f['username'] + ':' + 
                              f['password'] + '@' + dbhost + ':' + '3306' + '/' + 
                              SCHEMA, echo=False)
    return DB_CONNECTION

def return_table(DB_CONNECTION,schema,table_name,where=None,query=None):
    
    if where != None:
        select_query = f'SELECT * FROM {schema}.{table_name} {where};'
    elif query != None:
        select_query == query
    else:
        select_query = f'SELECT * FROM {schema}.{table_name};'

    data = pd.read_sql(select_query, DB_CONNECTION)
    
    return data
