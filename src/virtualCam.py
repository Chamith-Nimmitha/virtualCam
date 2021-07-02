
import os
import tkinter as tk
import tkinter.filedialog
import signal
import subprocess

pid = None

def get_virtual_cam(notify_str):
    os.system('sudo rmmod -f v4l2loopback')
    notify_str.set("############ PRIPARE ENVIRONMENT #############\n\n")
    notify_str.set(notify_str.get()+ "run command : sudo rmmod -f v4l2loopback\n")

    stream = os.popen("ls /dev/video*")
    output = stream.read()
    notify_str.set(notify_str.get()+ "run command : ls /dev/video*\n")
    old_cam_set = set(output.split("\n")[:-1])
    print(old_cam_set)

    os.system('sudo modprobe v4l2loopback')
    notify_str.set(notify_str.get()+ "run command : sudo modprobe v4l2loopback\n")

    stream = os.popen("ls /dev/video*")
    notify_str.set(notify_str.get()+ "run command : ls /dev/video*\n")
    output = stream.read()
    new_cam_set = set(output.split("\n")[:-1])
    print(new_cam_set)

    output_set = new_cam_set.difference(old_cam_set)
    for output in output_set:
        break
    notify_str.set(notify_str.get()+ f"Virtual cam : {output}\n")
    notify_str.set(notify_str.get()+ "############# PREPARATION FINISHED ###############\n\n")
    print(output)
    return output

def start_virtual_cam(video_location="", notify_str=None):
    global pid
    output = get_virtual_cam(notify_str)
    command = f"ffmpeg -stream_loop -1 -re -i {video_location} -map 0:v -f v4l2 {output}"
    notify_str.set(notify_str.get()+ f"run command : {command}")
    # os.popen(command)
    pid = subprocess.Popen(command,preexec_fn=os.setsid, shell=True).pid


root = tk.Tk(className="Virtual Camera")

def cancel_program():
    global pid
    if pid :
    # if event.char == 'q':
        os.killpg(os.getpgid(pid), signal.SIGTERM)
    root.quit()
        

# cancel task
# root.bind("<Key>",key_pressed)

canvas = tk.Canvas(root,width=500, height=400, bg="#99ccff")
canvas.pack()

# frame for user inputs
user_frame = tk.Frame(canvas,bg="#999")
user_frame.place(relx="0.05", rely="0.05", relwidth="0.9", relheight=0.3)


# loopback video location label
loopback_video_label = tk.Label(user_frame, bg="#eee" , text="Video Location", fg="black")
loopback_video_label.place(relx="0.025", rely="0.105", relwidth="0.25", relheight="0.2")

# show selected loopback video location
location_str = tk.StringVar()
location_str.set("")
loopback_video_location_label = tk.Label(user_frame,font=("Courier", 10), bg="#eee",wraplength="180", justify="left", fg="black", textvariable=location_str)
loopback_video_location_label.place(relx="0.3", rely="0.05", relwidth="0.425", relheight="0.4")

# popup file selector for select loopback video
def select_location():
    filename = tk.filedialog.askopenfilename(initialdir="~/Desktop", title="Select a video file", filetypes=(("mp4", "*.mp4"), ("mkv","*.mkv")))
    location_str.set(filename)

location_select_button = tk.Button(user_frame, text="Select a video", bg="#426367", fg="white", command=select_location)
location_select_button.place(relx="0.75", rely="0.105", relwidth="0.225", relheight="0.2")

# start button
submit_button = tk.Button(user_frame, text="Start", command=lambda:start_virtual_cam(location_str.get(), notify_str))
submit_button.place(relx="0.5",rely="0.6", relwidth="0.3", relheight="0.3")

# stop button
cancel_button = tk.Button(user_frame, text="Stop", command=lambda:cancel_program())
cancel_button.place(relx="0.1",rely="0.6", relwidth="0.3", relheight="0.3")

# frame for notifications
notify_frame = tk.Frame( canvas, bg="#693")
notify_frame.place(relx="0.05", rely="0.4", relwidth="0.9", relheight="0.55")

# notification label
notify_str = tk.StringVar()
notify_str.set("")
notify_label = tk.Label(notify_frame,wraplength="380", justify="left", bg="#aaa", font=("Courier", 8), textvariable=notify_str, fg="black")
notify_label.place(relx="0.05", rely="0.05", relwidth="0.9", relheight="0.9")


root.mainloop()