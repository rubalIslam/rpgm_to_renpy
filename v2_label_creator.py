import re
import os
import json

system_file = open("System.json")
system_file = json.load(system_file)

map_file = open("Mapinfos.json")
json_map = json.load(map_file)

start_map_id = system_file["startMapId"]

start_map_name = json_map[start_map_id]["name"]

new_map_name = ""

variable_dict = {}
#print(start_map_name)

start_map = True
call_map = True
if call_map == True:
    current_switches = []
    current_variables = []

s = open("./script.rpy","w",encoding="utf-8")
v = open("./variable_n_switches.rpy","w",encoding="utf-8")
l = open("./switches_with_labels_list.json","w",encoding="utf-8")

#s.writelines("call {}".format(start_map_name))

system_file = open("System.json")
system_file = json.load(system_file)

#save the system variables and system switches
pattern = r'[^A-Za-z0-9_ ]+'

def modify_variables(variable_name, value):
    variable_name = variable_name.strip()
    variable_dict.update({variable_name:value})

    with open("variable_n_switches.rpy", 'r') as file:
        lines = file.readlines()

    with open("variable_n_switches.rpy", 'w') as file:
        for i, line in enumerate(lines):
            if str(variable_name) in str(line):
                # Assuming you want to replace the entire line with the new value
                lines[i] = f"{variable_name} = {value}\n"
                #print("====================", line)

        file.writelines(lines)
    #print(variable_dict)
        

    

for variable in system_file["variables"]:
    current_variable = ""
    if variable.strip() != "":
        #print("var",variable)
        current_variable = variable.strip()
        current_variable = re.sub(pattern, '',current_variable).lower()
        current_variable = current_variable.replace(" ","_")
        if current_variable[0:1] == "_":
            #print(current_variable)
            current_variable.replace("_","")
            v.writelines('{} = ""\n'.format(current_variable.replace("_","")))
            variable_dict[current_variable] = ""
        else:
            #print(current_variable)
            current_variable.replace("_","")
            v.writelines('{} = ""\n'.format(current_variable))
            variable_dict[current_variable] = ""
data_list = {}
for switch in system_file["switches"]:
    current_switch = ""
    if switch.strip() != "":
        #print("var",variable)
        current_switch = switch.strip()
        current_switch = re.sub(pattern, '',current_switch).lower()
        current_switch = current_switch.replace(" ","_")
        if current_switch[0:1] == "_":
            #print(current_switch)
            #current_switch.replace("_","")
            #v.writelines('switch_{} = ""\n'.format(current_switch.replace("_","")))
            v.writelines('switch_{} = ""\n'.format(current_switch))
            data_list[f"switch_{current_switch}"] = []
            #data_list.append(data_list)
            variable_dict[current_switch] = ""
        else:
            #print(current_switch)
            #current_switch.replace("_","")
            #v.writelines('switch_{} = ""\n'.format(current_switch.replace("_","")))
            v.writelines('switch_{} = ""\n'.format(current_switch))
            data_list[f"switch_{current_switch}"] = []
            #data_list.append(data_list)
            variable_dict[current_switch] = ""
json.dump(data_list, l, indent=4)
current_label = ""
current_switch1 = ""
current_switch2 = ""
current_variable = ""
current_trigger = ""
def add_common_events(start_num,end_num):
    for x in range(start_num,end_num):
        file_name = "Map{}.json".format(f'{x:03}')
            #file_name = "Map096.json"
        #print (file_name)
        #file_name="Map019.json"
        #file_name="CommonEvents.json"

        json_file=open(file_name,encoding="utf8")
        json_data = json.load(json_file)
        file_name_without_ext=file_name.split(".")[0]
        
        count = 0
        current_char = ""
        prev_dialogue = ""
        sayer_list = []
        menu_name = []
        menu_name0 = ""
        menu_name1 = ""
        menu_name2 = ""
        menu_name3 = ""
        menu_name4 = ""
        menu_name5 = ""
        prev_dialogue = ""

        print (json_data["parallaxName"])

        #map_name = json_data["parallaxName"]

        num_pattern =  r'[^0-9]+'
        map_num = str(re.sub(num_pattern,'',file_name_without_ext))
        map_num = int(map_num.lstrip('0'))

        #print ("map_num::",map_num)


        
        #print (json_map[map_num]["name"])
        map_name = json_map[map_num]["name"].replace(" ", "_")
        name_pattern =  r'[^A-Za-z0-9_]+'
        map_name = str(re.sub(name_pattern,'',map_name)).lower()
        print (map_name)

        f = open("{fn}.rpy".format(fn=map_name),"w",encoding="utf-8")
        sayers = open("sayer.rpy","w",encoding="utf-8")

        #ev = open("./events_list/events_list_{fn}.rpy".format(fn=map_name),"w",encoding="utf-8")

        count = 0
        with open("{}.rpy".format(map_name), encoding="utf-8") as rpy_file:
            lines = rpy_file.readlines()
            #for current_line in reversed(lines):
            print(rpy_file)
            for current_line in lines:
                print(current_line)
                if "call" and "common_" in current_line:
                    trailing_spaces = len(current_line) - len(current_line.rstrip())
                    common_event_label = current_line.strip().split(" ")[1]
                    with open("common_events.rpy",encoding="utf-8") as c_file:
                        for c_lines in  c_file:
                            if c_lines.strip() != "return":
                                f.writelines(""*trailing_spaces+"".format(current_line))
                            if c_lines.strip() == "return":
                                break
                else:
                    f.writelines(current_line)
def main():
    #add_label(start_map_name)
    prev_map = start_map_name
    next_map = ""
    found_label = "False"
    next_label = ""
    prev_label = ""
    common_events = "False"
    found_common_label = "False"
    add_common_events(1,38)
    #add_label(start_map_name,prev_map,next_map,found_label,next_label,prev_label,common_events,found_common_label)
    

if __name__ == "__main__":
    main()