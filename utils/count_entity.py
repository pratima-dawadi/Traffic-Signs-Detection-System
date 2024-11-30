import pandas as pd
import numpy as np
import os

def count_entity(csv_path):
    df=pd.read_csv(csv_path)
    entity_count = df['entity'].value_counts()
    print(entity_count)
    return entity_count

if __name__=='__main__':
    count_entity(r'C:\Users\Dell\Downloads\output.csv')
