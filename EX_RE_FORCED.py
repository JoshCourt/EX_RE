### EXCEL SHEETS READER AND PARSER

import xlrd
from datetime import datetime as dt
from datetime import timedelta as tidelt
from os import listdir
from os.path import isfile
from os.path import isdir
from os.path import isfile, join
import time
import subprocess
import sys
import os
import shutil
import os.path
from pathlib import Path
import csv

"""
    1. CSV READER - https://www.programiz.com/python-programming/reading-csv-files

"""



if os.path.isfile("concatlist.txt"):
    os.remove("concatlist.txt")



## Make Log File
class Logger(object):
    def __init__(self):
        self.terminal = sys.stdout
        self.log = open("logfile.txt", "a")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        #this flush method is needed for python 3 compatibility.
        #this handles the flush command by doing nothing.
        #you might want to specify some extra behavior here.
        pass

sys.stdout = Logger()
## Make Log File

def message(message, string_to_print):
	#timap = Time at present
	timap = dt.today().strftime('%X')
	print("MESSAGE : "+str(timap)+" "+message+" "+str(string_to_print))


workingdirectory = os.path.abspath(os.path.dirname(sys.argv[0]))

footagelocation = workingdirectory+"/footage"
Final_Edited_Files_Location = "Final_Edited_Files"
exclude_suffix = (".xlsx", ".py", ".txt" )
number_of_segment_for_each_timecodelist = 4
CSV_PAATH = "Template_2.csv"

def fmttime(millisecs):
    secs = millisecs
    #secs = millisecs
    d = tidelt(seconds=secs)
    t = (dt.min + d).time()
    milli = t.strftime('%f')[:3]
    value = t.strftime('%H:%M:%S,') + milli
    message("converted milisecond to timecode : ", value)
    return value

def listfiles1(LOCATION):
    onlyfiles = [f for f in listdir(LOCATION) if isfile(join(LOCATION, f))]
    #print(onlyfiles)
    time.sleep(2)
    return(onlyfiles)

def listfiles_in_footage_loc(LOCATION):
    onlyfiles = [f for f in listdir(LOCATION) if isfile(join(LOCATION, f))]
    #print(onlyfiles)
    time.sleep(2)
    return(onlyfiles)

def generate_timecodes_list_for_ffmpeg_2(TCs_LIST):
    finallist = []
    for timecode in TCs_LIST:
        timecode = str(timecode)
        timecode = timecode[:-2]
        #message("INTCtimecode are : ", timecode)
        timecode = timecode[1:]
        #message("INTCtimecode are : ", timecode)
        finalstring = []
        count = 0
        charcount = 0
        for num in range(0, 11):
            if str(count) == "0":
                #message("final string is : ", finalstring)
                finalstring.append("0")
                count+=1
                message("1 final string is : ", finalstring)
                continue
            elif str(count) == "1":
                finalstring.append("0")
                count+=1
                message("2 final string is : ", finalstring)
                continue
            elif count == 2:
                finalstring.append(":")
                count+=1
                message("3 final string is : ", finalstring)
                continue
            elif count == 5:
                finalstring.append(":")
                count+=1
                message("4 final string is : ", finalstring)
                continue
            elif count == 8:
                finalstring.append(".")
                count+=1
                message("5 final string is : ", finalstring)
                continue
            else:
                finalstring.append(timecode[charcount])
                count += 1
                message("6 final string is : ", finalstring)
                charcount += 1
        finalstring = ''.join(finalstring)
        #message("finalstring are : ", finalstring)
        finallist.append(finalstring)
        return finallist

def generate_timecodes_list_for_ffmpeg(TCs_LIST):
    finallist = []
    for timecode in TCs_LIST:
        timecode = str(timecode)
        timecode = timecode[:-2]
        #message("INTCtimecode are : ", timecode)
        timecode = timecode[1:]
        #message("INTCtimecode are : ", timecode)
        finalstring = []
        count = 0
        charcount = 0
        for num in range(0, 11):
            if str(count) == "0":
                #message("count are : ", count)
                finalstring.append("0")
                count+=1
                message("1 final string is : ", finalstring)
                continue
            elif str(count) == "1":
                finalstring.append("0")
                count+=1
                message("2 final string is : ", finalstring)
                continue
            elif count == 2:
                finalstring.append(":")
                count+=1
                message("3 final string is : ", finalstring)
                continue
            #elif count == 5:
            #    finalstring.append(":")
            #    count+=1
            #    message("4 final string is : ", finalstring)
            #    continue
            elif count == 8:
                finalstring.append(".")
                count+=1
                message("5 final string is : ", finalstring)
                continue
            else:
                finalstring.append(timecode[charcount])
                count += 1
                charcount += 1
        finalstring = ''.join(finalstring)
        #message("finalstring are : ", finalstring)
        finallist.append(finalstring)
    return finallist

exlude_suffix_3 = (".xlsx", ".py", ".csv")

def csv_read(CSV_Path):
    TCs = list()
    with open(CSV_Path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            print(row)
            for _ in row:
                print(_)
                TCs.append(_)
    return TCs


def organise_TCs(TCs):
    # Returns IN and OUT TCs where list contains EG: IN OUT IN OUT ect.
    IN_TC = list()
    OUT_TC = list()
    count = 0
    for _ in TCs:
        if count == 0:
            print("COUNT IS : "+str(count))
            print("IN_TC is : "+str(_))
            IN_TC.append(_)
            count += 1
            continue
        elif count == 1:
            print("COUNT IS : "+str(count))
            print("OUT_TC is : "+str(_))
            OUT_TC.append(_)
            count = 0
            continue
    print("TCs are....")
    TC_counter = 0
    end_count = len(IN_TC)
    for _ in IN_TC:
        if TC_counter == end_count:
            break
        print(str(TC_counter)+". IN_TC : "+str(IN_TC[TC_counter])+" OUT_TC : "+str(OUT_TC[TC_counter]))
        TC_counter +=1
    return IN_TC, OUT_TC

def EXRE_FORCED():
    LOF = listfiles1(footagelocation)
    for name in LOF:
        message("Checking LOF list and editing. Currently checking : ", name)

        if name.endswith(exlude_suffix_3):
            message("BAD name detected is : ", name)
            LOF.remove(name)
            continue

    TC_count = 0
    TCs = csv_read(CSV_PAATH)
    print("TCs are : "+str(TCs))
    IN_TCs_LIST, OUT_TCs_LIST = organise_TCs(TCs)
    for num in range(0, len(LOF)):
        #IN_TCs_LIST = ["00:02:00.00", "00:17:25.05", "00:26:11.20", "00:37:56.05", "00:02:00.00", "00:14:47.08", "00:25:34.12", "00:36:47.04", "00:02:00.00", "00:16:53.19", "00:24:13.10", "00:39:31.09", "00:02:00.00", "00:15:14.01", "00:27:37.17", "00:36:47.16", "00:02:00.00", "00:15:18.16", "00:23:23.23", "00:37:08.05", "00:02:00.00", "00:15:05.21", "00:26:45.00", "00:37:36.00"]
        #OUT_TCs_LIST = ["00:17:25.05", "00:26:11.20", "00:37:56.05", "00:47:14.00", "00:14:47.08", "00:25:34.12", "00:36:47.04", "00:47:14.00", "00:16:53.19", "00:24:13.10", "00:39:31.09", "00:47:14.00", "00:15:14.01", "00:27:37.17", "00:36:47.16", "00:47:41.19", "00:15:18.16", "00:23:23.23", "00:37:08.05", "00:47:15.03", "00:15:05.21", "00:26:45.00", "00:37:36.00", "00:47:28.00"]
        INTCs_timecode_list = IN_TCs_LIST
        OUTTCs_timecode_list = OUT_TCs_LIST

        message("INTCs_timecode_list is : ", INTCs_timecode_list)
        message("OUTTCs_timecode_list is : ", OUTTCs_timecode_list)


        message("\n\nEDITING FILES!! : ", name)
        print(LOF[num])
        file = os.path.join(Path(footagelocation), LOF[num])
        for number in range(0, number_of_segment_for_each_timecodelist):
            message("number is : ", number)
            print(str(INTCs_timecode_list[TC_count])+" : "+str(OUTTCs_timecode_list[TC_count]))
            command = "ffmpeg -i \""+str(file)+"\" -ss "+str(INTCs_timecode_list[TC_count])+" -to "+str(OUTTCs_timecode_list[TC_count])+" -c copy -async 1 \""+str(file[:-4])+"_SEGMENT_"+str(number+1)+".mp4\""
            message("command is : ", command)
            TC_count += 1
            #subprocess.call(command, shell=True)


        """ RECHECK FOR FILES THAT SHOULDNT BE THERE!!! AND ONLY USE FILES WITH "SEGMENT" IN NAME"""
        """ RECHECK FOR FILES THAT SHOULDNT BE THERE!!! AND ONLY USE FILES WITH "SEGMENT" IN NAME"""
        """ RECHECK FOR FILES THAT SHOULDNT BE THERE!!! AND ONLY USE FILES WITH "SEGMENT" IN NAME"""

    """ The rest of the codde is for concatenating when the timecode list provided. cuts each episode into more thn 4 parts!! !!

            HAVE JUST CREATED A FUNCTION. DONT KNOW IF IT STILL WORKS BELLOW!!!!!!!"""
EXRE_FORCED()

def concatenate_6parts_into_4():
    LOF1 = listfiles1(footagelocation)
    for name in LOF1:
        message("Checking LOF list and editing. Currently checking : ", name)
        if str(name).endswith(".xlsx"):
            #message("xlsx1 name detected is : ", name)
            LOF1.remove(name)
            continue
        elif str(name).endswith(".py"):
            #message("py name detected is : ", name)
            LOF1.remove(name)
            continue
        elif str(name).endswith(".xlsx"):
            #message("xlsx2 name detected is : ", name)
            LOF1.remove(name)
            continue
        elif not "SEGMENT" in str(name):
            message("file not a second edit detected : ", name)
            LOF1.remove(name)
            continue

        """ RECHECK FOR FILES THAT SHOULDNT BE THERE!!! AND ONLY USE FILES WITH "SEGMENT" IN NAME"""
        """ RECHECK FOR FILES THAT SHOULDNT BE THERE!!! AND ONLY USE FILES WITH "SEGMENT" IN NAME"""
        """ RECHECK FOR FILES THAT SHOULDNT BE THERE!!! AND ONLY USE FILES WITH "SEGMENT" IN NAME"""

    message("\n\n\n\nEDITING FILES!! 2: ", name)
    print(LOF1[num])
    def concatmake(file1, file2):
        writethis = "file \'"+str(file1)+"\'\nfile \'"+str(file2)+"\'"
        with open("concatlist.txt", "w") as filnam:
            filnam.write(writethis+"\n")
        filnam.close()

    for file in LOF1:
        message("LOOKING FOR SEGMENT_2s : ", file)
        if file.endswith(exclude_suffix):
            continue
        if "SEGMENT_2" in file:
            message("SEGMENT_2 is in filename: ", file)
            # ffmpeg -i "concat:input1.ts|input2.ts|input3.ts" -c copy output.ts #
            #ffmpeg -i A.avi -i B.mp4 -c:a copy out3.mov
            """ CREATE CONCAT TXT"""
            #command = "ffmpeg -i \""+str(file)+"\" -i \""+str(file.replace("SEGMENT_2", "SEGMENT_3"))+"\" -c copy  \"2"+str(file)+"\""
            concatmake(str(file), str(file.replace("SEGMENT_2", "SEGMENT_3")))
            command2 = "ffmpeg -f concat -safe 0 -i concatlist.txt  -c copy  \"2"+str(file)+"\""
            message("command is : ", command2)
            subprocess.call(command2, shell=True)
            print("REMOVING : "+str(file))
            os.remove(file)
            print("REMOVING : "+str(file.replace("SEGMENT_2", "SEGMENT_3")))
            os.remove(file.replace("SEGMENT_2", "SEGMENT_3"))
            os.rename("2"+str(file), file)
            shutil.move(file, Final_Edited_Files_Location)
            os.remove("concatlist.txt")
            LOF1.remove(file.replace("SEGMENT_2", "SEGMENT_3"))
            LOF1.remove(file)

    for file in LOF1:
        message("file in LOF is : ", file)
        if file.endswith(exclude_suffix):
            continue
        if "SEGMENT_4" in file:
            message("SEGMENT_4 is in filename: ", file)
            # ffmpeg -i "concat:input1.ts|input2.ts|input3.ts" -c copy output.ts #
            #command = "ffmpeg -i \""+str(file)+"\" -i \""+str(file.replace("SEGMENT_4", "SEGMENT_5"))+"\" -c copy  \"2"+str(file)+"\""
            concatmake(str(file), str(file.replace("SEGMENT_4", "SEGMENT_5")))
            command3 = "ffmpeg -f concat -safe 0 -i concatlist.txt  -c copy  \"2"+str(file)+"\""
            message("command is : ", command3)
            subprocess.call(command3, shell=True)
            print("REMOVING : "+str(file))
            os.remove(file)
            print("REMOVING : "+str(file.replace("SEGMENT_4", "SEGMENT_5")))
            os.remove(file.replace("SEGMENT_4", "SEGMENT_5"))
            os.rename("2"+str(file), file)
            shutil.move(file, Final_Edited_Files_Location)
            os.remove("concatlist.txt")
            LOF1.remove(file.replace("SEGMENT_4", "SEGMENT_5"))
            LOF1.remove(file)

    LOF2 = listfiles1(footagelocation)
    for file in LOF2:
        if "SEGMENT" in file:
            print("MOVING OTHER FILES.")
            print("MOVING  : "+str(file))
            shutil.move(file, Final_Edited_Files_Location)
            LOF1.remove(file)

    """ RENAME FIONISHED FIES """
    LOF3 = listfiles1(Final_Edited_Files_Location)
    for file in LOF3:
        if "SEGMENT_2" in file:
            newname = file.replace("SEGMENT_2", "SEGMENT_3")
            newname = os.path.join(Final_Edited_Files_Location, newname)
            file = os.path.join(Final_Edited_Files_Location, file)
            os.rename(file, newname)

    for file in LOF3:
        if "SEGMENT_1" in file:
            newname = file.replace("SEGMENT_1", "SEGMENT_2")
            newname = os.path.join(Final_Edited_Files_Location, newname)
            file = os.path.join(Final_Edited_Files_Location, file)
            os.rename(file, newname)

    for file in LOF3:
        if "SEGMENT_0" in file:
            newname = file.replace("SEGMENT_0", "SEGMENT_1")
            newname = os.path.join(Final_Edited_Files_Location, newname)
            file = os.path.join(Final_Edited_Files_Location, file)
            os.rename(file, newname)

    #IN_TCs = []
    #IN_TCs.append(grab_cell_from_row_if_float(1))


    #INTCs_timecode_list = generate_timecodes_list_for_ffmpeg(IN_TCs_LIST)
    #OUTTCs_timecode_list = generate_timecodes_list_for_ffmpeg(OUT_TCs_LIST)

    #message("INTCs_timecode_list is : ", INTCs_timecode_list)
    #message("OUTTCs_timecode_list is : ", OUTTCs_timecode_list)
        #fmttime(INTCtimecode)

    #message("int(IN_TCs_LIST[0]) are : ", int(IN_TCs_LIST[0]))
    #fmttime(int(IN_TCs_LIST[0]))
