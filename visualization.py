# -*- encoding: utf-8 -*-
import folium
import pandas as pd
import json
import numpy
from dbfread import DBF
import csv

category = "A0,A1,A2,A3,A4,A5,A6,A7,A8,A9,A10,A11,A12,A13,A14,A15,A16,A17,A18,A19,A20,A21,A22,A23,A24,A25,A26,A27,A28,A29,A30"
category = list(map(str, category.split(',')))
category_name = '도형ID,GIS건물통합식별번호,고유번호,법정동코드,법정동명,특수지구분코드,특수지구분명,지번,건물식별번호,집한건물구분코드,집합건물구분,' \
               '대장종류코드,대장종류,건물명,건물동명,건물연면적,건축물구조코드,건축물구조명,주요용도코드,주요용도명,건물높이,' \
               '지상층수,지하층수,허가일자,사용승인일자,건물연령,연령대구분코드,연령대구분명,연령대5계급코드,연령대5계급명,데이터기준일자'
category_name = list(map(str, category_name.split(',')))
category = dict(zip(category, category_name))
print(category)

def dbf_to_csv(dbf_table_pth):  # Input a dbf, output a csv, same name, same path, except extension
    csv_fn = dbf_table_pth[:-4]+ ".csv"  # Set the csv file name
    table = DBF(dbf_table_pth, encoding='CP949')  # table variable is a DBF object
    with open(csv_fn, 'w', newline = '') as f:  # create a csv file, fill it with dbf content
        writer = csv.writer(f)
        writer.writerow(table.field_names)  # write the column name
        for record in table:  # write the rows
            writer.writerow(list(record.values()))
    return csv_fn


def read_csv(filename):
    df = pd.read_csv(filename, encoding='CP949', usecols=['A0', 'A1', 'A2', 'A3', 'A4', 'A7', 'A19', 'A20', 'A23', 'A24', 'A25', 'A26', 'A27', 'A28', 'A29'])
    # df = df.rename(columns=category, inplace=True)
    # print([category[x] for x in df.columns])
    df.columns = [category[x] for x in df.columns]
    print(df)
    return df


if __name__=="__main__":
    df = read_csv('./csv_data/광진구_20210114.csv')
    geo_json = 'https://raw.githubusercontent.com/southkorea/seoul-maps/master/kostat/2013/json/seoul_municipalities_geo_simple.json'\

    m = folium.Map(location=[37.562225, 126.978555], tiles="OpenStreetMap", zoom_start=11)
    folium.Choropleth(
        geo_data=geo_json,
        name='choropleth',
        data=df,
        columns=['법정동명', '건물연령'],
        key_on='feature.properties.name',
        fill_color='YlGn',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='건물연령',
    ).add_to(m)
    folium.LayerControl().add_to(m)
    m.save('test.html')
    m
    # filename = 'C:/Users/김태우/Downloads/AL_11215_D196_20210114/AL_11215_D196_20210114.dbf'
    # dbf_to_csv(filename)