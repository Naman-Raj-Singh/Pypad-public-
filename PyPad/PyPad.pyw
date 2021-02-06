#import pyximport;pyximport.install()
import PySimpleGUI as sg #pip install pysimplegui
import pathlib # pip install pathlib
import datetime
import time
import PyPDF2 #pip install PyPDF2
import docx2txt # pip install docx2txt

WIN_W = 45
WIN_H = 18
file = None
icon = "Icon.ico"


try:
    Fs = open("Text Size.txt", "r")
    FontSize = Fs.read()
    Th = open("Theme", "r")
    Theme = Th.read()
    As = open("Auto Save", "r")
    global Auto
    Auto = As.read()
    FontStyle_file= open("Font Style.txt","r")
    FontStyle= FontStyle_file.read()#Fretching Font Size, Theme and Font Style
    FontStyle_file = open("Font Style.txt", "r")
    FontStyle= FontStyle_file.read()
    if FontSize == "":
        FontSize= 12
    if Theme == "":
        Theme = "Black"
    
except:
    FontSize_file = open("PyPad\\Text Size.txt", "w+")
    FontSize_file.write("15\n")
    FontStyle_file = open("PyPad\\ Font Style.txt", "w+")
    FontStyle_file.write("Consolas\n")
    Theme_file = open("PyPad\\Theme.txt", "w+")
    Theme_file.write("Black\n")
    FontStyle_file= open("Font Style.txt","w+")
    FontStyle= FontStyle_file.read()
    FontStyle_file.close()
    FontSize_file.close()
    FontStyle_file.close()
    Theme_file.close()
    Fs = open("PyPad\\Text Size.txt", "r")
    FontSize = Fs.read()
    Th = open("PyPad\\Theme", "r")
    Theme = Th.read()
    FontStyle_file= open("Font Style.txt","r")
    FontStyle= FontStyle_file.read()# if file has been deleted creating files and reading it

menu_layout = [['File ', ['New (Ctrl+N)','---', 'Open (Ctrl+O)', 'Save (Ctrl+S)', 'Save As', '---','---', 'Exit']],
              ['View ', ['Window',['Minimize','Maximize','Restore','Exit'],'Status bar',['View','Hide'],'---','Time','Date','---']],
              ['Tools ', ['Word Count', 'Typing speed',['Start','Stop',],'---','Extract Word File','Extract PDF','---','Explore']],
              ['Theme ', ['Current theme: ' + Theme ,'---']],
              ['Settings',['Settings']],
              ['Help ', ['About']]]# The menu bar of PyPad

sg.theme(Theme)# Declaring the theme

layout = [[sg.Menu(menu_layout)],
          [sg.Text(' New file ', font=('Consolas', 15), size=(WIN_W, 1), key='_INFO_'),sg.Text("                                ",font=('Consolas', 12),justification='R',key="SaveCon")],
          [sg.Multiline(font=(FontStyle,FontSize ), size=(WIN_W, WIN_H),auto_refresh=True,autoscroll=True, key='_BODY_')],
          [sg.StatusBar("                                                                                                                                    ", font=('Consolas', 12),key="SB")]]# Setting the layout 
window = sg.Window('PyPad', layout=layout, margins=(0, 0), resizable=True, return_keyboard_events=True, finalize=True,icon=icon)

# Creatin the window^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
window['_BODY_'].expand(expand_x=True, expand_y=True)

# Making window resizable ^^^^^^^^^^^^^^^^^^^^^^^^^^^
def save_file(file):
    '''Save file instantly if already open; otherwise use `save-as` popup'''
    try:
        
        current_text=values.get('_BODY_')
        with open(filename, 'r') as file,open(filename ,'w+')as edit:
            filedata = file.read()
            edit.write(filedata.replace( filedata, current_text ))
    except:
        window['SaveCon'].Update("Text File = '.txt' extension")
        save_file_as()
        window['SaveCon'].Update(" ") # Saving The file

def save_file_as():
    '''Save new file or save existing file with another name'''
    window['SaveCon'].Update("Text File = '.txt' extension")
    global filename
    filename = sg.popup_get_file('Save As', save_as=True, no_window=True,file_types=(("Text file","*.txt*"),("All type","*.*")),icon=icon)
    if filename:
        file = pathlib.Path(filename)
        file.write_text(values.get('_BODY_'))
        window['_INFO_'].update(value=file.absolute())
        window['SaveCon'].Update(" ")
        return file # Making file saveas

while True:
    event, values = window.read()
    current_time = time.strftime("%H:%M")

    if event in ('Exit', None,sg.WIN_CLOSED):
        break

    if event in ('New (Ctrl+N)', 'n:78', 'N:78'):
        '''Reset body and info bar, and clear filename variable'''
        window['_BODY_'].update(value='')
        window['_INFO_'].update(value=' New File ')
        window['SaveCon'].Update('')

    if event in ('Open (Ctrl+O)', 'o:79', 'O:79'):
        try:
            global filename
            filename = sg.popup_get_file('Open',icon=icon, no_window=True,file_types=(("Text file","*.txt*"),("HTML","*.html*, *.htm*"),("All type","*.*")))
            if filename:
                file = pathlib.Path(filename)
                window['_BODY_'].update(value=file.read_text())
                window['_INFO_'].update(filename)
                window['SaveCon'].Update('')  
        except:
            window['SaveCon'].Update('Sorry the file is not supported')

    if event in ('Save (Ctrl+S)', 's:83', 'S:83'):
        save_file(file)

    if event == 'Save As':
        file = save_file_as() 

    if event == 'Word Count':
        words = [w for w in values['_BODY_'].split(' ') if w!='\n']
        word_count = len(words)
        sg.popup_no_wait('Word Count: {:,d}'.format(word_count),no_titlebar=True) # counting the words
        
    if event == 'Minimize':
        window.Minimize()

    if event == 'Maximize':
        window.Maximize()

    if event =='Restore':
        window.Normal()

    if event == 'About':
        sg.popup_no_wait('This python progect is created by NAMAN RAJ SINGH')

    if event == 'Settings':
        import os
        setting_path = "Setting.pyw"
        os.startfile(setting_path)

    if event == 'Extract Word File':
        Word_FILE= sg.popup_get_file("Get a Word file to Extract the text",no_titlebar=True,file_types=(("Word file"," *.docx*, *.doc*"),("All files","*.*")))
        window['_INFO_'].update(Word_FILE)
        text = docx2txt.process(Word_FILE)
        window['_BODY_'].update(text)# extracting and word file

    if event == "Extract PDF":
        PDF_FILE= sg.popup_get_file("Get a PDF file to Extract the text\nNOTE: Only text will be extracted imaged will not been extracted",no_titlebar=True,file_types=(("PDF File","*.pdf*"),("All files","*.*")))
        window['_INFO_'].update(PDF_FILE)
        pdfFileObj = open(PDF_FILE, 'rb')
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
        for i in range(pdfReader.getNumPages()):
            page= pdfReader.getPage(i)
            pagecontent= page.extractText()
            window['_BODY_'].update(str(pagecontent))# Extracting a word file
    
    if event == 'Time':
        sg.popup_no_buttons("Time is " + current_time,font= 'Any 15', no_titlebar= True, auto_close=True, auto_close_duration= 5 )
    
        if event == 'Date':
            dt = datetime.datetime.today()
            month= dt.strftime("%A %d %B")
            sg.popup_no_buttons("Today is "+ month + str(dt.year), font= 'Any 15', no_titlebar= True, auto_close=True, auto_close_duration= 5) # Displaying the time 

    if event == 'View':# Viewing Status bar
        window['SB'].Update(visible=True)
    
    elif event == 'Hide':# Hiding Status bar
        window['SB'].Update(visible=False)
    
    if Auto == 'save_file(file)':
        while True:
            save_file(file)
    if Auto == "  ":
        pass

    window['SB'].update("Events: " + event +"                                                                                        Time : "+current_time )
    # status bar responding ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
