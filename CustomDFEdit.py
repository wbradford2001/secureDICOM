import tkinter as tk
from typing import List

from matplotlib.pyplot import savefig

import TopLevelWindow





class text_box:
    list_of_boxes = []
    regular_boxes = []
    meta_boxes = []
    error_box_already_exists = False
    height = 20
    fontstyle = None
    def __init__(self, toplevel, fontstyle, index, dataelement, xpos, width, attrib, box_to_add_to, view_or_edit):
        self.toplevel = toplevel
        self.attrib = attrib
        self.border_width = 1
        self.fontsize = 8
        text_box.fontstyle = fontstyle
        self.xpos = xpos
        self.index = index
        self.width = width 
        self.element_str = tk.StringVar()
        self.view_or_edit = view_or_edit        
        if self.attrib == "tag":
            self.element_str.set(str(dataelement.tag))
        elif self.attrib == "keyword":
            self.element_str.set(str(dataelement.keyword))
        elif self.attrib == "VR":
            self.element_str.set(str(dataelement.VR))
        elif self.attrib == "value":
            if (dataelement.keyword) != "PixelData":
                self.element_str.set(str(dataelement.value))
            else:
                self.element_str.set("Array of {} elements".format(
                                                                        len(dataelement.value),))
        else:
            self.element_str.set(self.attrib)
        self.orig_string = self.element_str.get()
        text_box.list_of_boxes.append(self)
        if box_to_add_to == "regular":
            text_box.regular_boxes.append(self)
        elif box_to_add_to == "meta":
            text_box.meta_boxes.append(self)      
        self.label = tk.Entry(
                    self.toplevel, 
                    font = (self.fontstyle, self.fontsize),
                    textvariable=self.element_str,
                    bg = 'black',
                    bd = self.border_width,
                    fg = 'white',
                    relief = 'flat',
                    justify='center',
                    selectborderwidth = 1,
                    highlightcolor='black',
                    highlightbackground= 'black',

                    )
        if self.view_or_edit == 'view':
            self.element_str.trace_add("write", self.error_message)
        elif self.view_or_edit == 'edit':
            self.element_str.trace_add("write", self.change_made)            
    def change_made(self, one, two, three):
        save_button.config(state = tk.NORMAL)
        revert_button.config(state = tk.NORMAL)
    def place_self(self):
        self.label.place(x = self.xpos, y = self.index * self.height, anchor='nw', width = self.width, height = text_box.height-1)

    def error_message(self, one, two, three):
        self.element_str.set(self.orig_string)
        #global Error_Window
        if  text_box.error_box_already_exists == False:
            text_box.error_box_already_exists = True
            # Error_Window = TopLevelWindow.top_window(root=rootcopy, width=400, height=200, title="ERROR", color = 'grey')
            # error_message = tk.Label(Error_Window.toplevel, text = "Editing Data is only possible in 'Custom Edit' mode",
            #                         bg = 'grey',
            #                         fg = 'white')
            # error_message.place(relx = 0.5, rely = 0.5, anchor  ='center')
            global EW
            EW = TopLevelWindow.show_error_window(root=Full_DF_Wind.toplevel, fontstyle=text_box.fontstyle, message="Editing Data is only possible in 'Custom Edit' mode", width = 400)
            EW.toplevel.protocol("WM_DELETE_WINDOW", on_closing)
def on_closing():
    text_box.error_box_already_exists = False
    EW.toplevel.destroy()

def mouse_move(val):
    scroll.set(scroll.get() - val.delta)
    update_scroll(66)

def update_scroll(yo):
    val = scroll.get()
    num_boxes = 120
    canv.place_configure(
        y = (-canv_length+Full_DF_Wind.height - buffer)/(scroll_bar_to_) * int(val)
        )
    if int(val) != 0:
        if int(val) <= scroll_bar_to_ - num_boxes:
            for box in text_box.list_of_boxes[int(val)-1:int(val)-1+num_boxes]:
                box.place_self() 
        else:
            for box in text_box.list_of_boxes[int(val)-1:-2]:
                box.place_self() 
        if int(val) >= num_boxes:
            for box in text_box.list_of_boxes[int(val)-num_boxes:int(val)]:
                box.place_self() 
        else:
            for box in text_box.list_of_boxes[0:int(val)]:
                box.place_self() 
    else:
        for box in text_box.list_of_boxes[0:num_boxes]:
                box.place_self() 

    if int(val)> num_boxes:
        for box in text_box.list_of_boxes[0:int(val)-num_boxes]:
            box.label.place_forget() 
    if int(val)< scroll_bar_to_ - num_boxes:
        for box in text_box.list_of_boxes[int(val)+num_boxes: -1]:
            box.label.place_forget() 

   
def create_full_df_toplevel(root, imagename, df, df_meta, fontstyle, view_or_edit = 'edit'):
    global buffer
    if view_or_edit == "edit":
        buffer = 50
    else:
        buffer = 0
    global rootcopy
    rootcopy= root
    global dataframe
    dataframe = df

    #create window
    global image_name
    image_name = imagename
    title = "Full Data Frame: " + image_name
    window_width = 1200
    window_height = 500
    global Full_DF_Wind
    Full_DF_Wind = TopLevelWindow.top_window(root = root, width = window_width, height=window_height + buffer, title = title)
    Full_DF_Wind.toplevel.bind('<MouseWheel>', mouse_move)

    #create scrollbar
    global scroll
    scroll = tk.IntVar()
    scroll.set(0)
    scrollbar = tk.Scale(Full_DF_Wind.toplevel, orient = 'vertical', bg ='black', command = update_scroll, from_ = 0,variable = scroll)
    scrollbar.pack(side = tk.RIGHT, fill = tk.Y)

    #create canvas
    global canv
    canv_width = Full_DF_Wind.width - 22
    canv = tk.Canvas(Full_DF_Wind.toplevel, bg = 'white', width = Full_DF_Wind.width - 22, height = Full_DF_Wind.height)
    canv.place(x = 0, y = 0, anchor = 'nw')

    #clear text box list
    text_box.list_of_boxes.clear()
    text_box.regular_boxes.clear()
    text_box.meta_boxes.clear()
   #populate df_meta entries
    for index, dataelement in enumerate(df_meta):
        #tag
        newTB = text_box(toplevel = canv, fontstyle=fontstyle, index=index, dataelement=dataelement, xpos=0, width=canv_width/8, attrib = 'tag',
                box_to_add_to = 'meta', view_or_edit = view_or_edit)
        print(dataelement.tag, type(dataelement.tag))
        #keyword
        newTB2 = text_box(toplevel = canv, fontstyle=fontstyle, index=index, dataelement=dataelement, xpos=canv_width/8+1, width=canv_width/8, attrib = 'keyword',
                box_to_add_to = 'meta', view_or_edit = view_or_edit)
        print(dataelement.tag, type(dataelement.tag))
        #value
 
        newTB3 = text_box(toplevel = canv, fontstyle=fontstyle, index=index, dataelement=dataelement, xpos=2*canv_width/8+1, width=5*canv_width/8, attrib = 'value',
                box_to_add_to = 'meta', view_or_edit = view_or_edit)
        print(dataelement.tag, type(dataelement.tag))

        #VR
        newTB4 = text_box(toplevel = canv, fontstyle=fontstyle, index=index, dataelement=dataelement, xpos=7*canv_width/8+2, width=canv_width/8+2, attrib = 'VR',
                box_to_add_to = 'meta', view_or_edit = view_or_edit)
        print(dataelement.tag, type(dataelement.tag))
    global current_length
    current_length = len(df_meta)

    #populate df entries
    for index, dataelement in enumerate(df):
        print(dataelement, type(dataelement))
        #tag
        newTB = text_box(toplevel = canv, fontstyle=fontstyle, index=index+current_length, dataelement=dataelement, xpos=0, width=canv_width/8, attrib = 'tag',
                box_to_add_to = 'regular', view_or_edit = view_or_edit)
        print(dataelement.tag, type(dataelement.tag))

        #keyword
        newTB2 = text_box(toplevel = canv, fontstyle=fontstyle, index=index+current_length, dataelement=dataelement, xpos=canv_width/8+1, width=canv_width/8, attrib = 'keyword',
                box_to_add_to = 'regular', view_or_edit = view_or_edit)
        print(dataelement.tag, type(dataelement.tag))
        
        #value

        newTB3 = text_box(toplevel = canv, fontstyle=fontstyle, index=index+current_length, dataelement=dataelement, xpos=2*canv_width/8+1, width=5*canv_width/8, attrib = 'value',
                box_to_add_to = 'regular', view_or_edit = view_or_edit)
        print(dataelement.tag, type(dataelement.tag))


        #VR
        newTB4 = text_box(toplevel = canv, fontstyle=fontstyle, index=index+current_length, dataelement=dataelement, xpos=7*canv_width/8+2, width=canv_width/8+2, attrib = 'VR',
                box_to_add_to = 'regular', view_or_edit = view_or_edit)
        print(dataelement.tag, type(dataelement.tag))
    

    if view_or_edit == 'edit':
        #Save or revert canvas  
        save_or_revert_canv = tk.Canvas(Full_DF_Wind.toplevel, bg = 'grey', bd = 0, highlightthickness=0)
        save_or_revert_canv.place(x = 0, y = Full_DF_Wind.height - buffer, width = Full_DF_Wind.width - 18, height = buffer, anchor = 'nw')
        #save button
        global save_button
        save_button = tk.Button(save_or_revert_canv, text = "Save Changes", bg = 'black', fg = 'black', 
                                state = tk.DISABLED, command  = produce_just_one_or_all_files_window)
        save_button.place(relx = 0.25, rely = 0.5, relwidth = 0.3, relheight = 0.5, anchor = 'center')
        #revert button
        global revert_button
        revert_button = tk.Button(save_or_revert_canv, text = "Revert Back to Original", bg = 'black', fg = 'black', 
                                state = tk.DISABLED, command= revert)
        revert_button.place(relx = 0.75, rely = 0.5, relwidth = 0.3, relheight = 0.5, anchor = 'center')

        #create objects for final save changes window
        global just_one_or_all_files
        just_one_or_all_files = TopLevelWindow.top_window(rootcopy, width = 400, height=100, title = "Save Changes", color = 'grey')
        just_one_or_all_files.toplevel.withdraw()

        global option
        option = tk.StringVar()

        global just_one
        just_one = tk.Radiobutton(just_one_or_all_files.toplevel, text = 'Just for ' + image_name, variable = option, value = "Just One",
        bg = 'grey', fg = 'black', font = text_box.fontstyle)
        just_one.select()

        global all
        all = tk.Radiobutton(just_one_or_all_files.toplevel, text = 'All Files', variable = option, value = "All", 
        bg = 'grey', fg = 'black', font = text_box.fontstyle)
        
        global final_save_changes
        final_save_changes = tk.Button(just_one_or_all_files.toplevel, text = "Save Changes", bg = 'black', fg = 'black')

    #configure scroll bar to and from
    global scroll_bar_to_
    scroll_bar_to_ = len(text_box.list_of_boxes)
    scrollbar.config(to = scroll_bar_to_)
    scrollbar.config(from_ = 0)

    #configure canvas length
    global canv_length
    canv_length = text_box.height * (len(df) + len(df_meta))
    canv.place_configure(height = canv_length)
    update_scroll(1)



def revert():
    for box in text_box.list_of_boxes:
        box.element_str.set(box.orig_string)
def produce_just_one_or_all_files_window():
    just_one_or_all_files.toplevel.deiconify()
    just_one.place(relx = 0.33, rely = 0.33, anchor = 'center')
    all.place(relx = 0.75, rely = 0.33, anchor = 'center')
    final_save_changes.place(relx = 0.5, rely = 0.66, relwidth = 0.4, relheight = 0.3, anchor = 'center')

def save_changes_regular(input_df):
    
    for index, box in enumerate(text_box.regular_boxes):
        if box.orig_string != box.element_str.get():
            hex_key = list(input_df.keys())[box.index - current_length]
            # if box.attrib  =="tag":
            #     input_df[hex_key].tag = box.element_str.get()
            if box.attrib  =="keyword":
                input_df[hex_key].keyword = box.element_str.get()
            elif box.attrib  =="value":
                input_df[hex_key].value = str(box.element_str.get())
            elif box.attrib  =="VR":
                input_df[hex_key].VR = box.element_str.get()  
                
    return input_df
def save_changes_meta(input_df):
    
    for index, box in enumerate(text_box.meta_boxes):
        if box.orig_string != box.element_str.get():
            hex_key = list(input_df.keys())[box.index]
            # if box.attrib  =="tag":
            #     input_df[hex_key].tag = box.element_str.get()
            if box.attrib  =="keyword":
                input_df[hex_key].keyword = box.element_str.get()
            elif box.attrib  =="value":
                input_df[hex_key].value = str(box.element_str.get())
            elif box.attrib  =="VR":
                input_df[hex_key].VR = box.element_str.get()  
                
    return input_df