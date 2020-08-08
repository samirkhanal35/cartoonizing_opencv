import tkinter as tk
from tkinter import filedialog
import cv2
from PIL import Image, ImageTk

#from tkinter import *
window = tk.Tk()

window.title("Cartoonizing")
window.geometry('1200x800')

#header
header = tk.Label(window, text="GET YOUR IMAGE CARTOONIZED HERE!", bg="red", fg="black" ,font=("none bold",35), anchor="n") 
#anchor=n for top-central justification
header.place(x=300,y=1)
#header.pack()

#left frame
left_frame = tk.Frame(window, width=400, height=400, highlightbackground="black", highlightthickness=1)
left_frame.place(x=40,y=150)
left_frame.pack_propagate(0)

#left image label
# inp_image = tk.Label(left_frame, text="Input Image", font=("none Bold",10))
# inp_image.pack()


#left label
left_label = tk.Label(window, text="Input Image", font=("none Bold",20))
left_label.place(x=200,y=120)


#rigt_frame
rigt_frame = tk.Frame(window, width=400, height=400, highlightbackground="black", highlightthickness=1)
rigt_frame.place(x=760,y=150)
rigt_frame.pack_propagate(0)

#right image label
# out_image = tk.Label(rigt_frame, text="Output Image", font=("none Bold",10))
# out_image.pack()



#right label
right_label = tk.Label(window, text="Output Image", font=("none Bold",20))
right_label.place(x=930,y=120)



class variables:
    img = ""
    inp_img = ""
    out_img = ""

    #left image label
    inp_image = tk.Label(left_frame, text="Input Image", font=("none Bold",10))
    inp_image.pack()

    #right image label
    out_image = tk.Label(rigt_frame, text="Output Image", font=("none Bold",10))
    out_image.pack()

def working_design():
    #image selection button
    img_selection_btn = tk.Button(window, text="Select Image", fg="black", font=("none Bold",20) , command=open_file)
    img_selection_btn.place(x=520, y=100)
    #*--------------------------------
    # #sketching button
    img_sketching_btn = tk.Button(window, text="Cartoonize", fg="black", font=("none Bold",20) , command=Cartoonizing)
    img_sketching_btn.place(x=520, y=150)


def open_file(): 
    filename = filedialog.askopenfilename(filetypes=(("JPEG","*.jpg"),("PNG","*.png"),("All Files","*.*"))) 

    if filename!="" :
        variables.img = cv2.imread(filename)
        #resizing for image display
        variables.inp_img = resize_img(variables.img)
        #Rearranging the color channel
        b,g,r = cv2.split(variables.inp_img)
        img = cv2.merge((r,g,b))

        #convert image object into TkPhoto object
        im = Image.fromarray(img)
        img1 = ImageTk.PhotoImage(image=im)

        variables.inp_image.pack_forget()
        left_frame.update()

        variables.inp_image = tk.Label(left_frame, image=img1)
        variables.inp_image.image = img1
        variables.inp_image.pack()
        left_frame.update()

        
        
 

def resize_img(img):
    
    img1 = cv2.resize(img,(400,400)) #(a high-quality downsampling filter)       
    return img1

def Cartoonizing():
    img_rgb = variables.img
    print("inp img:",img_rgb.shape)
    numDownSamples = 2 # number of downscaling steps
    numBilateralFilters = 5  # number of bilateral filtering steps

    # -- STEP 1 --
    # downsample image using Gaussian pyramid
    img_color = img_rgb
    for _ in range(numDownSamples):
        img_color = cv2.pyrDown(img_color)

    # repeatedly apply small bilateral filter instead of applying
    # one large filter
    print("pyrdown img:",img_color.shape)
    for _ in range(numBilateralFilters):
        img_color = cv2.bilateralFilter(img_color, 10, 15, 15)

    # upsample image to original size
    print("bilateralfilter img:",img_color.shape)
    for _ in range(numDownSamples):
        img_color = cv2.pyrUp(img_color)

    # -- STEPS 2 and 3 --
    # convert to grayscale and apply median blur
    print("pyrup img:",img_color.shape)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)

    print("cvtcolor img:",img_gray.shape)
    img_blur = cv2.medianBlur(img_gray, 5)

    print("medianblur img:",img_blur.shape)

    # -- STEP 4 --
    # detect and enhance edges
    img_edge = cv2.adaptiveThreshold(img_blur, 255,
        cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 2)

    # -- STEP 5 --
    # convert back to color so that it can be bit-ANDed
    # with color image
    print("adaptivethresholding img:",img_blur.shape)
    img_edge = cv2.cvtColor(img_edge, cv2.COLOR_GRAY2RGB)
    print("cvtcolor img:",img_blur.shape)
    img = cv2.bitwise_and(img_color, img_edge)

    #resizing for image display
    variables.out_img = resize_img(img)
    #Rearranging the color channel
    b,g,r = cv2.split(variables.out_img)
    img = cv2.merge((r,g,b))
    #convert image object into TkPhoto object
    im = Image.fromarray(img)
    img1 = ImageTk.PhotoImage(image=im)
    
    variables.out_image.pack_forget()
    rigt_frame.update()

    variables.out_image = tk.Label(rigt_frame, image=img1)
    variables.out_image.image = img1
    variables.out_image.pack()
    rigt_frame.update()


working_design()

window.mainloop()
