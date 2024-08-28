import cv2
import os
#import pyperclip
import numpy as np
from random import randint
#import time
#from time import sleep
from cv2 import *
import tkinter as tk
from tkinter import *
from tkinter.ttk import Combobox
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image, ImageTk

class VideoCapture:
    def __init__(self):
        self.vid = cv2.VideoCapture(0)
        if not self.vid.isOpened():
            #raise ValueError("Unable to open video source")
            messagebox.showerror("Error", "Unable to open video source")

        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
        
        self.filter1 = cv2.COLOR_BGR2BGR555
        self.filter2 = cv2.COLOR_BGR2RGB
        self.filter3 = cv2.COLOR_BGR2BGR565
        self.filter4 = cv2.COLOR_BGR2GRAY
        self.filter5 = cv2.COLOR_BGR2LAB
        self.filter6 = cv2.COLOR_BGR2HLS
        self.filter7 = cv2.COLOR_BGR2LUV
        self.filter8 = cv2.COLOR_BGRA2RGB
        self.filter9 = cv2.COLOR_BGRA2RGBA
        self.filter10 = cv2.COLOR_BGR2XYZ
        self.filter11 = cv2.COLOR_BGR2YUV
        
        self.current_filter = self.filter2
        
        self.Height = 500
        self.Width = 600
        
        self.DescriptionText = "Camera vision"
        self.xTXT = 40
        self.yTXT = 40

        self.filtered_capture = self.current_filter

        self.root = tk.Tk()
        self.root.title("Camera Vision")
        self.root.geometry("1000x700")
        self.btnExit = Button(self.root, width=10, bg="red", text="exit", command=self.destroy_window)
        self.btnExit.pack(anchor="ne")
        self.filterDescription = Label(self.root, text="Filter: BGR2RGB")
        self.filterDescription.pack()
        self.label = Label(self.root, height=self.Height, width=self.Width)
        self.label.pack(anchor="n")
        self.file_pathTV = Label(self.root, text="Description: Image, video not captured. File path = None")
        self.file_pathTV.pack()
        self.capturebtnsFrame = tk.Frame(self.root)
        self.capturebtnsFrame.pack(pady=20)
        self.btnCapturePhoto = Button(self.capturebtnsFrame, width=50, height=8, text="capture photo", bg="yellow", command=self.capture_image)
        self.btnCapturePhoto.pack(side=tk.LEFT)
        self.btnCaptureVideo = Button(self.capturebtnsFrame, text="capture video", bg="green", width=50, height=8, command=self.capture_video)
        self.btnCaptureVideo.pack(side=tk.LEFT)
        self.menuBar = Menu(self.root)
        self.camfilters = Menu(self.root, tearoff=0)
        self.menuBar.add_cascade(label="Camera color filters", menu=self.camfilters)
        self.camfilters.add_command(label="BGR2RGB", command=self.set_filter2)
        self.camfilters.add_command(label="BGRBGR555", command=self.set_filter1)
        self.camfilters.add_command(label="BGR2BGR565", command=self.set_filter3)
        self.camfilters.add_command(label="BGR2GRAY", command=self.set_filter4)
        self.camfilters.add_command(label="BGR2LAB", command=self.set_filter5)
        self.camfilters.add_command(label="BGR2HLS", command=self.set_filter6)
        self.camfilters.add_command(label="BGR2LUV", command=self.set_filter7)
        self.camfilters.add_command(label="BGRA2RGB", command=self.set_filter8)
        self.camfilters.add_command(label="BGRA2RGBA", command=self.set_filter9)
        self.camfilters.add_command(label="BGR2XYZ", command=self.set_filter10)
        self.camfilters.add_command(label="BGR2YUV", command=self.set_filter11)
        
        self.editFunctions = Menu(self.root, tearoff=0)
        self.menuBar.add_cascade(label="Edit", menu=self.editFunctions)
        self.editFunctions.add_command(label="delete watermark", command=self.delete_description_on_frame)
        self.editFunctions.add_command(label="delete all objects")
        self.editFunctions.add_command(label="delete text")
        self.editFunctions.add_command(label="delete geometry objects")
        self.editFunctions.add_command(label="reset filters", command=self.set_filter2)
        self.editFunctions.add_command(label="resize cam screen", command=self.resize)
        self.editFunctions.add_command(label="edit watermark", command=self.draw_text)

        self.actionsFunctions = Menu(self.root, tearoff=0)
        self.menuBar.add_cascade(label="Actions", menu=self.actionsFunctions)
        self.actionsFunctions.add_command(label="Capture photo", command=self.capture_image)
        self.actionsFunctions.add_command(label="Capture video", command=self.capture_video)
        
        self.menuBar.add_radiobutton(label="See result", command=self.show_result)
        
        self.root.config(menu=self.menuBar)
        
    def destroy_window(self):
        self.root.destroy()
        
    def get_filters(self):
        self.filters.get()

    def show_result(self):
        try:
            self.resultroot = tk.Toplevel()
            self.resultroot.title("See result (captured content)")
            self.resultroot.geometry("500x600")
            self.image = Image.open(self.image_path)
            self.photo = ImageTk.PhotoImage(self.image)
            self.resulTV = tk.Label(self.resultroot, bg="white", image=self.photo)
            self.resulTV.pack()
            self.btnCopy = Button(self.resultroot, text="Copy", bg="orange", width=10, height=3, command=self.copy_image_to_clipboard)
            self.btnCopy.pack()
            self.resultroot.mainloop()
        except:
            self.resultroot.destroy()
            messagebox.showerror("Error", "Nothing to show!")

    def copy_image_to_clipboard(self):
        try:
            self.img = Image.open(self.image_path)
            self.img.save("copied_image.png")
            os.system("clip < copied_image.png")
            messagebox.showinfo("Info", "Image was copied!")
        except:
            messagebox.showerror("Error", "Operation failed!")

        
    def capture_image(self):
        self.result, self.image = self.vid.read()
        try:
            if self.result:
                #self.filtered_capture = cv2.cvtColor(self.image, self.current_filter)
                self.file_path = filedialog.asksaveasfile(defaultextension=".png", filetypes=[("PNG files", "*.png")])
                print(self.file_path.name)
                self.image_path = self.file_path.name
                self.file_pathTV.configure(text=f"Description: Image was captured. File path = {self.file_path.name}")
                cv2.imwrite(self.file_path.name, self.filtered_capture)
                messagebox.showinfo("Info", f"Image was saved!\nfile path = {self.file_path.name}")
            else:
                messagebox.showerror("Error", "Image not detected! Please try again.")
                self.file_pathTV.configure(text="Description: Capture error, please, try again!")
        except:
            messagebox.showerror("Error", "Operation failed! Please, try again.")
            self.file_pathTV.configure(text="Description: Capture error, please, try again!")
            
    def capture_video(self):
        try:
            self.cap = cv2.VideoCapture(0)
            self.frame_width = int(self.cap.get(3))
            messagebox.showwarning("Warning", "Video recording started! If you want to close recording, please push Q button on your keyboard.")
            self.frame_height = int(self.cap.get(4))
            #self.timerText = ""
            self.out = cv2.VideoWriter(f'outputCameraVision{randint(0, 100)}.mp4', cv2.VideoWriter_fourcc('H','2','6','4'), 30, (self.frame_width, self.frame_height))

            while(self.cap.isOpened()):
                ret, img = self.cap.read()
                if not ret:
                        break
        
                self.out.write(img)

                cv2.putText(img, self.DescriptionText, (self.xTXT, self.yTXT), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                #cv2.putText(img, self.timerText, (90, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.imshow("Video Recording", img)

        
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    messagebox.showinfo("Info", "Video recording ended")
                    break

                #while True:
                    #self.start_time = time.time()
                    #self.elapsed_time = time.time() - self.start_time
                    #self.timerText = f"Time: {int(self.elapsed_time)} sec"
                    #time.sleep(1)

        
            self.cap.release()
            self.out.release()
            cv2.destroyAllWindows()
        except:
            messagebox.showerror("Error", "Video recording failed! Try again.")

        
    def draw_description_on_frame(self, image):
        self.filtered_capture = cv2.putText(image, self.DescriptionText, (self.xTXT, self.yTXT), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        return self.filtered_capture
    
    def delete_description_on_frame(self):
        self.DescriptionText = ""

    def edit_description_on_frame(self):
        self.DescriptionText = self.txt.get()       

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                self.result_filter = cv2.cvtColor(frame, self.current_filter)
                return self.result_filter
            
    def set_filter1(self):
        self.current_filter = self.filter1
        self.filterDescription.configure(text="Filter: BGR2BGR555")

        
    def set_filter2(self):
        self.current_filter = self.filter2
        self.filterDescription.configure(text="Filter: BGR2RGB")
        
    def set_filter3(self):
        self.current_filter = self.filter3
        self.filterDescription.configure(text="Filter: BGR2BGR565")
    
    def set_filter4(self):
        self.current_filter = self.filter4
        self.filterDescription.configure(text="Filter: BGR2GRAY")
        
    def set_filter5(self):
        self.current_filter = self.filter5
        self.filterDescription.configure(text="Filter: BGR2LAB")
        
    def set_filter6(self):
        self.current_filter = self.filter6
        self.filterDescription.configure(text="Filter: BGR2HLS")
        
    def set_filter7(self):
        self.current_filter = self.filter7
        self.filterDescription.configure(text="Filter: BGR2LUV")
        
    def set_filter8(self):
        self.current_filter = self.filter8
        self.filterDescription.configure(text="Filter: BGRA2RGB")
        
    def set_filter9(self):
        self.current_filter = self.filter9
        self.filterDescription.configure(text="Filter: BGRA2RGBA")
        
    def set_filter10(self):
        self.current_filter = self.filter10
        self.filterDescription.configure(text="Filter: BGR2XYZ")
        
    def set_filter11(self):
        self.current_filter = self.filter11
        self.filterDescription.configure(text="Filter: BGR2YUV")
        
    def draw_text(self):
        self.txtroot = tk.Toplevel()
        self.txtroot.title("Edit watermark")
        self.txtroot.geometry("300x300")
        self.txtroot.resizable(0, 0)
        
        self.txtDescription = Label(self.txtroot, text="Enter text:")
        self.txtDescription.pack()
        self.txt = Entry(self.txtroot, width=25)
        self.txt.pack(pady=10)
        self.applyButton = Button(self.txtroot, text="Apply", bg="green", width=20, height=3, command=self.edit_description_on_frame)
        self.applyButton.pack()
        self.txtroot.mainloop()

        
    def resize(self):
        self.setsize = tk.Toplevel()
        self.setsize.title("Camera screen size")
        self.setsize.geometry("300x300")
        self.setsize.resizable(0, 0)
        
        self.hd = Label(self.setsize, text="Enter height:")
        self.hd.pack(pady=10)
        self.he = Entry(self.setsize, width=20)
        self.he.pack(pady=10)
        self.wd = Label(self.setsize, text="Enter width:")
        self.wd.pack(pady=10)
        self.we = Entry(self.setsize, width=20)
        self.we.pack(pady=10)
        self.btnApply = Button(self.setsize, text="Apply", bg="green", width=20, height=3, command=self.set_size)
        self.btnApply.pack(pady=10)
            
        self.setsize.mainloop()
        
    def set_size(self):
        try:
            self.height_data = self.he.get()
            self.width_data = self.we.get()
            self.Height = self.height_data
            self.Width = self.width_data
            self.label.configure(width=self.Width, height=self.Height)
        except:
            messagebox.showerror("Error", "Please, chek your values and try again")

    def show_frame(self):
        frame = self.get_frame()
        if frame is not None:
            self.draw_description_on_frame(frame)
            image = Image.fromarray(frame)
            photo = ImageTk.PhotoImage(image=image)
            self.label.imgtk = photo
            self.label.configure(image=photo)
            self.label.after(10, self.show_frame)

    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()
            
    def start(self):
        self.show_frame()
        self.root.mainloop()

if __name__ == "__main__":
    app = VideoCapture()
    app.start()
