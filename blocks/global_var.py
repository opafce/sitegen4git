import json
def getv(var_name, path_to_json_file = './configs/config.json'): #gets the needed variable from the json config file
    f = open(path_to_json_file)
    data = json.load(f)
    # Closing file
    f.close()
    #print(data[var_name])
    return data[var_name]


