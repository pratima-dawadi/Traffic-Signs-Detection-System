import json
import csv

def storing_to_csv(json_path,csv_path):
    names=[]
    amenties=[]
    with open(json_path) as f:
        data = json.load(f)
        for i in data['features']:
            if 'name' not in i['properties'] or 'amenity' not in i['properties']:
                continue
            names.append(i['properties']['name'])
            amenties.append(i['properties']['amenity'])

    print(names)
    print(amenties)

    with open(csv_path,'w',newline='')as file:
        writer=csv.writer(file)
        writer.writerow(['name','entity'])
        for name, amenity in zip(names,amenties):
            writer.writerow([name, amenity])

if __name__ == '__main__':
    storing_to_csv('osm_data.geojson','output.csv')
