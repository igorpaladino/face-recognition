import Tkinter as tk
import option_functions
import functions
from ScrolledText import ScrolledText
import os

class App (tk.Frame):
    """
    GUI
    Class that implements the Main App of face recognition
    In this frame options can be choosen to create, train and test a net
    """
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
                                       
        self.parent = parent
        self.parent.title("Face recognition")
        self.entry_list = []

        # frame for the label
        self.label_frame = tk.Frame(self)
        self.label = tk.Label(self.label_frame, text = "\nChoose one of the options below.\n")
        self.label.pack()

        # frame for the RUN Button
        self.but_run_frame = tk.Frame(self)
        self.run = tk.Button(self.but_run_frame, text="Run", command = self.run)
        self.run.pack()
        
        # frame for the options list
        self.radiobutton_frame = tk.Frame(self)
        options = [ ("(1) Create net", "1"),
                   ("(2) Read net from file", "2"),
                   ("(3) Set net threshold", "3"),
                   ("(4) Copy net", "4"),
                   ("(5) Train net with image files", "5"),
                   ("(6) Train net with image files, test before each training", "6"),
                   ("(7) Train net with image files, test threshold before each training", "7"),
                   ("(8) Train net with camera", "8"),
                   ("(9) Train net with camera, test before each training", "9"),
                   ("(10) Test net with image files", "10"),
                   ("(11) Test net with camera", "11"),
                   ("(12) Test net with camera and take pictures", "12"),
                   ("(13) Debugger", "13")]
        self.option_var = tk.StringVar()

        # frame for the Entries
        self.entries_frame = tk.Frame(self)

        # frame for the Results
        self.results_frame = tk.Frame(self)

        for text, mode in options:
            self.radiobutton = tk.Radiobutton(self.radiobutton_frame, text=text, variable = self.option_var, value = mode, command=self.choose_option)
            self.radiobutton.pack(anchor = tk.W)
        
        self.label_frame.pack()
        self.radiobutton_frame.pack()

        self.yes_counter = 0
        # counter to register how many pics were trained in option_function_5

    def makeentry (self, parent, caption, width):
        """
        Create an entry box with a label for input data
        Input = ( App, Parent frame, Caption, Width )
        Parent frame: frame that is going to hold the widget
        Caption: a label for the input entry
        Width: width of the text
        Output = entry created
        """
        entry_frame = tk.Frame(parent)
        tk.Label(entry_frame, text=caption).pack(side="left")
        entry = tk.Entry(entry_frame)
        entry.pack(side="left")
        entry_frame.pack()
        return entry
                                                                                   
    def choose_option(self):
        """
        Input = ( App )
        Based on the value passed on the choose button, choose one of the options
        to create, train or test a net
        """
        
        # clean entries_frame
        for entry in self.entries_frame.winfo_children():
            entry.destroy()
        self.entries_frame.pack_forget()

        # clean results_frame
        for result in self.results_frame.winfo_children():
            result.destroy()
        self.results_frame.pack_forget()
        
        self.entry_list = []
        
        if self.option_var.get() in ["1","2", "3", "5", "6", "7", "8", "9", "10", "11", "12"]:
            filename = self.makeentry(self.entries_frame, "Net filename:", 10)
            
        if self.option_var.get() == "1":                                                                  
            rows = self.makeentry(self.entries_frame, "Number of rows:", 10)
            columns = self.makeentry(self.entries_frame, "Number of columns:", 10)
            groupsize = self.makeentry(self.entries_frame, "Group size:", 10)
            self.entry_list = [filename, rows, columns, groupsize]

        elif self.option_var.get() == "2":
            details_var = tk.IntVar()
            details = tk.Checkbutton(self.entries_frame, text="Details", variable = details_var)
            details.pack()
            self.entry_list = [filename, details_var]

        elif self.option_var.get() == "3":                                                                  
            threshold = self.makeentry(self.entries_frame, "Net threshold:", 10)
            self.entry_list = [filename, threshold]

        elif self.option_var.get() == "4":
            filename_from = self.makeentry(self.entries_frame, "Net filename from:", 10)
            filename_to = self.makeentry(self.entries_frame, "Net filename to:", 10)
            self.entry_list = [filename_from, filename_to]

        elif self.option_var.get() in ["5", "6", "7", "10"]:
            img_path_folder = self.makeentry(self.entries_frame, "Image path folder:", 10)
            self.entry_list = [filename, img_path_folder]
  
        elif self.option_var.get() in ["8", "9", "11", "12"]:
            self.entry_list = [filename]
        
        self.entries_frame.pack()
        self.but_run_frame.pack()
        self.results_frame.pack()
    
    def run (self):
        """
        Input = ( App )
        Based on the value passed to the choose option, run the code to
        create, train or test a net, it calls the functions from option_functions
        """        
        # clean results_frame
        for result in self.results_frame.winfo_children():
            result.destroy()
        self.results_frame.pack_forget()
        
        input_list = []
        for input in self.entry_list:
            input_list.append(input.get())       

        try:
            if self.option_var.get() == "13":
                option_functions.option_11(input_list)
            
            else:
                input_list[0] = 'training/' + input_list[0]
                
                if self.option_var.get() == "1":
                    option_functions.option_1(self.results_frame,input_list)
                elif self.option_var.get() == "2":
                    option_functions.option_2(self.results_frame,input_list)
                elif self.option_var.get() == "3":
                    option_functions.option_3(self.results_frame, input_list)
                elif self.option_var.get() == "4":
                    input_list[1] = 'training/' + input_list[1]
                    option_functions.option_4(self.results_frame,input_list)
                elif self.option_var.get() == "5":
                    input_list[1] = 'images/training/' + input_list[1] + '/'
                    option_functions.option_5(self.results_frame,input_list)       
                elif self.option_var.get() == "6":
                    input_list[1] = 'images/training/' + input_list[1] + '/'
                    option_functions.option_6(self,input_list)       
                elif self.option_var.get() == "7":
                    input_list[1] = 'images/training/' + input_list[1] + '/'
                    option_functions.option_7(self,input_list)       
                elif self.option_var.get() == "8":
                    option_functions.option_8(self.results_frame,input_list)
                elif self.option_var.get() == "9":
                    option_functions.option_9(self, input_list)
                elif self.option_var.get() == "10":
                    input_list[1] = 'images/testing/' + input_list[1] + '/'
                    option_functions.option_10(self,input_list)
                elif self.option_var.get() == "11":
                    option_functions.option_11(self, input_list)
                elif self.option_var.get() == "12":
                    option_functions.option_12(self, input_list)
            
            self.results_frame.pack()
            
        except (IOError, ValueError) as occurring_exception:
        #except (ZeroDivisionError) as occurring_exception:
            text = tk.Label(self.results_frame, text = '\nUnexpected input.\nTry again.\n Error: ' + str(occurring_exception))
            text.pack()
            self.results_frame.pack()

    def display_test(self, net, summation, output, mode, myImage=None):
        """
        Display results based on the tested image
        If from image file, just display the threshold, summation and if the pattern was recognised or not ( True or False )
        If from camera, shows a bar with the output percentage, 100% being a total match
        Input = ( App, net, output summation for a image, mode )
        mode = 1: testing net with image files
        mode = 2: testing net with images from camera
        mode = 3: testing net with image files, ask if user wants to use image for training
        """
        if mode == 1 or mode == 3:
            text = tk.Label(self.results_frame.interior, text = '\nNet threshold: ' + str(net.threshold) + ', Output summation: ' + str(summation) + ', output:' + str(output) + '\n')
            text.pack()
            
            if mode == 3:
                
                waitVar = tk.BooleanVar()
                waitVar.set(True)

                def no():
                    waitVar.set(False)
                        
                def yes():
                    functions.train(net, myImage)
                    increase_yes_counter(self)
                    waitVar.set(False)

                def increase_yes_counter(self):
                    self.yes_counter += 1
                                
                # frame for the YES Button
                self.but_yes_frame = tk.Frame(self.results_frame)
                self.yes = tk.Button (self.but_yes_frame, text="Yes", command = yes)
                self.yes.pack()
                self.but_yes_frame.pack()

                # frame for the NO Button
                self.but_no_frame = tk.Frame(self.results_frame)
                self.no = tk.Button(self.but_no_frame, text="No", command = no)
                self.no.pack()
                self.but_no_frame.pack()

                self.wait_variable (waitVar)

                self.but_yes_frame.pack_forget()
                self.but_no_frame.pack_forget()
                text.pack_forget()
                        
        elif mode == 2:
            max = int(net.numFunctions*1.00) # max value chosen
            position = 200 - 160*net.threshold/(net.numFunctions)
            if not self.results_frame.winfo_children():
                self.bars_frame = tk.Frame(self.results_frame)
                height = 200 - 160*summation/max
                self.bar = tk.Canvas(self.bars_frame, width=80, height=240)
                self.bar.create_rectangle(15, 40, 65, 200, fill="red")
                # line determining threshold
                changing_bar = self.bar.create_rectangle(15, height, 65, 200, fill="blue")
                bar_id = self.bar.create_text(20,20)
                threshold_line = self.bar.create_line(15, position, 65, position, fill="white", dash=(4, 4))
                self.bar.itemconfig(bar_id, text = '%i' %int(summation*100.0/max) + '%' )
                self.bar.pack(side="right")
                self.bars_frame.pack()
                self.results_frame.pack()
                self.parent.update_idletasks()
            else:
                height = 200 - 160*summation/max
                self.bar.coords(2, 15, height, 65, 200)
                # 2 is equivalent to changing_bar
                self.bar.itemconfig(3, text = '%i' %int(summation*100.0/max) + '%')
                # 3 is equivalent to bar_id
                self.bar.coords(4, 15, position, 65, position)
                # 4 is equivalent to threshold_line
                self.results_frame.pack()
                self.parent.update_idletasks()
                
    def add_scroll_2_frame (self, frame):
        """
        Add a scroolbar to a frame
        Input = (App, window frame)
        """
                
        # create a canvas object and a vertical scrollbar for scrolling it
        vscrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL)
        vscrollbar.pack(fill=tk.Y, side=tk.RIGHT, expand=tk.FALSE)
        canvas = tk.Canvas(frame, bd=0, highlightthickness=0, yscrollcommand = vscrollbar.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE)
        vscrollbar.config(command=canvas.yview)
        
        # reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)
        
        # create a frame inside the canvas which will be scrolled with it
        frame.interior = interior = tk.Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior, anchor=tk.NW)

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
            # update the canvas's width to fit the inner frame
                canvas.config(width=interior.winfo_reqwidth())
        interior.bind('<Configure>', _configure_interior)
        
        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
            # update the inner frame's width to fill the canvas
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())
        canvas.bind('<Configure>', _configure_canvas)
        
        frame.pack()