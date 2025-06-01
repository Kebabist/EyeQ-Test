import tkinter as tk
import os
from PIL import ImageTk, Image
Image.CUBIC = Image.BICUBIC
from tkinter import ttk, StringVar
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from random import randint
#import ir
#import RPi.GPIO as GPIO
import threading

ir_pin=11
    
class App(ttk.Window):
    # mainsetup
    def __init__(self):
        super().__init__(themename='cyborg')
        #self.myclass = ir.ir_reciever()
        self.title('EyeQtest')
        self.button = ttk.Button(self, text='Menu', command=self.open_menu)
        self.button.pack()
        
        # Make the window fullscreen and borderless
       # self.attributes('-fullscreen', True)
        # self.attributes('-topmost', True)
       
        # widgets
        ImageImporter(self)
  
        #Initialize IR code
        self.ir_code = None

        #Start a new thread that will listen for IR signals
        self.ir_thread = threading.Thread(target=self.listen_for_ir)
        self.ir_thread.start()

        #run
        self.mainloop()
        
    def open_menu(self):
        self.menu = Menu(self)
        
    def on_key_press(self):
        if self.ir_code == '0x':
             self.open_menu()
        elif self.ir_code == '0xB':
            Menu.move_focus_next()
        elif self.ir_code == '0xC':
            Menu.move_focus_previous()
        elif self.ir_code == '0x1':
            Menu.increase_spinbox()
        elif self.ir_code == '0x2':
            Menu.decrease_spinbox()
        # Add more elif statements here for other IR codes
        else:
            print(f"Unknown IR code: {self.ir_code}")
            
    def listen_for_ir(self):
          print("Starting IR Listener")
          try:
                while True:
                    print("Waiting for signal")
                    GPIO.wait_for_edge(ir_pin, GPIO.FALLING)
                    code = self.myclass.on_ir_receive(ir_pin)
                    if code:
                        self.ir_code = str(hex(code))
                        print(self.ir_code)
                        self.on_key_press() 
                    else:
                        print("Invalid code")
          except Exception as e:
            print(f"An error occurred: {e}")
          finally:
            print("Cleaning up")
            GPIO.cleanup()
                    
class Menu:
    def __init__(self, master):

        self.master = master
        self.window = ttk.Toplevel(self.master)
        self.window.resizable(True,True)
        
        self.window.title('Menu')
        self.window.attributes('-fullscreen', True)
        self.window.attributes('-topmost', True)
        
        # Outer frame
        self.outer_frame = ttk.Frame(self.window,padding=75)
        self.outer_frame.pack(expand=True, fill='both')       

        # inner frame
        style = ttk.Style()
        style.configure('warning.TLabelframe.Label', font=('Helvetica', 25, 'bold'))

        self.inner_frame = ttk.Labelframe(self.outer_frame ,text='Settings', padding=10, relief='raised',
                                    style='warning.TLabelframe' , width= 700 , height=800)
        self.inner_frame.pack(side='top',anchor='center')      
        
        self.about_frame = ttk.Frame(self.outer_frame, width=600, height=100) 
        self.about_frame.pack(side='top', anchor='e', padx=600, pady=15) 
        
        self.nameframe = ttk.Frame(self.inner_frame)
        self.nameframe.pack(side='left',fill='y', pady=10, anchor='w')
        
        self.seperator = ttk.Separator(self.inner_frame, orient='vertical')
        self.seperator.pack(side='left', fill='y', padx=10)
        
        # About label
        about_label = ttk.Label(self.about_frame, text=' EyeQtest™ v0.1 \n ARMLab® inc. \n Copyright© 2024-2034',
                          font=("Helvetica", 12, "bold"), style='info', justify='left')
        about_label.pack(side='top',anchor='e' )
        
  
      # frames      
        
        self.brightness_frame = ttk.Frame(self.inner_frame)
        self.brightness_frame.pack(side='top',pady=10 , anchor='w')   
        
        self.contrast_frame = ttk.Frame(self.inner_frame)
        self.contrast_frame.pack(side='top',padx=20,pady=10 , anchor='w')   
        
        self.chartsize_frame = ttk.Frame(self.inner_frame)
        self.chartsize_frame.pack(side='top',padx=20,pady=10 , anchor='w')   
        
        self.distance_frame = ttk.Frame(self.inner_frame)
        self.distance_frame.pack(side='top',padx=20,pady=10 , anchor='w')   
        
        self.neardistance_frame = ttk.Frame(self.inner_frame)
        self.neardistance_frame.pack(side='top',padx=20,pady=10 , anchor='w') 
        
        self.time_frame = ttk.Frame(self.inner_frame)
        self.time_frame.pack(side='top',padx=20,pady=10 , anchor='w')  
        
        self.screensave_time_frame = ttk.Frame(self.inner_frame)
        self.screensave_time_frame.pack(side='top',padx=20,pady=10 , anchor='w')
                
        self.number_mode_frame = ttk.Frame(self.inner_frame)
        self.number_mode_frame.pack(side='top',padx=20,pady=10 , anchor='w') 
  
        self.language_frame = ttk.Frame(self.inner_frame)
        self.language_frame.pack(side='top',padx=20,pady=10 , anchor='w')
  
        self.profile_frame = ttk.Frame(self.inner_frame)
        self.profile_frame.pack(side='top',padx=20,pady=10 , anchor='w') 
        
        
        
        self.btn1_frame = ttk.Frame(self.inner_frame)
        self.btn1_frame.pack(side='right', padx=20, pady=10)
        
        self.btn2_frame = ttk.Frame(self.inner_frame)
        self.btn2_frame.pack(side='right', padx=20, pady=10)
        
        self.btn3_frame = ttk.Frame(self.inner_frame)
        self.btn3_frame.pack(side='right', padx=20, pady=10)

        
        
        
        
        # Custom style 
        style = ttk.Style()
        style.configure('TSpinbox', arrowcolor= 'red')
        
        style1 = ttk.Style()
        style1.configure('cosmo.TSpinbox', arrowcolor= 'gray')
        
        #  Brightness spinbox
        brightness_label = ttk.Label(self.nameframe, text='Brightnes', anchor='center', font=("Helvetica", 16, "bold"))
        brightness_label.pack(side='top', anchor='center', pady=65)

        self.brightness_spin_var = tk.StringVar() 
        self.brightness_spin_var.trace_add('write', lambda name, index, mode: self.update_meter('brightness', self.brightness_meter))
        self.brightness_spinbox = ttk.Spinbox(self.brightness_frame, from_=0, to=100,
                                              increment=1, style='darkly', textvariable=self.brightness_spin_var, width=3) 
        self.brightness_spinbox.pack(side='left', padx= 15)

        self.brightness_spinbox.bind('<FocusIn>', lambda e: self.brightness_spinbox.configure(style='TSpinbox'))
        self.brightness_spinbox.bind('<FocusOut>', lambda e: self.brightness_spinbox.configure(style='cosmo.TSpinbox'))

        #value = int(self.brightness_spin_var.get())
        self.brightness_meter = ttk.Meter(self.brightness_frame, metersize=150, padding=5, metertype="semi",#amountused=value,
                                 textright="%", subtextstyle="light", subtext=" ")
        self.brightness_meter.pack(side='left', padx=15)
        
       # self.brightness_spin_var.trace_add('write', lambda name, index, mode: self.update_meter('brightness', self.brightness_meter))


         
        # contrast spinbox        
        contrast_label = ttk.Label(self.nameframe, text='Contrast', anchor='center', font=("Helvetica", 16, "bold"))
        contrast_label.pack(side='top',pady=25, anchor='center')

        self.contrast_spinbox = ttk.Spinbox(self.contrast_frame, from_=-100, to=100, 
                                            increment=1,style='darkly', width=10)
        self.contrast_spinbox.pack(side='left')
        
        unit_label1 = ttk.Label(self.contrast_frame, text='')
        unit_label1.pack(side='left',padx=2)
        
        self.contrast_spinbox.bind('<FocusIn>', lambda e: self.contrast_spinbox.configure(style='TSpinbox'))
        self.contrast_spinbox.bind('<FocusOut>', lambda e: self.contrast_spinbox.configure(style='cosmo.TSpinbox'))
        
        
        # chart size spinbox
        chartsize_label = ttk.Label(self.nameframe, text='Chart Size', anchor='center', font=("Helvetica", 16, "bold"))
        chartsize_label.pack(side='top',pady=5, anchor='center')

        self.chartsize_spinbox = ttk.Spinbox(self.chartsize_frame, from_=0, to=100, 
                                            increment=1,style='darkly', width=10)
        self.chartsize_spinbox.pack(side='left', pady=10)
        
        unit_label2 = ttk.Label(self.chartsize_frame, text='%', font=("Helvetica", 10, "bold"))
        unit_label2.pack(side='left',padx=2)
        
        self.chartsize_spinbox.bind('<FocusIn>', lambda e: self.chartsize_spinbox.configure(style='TSpinbox'))
        self.chartsize_spinbox.bind('<FocusOut>', lambda e: self.chartsize_spinbox.configure(style='cosmo.TSpinbox'))
  
          # Distance spinbox        
        distance_label = ttk.Label(self.nameframe, text='Distance', anchor='center', font=("Helvetica", 16, "bold"))
        distance_label.pack(side='top',pady=25, anchor='center')

        self.distance_spinbox = ttk.Spinbox(self.distance_frame, from_=1, to=5, increment=0.2,style='darkly',width=10)
        self.distance_spinbox.pack(side='left')
        
        unit_label3 = ttk.Label(self.distance_frame, text='M', font=("Helvetica", 10, "bold"))
        unit_label3.pack(side='left',padx=2)
        
        self.distance_spinbox.bind('<FocusIn>', lambda e: self.distance_spinbox.configure(style='TSpinbox'))
        self.distance_spinbox.bind('<FocusOut>', lambda e: self.distance_spinbox.configure(style='cosmo.TSpinbox'))
        
        # Near Distance Mode spinbox        
        neardistance_label = ttk.Label(self.nameframe, text='NearDistance Mode', anchor='center', font=("Helvetica", 16, "bold"))
        neardistance_label.pack(side='top',pady=5, anchor='center')
        
        self.neardistance_spinbox = ttk.Spinbox(self.neardistance_frame, from_=0, to=1, increment=0.2,style='darkly',width=10)
        self.neardistance_spinbox.pack(side='left', pady=10)	
        
        self.neardistance_spinbox.bind('<FocusIn>', lambda e: self.neardistance_spinbox.configure(style='TSpinbox'))
        self.neardistance_spinbox.bind('<FocusOut>', lambda e: self.neardistance_spinbox.configure(style='cosmo.TSpinbox'))
        
        
        # time spinbox        
        time_label = ttk.Label(self.nameframe, text='Auto-time', anchor='center', font=("Helvetica", 16, "bold"))
        time_label.pack(side='top',pady=25, anchor='center')

        self.time_spinbox = ttk.Spinbox(self.time_frame, from_=0.1, to=10, increment=0.1,style='darkly' , width=10)
        self.time_spinbox.pack(side='left', padx=2)
        
        unit_label4 = ttk.Label(self.time_frame, text='S',font=("Helvetica", 10, "bold"))
        unit_label4.pack(side='left')
        
        self.time_spinbox.bind('<FocusIn>', lambda e: self.time_spinbox.configure(style='TSpinbox'))
        self.time_spinbox.bind('<FocusOut>', lambda e: self.time_spinbox.configure(style='cosmo.TSpinbox'))
        
         # screen save time spinbox
        screensave_time_label = ttk.Label(self.nameframe, text='Screen save time', anchor='center', font=("Helvetica", 16, "bold"))
        screensave_time_label.pack(side='top',pady=5, anchor='center')

        self.screensave_time_spinbox = ttk.Spinbox(self.screensave_time_frame, from_=0.1, to=10, increment=0.1,style='darkly' , width=10)
        self.screensave_time_spinbox.pack(side='left', padx=2, pady=10)
        
        unit_label5 = ttk.Label(self.screensave_time_frame, text='min',font=("Helvetica", 10, "bold"))
        unit_label5.pack(side='left')
        
        self.screensave_time_spinbox.bind('<FocusIn>', lambda e: self.screensave_time_spinbox.configure(style='TSpinbox'))
        self.screensave_time_spinbox.bind('<FocusOut>', lambda e: self.screensave_time_spinbox.configure(style='cosmo.TSpinbox'))
        
        # mode combobox        
        mode_label = ttk.Label(self.nameframe, text='Mode', anchor='center', font=("Helvetica", 16, "bold"))
        mode_label.pack(side='top',pady=30, anchor='center')

        self.mode_combobox = ttk.Combobox(self.number_mode_frame, values=["","Letter Mode", "Number Mode"], state='readonly', width=15)
        self.mode_combobox.pack(side='left', padx= 2)
        
        self.mode_combobox.bind('<FocusIn>', lambda e: self.mode_spinbox.configure(style='TSpinbox'))
        self.mode_combobox.bind('<FocusOut>', lambda e: self.mode_spinbox.configure(style='cosmo.TSpinbox'))
  
        # language combobox        
        language_label = ttk.Label(self.nameframe, text='Language', anchor='center', font=("Helvetica", 16, "bold"))
        language_label.pack(side='top',pady=0, anchor='center')

        self.language_combobox = ttk.Combobox(self.language_frame, values=['English', 'فارسی'], state='readonly', width=15)
        self.language_combobox.pack(side='left', padx= 2,pady=10)
        
        self.language_combobox.bind('<FocusIn>', lambda e: self.language_combobox.configure(style='TSpinbox'))
        self.language_combobox.bind('<FocusOut>', lambda e: self.language_combobox.configure(style='cosmo.TSpinbox'))
        
          # Profile combobox    
        profile_label = ttk.Label(self.nameframe, text='Profile', anchor='center', font=("Helvetica", 16, "bold"))
        profile_label.pack(side='top',pady=30, anchor='center')

        self.profile_combobox = ttk.Combobox(self.profile_frame, 
                                       values=["Profile 1", "Profile 2", 'Profile 3', 'Profile 4', 'Profile 5'], state='readonly', width=15)
        self.profile_combobox.pack(side='left', padx= 2)
        
        self.profile_combobox.bind('<FocusIn>', lambda e: self.profile_combobox.configure(style='TSpinbox'))
        self.profile_combobox.bind('<FocusOut>', lambda e: self.profile_combobox.configure(style='cosmo.TSpinbox'))
        #handle profile auto-save on menu window close
        


        # buttons
        self.btn1 = ttk.Button(self.btn1_frame, text='Reset', style='danger.TButton')
        self.btn1.pack(side='left')
        #self.btn1.bind('<FocusIn>', lambda e: self.btn1.configure(background='blue'))

        self.btn2 = ttk.Button(self.btn2_frame, text='Restart',style='warning.TButton',command=lambda: os.system('reboot'))
        self.btn2.pack(side='left')
        self.btn2.bind('<FocusIn>', lambda e: self.btn2.configure(background='blue'))

        self.btn3 = ttk.Button(self.btn3_frame, text=' Exit ', style='primary.TButton', command=self.window.destroy)
        self.btn3.pack(side='left')
        

        self.widgets_list= [self.brightness_spinbox, self.contrast_spinbox, self.chartsize_spinbox, self.distance_spinbox, self.neardistance_spinbox, self.time_spinbox, self.screensave_time_spinbox, self.mode_combobox, self.language_combobox, self.profile_combobox]
        self.current_widget_index = 0
        self.widgets_list[self.current_widget_index][1].focus()
        self.window.bind('<Down>', self.move_focus_next)
        self.window.bind('<Up>', self.move_focus_previous)
      
        # # Set initial focus
        # self.brightness_spinbox.focus_set()
        
        
     # update meter widgets value   
    def update_meter(self, variable_name, meter_widget):
        value = int(self.brightness_spin_var.get())
        meter_widget['amountused'] = value
        meter_widget['format'] = "%.0f"

        
    def create_band(self, master, text, _from , _to):
        """Create and pack an equalizer band"""
        value = tk.IntVar(master, value=randint(_from, _to))

        # header label
        hdr = ttk.Label(master, text=text, anchor='center')
        hdr.pack(side='top', fill='x', pady=10)
        
        # brightness scale
        scale = ttk.Scale(
            master,
            orient='horizontal',  
            from_=_from, 
            to=_to,  
            variable=value,
            command=lambda x: self.update_value(value, text),
            cursor='hand2',
            takefocus=1,
            length=500,
            # style='info.Horizontal.TScale'                         
        )
        scale.pack()
        
        # value label
        val = ttk.Label(master, textvariable=value)
        val.pack()
        
        if( text == 'Brightness'):
            scale.focus_set()


    def update_value(self, value, name):
        value.set(f"{float(value.get()):.0f}")

    def on_focus_in(event):
        event.widget.configure(style='TSpinbox')

    def on_focus_out(event):
        event.widget.configure(style='cosmo')

    def move_focus_next(self, event):
        self.current_widget_index = (self.current_widget_index + 1) % len(self.widgets)
        self.widgets_list[self.current_widget_index].focus_set()
    def move_focus_previous(self, event):
        self.current_widget_index = (self.current_widget_index - 1) % len(self.widgets)
        self.widgets_list[self.current_widget_index].focus_set()

    def increase_spinbox(self):
        current_widget = self.widgets_list[self.current_widget_index]
        if isinstance(current_widget, ttk.Spinbox):
            current_value = int(current_widget.get())
            # current_widget.delete(0, 'end')
            # current_widget.insert(0, current_value + 1)
            current_widget.set(current_value + 1)
        else:
             if isinstance(current_widget, ttk.Combobox):
                current_index = current_widget.current()
                next_index = (current_index + 1) % len(current_widget['values'])
                current_widget.current(next_index)

    def decrease_spinbox(self):
        current_widget = self.widgets_list[self.current_widget_index]
        if isinstance(current_widget, ttk.Spinbox):
            current_value = float(current_widget.get())
            current_widget.set(current_value - 1)
        else :
            if isinstance(current_widget, ttk.Combobox):
                current_index = current_widget.current()
                next_index = (current_index - 1) % len(current_widget['values'])
                current_widget.current(next_index)
            
class ImageImporter:
    def __init__(self, root):
        # self.root = root
        # self.img_path = r'C:\Users\FFear\OneDrive\Desktop\New folder\images'
        # self.images = self.load_images()
        # self.current_image = 0

        # self.label = tk.Label(self.root)
        # self.label.pack(fill='both', expand=True)

        # self.display_image(self.images[self.current_image])

        # self.root.bind('<Left>', self.prev_image)
        # self.root.bind('<Right>', self.next_image)
        pass

    def load_images(self):
        # images = []
        # for file in os.listdir(r"C:\Users\FFear\OneDrive\Desktop\New folder\images"):
        # 	if file.endswith(".jpg"):
        # 		img = Image.open(os.path.join(r"C:\Users\FFear\OneDrive\Desktop\New folder\images", file))
        # 		photo = ImageTk.PhotoImage(img)
        # 		images.append(photo)
        # return images
        pass

    def display_image(self, image):
        self.label.config(image=image)
        self.label.image = image

    def prev_image(self, event):
        self.current_image -= 1
        if self.current_image < 0:
            self.current_image = len(self.images) - 1
        self.display_image(self.images[self.current_image])

    def next_image(self, event):
        self.current_image += 1
        if self.current_image >= len(self.images):
            self.current_image = 0
        self.display_image(self.images[self.current_image])


def main():
   app = App()
if __name__ == "__main__":
    main()










