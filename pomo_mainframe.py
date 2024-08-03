from tkinter import *
from tkinter import ttk
import PIL.Image, PIL.ImageTk
from win10toast import ToastNotifier
from threading import Thread
#BUG: Stop button during break is useless. 
#TODO:  Make timer input, take input for time and make rest ceil(inp//5). Make progress bar circle. Display countdown in timer. 
# Initializing some values
root = Tk()
pomo_count = IntVar()
counter = 0
remaining_time = 1
break_time = 1
countdown_display = StringVar()
timer_condition = BooleanVar()
total_time_focused = StringVar()
time_focused = 0
focus_goal = 30
on_break = BooleanVar(value=False)
n = ToastNotifier()
# Function to display the total time spent focusing
def time_spent_focusing(*args): 
    hrs_focused = time_focused // 3600
    mins_focused = (time_focused % 3600) // 60
    secs_focused = time_focused % 60
    time_display_focused = f"{hrs_focused:02}:{mins_focused:02}:{secs_focused:02}"
    total_time_focused.set(f'{time_display_focused}')
    progress['value'] = time_focused/focus_goal * 100
# Function to update the countdown timer
def show_notification(message):
    n.show_toast(message, duration=5)
def update_countdown():
    global remaining_time, time_focused, counter
    if timer_condition.get():
        # Disabling the buttons depending on if timer is running or not
        start_button.config(state=DISABLED)
        stop_button.config(state=ACTIVE)
        if remaining_time > 0:
            time_focused += 1
            remaining_time -= 1
            display_time(remaining_time)
            root.after(1000, update_countdown)
        else:
            Thread(target=show_notification, args=("Well done.",)).start()
            countdown_display.set("Take a break.")
            counter += 1
            pomo_count.set(counter)
            stop_button.config(state=DISABLED)
            start_button.grid_remove()
            break_button.grid()
            break_button.config(state=ACTIVE)
            time_spent_focusing()
    else:
        display_time(remaining_time)
        start_button.config(state=ACTIVE)

# Function to initialize the countdown
def init_countdown():
    global remaining_time
    remaining_time = 1
    timer_condition.set(True)
    update_countdown()

# Function to display the time currently left
def display_time(time_left):
    hrs = time_left // 3600
    mins = (time_left % 3600) // 60
    secs = time_left % 60
    time_display = f"{hrs:02}:{mins:02}:{secs:02}"
    countdown_display.set(f'{time_display}')

# Function to stop the countdown
def stop_countdown():
    global remaining_time
    if timer_condition.get():
        timer_condition.set(False)
    else:
        remaining_time = 0
        display_time(remaining_time)
        timer_condition.set(False)
        time_spent_focusing()
        stop_button.config(state=DISABLED)

# Function to start the break countdown
def start_break(*args):
    global break_time, counter
    stop_button.config(state=ACTIVE)
    if break_time > 0:
        break_time -= 1
        display_time(break_time)
        break_button.config(state=DISABLED)
        root.after(1000, start_break)
    else:
        Thread(target=show_notification, args=("Break's over",)).start()
        countdown_display.set("Time to focus.")
        break_time = 1 
        if (counter+1)%4 == 0:
            break_time *= 5
        break_button.grid_remove()
        start_button.grid()
        stop_button.config(state=DISABLED)
        start_button.config(state=ACTIVE)

# Initializing frame of the app
root.title("Pomodoro App")
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

break_button = ttk.Button(mainframe, text="Start Break", command=start_break)
break_button.grid(column=3, row=5, sticky=(W, E))
break_button.grid_remove()

start_button = ttk.Button(mainframe, text="Start Timer", command=init_countdown)
start_button.grid(column=3, row=5, sticky=(W, E))

stop_button = ttk.Button(mainframe, text="Stop", command=stop_countdown)
stop_button.grid(column=1, row=5, sticky=(W, E))
stop_button.config(state=DISABLED)


img = PIL.Image.open("C:/Users/Vaibhav/Desktop/python/pomo_project/Pomodoro/logo.png")
img = img.reduce(50)
image_insert = PIL.ImageTk.PhotoImage(img)
image_label = Label(mainframe, image=image_insert)
image_label.grid(row=2, column=3, sticky=NE)

ttk.Label(mainframe, text="Pomos today:").grid(column=1, row=2, sticky=W)
ttk.Label(mainframe, textvariable=pomo_count).grid(column=2, row=2, sticky=W)

ttk.Label(mainframe, text="Time spent focusing:").grid(column=1, row=4, sticky=W)
ttk.Label(mainframe, textvariable=total_time_focused).grid(column=2, row=4, sticky=W)

ttk.Label(mainframe, text="Time left:").grid(column=1, row=3, sticky=W)
ttk.Label(mainframe, textvariable=countdown_display, width=12).grid(column=2, row=3, sticky=W)

progress = ttk.Progressbar(mainframe, orient=HORIZONTAL, length=200, mode='determinate')
progress.grid(column=1, row=6, columnspan=3, sticky=(W,E))
progress['maximum'] = 100
progress['value'] = 0
for child in mainframe.winfo_children():
    child.grid_configure(padx=20, pady=5)
root.bind("<Return>", init_countdown)
root.mainloop()
