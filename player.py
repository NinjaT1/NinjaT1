import vlc
import keyboard
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog


def browse_media_file():
    global media_path
    file_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4 *.mkv *.avi")])
    if file_path:
        media_path = file_path
        update_media()


# noinspection PyGlobalUndefined
def update_media():
    global media
    media = instance.media_new(media_path)
    player.set_media(media)
    play_media()


def play_media():
    player.play()


# Create the main application window
root = tk.Tk()
root.title("Media Player")

# Define the paths
libvlc_path = r'E:\VLC\libvlc.dll'
media_path = ""  # Initialize with an empty string

# Create a VLC instance and media player
instance = vlc.Instance(f'--no-xlib --plugin-path={libvlc_path}')
player = instance.media_player_new()

# Initialize media with an empty path
update_media()

# Create a label to display time information
time_label = tk.Label(root, text="", font=("Helvetica", 16))
time_label.pack(pady=10)

# Create a progress bar to show time elapsed
progress_bar = ttk.Progressbar(root, length=300, mode='determinate')
progress_bar.pack(pady=10)


# Function to update the time display and progress bar
def update_time_display():
    current_time = player.get_time()
    total_duration = player.get_length()

    if current_time is not None and total_duration is not None and total_duration > 0:
        # Calculate the time elapsed as a percentage
        elapsed_percent = (current_time / total_duration) * 100

        current_time_str = f"Current Time: {current_time // 1000} seconds"
        total_duration_str = f"Total Duration: {total_duration // 1000} seconds"

        time_label.config(text=f"{current_time_str}\n{total_duration_str}")
        progress_bar['value'] = elapsed_percent

    root.after(1000, update_time_display)  # Update every second


# Start updating the time display and progress bar
update_time_display()


# Function to play or pause the media
def play_pause():
    if player.get_state() == vlc.State.Playing:
        player.pause()
    else:
        player.play()


# Register keyboard shortcuts
keyboard.add_hotkey('space', play_pause)


# Function to rewind by 10 seconds
def rewind():
    current_time = player.get_time()
    new_time = max(0, current_time - 10000)  # Rewind 10 seconds
    player.set_time(new_time)


# Register keyboard shortcut for rewind (LEFT ARROW)
keyboard.add_hotkey('left', rewind)


# Function to fast-forward by 10 seconds
def fast_forward():
    current_time = player.get_time()
    duration = player.get_length()
    new_time = min(duration, current_time + 10000)  # Fast-forward 10 seconds
    player.set_time(new_time)


# Register keyboard shortcut for fast-forward (RIGHT ARROW)
keyboard.add_hotkey('right', fast_forward)

# Define aspect ratios
aspect_ratios = ["default", "16:9", "4:3", "1:1"]
current_aspect_ratio = 0


# Function to change aspect ratio (Press 'a' key)
def change_aspect_ratio():
    global current_aspect_ratio
    current_aspect_ratio = (current_aspect_ratio + 1) % len(aspect_ratios)
    player.video_set_aspect_ratio(aspect_ratios[current_aspect_ratio])


# Register keyboard shortcut for changing aspect ratio (Press 'a' key)
keyboard.add_hotkey('a', change_aspect_ratio)

# Define playback speeds
playback_speeds = [0.5, 0.75, 1.0, 1.25, 1.5, 2.0]
current_speed_index = 2


# Function to change playback speed (Press 's' key)
def change_playback_speed():
    global current_speed_index
    current_speed_index = (current_speed_index + 1) % len(playback_speeds)
    speed = playback_speeds[current_speed_index]
    player.set_rate(speed)


# Register keyboard shortcut for changing playback speed (Press 's' key)
keyboard.add_hotkey('s', change_playback_speed)


def vol_up():
    current_volume = player.audio_get_volume()
    new_volume = min(100, current_volume + 10)  # Increase by 10 units
    player.audio_set_volume(new_volume)


keyboard.add_hotkey('up', vol_up)  # Volume up


def vol_down():
    current_volume = player.audio_get_volume()
    new_volume = max(0, current_volume - 10)  # Decrease by 10 units
    player.audio_set_volume(new_volume)


keyboard.add_hotkey('down', vol_down)  # Volume down

# Create a button to browse for the media file
browse_button = tk.Button(root, text="Browse Media File", command=browse_media_file)
browse_button.pack(pady=10)

# Close the Tkinter window when exiting
root.protocol("WM_DELETE_WINDOW", root.destroy)

# Run the Tkinter main loop
root.mainloop()
