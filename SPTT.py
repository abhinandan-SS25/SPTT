#Importing required libraries
from tkinter import *
from mysql.connector import *
from tkinter.font import *
import speech_recognition as sr 
import os 
from pydub import AudioSegment
from pydub.silence import split_on_silence
import pyaudio 
import wave 
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
from PIL import Image, ImageTk


USERNAME=[""] #to remember login username

#creating functions
#configuration for hover on buttons
def on_enter(e):
    e.widget["background"]='#084161'
def on_leave(e):
    e.widget["background"]= '#0D1B2C'
def on_enter_exit(e):
    e.widget["background"]='#A57700'
def on_leave_exit(e):
    e.widget["background"]= '#111C2A'
def on_exit_main(e):
    e.widget["background"]="#596065"
def on_enter_loginback(e):
    e.widget["background"]='#A57700'
def on_leave_loginback(e):
    e.widget["background"]= '#889BB2'
def on_enter_signupback(e):
    e.widget["background"]='#A57700'
def on_leave_signupback(e):
    e.widget["background"]= '#385287'
#login check for access
def login_check(un,pas):
    if un=="" or pas=="":
        #error handle for wrong entries
        loginerror["fg"]="red"
        loginerror["text"]="PLEASE PROVIDE YOUR CREDENTIALS"
        return#return used to break out of function
    myDB=connect(host="localhost",user="root",password="a1289141144114", database="sptt1")
    cursor=myDB.cursor()
    cursor.execute("SELECT name,username,password FROM userdata;")
    data=cursor.fetchall()
    for i in range(len(data)):
        if data[i][1]==un and data[i][2]==pas:
            #correct login info
            loginerror["fg"]="green"
            loginerror["text"]="LOGIN SUCCESSFUL"
            USERNAME[0]=un
            mainframe.tkraise()
            prepare_main()
            break
            
    else:
        #error handle for faulty login creds.
        loginerror["fg"]="red"
        loginerror["text"]="INVALID PASSWORD AND/OR PASSWORD"
        
#back function 
def back_login():
    lab_clear(loginerror)
    del_entry(username)
    del_entry(password)
    homeframe.tkraise()
def back_signup():
    lab_clear(signuperror)
    del_entry(signupname)
    del_entry(signupusername)
    del_entry(signuppassword)
    del_entry(signuppasswordconfirm)
    homeframe.tkraise()    
def back_mainpg():
    del_entry(mainconsole)
    del_entry(maineditor)
    back_login()
    
#clear function for clearing out entries on clicking back
def lab_clear(c):
    c["text"]=""
def del_entry(f):
    f.delete(0,END)
def back_signup():
    lab_clear(signuperror)
    del_entry(signupname)
    del_entry(signupusername)
    del_entry(signuppassword)
    del_entry(signuppasswordconfirm)
    homeframe.tkraise()   
def back_mainpg():
    mainconsole.delete(1.0,END)
    maineditor.delete(1.0,END)
    del_entry(seconds)
    homeframe.tkraise()
    
#seup main page
def prepare_main():
    mainconsole.insert(END,"WELCOME TO SPTT\nThe app uses google speech to text for converting speech to text.\nAnything written, will not be saved if you press back before saving.\nPlease specify the no. of seconds you would like to record for conversion in the entry provided below he console. \nUse RECORD button to record your voice which you want to covert to text.\n Use RECOGNIZE button to convert to text.\nThere maybe issues with recognition and this is not fullproof and may have some delays for execution.\n\n\n")
    #open user file(for retrieving previous save) if any
    try:
        wf=open("C:\\Users\\abhin\\OneDrive\\Desktop\\SPTT\\users\\"+USERNAME[0]+"\\"+USERNAME[0]+".txt","r")
    except:
        return
    #retrieve data for user
    maineditor.insert(END,wf.read())
    wf.close()
    
#save function for main
def save():
    data=maineditor.get(1.0,END)
    sf=open("C:\\Users\\abhin\\OneDrive\\Desktop\\SPTT\\users\\"+USERNAME[0]+"\\"+USERNAME[0]+".txt","w")
    sf.write(data)
    sf.close()
    mainconsole.insert(END,"Saved successfully\n")
    
#signup new user
def signup_check(n,un,pas,cpass):
    #error check 
    if un=="" or pas=="" or n=="" or cpass=="":
        signuperror["fg"]="red"
        signuperror["text"]="PLEASE PROVIDE YOUR CREDENTIALS"
        return
    #create new folder for user using username
    if not os.path.isdir("C:\\Users\\abhin\\OneDrive\\Desktop\\SPTT\\users\\"+un):
        os.mkdir("C:\\Users\\abhin\\OneDrive\\Desktop\\SPTT\\users\\"+un)
    #error handle
    if pas!=cpass:
        signuperror["fg"]="red"
        signuperror["text"]="THE PASSWORDS DO NOT MATCH"
        return 
    myDB=connect(host="localhost",user="root",password="a1289141144114", database="sptt1")
    cursor=myDB.cursor()
    cursor.execute("SELECT name,username,password FROM userdata;")
    data=cursor.fetchall()
    for i in range(len(data)):
        if data[i][0]==n or data[i][1]==un:
            #user exists
            signuperror["fg"]="red"
            signuperror["text"]="USERNAME AND/OR NAME ALREADY EXISTS"
            break
        
    else:
        #enter new user into database
        cursor.execute("INSERT INTO userdata (name,username,password) VALUES(%s,%s,%s);",(n,un,pas))
        myDB.commit()
        signuperror["fg"]="green"
        signuperror["text"]="SUCCESSFULLY SIGNED UP"
    
#recognition functions
def get_large_audio_transcription(path):
    """
    Splitting the large audio file into chunks
    and apply speech recognition on each of these chunks
    """   
    # create a speech recognition object
    r = sr.Recognizer()

    # open the audio file using pydub
    sound = AudioSegment.from_wav(path)  
    # split audio sound where silence is 700 miliseconds or more and get chunks
    chunks = split_on_silence(sound,
        # experiment with this value for your target audio file
        min_silence_len = 500,
        # adjust this per requirement
        silence_thresh = sound.dBFS-14,
        # keep the silence for 1 second, adjustable as well
        keep_silence=500,
    )
    folder_name = "C:\\Users\\abhin\\OneDrive\\Desktop\\SPTT\\users\\"+USERNAME[0]+"\\audio-chunks"
    # create a directory to store the audio chunks
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    whole_text = ""
    # process each chunk 
    for i, audio_chunk in enumerate(chunks, start=1):
        # export audio chunk and save it in
        # the `folder_name` directory.
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")
        # recognize the chunk
        with sr.AudioFile(chunk_filename) as source:
            audio_listened = r.record(source)
            # try converting it to text
            try:
                text = r.recognize_google(audio_listened)
            except sr.UnknownValueError as e:
                mainconsole.insert(END,"Error:", str(e))
            else:
                text = f"{text.capitalize()}. "
                mainconsole.insert(END,chunk_filename, ":", text)
                whole_text += text
    # return the text for all chunks detected
    return whole_text


def start_rec(s):
    # Setup channel info
    FORMAT = pyaudio.paInt16 # data type formate
    CHANNELS = 2 # Adjust to your number of channels
    RATE = 44100 # Sample Rate
    CHUNK = 9024 # Block Size
    RECORD_SECONDS = s # Record time as provided
    WAVE_OUTPUT_FILENAME = "C:\\Users\\abhin\\OneDrive\\Desktop\\SPTT\\users\\"+USERNAME[0]+"\\file.wav"

    # Startup pyaudio instance
    audio = pyaudio.PyAudio()
    # start Recording
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
    mainconsole.insert (END,"recording...\n")
    frames = []
    # Record for RECORD_SECONDS
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    mainconsole.insert (END,"finished recording\n")
    # Stop Recording
    stream.stop_stream()
    stream.close()
    audio.terminate()
    # Write your new .wav file with built in Python 3 Wave module
    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()
 

#creating window
window = Tk()

window.geometry("1152x700")
window.configure(bg = "#FFFFFF")


#creating homeframe and canvas
##creating homeframe
homeframe=Frame(window,
                bg="#FFFFFF",
                height=700,
                width=1152)
homeframe.place(x=0,y=0)
##creating homecanvas
homecanvas=Canvas(homeframe,
                  bg="#FFFFFF",
                  height=700,
                  width=1152,
                  bd=0,
                  highlightthickness=0,relief="ridge")
homecanvas.place(x=0,y=0)
homeback=PhotoImage(file="C:\\Users\\abhin\\OneDrive\\Desktop\\SPTT\\assets\\home.png")
home=homecanvas.create_image(576.0,
                             350.0,image=homeback)
homecanvas.homeback=homeback

#buttons for home
SIGNUP=Button(homeframe,
             command=lambda: signupframe.tkraise(),
             borderwidth=0,
             highlightthickness=5,
             bg="#0D1C32",
             fg="#FFFFFF",
             text="SIGNUP",
             font=Font(size=22),
             justify="center",
             activebackground="#9EBBC8",
             activeforeground="black")
SIGNUP.place(
    x=606.0,
    y=511.0,
    width=357.0,
    height=117.638427734375
)
SIGNUP.bind('<Enter>', on_enter)
SIGNUP.bind('<Leave>', on_leave)

LOGIN=Button(homeframe,
             command=lambda: [loginframe.tkraise(),lab_clear(loginerror),
    del_entry(username),
    del_entry(password)],
             borderwidth=0,
             highlightthickness=5,
             bg="#0D1C32",
             fg="#FFFFFF",
             text="LOGIN",
             font=Font(size=22),
             justify="center",
             activebackground="#9EBBC8",
             activeforeground="black")
LOGIN.place(
    x=189.0,
    y=511.0,
    width=357.0,
    height=117.638427734375
)
LOGIN.bind('<Enter>', on_enter)
LOGIN.bind('<Leave>', on_leave)

EXITHOME=Button(homeframe, 
                command=lambda: window.destroy(),
                borderwidth=0,
                highlightthickness=5,
                bg="#111C2A",
                text="EXIT",
                fg="#FFFFFF",
                font=Font(size=10),
                justify="center",
                activebackground="#FF9A22",
                activeforeground="black")
EXITHOME.place(
    x=0.0,
    y=643.0,
    width=80.0,
    height=57.0
)
EXITHOME.bind('<Enter>', on_enter_exit)
EXITHOME.bind('<Leave>', on_leave_exit)


#creating login frame and canvas
##creating loginframe
loginframe=Frame(window,
                bg="#FFFFFF",
                height=700,
                width=1152)
loginframe.place(x=0,y=0)
##creating logincanvas
logincanvas=Canvas(loginframe,
                  bg="#FFFFFF",
                  height=700,
                  width=1152,
                  bd=0,
                  highlightthickness=0,relief="ridge")
logincanvas.place(x=0,y=0)
loginback=PhotoImage(file="C:\\Users\\abhin\\OneDrive\\Desktop\\SPTT\\assets\\login.png")
login=logincanvas.create_image(576.0,
                             350.0,image=loginback)
logincanvas.loginback=loginback

#creating buttons for login
LOGINSUBMIT = Button(loginframe, 
                     command = lambda: login_check(username.get(),password.get()),
                     text="SUBMIT", 
                     font=Font(size=22),
                     bg="#1A1918",
                     fg="white",
                     justify="center",
                     activeforeground="black",
                     activebackground="#9EBBC8",
                     borderwidth=0,
                     highlightthickness=0,
                     relief="flat")
LOGINSUBMIT.place(
    x=475.0,
    y=456.0,
    width=179.0,
    height=71.0
)
LOGINSUBMIT.bind('<Enter>', on_enter)
LOGINSUBMIT.bind('<Leave>', on_leave)

loginerror=Label(logincanvas,
                 text="", 
                 fg="red", 
                 padx=10,
                 pady=10,
                 bg="white",
                 justify="center")
loginerror.place(
    x=407.0,
    y=225.0,
    width=359.0,
    height=37.0
    )

EXITLOGIN=Button(loginframe, 
                command=lambda: window.destroy(),
                borderwidth=0,
                highlightthickness=5,
                bg="#111C2A",
                text="EXIT",
                fg="#FFFFFF",
                font=Font(size=10),
                justify="center",
                activebackground="#FF9A22",
                activeforeground="black")
EXITLOGIN.place(
    x=0.0,
    y=643.0,
    width=80.0,
    height=57.0
)
EXITLOGIN.bind('<Enter>', on_enter_exit)
EXITLOGIN.bind('<Leave>', on_leave_exit)

BACKLOGIN=Button(loginframe, 
                command=lambda: back_login(),
                borderwidth=0,
                highlightthickness=5,
                bg="#889BB2",
                text="BACK",
                fg="#FFFFFF",
                font=Font(size=10),
                justify="center",
                activebackground="#FF9A22",
                activeforeground="black")
BACKLOGIN.place(
    x=0.0,
    y=0.0,
    width=80.0,
    height=57.0
)
BACKLOGIN.bind('<Enter>', on_enter_loginback)
BACKLOGIN.bind('<Leave>', on_leave_loginback)

#creating entries
username = Entry(loginframe,
    bd=0,
    bg="#9DF3F3",
    font=Font(size=16),
    highlightthickness=0
)
username.place(
    x=420.0,
    y=315.0,
    width=311.0,
    height=36.0
)

password = Entry(loginframe,
    bd=0,
    bg="#9DF3F3",
    highlightthickness=0,
)
password.place(
    x=420.0,
    y=393.0,
    width=311.0,
    height=36.0
)


#creating signupframe and canvas
##creating signup canvas
signupframe=Frame(window,
                bg="#FFFFFF",
                height=700,
                width=1152)
signupframe.place(x=0,y=0)
##creating signupcanvas
signupcanvas=Canvas(signupframe,
                  bg="#FFFFFF",
                  height=700,
                  width=1152,
                  bd=0,
                  highlightthickness=0,relief="ridge")
signupcanvas.place(x=0,y=0)
signupback=PhotoImage(file="C:\\Users\\abhin\\OneDrive\\Desktop\\SPTT\\assets\\signup.png")
signup=signupcanvas.create_image(576.0,
                             350.0,image=signupback)
signupcanvas.signupback=signupback

#buttons for signup frames
SIGNUPSUBMIT = Button(signupframe, 
                     command = lambda: signup_check(signupusername.get(),signupname.get(),signuppassword.get(),signuppasswordconfirm.get()),
                     text="SUBMIT", 
                     font=Font(size=22),
                     bg="#1A1918",
                     fg="white",
                     justify="center",
                     activeforeground="black",
                     activebackground="#9EBBC8",
                     borderwidth=0,
                     highlightthickness=0,
                     relief="flat")
SIGNUPSUBMIT.place(
    x=494.0,
    y=488.0,
    width=179.0,
    height=71.0
)
SIGNUPSUBMIT.bind('<Enter>', on_enter)
SIGNUPSUBMIT.bind('<Leave>', on_leave)

EXITSIGNUP=Button(signupframe, 
                command=lambda: window.destroy(),
                borderwidth=0,
                highlightthickness=5,
                bg="#111C2A",
                text="EXIT",
                fg="#FFFFFF",
                font=Font(size=10),
                justify="center",
                activebackground="#FF9A22",
                activeforeground="black")
EXITSIGNUP.place(
    x=0.0,
    y=643.0,
    width=80.0,
    height=57.0
)
EXITSIGNUP.bind('<Enter>', on_enter_exit)
EXITSIGNUP.bind('<Leave>', on_leave_exit)

BACKSIGNUP=Button(signupframe, 
                command=lambda: back_signup(),
                borderwidth=0,
                highlightthickness=5,
                bg="#385287",
                text="BACK",
                fg="#FFFFFF",
                font=Font(size=10),
                justify="center",
                activebackground="#FF9A22",
                activeforeground="black")
BACKSIGNUP.place(
    x=0.0,
    y=0.0,
    width=80.0,
    height=57.0
)
BACKSIGNUP.bind('<Enter>', on_enter_signupback)
BACKSIGNUP.bind('<Leave>', on_leave_signupback)

signuperror=Label(signupcanvas,
                 text="", 
                 fg="red", 
                 padx=10,
                 pady=10,
                 bg="white",
                 justify="center")
signuperror.place(
    x=411.0,
    y=195.0,
    width=359.0,
    height=37.0
    )

#creating entries for signup
signupusername = Entry(signupframe,
                   bd=0,
                   bg="#9EF3F3",
                   highlightthickness=0,
                   font=Font(size=16))
signupusername.place(x=435.0,
                 y=272.0,
                 width=311.0,
                 height=38.0)

signupname = Entry(signupframe,
                       bd=0,
                       bg="#9EF3F3",
                       highlightthickness=0,
                       font=Font(size=16))
signupname.place( x=435.0,
                     y=350.0,
                     width=311.0,
                     height=36.0)


signuppasswordconfirm = Entry(signupframe,
                              bd=0,
                              bg="#9EF3F3",
                              highlightthickness=0)
signuppasswordconfirm.place(x=597.0,
                            y=428.0,
                            width=141.0,
                            height=36.0)

signuppassword = Entry(signupframe,
                       bd=0,
                       bg="#9EF3F3",
                       highlightthickness=0)
signuppassword.place(x=427.0,
    y=428.0,
    width=142.0,
    height=36.0)

#creating mainframe and canvas
##creating main frame
mainframe=Frame(window,
                bg="#FFFFFF",
                height=700,
                width=1152)
mainframe.place(x=0,y=0)
##creating main canvas
maincanvas = Canvas(
    mainframe,
    bg = "#FFFFFF",
    height = 700,
    width = 1152,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

maincanvas.place(x = 0, y = 0)
mainback = PhotoImage(
    file="C:\\Users\\abhin\\OneDrive\\Desktop\\SPTT\\assets\\main.png")
main = maincanvas.create_image(
    576.0,
    350.0,
    image=mainback
)
maincanvas.mainback=mainback

#creating buttons for main
SAVEMAIN=Button(mainframe, 
                command=lambda: save(),
                borderwidth=0,
                highlightthickness=5,
                bg="#596065",
                text="SAVE",
                fg="#FFFFFF",
                font=Font(size=10),
                justify="center",
                activebackground="#FF9A22",
                activeforeground="black")
SAVEMAIN.place(
    x=1054.0,
    y=0.0,
    width=98.0,
    height=47.0
)
SAVEMAIN.bind('<Enter>', on_enter_exit)
SAVEMAIN.bind('<Leave>', on_exit_main)

BACKMAIN=Button(mainframe, 
                command=lambda: back_mainpg(),
                borderwidth=0,
                highlightthickness=5,
                bg="#596065",
                text="BACK",
                fg="#FFFFFF",
                font=Font(size=10),
                justify="center",
                activebackground="#FF9A22",
                activeforeground="black")
BACKMAIN.place(
    x=0.0,
    y=0.0,
    width=98.0,
    height=47.0
)
BACKMAIN.bind('<Enter>', on_enter_signupback)
BACKMAIN.bind('<Leave>', on_exit_main)

RECORD=Button(mainframe, 
                command=lambda: start_rec(int(seconds.get())),
                borderwidth=0,
                highlightthickness=5,
                bg="#596065",
                text="RECORD",
                fg="#FFFFFF",
                font=Font(size=10),
                justify="center",
                activebackground="#9EBBC8",
                activeforeground="black")
RECORD.place(
    x=119.0,
    y=0.0,
    width=189.0,
    height=47.0
)
RECORD.bind('<Enter>', on_enter)
RECORD.bind('<Leave>', on_exit_main)

RECOGNIZE=Button(mainframe, 
                command=lambda: maineditor.insert(END,get_large_audio_transcription("C:\\Users\\abhin\\OneDrive\\Desktop\\SPTT\\users\\"+USERNAME[0]+"\\file.wav")),
                borderwidth=0,
                highlightthickness=5,
                bg="#596065",
                text="RECOGNIZE",
                fg="#FFFFFF",
                font=Font(size=10),
                justify="center",
                activebackground="#9EBBC8",
                activeforeground="black")
RECOGNIZE.place(
    x=788.0,
    y=0.0,
    width=189.0,
    height=47.0
)
RECOGNIZE.bind('<Enter>', on_enter)
RECOGNIZE.bind('<Leave>', on_exit_main)

#creating entries
maineditor = Text(
    mainframe,
    bg="#D7E7EA",
    font=Font(size=12),
    bd=0,
    fg="black",
    highlightthickness=0
)
maineditor.place(
    x=417.0,
    y=67.0,
    width=695.0,
    height=581.0
)
mainconsole = Text(
    mainframe,
    bd=0,
    bg="#1B1C14",
    highlightthickness=0,
    fg="white"
)
mainconsole.place(
    x=39.0,
    y=112.0,
    width=349.0,
    height=496.0
)

seconds = Entry(
    mainframe,
    bd=0,
    bg="#1F2018",
    highlightthickness=0,
    fg="white",
    font=Font(size=12)
)
seconds.place(
    x=322.0,
    y=620.0,
    width=44.0,
    height=18.0
)

homeframe.tkraise()

window.resizable(False, False)
window.mainloop()
