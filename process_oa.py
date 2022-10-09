# This script is used for parsing *.json of each month with OA DB
# So, for users who want to use this script, should dump your own *.json from OA HTML
# The DB of each month should be saved as "01", "02", ......
# Finally give you the total overtime of this year
# NOTE: Current month and future months, which are not finished yet could not be parsed
import json
import os
import re
from datetime import datetime

total_time = 0
clock_in_times = {}

spring_festival = input('If you choose time in Spring Festival, input 0; or if you choose ¥, input 1: ')
national_holiday = input('If you choose time in National Holiday, input 0; or if you choose ¥, input 1: ')

def oa(clock_in_times):
    directory = "/<your dir>/2022/"
    for subdir, dirs, files in os.walk(directory):
        for file in sorted(files):
            parse(directory + file, clock_in_times)
    print("Each month of clock-in time in 2022 are: ")
    total = 0
    for mon in clock_in_times:
        total += clock_in_times[mon]
        print(mon, ":", clock_in_times[mon])
    print("The total clock-in time of 2022 is: ", total)


def cal_working_day(working_hours, times):
    if working_hours >= 9:
        current_clock_in_times = working_hours - 9
        if current_clock_in_times >= 2:
            times += 2
        else:
            times += int(current_clock_in_times/0.5) * 0.5
    return times


def cal_holiday(working_hours, times, holiday_name):
    if re.findall("春节", holiday_name) and int(spring_festival) == 1:
        print("Since you chose ¥ in Spring Festival, so we remove the clock-in times...")
        return times
    if working_hours >= 8:
        times += 8
    elif working_hours >= 4:
        times += int(working_hours/0.5) * 0.5
    return times


def parse(file, clock_in_times):
    with open(file) as f:
        data = json.load(f)
    month = os.path.basename(file)
    i = 0
    clock_in_times[month] = 0
    while i < len(data['result']):
        start_time = data['result'][i]['worktime'].split(" ")[0]
        end_time   = data['result'][i]['worktime'].split(" ")[2]
        if len(start_time) == 0 or len(end_time) == 0:
            i += 1
            continue
        s = datetime.strptime(start_time, '%H:%M')
        e = datetime.strptime(end_time, '%H:%M')
        working_hours = (e-s).seconds/3600
        # 1. working day
        #          - 9 hours at least
        #          - 2 hours clock-in times maximum
        # 2. holiday
        #          - 4 hours at least
        #          - 8 hours maximum, no more clock-in times
        if data['result'][i]['isWorkDay'] == "yes":
            clock_in_times[month] = cal_working_day(working_hours, clock_in_times[month])
        else:
            holidayname = ""
            if('holidayname' in data['result'][i].keys()):
                holidayname = data['result'][i]['holidayname']
            clock_in_times[month] = cal_holiday(working_hours, clock_in_times[month], holidayname)
        i += 1


oa(clock_in_times)