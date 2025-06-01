import tkinter as tk
import os
from PIL import ImageTk, Image
Image.CUBIC = Image.BICUBIC # Setting the resampling filter for image resizing
from tkinter import ttk, StringVar
import ttkbootstrap as ttk # Importing ttkbootstrap for enhanced tkinter styling
from ttkbootstrap.constants import * # Importing all constants from ttkbootstrap
from random import randint
#import ir # Commented out: Potentially for IR remote functionality
#import RPi.GPIO as GPIO # Commented out: Potentially for Raspberry Pi GPIO interaction
import threading # For running tasks in parallel, like listening for IR signals

ir_pin=11 # Global variable for the IR receiver GPIO pin number (if RPi.GPIO was used)
    
class App(ttk.Window):
    # mainsetup
    def __init__(self):
        super().__init__(themename='cyborg') # Initialize the main window with the 'cyborg' theme from ttkbootstrap
        #self.myclass = ir.ir_reciever() # Commented out: Instantiation of an IR receiver class
        self.title('EyeQtest') # Set the title of the main window
        self.button = ttk.Button(self, text='Menu', command=self.open_menu) # Create a button to open the menu
        self.button.pack() # Add the button to the main window
        
        # Make the window fullscreen and borderless (currently commented out)
        # self.attributes('-fullscreen', True)
        # self.attributes('-topmost', True)
        
        # widgets
        ImageImporter(self) # Instantiate the ImageImporter class (currently its functionality is placeholder)
 
        #Initialize IR code
        self.ir_code = None # Variable to store the last received IR code

        #Start a new thread that will listen for IR signals
        self.ir_thread = threading.Thread(target=self.listen_for_ir) # Create a new thread for the IR listener
        self.ir_thread.daemon = True # Set the thread as a daemon so it closes when the main app closes
        self.ir_thread.start() # Start the IR listener thread

        #run
        self.mainloop() # Start the tkinter event loop
        
    def open_menu(self):
        """Opens the settings menu."""
        self.menu = Menu(self) # Create an instance of the Menu class
         
    def on_key_press(self):
        """Handles actions based on the received IR code."""
        # This function is intended to be called when an IR signal is processed.
        # It checks the value of self.ir_code and performs actions accordingly.
        if self.ir_code == '0x': # Example IR code for opening the menu
             self.open_menu()
        elif self.ir_code == '0xB': # Example IR code for moving focus to the next widget in the menu
            Menu.move_focus_next() # Calls the static method - this will cause an error if Menu instance is not handled correctly
        elif self.ir_code == '0xC': # Example IR code for moving focus to the previous widget in the menu
            Menu.move_focus_previous() # Calls the static method - this will cause an error
        elif self.ir_code == '0x1': # Example IR code for increasing a spinbox value in the menu
            Menu.increase_spinbox() # Calls the static method - this will cause an error
        elif self.ir_code == '0x2': # Example IR code for decreasing a spinbox value in the menu
            Menu.decrease_spinbox() # Calls the static method - this will cause an error
        # Add more elif statements here for other IR codes
        else:
            print(f"Unknown IR code: {self.ir_code}") # Prints if the IR code is not recognized
            
    def listen_for_ir(self):
        """Listens for IR signals in a separate thread."""
        # This method is intended to run in a loop, waiting for IR signals.
        # It uses GPIO pins, suggesting it's designed for a Raspberry Pi.
        # The RPi.GPIO and ir libraries are currently commented out, so this will not function as is.
        print("Starting IR Listener")
        try:
            while True:
                print("Waiting for signal")
                # GPIO.wait_for_edge(ir_pin, GPIO.FALLING) # Waits for a falling edge on the IR pin
                # code = self.myclass.on_ir_receive(ir_pin) # Reads the IR code
                code = None # Placeholder since GPIO is commented out
                if code:
                    self.ir_code = str(hex(code)) # Converts the received code to a hex string
                    print(self.ir_code) # Prints the received IR code
                    self.on_key_press() # Calls the handler for the received IR code
                else:
                    # print("Invalid code") # Prints if an invalid code is received
                    pass # Keep the loop running even if no code or invalid code for now
                # Simulate some delay or alternative event trigger if not using GPIO
                threading.Event().wait(1) # Prevents busy-waiting if GPIO is not used, adjust as needed
        except Exception as e:
            print(f"An error occurred in IR listener: {e}")
        finally:
            print("Cleaning up IR listener") # This part might be problematic if GPIO was never set up
            # GPIO.cleanup() # Cleans up GPIO resources on exit
            
class Menu:
    """Class to create and manage the settings menu."""
    def __init__(self, master):
        """Initializes the Menu window and its widgets."""
        self.master = master # Reference to the parent window (App instance)
        self.window = ttk.Toplevel(self.master) # Create a new top-level window for the menu
        self.window.resizable(True,True) # Allow the menu window to be resizable
        
        self.window.title('Menu') # Set the title of the menu window
        self.window.attributes('-fullscreen', True) # Make the menu window fullscreen
        self.window.attributes('-topmost', True) # Keep the menu window on top of other windows
        
        # Outer frame for padding around the main content
        self.outer_frame = ttk.Frame(self.window,padding=75)
        self.outer_frame.pack(expand=True, fill='both')     

        # Inner frame styled as a Labelframe to contain settings
        style = ttk.Style()
        style.configure('warning.TLabelframe.Label', font=('Helvetica', 25, 'bold')) # Configure font for Labelframe title

        self.inner_frame = ttk.Labelframe(self.outer_frame ,text='Settings', padding=10, relief='raised',
                                         style='warning.TLabelframe' , width= 700 , height=800)
        self.inner_frame.pack(side='top',anchor='center') # Pack the inner frame centered at the top
        
        # Frame for the "About" information
        self.about_frame = ttk.Frame(self.outer_frame, width=600, height=100) 
        self.about_frame.pack(side='top', anchor='e', padx=600, pady=15) # Pack it to the top-east
        
        # Frame to hold the labels for settings (e.g., "Brightness", "Contrast")
        self.nameframe = ttk.Frame(self.inner_frame)
        self.nameframe.pack(side='left',fill='y', pady=10, anchor='w') # Pack it to the left of inner_frame
        
        # Vertical separator between labels and controls
        self.seperator = ttk.Separator(self.inner_frame, orient='vertical')
        self.seperator.pack(side='left', fill='y', padx=10)
        
        # About label with application information
        about_label = ttk.Label(self.about_frame, text=' EyeQtest™ v0.1 \n ARMLab® inc. \n Copyright© 2024-2034',
                                font=("Helvetica", 12, "bold"), style='info', justify='left')
        about_label.pack(side='top',anchor='e' )
        
 
    # frames for each setting control       
        
        # Frame for brightness controls
        self.brightness_frame = ttk.Frame(self.inner_frame)
        self.brightness_frame.pack(side='top',pady=10 , anchor='w')  
        
        # Frame for contrast controls
        self.contrast_frame = ttk.Frame(self.inner_frame)
        self.contrast_frame.pack(side='top',padx=20,pady=10 , anchor='w')  
        
        # Frame for chart size controls
        self.chartsize_frame = ttk.Frame(self.inner_frame)
        self.chartsize_frame.pack(side='top',padx=20,pady=10 , anchor='w')  
        
        # Frame for distance controls
        self.distance_frame = ttk.Frame(self.inner_frame)
        self.distance_frame.pack(side='top',padx=20,pady=10 , anchor='w')  
        
        # Frame for near distance mode controls
        self.neardistance_frame = ttk.Frame(self.inner_frame)
        self.neardistance_frame.pack(side='top',padx=20,pady=10 , anchor='w') 
        
        # Frame for auto-time controls
        self.time_frame = ttk.Frame(self.inner_frame)
        self.time_frame.pack(side='top',padx=20,pady=10 , anchor='w')  
        
        # Frame for screen save time controls
        self.screensave_time_frame = ttk.Frame(self.inner_frame)
        self.screensave_time_frame.pack(side='top',padx=20,pady=10 , anchor='w')
                
        # Frame for number mode selection
        self.number_mode_frame = ttk.Frame(self.inner_frame)
        self.number_mode_frame.pack(side='top',padx=20,pady=10 , anchor='w') 
 
        # Frame for language selection
        self.language_frame = ttk.Frame(self.inner_frame)
        self.language_frame.pack(side='top',padx=20,pady=10 , anchor='w')
 
        # Frame for profile selection
        self.profile_frame = ttk.Frame(self.inner_frame)
        self.profile_frame.pack(side='top',padx=20,pady=10 , anchor='w') 
        
        
        
        # Frames for action buttons (Reset, Restart, Exit)
        self.btn1_frame = ttk.Frame(self.inner_frame) # Frame for Reset button
        self.btn1_frame.pack(side='right', padx=20, pady=10) # Packed to the right
        
        self.btn2_frame = ttk.Frame(self.inner_frame) # Frame for Restart button
        self.btn2_frame.pack(side='right', padx=20, pady=10) # Packed to the right
        
        self.btn3_frame = ttk.Frame(self.inner_frame) # Frame for Exit button
        self.btn3_frame.pack(side='right', padx=20, pady=10) # Packed to the right

        
        
        
        
        
        # Custom style for Spinbox arrows when focused
        style = ttk.Style()
        style.configure('TSpinbox', arrowcolor= 'red') # When focused, arrow color is red
        
        style1 = ttk.Style()
        style1.configure('cosmo.TSpinbox', arrowcolor= 'gray') # Default/unfocused arrow color is gray
        
        #  Brightness spinbox and meter
        brightness_label = ttk.Label(self.nameframe, text='Brightnes', anchor='center', font=("Helvetica", 16, "bold"))
        brightness_label.pack(side='top', anchor='center', pady=65) # Label for brightness

        self.brightness_spin_var = tk.StringVar() # StringVar to hold the brightness value
        # Trace the variable to update the meter whenever the spinbox value changes
        self.brightness_spin_var.trace_add('write', lambda name, index, mode: self.update_meter('brightness', self.brightness_meter))
        self.brightness_spinbox = ttk.Spinbox(self.brightness_frame, from_=0, to=100,
                                             increment=1, style='darkly', textvariable=self.brightness_spin_var, width=3) 
        self.brightness_spinbox.pack(side='left', padx= 15)

        # Change spinbox style on focus in/out
        self.brightness_spinbox.bind('<FocusIn>', lambda e: self.brightness_spinbox.configure(style='TSpinbox'))
        self.brightness_spinbox.bind('<FocusOut>', lambda e: self.brightness_spinbox.configure(style='cosmo.TSpinbox'))

        #value = int(self.brightness_spin_var.get()) # Attempt to get value before it's set might be problematic
        self.brightness_meter = ttk.Meter(self.brightness_frame, metersize=150, padding=5, metertype="semi",#amountused=value,
                                      textright="%", subtextstyle="light", subtext=" ") # Meter to visually represent brightness
        self.brightness_meter.pack(side='left', padx=15)
        
        # self.brightness_spin_var.trace_add('write', lambda name, index, mode: self.update_meter('brightness', self.brightness_meter)) # Redundant trace


         
        # contrast spinbox          
        contrast_label = ttk.Label(self.nameframe, text='Contrast', anchor='center', font=("Helvetica", 16, "bold"))
        contrast_label.pack(side='top',pady=25, anchor='center') # Label for contrast

        self.contrast_spinbox = ttk.Spinbox(self.contrast_frame, from_=-100, to=100, 
                                             increment=1,style='darkly', width=10)
        self.contrast_spinbox.pack(side='left')
        
        unit_label1 = ttk.Label(self.contrast_frame, text='') # Placeholder for unit or additional info
        unit_label1.pack(side='left',padx=2)
        
        # Change spinbox style on focus in/out
        self.contrast_spinbox.bind('<FocusIn>', lambda e: self.contrast_spinbox.configure(style='TSpinbox'))
        self.contrast_spinbox.bind('<FocusOut>', lambda e: self.contrast_spinbox.configure(style='cosmo.TSpinbox'))
        
        
        # chart size spinbox
        chartsize_label = ttk.Label(self.nameframe, text='Chart Size', anchor='center', font=("Helvetica", 16, "bold"))
        chartsize_label.pack(side='top',pady=5, anchor='center') # Label for chart size

        self.chartsize_spinbox = ttk.Spinbox(self.chartsize_frame, from_=0, to=100, 
                                             increment=1,style='darkly', width=10)
        self.chartsize_spinbox.pack(side='left', pady=10)
        
        unit_label2 = ttk.Label(self.chartsize_frame, text='%', font=("Helvetica", 10, "bold")) # Unit label for chart size
        unit_label2.pack(side='left',padx=2)
        
        # Change spinbox style on focus in/out
        self.chartsize_spinbox.bind('<FocusIn>', lambda e: self.chartsize_spinbox.configure(style='TSpinbox'))
        self.chartsize_spinbox.bind('<FocusOut>', lambda e: self.chartsize_spinbox.configure(style='cosmo.TSpinbox'))
 
         # Distance spinbox          
        distance_label = ttk.Label(self.nameframe, text='Distance', anchor='center', font=("Helvetica", 16, "bold"))
        distance_label.pack(side='top',pady=25, anchor='center') # Label for distance

        self.distance_spinbox = ttk.Spinbox(self.distance_frame, from_=1, to=5, increment=0.2,style='darkly',width=10)
        self.distance_spinbox.pack(side='left')
        
        unit_label3 = ttk.Label(self.distance_frame, text='M', font=("Helvetica", 10, "bold")) # Unit label for distance (Meters)
        unit_label3.pack(side='left',padx=2)
        
        # Change spinbox style on focus in/out
        self.distance_spinbox.bind('<FocusIn>', lambda e: self.distance_spinbox.configure(style='TSpinbox'))
        self.distance_spinbox.bind('<FocusOut>', lambda e: self.distance_spinbox.configure(style='cosmo.TSpinbox'))
        
        # Near Distance Mode spinbox          
        neardistance_label = ttk.Label(self.nameframe, text='NearDistance Mode', anchor='center', font=("Helvetica", 16, "bold"))
        neardistance_label.pack(side='top',pady=5, anchor='center') # Label for near distance mode
        
        self.neardistance_spinbox = ttk.Spinbox(self.neardistance_frame, from_=0, to=1, increment=0.2,style='darkly',width=10)
        self.neardistance_spinbox.pack(side='left', pady=10)      
        
        # Change spinbox style on focus in/out
        self.neardistance_spinbox.bind('<FocusIn>', lambda e: self.neardistance_spinbox.configure(style='TSpinbox'))
        self.neardistance_spinbox.bind('<FocusOut>', lambda e: self.neardistance_spinbox.configure(style='cosmo.TSpinbox'))
        
        
        # time spinbox (Auto-time)        
        time_label = ttk.Label(self.nameframe, text='Auto-time', anchor='center', font=("Helvetica", 16, "bold"))
        time_label.pack(side='top',pady=25, anchor='center') # Label for auto-time

        self.time_spinbox = ttk.Spinbox(self.time_frame, from_=0.1, to=10, increment=0.1,style='darkly' , width=10)
        self.time_spinbox.pack(side='left', padx=2)
        
        unit_label4 = ttk.Label(self.time_frame, text='S',font=("Helvetica", 10, "bold")) # Unit label for time (Seconds)
        unit_label4.pack(side='left')
        
        # Change spinbox style on focus in/out
        self.time_spinbox.bind('<FocusIn>', lambda e: self.time_spinbox.configure(style='TSpinbox'))
        self.time_spinbox.bind('<FocusOut>', lambda e: self.time_spinbox.configure(style='cosmo.TSpinbox'))
        
         # screen save time spinbox
        screensave_time_label = ttk.Label(self.nameframe, text='Screen save time', anchor='center', font=("Helvetica", 16, "bold"))
        screensave_time_label.pack(side='top',pady=5, anchor='center') # Label for screen save time

        self.screensave_time_spinbox = ttk.Spinbox(self.screensave_time_frame, from_=0.1, to=10, increment=0.1,style='darkly' , width=10)
        self.screensave_time_spinbox.pack(side='left', padx=2, pady=10)
        
        unit_label5 = ttk.Label(self.screensave_time_frame, text='min',font=("Helvetica", 10, "bold")) # Unit label for screen save time (minutes)
        unit_label5.pack(side='left')
        
        # Change spinbox style on focus in/out
        self.screensave_time_spinbox.bind('<FocusIn>', lambda e: self.screensave_time_spinbox.configure(style='TSpinbox'))
        self.screensave_time_spinbox.bind('<FocusOut>', lambda e: self.screensave_time_spinbox.configure(style='cosmo.TSpinbox'))
        
        # mode combobox (e.g., Letter Mode, Number Mode)        
        mode_label = ttk.Label(self.nameframe, text='Mode', anchor='center', font=("Helvetica", 16, "bold"))
        mode_label.pack(side='top',pady=30, anchor='center') # Label for mode selection

        self.mode_combobox = ttk.Combobox(self.number_mode_frame, values=["","Letter Mode", "Number Mode"], state='readonly', width=15) # Readonly combobox for mode
        self.mode_combobox.pack(side='left', padx= 2)
        
        # Change combobox style on focus in/out (using spinbox styles here, might need specific combobox styling)
        self.mode_combobox.bind('<FocusIn>', lambda e: self.mode_combobox.configure(style='TSpinbox')) # Note: applying TSpinbox style to Combobox
        self.mode_combobox.bind('<FocusOut>', lambda e: self.mode_combobox.configure(style='cosmo.TSpinbox')) # Note: applying cosmo.TSpinbox style
 
        # language combobox         
        language_label = ttk.Label(self.nameframe, text='Language', anchor='center', font=("Helvetica", 16, "bold"))
        language_label.pack(side='top',pady=0, anchor='center') # Label for language selection

        self.language_combobox = ttk.Combobox(self.language_frame, values=['English', 'فارسی'], state='readonly', width=15) # Readonly combobox for language
        self.language_combobox.pack(side='left', padx= 2,pady=10)
        
        # Change combobox style on focus in/out
        self.language_combobox.bind('<FocusIn>', lambda e: self.language_combobox.configure(style='TSpinbox')) # Note: TSpinbox style
        self.language_combobox.bind('<FocusOut>', lambda e: self.language_combobox.configure(style='cosmo.TSpinbox')) # Note: cosmo.TSpinbox style
        
         # Profile combobox      
        profile_label = ttk.Label(self.nameframe, text='Profile', anchor='center', font=("Helvetica", 16, "bold"))
        profile_label.pack(side='top',pady=30, anchor='center') # Label for profile selection

        self.profile_combobox = ttk.Combobox(self.profile_frame, 
                                           values=["Profile 1", "Profile 2", 'Profile 3', 'Profile 4', 'Profile 5'], state='readonly', width=15) # Readonly combobox for profiles
        self.profile_combobox.pack(side='left', padx= 2)
        
        # Change combobox style on focus in/out
        self.profile_combobox.bind('<FocusIn>', lambda e: self.profile_combobox.configure(style='TSpinbox')) # Note: TSpinbox style
        self.profile_combobox.bind('<FocusOut>', lambda e: self.profile_combobox.configure(style='cosmo.TSpinbox')) # Note: cosmo.TSpinbox style
        #handle profile auto-save on menu window close (Placeholder comment for future functionality)
        


        # buttons for actions
        self.btn1 = ttk.Button(self.btn1_frame, text='Reset', style='danger.TButton') # Reset button
        self.btn1.pack(side='left')
        #self.btn1.bind('<FocusIn>', lambda e: self.btn1.configure(background='blue')) # Example focus behavior (commented out)

        self.btn2 = ttk.Button(self.btn2_frame, text='Restart',style='warning.TButton',command=lambda: os.system('reboot')) # Restart button (executes system reboot)
        self.btn2.pack(side='left')
        self.btn2.bind('<FocusIn>', lambda e: self.btn2.configure(background='blue')) # Example focus behavior (may not work as expected with ttk themes)

        self.btn3 = ttk.Button(self.btn3_frame, text=' Exit ', style='primary.TButton', command=self.window.destroy) # Exit button (closes the menu window)
        self.btn3.pack(side='left')
        

        # List of all interactive widgets in the menu for focus navigation
        self.widgets_list= [self.brightness_spinbox, self.contrast_spinbox, self.chartsize_spinbox, self.distance_spinbox, self.neardistance_spinbox, self.time_spinbox, self.screensave_time_spinbox, self.mode_combobox, self.language_combobox, self.profile_combobox, self.btn1, self.btn2, self.btn3] # Added buttons to list
        self.current_widget_index = 0 # Index of the currently focused widget
        if self.widgets_list: # Ensure the list is not empty
            self.widgets_list[self.current_widget_index].focus_set() # Set initial focus on the first widget
        
        # Bind arrow keys for navigating between widgets
        self.window.bind('<Down>', self.move_focus_next) # Move focus to next widget on Down arrow key
        self.window.bind('<Up>', self.move_focus_previous) # Move focus to previous widget on Up arrow key
      
        # # Set initial focus (alternative way, now handled by widgets_list)
        # self.brightness_spinbox.focus_set()
        
        
     # update meter widgets value   
    def update_meter(self, variable_name, meter_widget):
        """Updates the specified meter widget's value."""
        # Currently, this method only updates based on brightness_spin_var,
        # a more generic approach might be needed if other meters are added.
        try:
            value = int(self.brightness_spin_var.get()) # Get the value from the brightness StringVar
            if 0 <= value <= 100: # Ensure value is within meter's expected range
                 meter_widget.configure(amountused=value) # Set the meter's 'amountused' property
            # meter_widget['format'] = "%.0f" # This line seems to be for ttk.Meter's text formatting if it supports it
        except ValueError:
            # Handle cases where the spinbox value might not be a valid integer (e.g., empty)
            meter_widget.configure(amountused=0) 

      
    def create_band(self, master, text, _from , _to):
        """
        Create and pack an equalizer band-like widget group (Label, Scale, Value Label).
        This function is defined but not directly used in the Menu __init__ for the main settings.
        It seems like a utility for creating scale-based inputs.
        """
        value = tk.IntVar(master, value=randint(_from, _to)) # Create an IntVar for the scale

        # header label
        hdr = ttk.Label(master, text=text, anchor='center') # Label for the band
        hdr.pack(side='top', fill='x', pady=10)
        
        # brightness scale (though named brightness, it's generic here)
        scale = ttk.Scale(
            master,
            orient='horizontal',  
            from_=_from, 
            to=_to,  
            variable=value, # Link scale to the IntVar
            command=lambda x: self.update_value(value, text), # Command to execute on scale change
            cursor='hand2',
            takefocus=1, # Allow the scale to receive focus
            length=500,
            # style='info.Horizontal.TScale' # Optional style for the scale          
        )
        scale.pack()
        
        # value label to display the current scale value
        val = ttk.Label(master, textvariable=value) # Label linked to the IntVar
        val.pack()
        
        if( text == 'Brightness'): # Special case: if this band is for "Brightness", set focus to its scale
            scale.focus_set()


    def update_value(self, value, name):
        """Formats and sets the value of an IntVar, typically from a scale."""
        # This function is used as a callback for the scale's command.
        # It ensures the value is formatted as a float with no decimal places.
        value.set(f"{float(value.get()):.0f}")

    def on_focus_in(self, event): # Renamed to avoid conflict, and should be method of class if used with self
        """Changes widget style when it gains focus."""
        # This is a generic handler, intended to be bound to widget focus events.
        event.widget.configure(style='TSpinbox') # Applies 'TSpinbox' style (red arrows)

    def on_focus_out(self, event): # Renamed to avoid conflict, and should be method of class if used with self
        """Changes widget style when it loses focus."""
        # This is a generic handler, intended to be bound to widget focus-out events.
        event.widget.configure(style='cosmo.TSpinbox') # Applies 'cosmo.TSpinbox' style (gray arrows)

    def move_focus_next(self, event=None): # Added event=None for potential direct calls
        """Moves focus to the next widget in the widgets_list."""
        if not self.widgets_list: return # Do nothing if there are no widgets
        self.current_widget_index = (self.current_widget_index + 1) % len(self.widgets_list) # Cycle to next widget
        self.widgets_list[self.current_widget_index].focus_set() # Set focus
        # print(f"Focus moved to: {self.widgets_list[self.current_widget_index].winfo_class()}")

    def move_focus_previous(self, event=None): # Added event=None for potential direct calls
        """Moves focus to the previous widget in the widgets_list."""
        if not self.widgets_list: return # Do nothing if there are no widgets
        self.current_widget_index = (self.current_widget_index - 1) % len(self.widgets_list) # Cycle to previous widget
        self.widgets_list[self.current_widget_index].focus_set() # Set focus
        # print(f"Focus moved to: {self.widgets_list[self.current_widget_index].winfo_class()}")

    def increase_spinbox(self):
        """Increases the value of the currently focused Spinbox or cycles the Combobox."""
        if not self.widgets_list: return
        current_widget = self.widgets_list[self.current_widget_index] # Get the currently focused widget
        if isinstance(current_widget, ttk.Spinbox):
            try:
                # For Spinbox, directly use its internal increment/decrement methods if available,
                # or manually change value. ttk.Spinbox might not have a simple .step() or similar.
                current_value = float(current_widget.get())
                increment = float(current_widget.cget('increment')) # Get the increment step
                to_val = float(current_widget.cget('to'))
                if current_value + increment <= to_val:
                    current_widget.set(current_value + increment)
                else:
                    current_widget.set(to_val) # Set to max if increment exceeds 'to' value
            except (ValueError, tk.TclError): # Handle cases where value might not be number or spinbox is not fully configured
                pass # Or some default increment logic
        elif isinstance(current_widget, ttk.Combobox):
            current_index = current_widget.current() # Get current selection index
            values_count = len(current_widget['values'])
            if values_count > 0:
                next_index = (current_index + 1) % values_count # Cycle to next option
                current_widget.current(next_index) # Set new selection

    def decrease_spinbox(self):
        """Decreases the value of the currently focused Spinbox or cycles the Combobox."""
        if not self.widgets_list: return
        current_widget = self.widgets_list[self.current_widget_index] # Get the currently focused widget
        if isinstance(current_widget, ttk.Spinbox):
            try:
                current_value = float(current_widget.get())
                increment = float(current_widget.cget('increment')) # Get the increment step
                from_val = float(current_widget.cget('from'))
                if current_value - increment >= from_val:
                    current_widget.set(current_value - increment)
                else:
                    current_widget.set(from_val) # Set to min if decrement goes below 'from' value
            except (ValueError, tk.TclError):
                pass
        elif isinstance(current_widget, ttk.Combobox):
            current_index = current_widget.current() # Get current selection index
            values_count = len(current_widget['values'])
            if values_count > 0:
                next_index = (current_index - 1 + values_count) % values_count # Cycle to previous option
                current_widget.current(next_index) # Set new selection
            
class ImageImporter:
    """
    Class intended for importing and displaying images.
    Currently, most of its functionality is commented out or placeholder.
    """
    def __init__(self, root):
        # self.root = root # Reference to the parent window
        # self.img_path = r'C:\Users\FFear\OneDrive\Desktop\New folder\images' # Path to image directory
        # self.images = self.load_images() # Load images from the path
        # self.current_image = 0 # Index of the currently displayed image

        # self.label = tk.Label(self.root) # Label widget to display images
        # self.label.pack(fill='both', expand=True)

        # if self.images: # If images were loaded
        #     self.display_image(self.images[self.current_image]) # Display the first image

        # # Bind arrow keys for image navigation (if active)
        # self.root.bind('<Left>', self.prev_image)
        # self.root.bind('<Right>', self.next_image)
        pass # Current __init__ does nothing

    def load_images(self):
        """Loads images from the specified directory."""
        # images = []
        # for file in os.listdir(r"C:\Users\FFear\OneDrive\Desktop\New folder\images"):
        #   if file.endswith(".jpg"): # Check for .jpg files
        #         img = Image.open(os.path.join(r"C:\Users\FFear\OneDrive\Desktop\New folder\images", file)) # Open image
        #         photo = ImageTk.PhotoImage(img) # Convert to PhotoImage for tkinter
        #         images.append(photo)
        # return images
        pass # Current load_images does nothing

    def display_image(self, image):
        """Displays a given image on the label."""
        # self.label.config(image=image) # Set the image for the label
        # self.label.image = image # Keep a reference to avoid garbage collection
        pass # Current display_image does nothing

    def prev_image(self, event):
        """Displays the previous image in the list."""
        # self.current_image -= 1
        # if self.current_image < 0: # Wrap around to the last image
        #     self.current_image = len(self.images) - 1
        # self.display_image(self.images[self.current_image])
        pass # Current prev_image does nothing

    def next_image(self, event):
        """Displays the next image in the list."""
        # self.current_image += 1
        # if self.current_image >= len(self.images): # Wrap around to the first image
        #     self.current_image = 0
        # self.display_image(self.images[self.current_image])
        pass # Current next_image does nothing


def main():
    """Main function to create and run the application."""
    app = App() # Create an instance of the App class
    # The app.mainloop() is called within App's __init__

if __name__ == "__main__":
    # This block ensures that main() is called only when the script is executed directly
    main()
