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
from timecode import Timecode
from pymediainfo import MediaInfo
from send2trash import send2trash


"""
    1. CSV READER - https://www.programiz.com/python-programming/reading-csv-files

"""

file_working_on = "program_file_1.txt"

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

def CUSTMF(FOLDERLOCATION):
	# Make a custom Folder Location
	if not os.path.exists(FOLDERLOCATION):
		print("Making "+str(FOLDERLOCATION)+" Folder")
		try:
			os.mkdir(FOLDERLOCATION)
		except:
			print("Could not create "+str(FOLDERLOCATION)+" \nCould be a problem with permissions or disk space...?")
			pass
	else:
		print(str(FOLDERLOCATION)+" Already exists! Continuing!!")

workingdirectory = os.path.abspath(os.path.dirname(sys.argv[0]))

footagelocation = workingdirectory+"/footage"
footagelocation_afterfirstedit = workingdirectory+"/first_edit"
Final_Edited_Files_Location = "Final_Edited_Files"
exclude_suffix = (".xlsx", ".py", ".txt" )
number_of_segment_for_each_timecodelist = 6
CSV_PAATH = "Template_2.csv"
Concat_6_parts_too_4_ = "YES"
ffmpeg_loc = workingdirectory+"/ffmpeg.exe"
ffmpeg_loc = Path(ffmpeg_loc)
ffmpeg_loc = str(ffmpeg_loc)

CUSTMF(footagelocation)
CUSTMF(footagelocation_afterfirstedit)
CUSTMF(Final_Edited_Files_Location)

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


def grab_framerate(filelocatione):
    try:
        media_info = MediaInfo.parse(filelocatione)
        tracks = media_info.tracks
    except Exception as E:
        print("ERROR PARSING VIDEO with mediainfo. Maybe Not Video? : "+str(E))
        return False
    for track in tracks:
        if track.frame_rate:
            F_R = float(track.frame_rate)
            global FRAME_RATE
            FRAME_RATE = F_R
            print("FOUND FRAME RATE!!. Frame Rate is : "+str(FRAME_RATE)+" fps.")
            return True
        else:
            print("Cannot find frame rate!!")
            return False

def add_timecodes(timecode_a, timecode_b):
    tc1 = Timecode(FRAME_RATE, timecode_a)
    tc2 = Timecode(FRAME_RATE, timecode_b)
    tc3 = tc1 + tc2
    return tc3

def add_1minute_too_TC(TC):
    TC = TC.replace(".", ":")
    #print("1. add_1minute TC is : "+str(TC))
    TC = add_timecodes(TC, "00:01:00:00")
    #print("2. add_1minute is returning : "+str(TC))
    return TC

def replacer(s, newstring, index, nofail=False):
    # raise an error if index is outside of the string
    if not nofail and index not in range(len(s)):
        raise ValueError("index outside given string")

    # if not erroring, but the index is still not in the correct range..
    if index < 0:  # add it to the beginning
        return newstring + s
    if index > len(s):  # add it to the end
        return s + newstring

    # insert the new string between "slices" of the original
    return s[:index] + newstring + s[index + 1:]

def adjust_timecodes_with_ten_and_all_colons_and_within_hour_long(TC):
    #print("1. TC is : "+str(TC))
    TC = TC[2:]
    #print("2. TC[2:] is : "+str(TC))
    TC_nano_2 = TC[-1]
    #print("3. TC_nano_2 is : "+str(TC_nano_2))
    TC_nano_1 = TC[-2]
    #print("4. TC_nano_1 is : "+str(TC_nano_1))
    TC = "00"+TC
    #print("5. TC is : "+str(TC))
    TC = TC[:-3]
    #print("6. TC is : "+str(TC))
    TC = TC+"."+TC_nano_1+TC_nano_2
    #print("7. TC is : "+str(TC))
    return TC

def adjust_timecodes_with_ONE_and_all_colons_and_within_hour_long(TC):
    # PRESUMING THE ONE IS AN INDICATOR THAT EVERYTHING IN THE TIMECODE IS ACTUALY + 1 MINUTE!!!!

    #print("1. TC is : "+str(TC))
    TC = TC[1:]
    #print("2. TC[1:] is : "+str(TC))
    TC_nano_2 = TC[-1]
    #print("3. TC_nano_2 [-1] is : "+str(TC_nano_2))
    TC_nano_1 = TC[-2]
    #print("4. TC_nano_1 [-2] is : "+str(TC_nano_1))
    TC = "00"+TC
    #print("5. TC is : "+str(TC))
    TC = TC[:-3]
    #print("6. TC is : "+str(TC))
    TC = TC+":"+TC_nano_1+TC_nano_2+".00"
    #print("7. TC is : "+str(TC))
    TC = add_1minute_too_TC(TC)

    TC = replacer(str(TC), ".", 8)
    print("8. TC is : "+str(TC))
    return TC

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
        _ = adjust_timecodes_with_ONE_and_all_colons_and_within_hour_long(_)
        if count == 0:
            #print("COUNT IS : "+str(count))
            #print("IN_TC is : "+str(_))
            IN_TC.append(_)
            count += 1
            continue
        elif count == 1:
            #print("COUNT IS : "+str(count))
            #print("OUT_TC is : "+str(_))
            OUT_TC.append(_)
            count = 0
            continue
    #print("TCs are....")
    TC_counter = 0
    end_count = len(IN_TC)
    for _ in IN_TC:
        if TC_counter == end_count:
            break
        print(str(TC_counter)+". IN_TC : "+str(IN_TC[TC_counter])+" OUT_TC : "+str(OUT_TC[TC_counter]))
        TC_counter +=1
    return IN_TC, OUT_TC

def read_first_line(file):
    with open(file, "r") as fil:
        line = fil.readline()
        print("read_first_line is : "+str(line))
        return line
        #cnt = 1
        #while line:
        #    check_file2(str(line.strip()))
        #    line = filelist.readline()
        #    cnt += 1


def check_for_unfinished_file():
    if os.path.exists(file_working_on):
        print(str(file_working_on)+" : Exists! Checking contents.")
        delete_file_location = read_first_line(file_working_on)
        os.remove(delete_file_location)
        os.remove(file_working_on)

def create_file_working_on_txt(text_to_write):
    with open(file_working_on, "w") as yum:
        yum.write(str(text_to_write))
    yum.close()

def EXRE_FORCED():

    """
            NEED TOO OUTPUT TO SPEERTE FOLDER!!!!!!!!!
            NEED TOO OUTPUT TO SPEERTE FOLDER!!!!!!!!!              NEED TOO OUTPUT TO SPEERTE FOLDER!!!!!!!!!              NEED TOO OUTPUT TO SPEERTE FOLDER!!!!!!!!!
    """

    # check for any "file working on txt". Delete the file in that text and the text. If it had been completed that text wouldnt be there
    check_for_unfinished_file()
    LOF = listfiles1(footagelocation)
    for name in LOF:
        # ALERT : All files must be of the same frame rate for timecodes to add together properly.
        message("Checking LOF list and editing. Currently checking : ", name)
        framerate_file = os.path.join(Path(footagelocation),name)
        if name.endswith(exlude_suffix_3):
            message("BAD name suffix detected is : ", name)
            LOF.remove(name)
            continue

    TC_count = 0
    TCs = csv_read(CSV_PAATH)
    print("TCs are : "+str(TCs))
    grab_framerate(framerate_file)
    IN_TCs_LIST, OUT_TCs_LIST = organise_TCs(TCs)
    for num in range(0, len(LOF)):
        #IN_TCs_LIST = ["00:02:00.00", "00:17:25.05", "00:26:11.20", "00:37:56.05", "00:02:00.00", "00:14:47.08", "00:25:34.12", "00:36:47.04", "00:02:00.00", "00:16:53.19", "00:24:13.10", "00:39:31.09", "00:02:00.00", "00:15:14.01", "00:27:37.17", "00:36:47.16", "00:02:00.00", "00:15:18.16", "00:23:23.23", "00:37:08.05", "00:02:00.00", "00:15:05.21", "00:26:45.00", "00:37:36.00"]
        #OUT_TCs_LIST = ["00:17:25.05", "00:26:11.20", "00:37:56.05", "00:47:14.00", "00:14:47.08", "00:25:34.12", "00:36:47.04", "00:47:14.00", "00:16:53.19", "00:24:13.10", "00:39:31.09", "00:47:14.00", "00:15:14.01", "00:27:37.17", "00:36:47.16", "00:47:41.19", "00:15:18.16", "00:23:23.23", "00:37:08.05", "00:47:15.03", "00:15:05.21", "00:26:45.00", "00:37:36.00", "00:47:28.00"]
        INTCs_timecode_list = IN_TCs_LIST
        OUTTCs_timecode_list = OUT_TCs_LIST

        #message("INTCs_timecode_list is : ", INTCs_timecode_list)
        #message("OUTTCs_timecode_list is : ", OUTTCs_timecode_list)


        print(LOF[num])
        file = os.path.join(Path(footagelocation), LOF[num])
        for number in range(0, number_of_segment_for_each_timecodelist):
            segment_creator(file, number, file_working_on, INTCs_timecode_list, OUTTCs_timecode_list, LOF[num], TC_count)
            TC_count += 1
        """ RECHECK FOR FILES THAT SHOULDNT BE THERE!!! AND ONLY USE FILES WITH "SEGMENT" IN NAME"""
        """ RECHECK FOR FILES THAT SHOULDNT BE THERE!!! AND ONLY USE FILES WITH "SEGMENT" IN NAME"""
        """ RECHECK FOR FILES THAT SHOULDNT BE THERE!!! AND ONLY USE FILES WITH "SEGMENT" IN NAME"""

    """ The rest of the codde is for concatenating when the timecode list provided. cuts each episode into more thn 4 parts!! !!

            HAVE JUST CREATED A FUNCTION. DONT KNOW IF IT STILL WORKS BELLOW!!!!!!!"""

def segment_creator(file, number, file_working_on, INTCs_timecode_list, OUTTCs_timecode_list, just_filename, TC_count):
    finished_filename = footagelocation_afterfirstedit+"/"+str(just_filename[:-4])+"_SEGMENT_"+str(number+1)+".mpg"
    finished_filename = Path(finished_filename)
    print("finished_filename is : "+str(finished_filename))
    message("number is : ", number)
    print(str(INTCs_timecode_list[TC_count])+" : "+str(OUTTCs_timecode_list[TC_count]))
    #command = "ffmpeg -i \""+str(file)+"\" -ss "+str(INTCs_timecode_list[TC_count])+" -to "+str(OUTTCs_timecode_list[TC_count])+" -crf 0 -filter_complex aresample \""+str(file[:-4])+"_SEGMENT_"+str(number+1)+".mpg\""
    #command = "ffmpeg -i \""+str(file)+"\" -ss "+str(INTCs_timecode_list[TC_count])+" -to "+str(OUTTCs_timecode_list[TC_count])+" -c copy \""+str(file[:-4])+"_SEGMENT_"+str(number+1)+".mpg\""
    #command = "ffmpeg -i \""+str(file)+"\" -target pal-dvd -ps 1500000000 -ss "+str(INTCs_timecode_list[TC_count]).replace(";", ".")+" -to "+str(OUTTCs_timecode_list[TC_count]).replace(";", ".")+" -crf 0 -filter_complex aresample \""+str(file[:-4])+"_SEGMENT_"+str(number+1)+".mpg\""
    # https://ffmpeg.org/ffmpeg-filters.html
    #command = "ffmpeg -i \""+str(file)+"\"  -aspect 16:9 -target pal-dvd -ps 1500000000 -ss "+str(INTCs_timecode_list[TC_count]).replace(";", ".")+" -to "+str(OUTTCs_timecode_list[TC_count]).replace(";", ".")+" -crf 0 -filter_complex aresample=async=1000 \""+str(file[:-4])+"_SEGMENT_"+str(number+1)+".mpg\""
    # -loglevel warning
    #command = "ffmpeg -i \""+str(file)+"\" -aspect 16:9 -target pal-dvd -ps 1500000000 -ss "+str(INTCs_timecode_list[TC_count]).replace(";", ".")+" -to "+str(OUTTCs_timecode_list[TC_count]).replace(";", ".")+" -crf 0 -filter_complex aresample=async=1000 \""+str(finished_filename)+"\""
    command = "\""+str(ffmpeg_loc)+"\" -i \""+str(file)+"\" -aspect 16:9 -target pal-dvd -ps 1500000000 -ss "+str(INTCs_timecode_list[TC_count]).replace(";", ".")+" -to "+str(OUTTCs_timecode_list[TC_count]).replace(";", ".")+" -crf 0 -filter_complex aresample=async=1000 \""+str(finished_filename)+"\""


    message("command is : ", command)
    # Check function. Does file exist already. If yes. Continue
    if os.path.exists(finished_filename) == True:
        print(str(finished_filename)+" : EXISTS! Moving onto next file")
        #TC_count += 1
    else:
        # Function to create file working on txt
        print(str(finished_filename)+" : DOESNT EXIST! RENDERING \n\n")
        create_file_working_on_txt(finished_filename)
        subprocess.call(command, shell=True)

        # Function to delete file working on txt
        os.remove(file_working_on)
        #TC_count += 1

EXRE_FORCED()

def concatenate_6parts_into_4():
    LOF1 = listfiles1(footagelocation_afterfirstedit)
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
    #print(LOF1[num])
    def concatmake(file1, file2):
        writethis = "file \'"+str(file1)+"\'\nfile \'"+str(file2)+"\'"
        with open("concatlist.txt", "w") as filnam:
            filnam.write(writethis+"\n")
        filnam.close()

    Final_Edited_Files_Location_FULL = Path(workingdirectory) / Final_Edited_Files_Location
    Final_Edited_Files_Location_FULL = str(Final_Edited_Files_Location_FULL)
    for file in LOF1:
        file_location = Path(footagelocation_afterfirstedit) / file
        file_location = str(file_location)
        message("LOOKING FOR SEGMENT_3s : ", file)
        if file.endswith(exclude_suffix):
            continue
        if "SEGMENT_3" in file:
            message("SEGMENT_3 is in filename: ", file)
            # ffmpeg -i "concat:input1.ts|input2.ts|input3.ts" -c copy output.ts #
            #ffmpeg -i A.avi -i B.mp4 -c:a copy out3.mov
            """ CREATE CONCAT TXT"""
            #command = "ffmpeg -i \""+str(file)+"\" -i \""+str(file.replace("SEGMENT_2", "SEGMENT_3"))+"\" -c copy  \"2"+str(file)+"\""
            os.chdir(footagelocation_afterfirstedit)
            concatmake(str(file), str(file.replace("SEGMENT_3", "SEGMENT_4")))
            command2 = "\""+str(ffmpeg_loc)+"\" -f concat -safe 0 -i concatlist.txt -c:v copy \"2"+str(file)+"\""
            message("command is : ", command2)
            subprocess.call(command2, shell=True)
            print("REMOVING : "+str(file))
            #os.remove(file)
            send2trash(file)
            print("REMOVING : "+str(file.replace("SEGMENT_3", "SEGMENT_4")))
            #os.remove(file.replace("SEGMENT_2", "SEGMENT_3"))
            send2trash(file.replace("SEGMENT_3", "SEGMENT_4"))
            os.rename("2"+str(file), file)
            shutil.move(file_location, Final_Edited_Files_Location_FULL)
            os.remove("concatlist.txt")
            LOF1.remove(file.replace("SEGMENT_3", "SEGMENT_4"))
            LOF1.remove(file)
            os.chdir('../')

    for file in LOF1:
        file_location = Path(footagelocation_afterfirstedit) / file
        file_location = str(file_location)
        message("file in LOF is : ", file)
        if file.endswith(exclude_suffix):
            continue
        if "SEGMENT_5" in file:
            message("SEGMENT_5 is in filename: ", file)
            # ffmpeg -i "concat:input1.ts|input2.ts|input3.ts" -c copy output.ts #
            #command = "ffmpeg -i \""+str(file)+"\" -i \""+str(file.replace("SEGMENT_4", "SEGMENT_5"))+"\" -c copy  \"2"+str(file)+"\""
            os.chdir(footagelocation_afterfirstedit)
            concatmake(str(file), str(file.replace("SEGMENT_5", "SEGMENT_6")))
            command3 = "\""+str(ffmpeg_loc)+"\" -f concat -safe 0 -i concatlist.txt -c:v copy \"2"+str(file)+"\""
            message("command is : ", command3)
            subprocess.call(command3, shell=True)
            print("REMOVING : "+str(file))
            #os.remove(file)
            send2trash(file)
            print("REMOVING : "+str(file.replace("SEGMENT_5", "SEGMENT_6")))
            #os.remove(file.replace("SEGMENT_4", "SEGMENT_5"))
            send2trash(file.replace("SEGMENT_5", "SEGMENT_6"))
            os.rename("2"+str(file), file)
            shutil.move(file_location, Final_Edited_Files_Location_FULL)
            os.remove("concatlist.txt")
            file.replace("SEGMENT_5", "SEGMENT_6")
            LOF1.remove(file.replace("SEGMENT_5", "SEGMENT_6"))
            LOF1.remove(file)
            os.chdir('../')

    LOF2 = listfiles1(footagelocation_afterfirstedit)
    for file_2 in LOF2:
        print(str(file_2))
        if file_2.endswith(".mpg"):
            print(" MOVING FILE!\n")
            file_location = Path(footagelocation_afterfirstedit) / file_2
            file_location = str(file_location)
            shutil.move(file_location, Final_Edited_Files_Location_FULL)
    #for file_2 in LOF2:
    #    print("PRINTING LOF 2. File is : "+str(file_2))
    #    file_location = Path(footagelocation_afterfirstedit) / file_2
    #    file_location = str(file_location)
    #    if "SEGMENT" in file:
    #        print("MOVING OTHER FILES.")
    #        print("MOVING  : "+str(file))
    #        shutil.move(file_location, Final_Edited_Files_Location_FULL)
    #        LOF2.remove(file)
    #        continue
    #    else:
            #print("SEGMENT not in file : "+str(file))

    """ RENAME FIONISHED FIES """
    LOF3 = listfiles1(Final_Edited_Files_Location_FULL)
    for file in LOF3:
        if "SEGMENT_5" in file:
            print("RENAMING SEGMENT_5 : SEGMENT_4")
            newname = file.replace("SEGMENT_5", "SEGMENT_4")
            newname = os.path.join(Final_Edited_Files_Location_FULL, newname)
            file = os.path.join(Final_Edited_Files_Location_FULL, file)
            os.rename(str(file), str(newname))
#
#    for file in LOF3:
#        if "SEGMENT_1" in file:
#            newname = file.replace("SEGMENT_1", "SEGMENT_2")
#            newname = os.path.join(Final_Edited_Files_Location_FULL, newname)
#            file = os.path.join(Final_Edited_Files_Location_FULL, file)
#            os.rename(file, newname)
#
#    for file in LOF3:
#        if "SEGMENT_0" in file:
#            newname = file.replace("SEGMENT_0", "SEGMENT_1")
#            newname = os.path.join(Final_Edited_Files_Location_FULL, newname)
#            file = os.path.join(Final_Edited_Files_Location_FULL, file)
#            os.rename(file, newname)

if Concat_6_parts_too_4_ == "YES":
    concatenate_6parts_into_4()
