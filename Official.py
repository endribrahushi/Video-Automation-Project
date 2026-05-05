import cv2
import os
import numpy as np
from scenedetect import detect, ContentDetector
from moviepy import VideoFileClip, concatenate_videoclips
import random
import datetime
import time

def Substract_Timestamps(Timestamp1, Timestamp2):
    Timestamp1_Splitted = Timestamp1.split(":")
    Timestamp2_Splitted = Timestamp2.split(":")
    
    Seconds_Final = 0
    Minutes_Final = 0
    Hours_Final = 0

    Timestamp1_Seconds = float(Timestamp1_Splitted[2])
    Timestamp2_Seconds = float(Timestamp2_Splitted[2])

    Timestamp1_Minutes = int(Timestamp1_Splitted[1])
    Timestamp2_Minutes = int(Timestamp2_Splitted[1])

    Timestamp1_Hours = int(Timestamp1_Splitted[0])
    Timestamp2_Hours = int(Timestamp2_Splitted[0])

    if Timestamp2_Seconds - Timestamp1_Seconds < 0:
        Minutes_Final -= 1
        # print(Timestamp2_Seconds - Timestamp1_Seconds)
        Seconds_Final = round(60 + (Timestamp2_Seconds - Timestamp1_Seconds), 3)
        # print(Seconds_Final)
    elif Timestamp2_Seconds - Timestamp1_Seconds == 0:
        pass
    else:
        Seconds_Final += round((Timestamp2_Seconds - Timestamp1_Seconds), 3)
    
    if Timestamp2_Minutes - Timestamp1_Minutes < 0:
        Hours_Final -= 1
        Minutes_Final += 60 + (Timestamp2_Minutes - Timestamp1_Minutes)
    elif Timestamp2_Seconds - Timestamp1_Seconds == 0:
        pass
    else:
        Minutes_Final += (Timestamp2_Minutes - Timestamp1_Minutes)

    Hours_Final += Timestamp2_Hours - Timestamp1_Hours

    timestamp = "%02d:%02d:%#06.3f" % (Hours_Final,Minutes_Final,Seconds_Final)
    return timestamp
def Add_Timestamps(Timestamp1, Timestamp2):
    Timestamp1_Splitted = Timestamp1.split(":")
    Timestamp2_Splitted = Timestamp2.split(":")
    
    Seconds_Final = 0
    Minutes_Final = 0
    Hours_Final = 0

    Timestamp1_Seconds = float(Timestamp1_Splitted[2])
    Timestamp2_Seconds = float(Timestamp2_Splitted[2])

    Timestamp1_Minutes = int(Timestamp1_Splitted[1])
    Timestamp2_Minutes = int(Timestamp2_Splitted[1])

    Timestamp1_Hours = int(Timestamp1_Splitted[0])
    Timestamp2_Hours = int(Timestamp2_Splitted[0])

    if Timestamp2_Seconds + Timestamp1_Seconds > 60:
        Minutes_Final += 1
        # print(Timestamp2_Seconds - Timestamp1_Seconds)
        Seconds_Final += round((Timestamp2_Seconds + Timestamp1_Seconds) - 60, 3)
        # print(Seconds_Final)
    else:
        Seconds_Final += round((Timestamp2_Seconds + Timestamp1_Seconds), 3)
    
    if Timestamp2_Minutes - Timestamp1_Minutes > 60:
        Hours_Final += 1
        Minutes_Final += (Timestamp2_Minutes + Timestamp1_Minutes) - 60
    else:
        Minutes_Final += (Timestamp2_Minutes + Timestamp1_Minutes)

    Hours_Final += Timestamp2_Hours + Timestamp1_Hours

    timestamp = "%02d:%02d:%#06.3f" % (Hours_Final,Minutes_Final,Seconds_Final)
    return timestamp
def Timestamps_To_Seconds(Timestamp):
    Timestamp_Splitted = Timestamp.split(":")
    Seconds_Final = 0
    for i, Splitted_Part in enumerate(Timestamp_Splitted):
        if i == 0:
            if int(Splitted_Part) == 00:
                pass
            else:
                Seconds_Final += int(Splitted_Part) * 3600
        if i == 1:
            if int(Splitted_Part) == 00:
                pass
            else:
                Seconds_Final += int(Splitted_Part) * 60
        if i == 2:
            if float(Splitted_Part) == 00:
                pass
            else:
                Seconds_Final += float(Splitted_Part)

    return round(float(Seconds_Final), 3)
def Frames_To_Timestamp(Number_Of_Frames):
    hours = 0
    minutes = 0
    seconds = 0

    Seconds = Number_Of_Frames / 30

    if Seconds >= 3600:
        hours +=1
        Seconds-= 3600
    if Seconds >= 60:
        minutes =  Seconds // 60
        Seconds = Seconds - (minutes * 60)
    if Seconds < 60:
        seconds = round(Seconds, 3)
    
    timestamp = "%02d:%02d:%#06.3f" % (hours,minutes,seconds)
    return timestamp
def Calculate_Part_Length(array):
    x = 0
    Length_Of_The_Part =  0
    while x < len(array)-1:
        if int(x) == 0:
            First_Clip = array[x][5]
            Seconds_Clip = array[x+1][5]
            # print(First_Clip,Seconds_Clip)
            Length_Of_The_Part = Add_Timestamps(First_Clip, Seconds_Clip)
            x += 1
        else:
            Actual_length = Length_Of_The_Part
            Next_Clip = array[x+1][5]
            Length_Of_The_Part = Add_Timestamps(Actual_length, Next_Clip)
            x += 1
    return Length_Of_The_Part
def Detect_Black_Frames(file):
    cam = cv2.VideoCapture(file)
    currentframe = 0
    Black_Frames = []
    Black_Frame_Switch = False
    Other_Frame_Switch = False
    length = int(cam.get(cv2.CAP_PROP_FRAME_COUNT))
    
    while(True): 
        # reading from frame 
        ret,frame = cam.read() 
        if ret:
            currentframe += 1
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            if currentframe == 1:
                # print("First frame")
                if np.average(gray) > 0.1:
                    print(np.average(gray))
                    Other_Frame_Switch = True
                    Black_Frame_Switch = False
                else:
                    Other_Frame_Switch = False
                    Black_Frame_Switch = True
                    Black_Frames.append(currentframe)
            else:
                if np.average(gray) < 0.1:  # Nqoftse osht Zi
                    print(np.average(gray))
                    if Black_Frame_Switch == True:
                        Other_Frame_Switch = False
                        pass
                    elif Black_Frame_Switch == False:
                        Black_Frames.append((currentframe - 1 ))
                        Black_Frame_Switch = True
                elif np.average(gray) > 0.1: # Nqoftse nuk osht Zi
                    print(np.average(gray))
                    if Other_Frame_Switch == True:
                        Black_Frame_Switch = False
                        pass
                    elif Other_Frame_Switch == False:
                        Other_Frame_Switch = True
                        Black_Frames.append((currentframe))
            Progress = "%d/%d" % (currentframe, length)
            print(Progress, end="\r")
        else: 
            break
    # Release all space and windows once done


    cam.release() 
    cv2.destroyAllWindows()
    Final_Black_Frames = [Black_Frames[n:n+2] for n in range(len(Black_Frames)) if not n%2]
    for i, scene in enumerate(Final_Black_Frames):
        if len(scene) < 2:
            Final_Black_Frames.pop(i)
            continue
        Segment_Length = int(scene[1]) - int(scene[0])
        scene.append(Segment_Length)
        scene.append(Frames_To_Timestamp(Segment_Length))
    for i, scene in enumerate(Final_Black_Frames):
        if scene[2] < 100:
            Final_Black_Frames.pop(i)
            continue
    
    return Final_Black_Frames, Black_Frames
def Scene_Detect(file):

    scenes = []
    scene_list = detect(file, ContentDetector(), show_progress = True)
    for scene ,scene_1 in scene_list:
        scenes.append([
            scene.get_timecode(),scene_1.get_timecode(),
            scene.get_frames(),scene_1.get_frames(),
            int(scene_1.get_frames()) - int(scene.get_frames()),
            Substract_Timestamps(scene.get_timecode(),scene_1.get_timecode())
            ])
    return scenes
def Print_Parts(array):
    for part in array:
        print(part, end='\n\n\n')
def Print_Clips(array):
    for part in array:
        print(part, end='\n\n\n')
        for clip in part:
            print(clip)
        

File_Path = "Video 18 - RARE SWORDS On Pawn Stars!.mp4"
Folder = File_Path[:-4]
if os.path.exists(Folder):
    pass
else:
    os.mkdir(Folder)
File_Exists = False
print("Waiting for file")
while File_Exists == False:
    if not os.path.isfile(File_Path):
        continue
    else:
        File_Exists = True
        print("Found")
        # time.sleep(10)                                                ##########
Start_Script_Time = time.time()


video = VideoFileClip(File_Path)

scene_list = Scene_Detect(File_Path)
Black_Frames = Detect_Black_Frames(File_Path)
time.sleep(5)


Black_Segments = []
Parts = []
Part_Lengths = []
Parts_Arranged = []
Video_Parts = []
Video_Parts_Final = []
Voiceover_Parts = []
Final_MoviePy_Video = []


file_name = File_Path.split("-")
file_name = file_name[0]


with open(os.path.join(Folder, file_name + "_Saved_clips.txt"), "w", encoding='utf-8-sig') as Saved_Clips:                     
    Saved_Clips.write(str(scene_list))
    print("Saved_clips")
with open(os.path.join(Folder, file_name + "_Saved_Black_Segements.txt"), "w", encoding='utf-8-sig') as Saved_Black_Segements:
    Saved_Black_Segements.write(str(Black_Frames[0]))
    print("Saved_Black_Segements")
with open(os.path.join(Folder,file_name + "_Saved_Black_Segements_Raw.txt"), "w", encoding='utf-8-sig') as Saved_Black_Segements_Raw:
    Saved_Black_Segements_Raw.write(str(Black_Frames[1]))
    print("Raw_Saved_Black_Segements")
    

for Black_Segment in Black_Frames: # Find the black segments in the scene list
    for i, scene in enumerate(scene_list):
        # print(i)
        # print(scene)
        if (int(scene[2]) - 35) <= int(Black_Segment[0]) <= (int(scene[2]) + 35) and (int(scene[3]) - 35) <= int(Black_Segment[1]) <= (int(scene[3]) + 35):
            # print(True)
            Black_Segments.append(i)

for i, part in enumerate(Black_Segments):   # Save the clips corresponding to the Black Segment as parts
    Part_Temp = []
    Clips_Temp = []
    if i == len(Black_Segments)-1:
        Start = Black_Segments[i]
        # print(Start + 1, len(scene_list)-1)
        Part_Temp.append(list(scene_list[Start+1 : len(scene_list)]))
    else:
        Start = Black_Segments[i]
        End = Black_Segments[i+1]
        # print(Start, End)
        Part_Temp.append(list(scene_list[Start+1 : End]))
    
    for part in Part_Temp:
        for clip in part:
            Clips_Temp.append(list(clip))
        Parts.append(Clips_Temp)

for i, part in enumerate(Parts): #Remove the scenes that are shorter than 1 second
    Parts[i] = [clip for clip in part if int(clip[4]) >= 30]

for part in Parts: #Update the length of the Clips
    for clip in part:
        Start_Time = clip[0]
        End_Time = clip[1]
        Clip_Length = Substract_Timestamps(Start_Time,End_Time)
        clip[5] = Clip_Length
        # print(Start_Time,End_Time, Clip_Length)

for i, part in enumerate(Parts): #Calculate the length of each part and save it to Part_Lengths
    x = 0
    Length_Of_The_Part =  0
    while x < len(part)-1:
        if int(x) == 0:
            First_Clip = part[x][5]
            Seconds_Clip = part[x+1][5]
            # print(First_Clip,Seconds_Clip)
            Length_Of_The_Part = Add_Timestamps(First_Clip, Seconds_Clip)
            x += 1
        else:
            Actual_length = Length_Of_The_Part
            Next_Clip = part[x+1][5]
            Length_Of_The_Part = Add_Timestamps(Actual_length, Next_Clip)
            x += 1
    Part_Lengths.append(Length_Of_The_Part)
    # print(Length_Of_The_Part)
        
for i, part in enumerate(Parts): # Make the length of the clip <= 3.500 seconds
    for j, clip in enumerate(part):
        if Timestamps_To_Seconds(clip[5]) > 3.5:
            Clip_Length = clip[5]
            Original_End_Timestamp = clip[1] # The Original_End_Timestamp
            Amount_To_Substract =   Substract_Timestamps("00:00:03.500",Clip_Length) # Amount that we're gonna substract from End_Timestamp inorder to get the max 3.500 seconds
            New_Timestamp = Substract_Timestamps(Amount_To_Substract,Original_End_Timestamp)
            # print("Part Number:", i,"\nPart_Length_Before:",Part_Lengths[i],"\nStart_Time_Before:",clip[0],"\nEnd_Time_Before_Length", Original_End_Timestamp,"\nClip_Length_Before:",Clip_Length,"\n\nAmount to substract is:",Amount_To_Substract,"\n")
            clip[1] = New_Timestamp
            # print("Part Number:", i,"Part_Length_After:",Substract_Timestamps(Amount_To_Substract, Part_Lengths[i]),"\nStart_Time_After:",clip[0],"\nEnd_Time_After_Length:", New_Timestamp,"\nClip_Length_After:",Substract_Timestamps(clip[0],New_Timestamp),"\n\n\n")
            Part_Lengths[i] = Substract_Timestamps(Amount_To_Substract, Part_Lengths[i])
            clip[5] = Substract_Timestamps(clip[0],New_Timestamp)

for i, part in enumerate(Parts): # Remove empty clips and arrays, sometimes we get one
    if not part:
        print("Empty part removed from Parts")
        scene_list.pop(i)
    else:
        pass
    for j ,clip in enumerate(part):
        if not clip:
            print("Empty clip removed from Parts")
            part.pop(j)
        else:
            pass

for i, part in enumerate(Parts): #Add clips to fill the Black Segments

    Length_Needed = Black_Frames[i][3]
    Actual_length = Part_Lengths[i]

    Length_Needed_To_Seconds = round(Timestamps_To_Seconds(Length_Needed), 3)
    Actual_length_To_Seconds = round(Timestamps_To_Seconds(Actual_length),3)
    
    Choosen_clips = []

    if Actual_length_To_Seconds <= Length_Needed_To_Seconds:
        while Actual_length_To_Seconds <= Length_Needed_To_Seconds:
            
            if int(i) == len(Parts)-1:
                New_Clip = random.choice(Parts[i-1])
            else:
                New_Clip = random.choice(Parts[i+1])
            
            if not Choosen_clips:
                pass
            elif Choosen_clips[len(Choosen_clips) - 1] == New_Clip[5]:
                if int(i) == len(Parts)-1:
                    New_Clip = random.choice(Parts[i-1])
                else:
                    New_Clip = random.choice(Parts[i+1])
            elif Choosen_clips[len(Choosen_clips) - 1] == New_Clip[5]:
                if int(i) == len(Parts)-1:
                    New_Clip = random.choice(Parts[i-1])
                else:
                    New_Clip = random.choice(Parts[i+1])
            
            New_Clip = list(New_Clip)
            Choosen_clips.append(New_Clip[5])
            part.append(New_Clip)
            New_Clip_Length = New_Clip[5]
            Actual_length = Add_Timestamps(Actual_length, New_Clip_Length)
            Actual_length_To_Seconds += Timestamps_To_Seconds(New_Clip_Length)
            Part_Lengths[i] = Actual_length
            # print("Actual length after adding clips:", Actual_length)
    else:
        pass

for i, part in enumerate(Parts): #Remove the excess length for each part
    Length_Needed = Black_Frames[i][3]
    Actual_length = Part_Lengths[i]
    # print("Part:", i)
    # print("Length_Needed:",Length_Needed,"\n","Actual_length:",Actual_length)

    Length_Needed_To_Seconds = round(Timestamps_To_Seconds(Length_Needed), 3)
    Actual_length_To_Seconds = round(Timestamps_To_Seconds(Actual_length),3)

    if Actual_length_To_Seconds <= Length_Needed_To_Seconds:
        print("Error there's not enough clips for part")
    else:
        Excess_Length = Substract_Timestamps(Length_Needed, Actual_length)
        Excess_Length_To_Seconds = round(Timestamps_To_Seconds(Excess_Length), 3)
        Excess_Remover = "00:00:%#06.3f" % (Excess_Length_To_Seconds)
        # print(Excess_Remover,"\n")
        
        if Excess_Length_To_Seconds < 1:
            # print("Excess length shorter than 1 second")
            for m ,clip in enumerate(part):
                # print(m)
                Original_End_Timestamp = Parts[i][m][1]
                Original_Length = Parts[i][m][5]
                Clip_Length_To_Seconds = Timestamps_To_Seconds(Original_Length)
                if Clip_Length_To_Seconds > 2:
                    # print("Clip_Length_To_Seconds:",Clip_Length_To_Seconds,"\n", clip,"\n")
                    New_End_Timestamp = Substract_Timestamps(Excess_Length,Original_End_Timestamp)
                    New_Length = Substract_Timestamps(Excess_Length,Original_Length)
                    # print(New_End_Timestamp,"\n",New_Length)
                    Parts[i][m][1] = New_End_Timestamp
                    Parts[i][m][5] = New_Length
                    break
                else:
                    continue
        else:
            # print("Excess length longer than 1 second")
            Dividors = []
            Clips_Sorted = []
            Excess_Length = Substract_Timestamps(Length_Needed, Actual_length)
            Excess_Length_To_Seconds = round(Timestamps_To_Seconds(Excess_Length), 3)

            for l, clip in enumerate(part):
                Clips_Sorted.append([Timestamps_To_Seconds(clip[5]),list(clip),l])
            Clips_Sorted.sort(reverse=True)

            for j in range(len(part)):
                if j == 0 or j == 1:
                    continue
                # print(Excess_Length_To_Seconds*1000)
                Excess_Length_Remainder = (Excess_Length_To_Seconds*1000) % j
                if Excess_Length_Remainder == 0:
                    Dividors.append(j)
            if Dividors:
                Random_Dividor = random.choice(Dividors)
                Divided_Excess_Length_To_Seconds = round(Excess_Length_To_Seconds / Random_Dividor, 3)
                Divided_Excess_Remover = "00:00:%#06.3f" % (Divided_Excess_Length_To_Seconds)
                # print(Divided_Excess_Remover,Divided_Excess_Length_To_Seconds,Excess_Length,Random_Dividor)
                for k in range(Random_Dividor):
                    Clip_To_Edit = part[Clips_Sorted[k][2]]
                    Original_End_Timestamp = Clip_To_Edit[1]
                    Original_Length = Clip_To_Edit[5]
                    New_End_Timestamp = Substract_Timestamps(Divided_Excess_Remover, Original_End_Timestamp)
                    New_Clip_Length = Substract_Timestamps(Divided_Excess_Remover, Original_Length)
                    Clip_To_Edit[1] = New_End_Timestamp
                    Clip_To_Edit[5] = New_Clip_Length
            else:
                # print("No dividors found")
                Dividors = []
                Clips_Sorted = []
                for l, clip in enumerate(part):
                    Clips_Sorted.append([Timestamps_To_Seconds(clip[5]),list(clip),l])
                Clips_Sorted.sort(reverse=True)
                Clip_To_Edit = part[Clips_Sorted[0][2]]
                Original_End_Timestamp = Clip_To_Edit[1]
                Original_Length = Clip_To_Edit[5]
                New_End_Timestamp = Substract_Timestamps(Excess_Length, Original_End_Timestamp)
                New_Clip_Length = Substract_Timestamps(Excess_Length, Original_Length)
                Clip_To_Edit[1] = New_End_Timestamp
                Clip_To_Edit[5] = New_Clip_Length

for part in Parts: #Shuffle the parts
    random.shuffle(part)
    # print(part)

for i, Black_Segment in enumerate(Black_Segments):   #Prepare the Video_Parts
    if i == 0:
        # print(0)
        Start = 0
        End = Black_Segment
        # print(Black_Frames[0][0])
        # print("Start Clip:",scene_list[Start],'\n',
        #       "End Clip:",scene_list[End],'\n\n')
        Video_Parts.append(list([scene_list[Start][0], Frames_To_Timestamp(int(Black_Frames[0][0])), 
                                 0, Black_Frames[0][0], Black_Frames[0][0], 
                                 Substract_Timestamps(scene_list[Start][0], Frames_To_Timestamp(int(Black_Frames[0][0])))]))
    elif i  == len(Black_Segments)-1:
        # print("latest part")
        Start = Black_Segments[i-1] + 1
        End = Black_Segment
        Latest_Start = End + 1
        Latest_End = len(scene_list)
        
        # print("Start Clip:",scene_list[Start],'\n',
        #       "End Clip:",scene_list[End],'\n'
        #       "Latest_Clip_Start:",Latest_Start,'\n'
        #       "Latest_Clip_End:",Latest_End,'\n')
        Video_Parts.append(list([scene_list[Start][0], scene_list[End][0], 
                                 scene_list[Start][2] , scene_list[End][2], scene_list[End][2] - scene_list[Start][2], 
                                 Substract_Timestamps(scene_list[Start][0], scene_list[End][0])]))
        Video_Parts.append(list([scene_list[Latest_Start][0], scene_list[Latest_End-1][1], 
                                 scene_list[Latest_Start][2] , scene_list[Latest_End-1][3], scene_list[Latest_End-1][3] - scene_list[Latest_Start][2], 
                                 Substract_Timestamps(scene_list[Latest_Start][0], scene_list[Latest_End-1][1])]))
    else:
        # print("else")
        Start = Black_Segments[i-1] + 1
        End = Black_Segment
        # print("Start Clip:",scene_list[Start],'\n',
        #       "End Clip:",scene_list[End],'\n\n')
        Video_Parts.append(list([scene_list[Start][0], scene_list[End][0], 
                                 scene_list[Start][2] , scene_list[End][2], scene_list[End][2] - scene_list[Start][2], 
                                 Substract_Timestamps(scene_list[Start][0], scene_list[End][0])]))

for i, part in enumerate(Parts): #Prepare the Voiceover_Parts for exporting
    Audio_Start = Video_Parts[i][1]
    Audio_End = Video_Parts[i+1][0]
    print(Audio_Start, Audio_End)
    Clips = []

    for clip in part:
        Clips.append(video.subclipped(clip[0],clip[1]))

    Clips_Without_Audio = concatenate_videoclips(Clips)
    audio_segment = video.audio.subclipped(Audio_Start, Audio_End)
    Clips_With_Audio = Clips_Without_Audio.with_audio(audio_segment)

    Voiceover_Parts.append(Clips_With_Audio)

for Video_Part in Video_Parts: #Prepare the Video_Parts for exporting
    print(Video_Part[0],Video_Part[1])
    Video_Parts_Final.append(video.subclipped(Video_Part[0],Video_Part[1]))

for i in range(len(Voiceover_Parts)): #Arrange the  clips and Voice Overs
    if i == 0:
        Final_MoviePy_Video.append(Video_Parts_Final[i])
        Final_MoviePy_Video.append(Voiceover_Parts[i])
    elif i  == len(Voiceover_Parts)-1:
        Final_MoviePy_Video.append(Video_Parts_Final[i])
        Final_MoviePy_Video.append(Voiceover_Parts[i])
        Final_MoviePy_Video.append(Video_Parts_Final[i+1])
    else:
        Final_MoviePy_Video.append(Video_Parts_Final[i])
        Final_MoviePy_Video.append(Voiceover_Parts[i])


# Print_Parts(Parts_Arranged)
# Print_Parts(Video_Parts)
print("Amount of black segments:",len(Black_Segments),'\n',
      "Amount of parts:",len(Parts),'\n',
      "Final_MoviePy_Video:",len(Final_MoviePy_Video),'\n',
      "Amount of Video_Parts_Final:",len(Video_Parts_Final),'\n',
      "Amount of Voiceover_Parts:",len(Voiceover_Parts),'\n')

Final_Video = concatenate_videoclips(Final_MoviePy_Video)

Final_Video.write_videofile(File_Path[:-4] + "_Final_Video.mp4", codec="h264_nvenc", audio_codec="aac")




print("%s seconds ---" % (time.time() - Start_Script_Time))