import tkinter as tk
from PIL import Image
from tkinter import ttk

"""
LoL application ?
- use of the API
- show statistics
"""


def run_gif(r, filename: str):
    info = Image.open(filename)
    frames = info.n_frames  # number of frames

    photoimage_objects = []
    for i in range(frames):
        obj = tk.PhotoImage(file=filename, format=f"gif -index {i}")
        photoimage_objects.append(obj)


    def animation(current_frame=0):
        global loop
        image = photoimage_objects[current_frame]

        gif_label.configure(image=image)
        current_frame = current_frame + 1

        if current_frame == frames:
            current_frame = 0

        loop = r.after(50, lambda: animation(current_frame))


    def stop_animation():
        r.after_cancel(loop)


    gif_label = tk.Label(r, image="")
    gif_label.pack()

    start = tk.Button(r, text="Start", command=lambda: animation(current_frame=0))
    start.pack()

    stop = tk.Button(r, text="Stop", command=stop_animation)
    stop.pack()

def browse_file():
    ...

def main():
    r = tk.Tk()
    r.title("Hello World")
    r.minsize(200, 200)
    r.maxsize(800, 800)
    r.geometry("800x600")

    file = "pikachu.gif"
    run_gif(r, file)

    #browse_button = tk.Button(r, text="Browse File", command=browse_file)
    #browse_button.pack(pady=5)

    menu = tk.Menu(r)

    r.mainloop()

if __name__ == '__main__':
    main()