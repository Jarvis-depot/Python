import re

# Define regular expression patterns for each field

reg_name_pattern = r'^\d+\.\d+\.\d+\s+Offset\s+(.*):\s+(\w+)\s+–'
field_attr_pattern = r'(\d+):?(\d+)?\s+(\w+)\s+?(\S+)?(.*)?'
field_reserved_pattern = r'(\d+):?(\d+)?\s+(\w+)\s+?(\S+)?\s+?Reserved'
# 31:0 RO 0‟s
# 17:16 RW 00 should be striped across.
field_name_pattern = r'.*\((\w+)\):'
# Stream Number (STRM): This value reflects the Tag associated with the

ignore_pattern = r'.*\.\.\.\.\.\.\.\.\.\.\.\.\.\.\.\.*'

registers = {}
# Open input and output files
with open('../pdf/Audio_new.txt', 'r') as input_file:
    # Initialize variables
    reg_name = None
    reg_offset = None
    field_name = None
    field_offset = None
    field_access = None
    field_reset = None
    current_line = None
    tag = 0
    k = 0
    v = 0
    # Loop through each line in the input file
    for line in input_file:
        if re.match(ignore_pattern, line):
            # print("line0: ", line)
            continue
        # Check if the line matches the reg_name_pattern
        reg_name_match = re.match(reg_name_pattern, line)
        field_name_match = re.match(field_name_pattern, line)
        field_attr_match = re.match(field_attr_pattern, line)
        field_reserved_match = re.match(field_reserved_pattern, line)
        #print(field_name_match,line)
        if reg_name_match:
            tag = 1
            # Update the current reg_name and reset the current field and reset values
            reg_name = reg_name_match.group(2)
            reg_offset = reg_name_match.group(1)
            registers[reg_name] = {'offset': reg_offset, 'fields': {}}
            field_name = ""
            field_hb = ""
            field_lb = ""
            field_access = ""
            field_reset = ""
            field_desc = ""
        elif field_reserved_match:
            # field_reserved_pattern = r'(\d+):?(\d+)?\s+(\w+)\s+?(\S+)?\s+Reserved'
            field_hb = int(field_reserved_match.group(1))
            if field_reserved_match.group(2):
                field_lb = int(field_reserved_match.group(2))
            else:
                field_lb = ""
            field_access = field_reserved_match.group(3)
            field_reset = field_reserved_match.group(4) or ""
            registers[reg_name]['fields']['Reserved'] = {
                'offset': field_offset,
                'access': field_access,
                'high_bits': field_hb,
                'low_bits': field_lb,
                'reset': field_reset,
                'description': ""
            }
        elif field_attr_match:
            # field_attr_pattern = r'(\d+):?(\d+)?\s+(\w+)\s+?(\S+)?(.*)?'
            field_hb = int(field_attr_match.group(1))
            field_lb = ""
            # field_access = ""
            field_reset = ""
            field_access = field_attr_match.group(3) or ""
            field_desc += field_attr_match.group(5)
            if field_attr_match.group(2):
                field_lb = int(field_attr_match.group(2))
            if field_attr_match.group(4):
                field_reset = field_attr_match.group(4)
            # 如果 Key 置 1，那么填写 Value 后将 Key 清 0
            # 永远将自己 (Value) 置 1，代表已经获取到 Value 值
            if k == 1:
                registers[reg_name]['fields'][field_name] = {
                    'offset': field_offset,
                    'access': field_access,
                    'high_bits': field_hb,
                    'low_bits': field_lb,
                    'reset': field_reset,
                    'description': field_desc
                }
                k = 0
            v = 1
        elif field_name_match:
            field_name = field_name_match.group(1)
            field_desc = ""
            # 如果 Value 置 1，那么构建 Key 后将 Value 填入 Dict
            # 永远将自己 (Value) 置 1，代表已经获取到 Value 值
            if v == 1:
                registers[reg_name]['fields'][field_name] = {
                    'offset': field_offset,
                    'access': field_access,
                    'high_bits': field_hb,
                    'low_bits': field_lb,
                    'reset': field_reset,
                    'description': field_desc
                }
                v = 0
            elif v == 0:
                registers[reg_name]['fields'][field_name] = {
                    'description': ""
                }
            k = 1
        elif tag == 1:
            # print(field_desc)
            # print("reg:", reg_name)
            # print("field:", field_name)
            # print("line: ", line)
            if field_name:
                registers[reg_name]['fields'][field_name]['description'] += line
            field_desc += line

# Output the extracted register information in the desired format
with open('../data/Audio.rdl', 'w') as f:
    for reg_name, reg_info in registers.items():
        f.write(f'register :{reg_name} do\n')
        f.write(f'\taccess \n')
        f.write(f'\tdescription ""\n')
        f.write(f'\tsection_ref \n')
        f.write(f'\timplement_ref \n')
        f.write(f'\tmap to: :, at: {reg_info["offset"]}\n')
        f.write(f'\twidth \n')
        for field_name, field_info in reg_info['fields'].items():
            if field_info["low_bits"] != "":
                f.write(f'\tfield :{field_name} [{field_info["high_bits"]}..{field_info["low_bits"]}] do\n')
            else:
                f.write(f'\tfield :{field_name} [{field_info["high_bits"]}] do \n')
            if field_info["reset"] != "":
                f.write(f'\t\treset h\'{field_info["reset"]}\n')
            f.write(f'\t\tdescription "{field_info["description"]}"\n')
            f.write(f'\tend\n')
        f.write(f'end\n')