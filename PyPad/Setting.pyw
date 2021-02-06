import pyximport;pyximport.install()
import PySimpleGUI as sg
import webbrowser
from tkinter import *


image = "Settings.png"
png_ico = "Icon.png"
icon = "Icon.ico"
back_button = "Back.png"

 


def settings():
    As = open("Auto Save", "r")    
    Auto = As.read()
    if Auto == "save_file(file)":
        Naman = True
    else:
        Naman = False

    layout = [ 
            [sg.Image(image)],
             [sg.Image(png_ico,enable_events=True,key='Icon_click')],
            [sg.Button("Font",size=(8,1)),sg.Button("Theme",size=(8,1)),sg.Checkbox("Auto save",size=(8,1),default=Naman,enable_events=True,auto_size_text=True,key='Auto_Save')],
            [sg.Exit("Exit",button_color=('white', 'firebrick'),size=(30,1),tooltip="Double tap")]]
    global window          
    window = sg.Window('SETTINGS', layout=layout,no_titlebar=False,grab_anywhere=True,finalize=True,auto_size_buttons=True,icon=icon)
    
    while True:
        
        event, values = window.read()
        if event in ('Exit', None,sg.WIN_CLOSED):
            break
        if event == "Icon_click":
            pass
        if event == 'Font':
            font()
        if event == 'Theme' :
            Theme()
        if event == 'Auto_Save':
            if Naman == True:
                with open("Auto Save", "w+") as As:
                    As.write(Auto.replace(Auto," "))
                    window["Auto_Save"].update(text="AutoSave \n OFF")
            if Naman == False:
                with open("Auto Save", "w+") as As:
                    As.write(Auto.replace(Auto,"save_file(file)"))
                    window["Auto_Save"].update(text="AutoSave \n ON")

  
def font():
    window.hide()
    global font_size_file
    font_size_file = "Text Size.txt" 
    File = open(font_size_file,"r")
    current_font_size = str(File.read())
    Font_Size_List = list(range(1,400))
    Font_Style_File = "Font Style.txt"
    current_Font = open(Font_Style_File,"r")
    current_Font_Style = current_Font.read()
    from tkinter import font
    fonts=font.families()
    font_layout = [[sg.Text("Font size",font=("Helvetica",13)),sg.Text("       Font style",font=("Helvetica",13))],
                        [sg.Input(size=(8,1),key="new_fs"),sg.Listbox(fonts,size=(20,15),default_values=current_Font_Style,enable_events=True,key="FontStyle")],
                        [sg.Text("")],
                        [sg.Text("Font ",font=("Helvetica",13))],
                        [sg.Button("Apply", button_color=('white', '#007339'),size=(27,1))]]
    font_window = sg.Window('SETTINGS', layout=font_layout,no_titlebar=True,grab_anywhere=False,finalize=True)
    while True:
        event,values = font_window.read()
        if event in ('Apply', None):
            new_font_style = str(values["FontStyle"][0])
            new_font_size = values["new_fs"]
            with open(font_size_file ,'w+')as edit, open(Font_Style_File,"w+")as EditForFS:
                edit.write(current_font_size.replace(current_font_size, new_font_size ))
                EditForFS.write(current_Font_Style.replace(current_Font_Style, new_font_style))
                EditForFS.close()
                edit.close()
                current_Font.close()
                File.close()
                font_window.close()
                return settings()

def Theme():
    window.hide()
    global font_size_file
    theme_file = "Theme"
    with open(theme_file,'r') as File:
        global current_theme
        current_theme = File.read()
        theme_layout = [
                        [sg.Image(back_button,tooltip="Back",enable_events=True,key="-Back-"),sg.Text("Themes setting",font=("Helvetica",18))],
                        [sg.Text("Choose a theme",font=("Helvetica",12))],
                        [sg.Listbox(values=sg.theme_list(), size=(40, 12),default_values=current_theme, key='-LIST-', enable_events=True)],
                        [sg.Button("View",size=(13,1))],
                        [sg.Button("Apply", button_color=('white', '#007339'),size=(27,1))]]
        theme_window = sg.Window('SETTINGS', layout=theme_layout,no_titlebar=True,grab_anywhere=False,finalize=True,auto_size_buttons=True)
        while True:
            event,values = theme_window.read()
            global new_theme
            new_theme = sg.theme(values['-LIST-'][0])

            if event in ('Apply'):
                new_font_size= values.get(values['-LIST-'][0])
                with open(theme_file ,'w+')as edit:
                        edit.write(current_theme.replace(current_theme, new_theme ))
                        theme_window.close()
                        return settings()
            
            if event == "View":
                sg.theme(new_theme)
                theme_window.close()
                return settings()
            if event == "-Back-":
                theme_window.close()
                return settings()

if __name__ == "__main__":
    settings()

