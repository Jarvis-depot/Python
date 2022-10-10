import os
import re

# members you want to check disk usage
members = ['a', 'b', 'c', ...]
# Here for loading public tool, which could be added by "module load xxx" in linux
os.environ['A'] = 'A'
os.environ['B'] = 'B'

# Here we only need to support three kinds of storage
def convert(storage):
    if re.match(r'.*GB', storage):
        return float(storage.split("GB")[0]) / 1024
    elif re.match(r'.*MB', storage):
        return float(storage.split("MB")[0]) / (1024 * 1024)
    else:
        return float(storage.split("TB")[0])

# Generate the mail message
def mail(mail_list, path, case):
    if case == 1:
        mail_msg = "echo \"<font size=4>Hi all, <br><br>The usage of </font><font size=4 color=\"#FF0000\">"\
                    + path + "</font><font size=4> is more than 90%, so please help to cleanup your dir<br><br></font>\""
    else:
        mail_msg = "echo \"<font size=4>Hi all, <br><br>The left space of </font><font size=4 color=\"#FF0000\">"\
                    + path + "</font><font size=4> is less than 3TB, so please help to cleanup your dir<br><br></font>\""
    mail_attr = " | mail " + mail_list + "-cc xxx -subject \"[AUTO-MSG] Please help to release space\""
    os.system(mail_msg + mail_attr)

# Main program, monitor the disk usage by using <tool execute cmd>
def calculate(path):
    case = 0
    mail_list = ""
    cmd = "export PATH=$PATH:xxx\
           export PATH=$PATH:yyy\
           <tool execute cmd> " + path
    obj = os.popen(cmd)
    disk_usages = obj.read().strip()
    print("Checking", path)
    for disk_usage in disk_usages.split("\n"):
        msg = disk_usage.split("|")
        if (len(msg) > 10) and (re.match(r'\s*.*TB', msg[3].strip())):
            total        = convert(msg[3].strip())
            used         = convert(msg[4].strip())
            left         = convert(msg[5].strip())
            user         = msg[9].strip()
            disk_usage   = msg[10].strip()
            percentage   = int(used/total*100)
            if percentage > 90:
                case = 1
            elif left < 3:
                case = 2
            if re.match(r'\s*.*TB', disk_usage) and (user in members):
                 mail_list += user + "@xxxx.com "
    print("Checking", path, "done...")
    if mail_list != "" and case != 0:
        print("Mail users to cleanup...")
        mail(mail_list, path, case)

# choose which directories you wanna to check
def check():
    paths = ["AAA",
             "BBB"
             "CCC"]
    for path in paths:
        calculate(path)

check()