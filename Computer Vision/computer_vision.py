import requests
import matplotlib.pyplot as plt
from PIL import Image
from tkinter import *
from PIL import Image, ImageTk
from tkinter import filedialog
import numpy as np
import cv2
from tkinter import messagebox

def getImage():
    filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
    return filename

def saveImage():
    try:
        img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        file = filedialog.asksaveasfilename(initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
        print(file)
        cv2.imwrite(file,img)
        messagebox.showinfo("Saved", "Image Saved")
    except:
        messagebox.showinfo("Message", "first browse an image using Browse Image button")
def proceessImage():
    subscription_key = "<Subscription Key>"
    assert subscription_key
    vision_base_url = "https://westcentralus.api.cognitive.microsoft.com/vision/v2.0/"
    analyze_url = vision_base_url + "analyze"
    image_path = getImage()
    image_data = open(image_path, "rb").read()
    headers    = {'Ocp-Apim-Subscription-Key': subscription_key,'Content-Type': 'application/octet-stream'}
    params     = {'visualFeatures': 'Categories,Description,Color'}
    response = requests.post(analyze_url, headers=headers, params=params, data=image_data)
    response.raise_for_status()
    analysis = response.json()
    #print(analysis)
    Nametext = str(analysis["categories"][0]["detail"]["celebrities"][0]["name"])
    #print("Name: "+Nametext)
    captionstext = str(analysis["description"]["captions"][0]["text"])
    #print("captionstext: "+captionstext)
    metadatatextw = str(analysis["metadata"]["width"])
    metadatatexth = str(analysis["metadata"]["height"])
    metadatatextf = str(analysis["metadata"]["format"])
    
    image_caption = analysis["description"]["captions"][0]["text"].capitalize()
    x = analysis["categories"][0]["detail"]["celebrities"][0]["faceRectangle"]["left"]
    y = analysis["categories"][0]["detail"]["celebrities"][0]["faceRectangle"]["top"]
    w = analysis["categories"][0]["detail"]["celebrities"][0]["faceRectangle"]["width"]
    h = analysis["categories"][0]["detail"]["celebrities"][0]["faceRectangle"]["height"]
    global image
    image = cv2.imread(image_path)
    cv2.rectangle(image, (x, y), (x+w, y+h), (230, 25, 127), 2)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(image)
    img = img.resize((500, 400), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)
    panel = Label(window, image = img)
    panel.image = img
    panel.place(x=10, y=10)

    Name = Label(window,text=Nametext,font='Helvetica 18 bold',fg="red")
    Name.place(x=600,y=20)
    
    Name = Label(window,text=captionstext,font='Helvetica 12 bold')
    Name.place(x=550,y=60)

    Name = Label(window,text="Width: "+metadatatextw,font='Helvetica 14 bold')
    Name.place(x=610,y=100)

    Name = Label(window,text="Height: "+metadatatexth,font='Helvetica 14 bold')
    Name.place(x=600,y=155)

    Name = Label(window,text="Format: "+metadatatextf,font='Helvetica 14 bold')
    Name.place(x=600,y=180)

       
if __name__ == '__main__':
    window = Tk()
    window.iconbitmap('face-detection.ico')
    window.title("Face Detection")
    
    btn1 = Button(window, text = "Browse Image",activebackground="#2896F6",command=proceessImage)
    btn1.pack()
    btn1.place(x=100,y=450)

    btn3 = Button(window, text = "Save Image",activebackground="#2896F6",command=saveImage)
    btn3.pack()
    btn3.place(x=300,y=450)

    window.geometry("900x500")
    window.resizable(False, False)
    window.mainloop()

