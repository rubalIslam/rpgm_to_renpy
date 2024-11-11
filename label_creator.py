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
'''
def modify_variables(variable_name, value):
    print("---",variable_name,value)
    variable_name = variable_name.strip()
    with open("variable_n_switches.rpy", 'r') as file:
        lines = file.readlines()
        for i,line in enumerate(lines):
            #print(f"==========={variable_name.strip()}=========={line}")
            if str(variable_name) in str(line):
                lines[i] = str(variable_name)+" = "+str(value)
                print("====================",line)
    with open("variable_n_switches.rpy", 'w') as file:
        file.writelines(lines)
'''

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

for switch in system_file["switches"]:
    current_switch = ""
    if switch.strip() != "":
        #print("var",variable)
        current_switch = switch.strip()
        current_switch = re.sub(pattern, '',current_switch).lower()
        current_switch = current_switch.replace(" ","_")
        if current_switch[0:1] == "_":
            #print(current_switch)
            current_switch.replace("_","")
            v.writelines('switch_{} = ""\n'.format(current_switch.replace("_","")))
            variable_dict[current_switch] = ""
        else:
            #print(current_switch)
            current_switch.replace("_","")
            v.writelines('switch_{} = ""\n'.format(current_switch.replace("_","")))
            variable_dict[current_switch] = ""

current_label = ""
current_switch1 = ""
current_switch2 = ""
current_variable = ""
current_trigger = ""

def add_label(map_name,prev_map,next_map,found_label,next_label,prev_label,common_events,found_common_label):
    
    with open("{}.rpy".format(map_name), encoding="utf-8") as rpy_file:
        lines = rpy_file.readlines()

        # Iterate over lines in reverse order
        #for current_line in reversed(lines):
        for current_line in lines:
            print("p_map::"+prev_map+";label::"+prev_label)
            print("n_map::"+next_map+";label::"+next_label)
            if "label" in current_line and "#" in current_line:
                current_label = current_line.split("#")[0]
                current_label = current_label.strip().split(" ")[1][:-1]
                
                current_switch1 = current_line.split("#")[1]
                current_switch1 = current_switch1.strip().split(":")[1]
                switch1_key = current_switch1.strip().split("=")[0].strip()
                switch1_value = current_switch1.strip().split("=")[1].strip()
            
                current_switch2 = current_line.split("#")[2]
                current_switch2 = current_switch2.strip().split(":")[1]
                switch2_key = current_switch2.strip().split("=")[0].strip()
                switch2_value = current_switch2.strip().split("=")[1].strip()

                current_variable = current_line.split("#")[4]
                current_variable = current_variable.strip().split(":")[1]
                variable1_key = current_variable.strip().split("=")[0].strip()
                #variable1_value = current_variable.strip().split("=")[1].strip()
                
                current_trigger = current_line.split("#")[4]
                current_trigger = current_trigger.strip().split(":")[1]
                #print(current_trigger)
                if call_map == True:
                    #print(current_label)
                    if str(current_trigger).strip() == "autorun":
                        #print(current_label)
                        if "False" in current_switch1 and "False" in current_switch2:
                            s.writelines("call {}\n".format(current_label))
                            
                            v.writelines('{} = "True"\n'.format(current_label))
                            found_label = "True"
                            prev_label = current_label
                            #call_map = False
                if "= True" in current_line:
                    print("d",variable_dict[switch1_key])
                    print("v:",switch1_value)
                    if variable_dict[switch1_key] == switch1_value:
                        print("c:",current_line)
                
            if "label" in current_line and "common_" in current_line and map_name == "common_events":
                print("n L::",next_label)
                if next_label == current_line.strip().split(" ")[1][:-1]:
                    print("xyz",current_line)
                    s.writelines(current_line)
                    next_label = current_line.strip().split(" ")[1][:-1]
                    found_common_label = "True"
            if common_events == "True" and found_common_label == "True":    
                if "return" in current_line:
                    next_map = prev_map
                    next_label = prev_label
                    print("common_returnnn:::",prev_map,prev_map,next_map,"True",next_label,prev_label,"False","False")
                    add_label(prev_map,prev_map,next_map,"True",next_label,prev_label,"False","False")
            if found_label == "True":
                if "#map" in current_line:
                    #call_map = True
                    if "call" in current_line:
                        call_map_name = current_line.strip().split(" ")[1]
                        print("===============MAP CALLED=============",call_map_name)
                        prev_map = next_map
                        next_map = call_map_name
                        next_label = current_line.strip().split(" ")[1][:-1]
                        add_label(call_map_name,prev_map,next_map,"True",next_label,prev_label,"False","False")
                        break
                        #start
                if "return" in current_line and common_events == "False":
                    next_map = prev_map
                    print("s",next_map)
                    print("returnnn:::",prev_map,prev_map,next_map,"True",next_label,prev_label,"False","False")
                    add_label(prev_map,prev_map,next_map,"True",next_label,prev_label,"False","False")
                    break
                #variable
                if current_line.strip()[0:1] == "$":
                    variable_set = current_line.split(" = ")
                    variable_name = variable_set[0][2:].strip().replace("$","")
                    variable_value = variable_set[1].strip()
                    print("::::",variable_name," = ",variable_value)
                    modify_variables(variable_name,variable_value)
                if "call" in current_line and "#map" not in current_line and current_line.strip().split(" ")[1].strip().split("_")[0] == "common":
                    #prev_map = next_map
                    next_map = "common_events"
                    #prev_label = next_label
                    print("c++++",next_map)
                    common_events = "True"
                    next_label = current_line.strip().split(" ")[1]
                    add_label(next_map,prev_map,next_map,"True",next_label,prev_label,"True","False")
                    print("next_label[[[[[[[]]]]]]]",next_label)

                    break
                    #s.writelines("call {}")
                s.writelines('{}\n'.format(current_line))
        #for current_line in lines:

                
    with open("{}.rpy".format(map_name), encoding="utf-8") as rpy_file:
        lines = rpy_file.readlines()
        for current_line in lines:
            if "True" in current_line:
                print("variable true",current_line)

def main():
    #add_label(start_map_name)
    prev_map = start_map_name
    next_map = ""
    found_label = "False"
    next_label = ""
    prev_label = ""
    common_events = "False"
    found_common_label = "False"
    add_label(start_map_name,prev_map,next_map,found_label,next_label,prev_label,common_events,found_common_label)
    

if __name__ == "__main__":
    main()