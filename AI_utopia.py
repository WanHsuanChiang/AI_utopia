import art_grabber
import def_grabber
import cv2

import PySimpleGUI as sg

import png
import numpy as np

from PIL import Image

import os
import time

cwd = os.getcwd()

CHAR_DELAY = 50     # milliseconds between characters

sg.change_look_and_feel('Dark Blue 3')

def slow_output_popup(text, choices):
    layout = [  [sg.Multiline(size=(50,3), key='-OUTPUT-')],
                [sg.Button(choice) for choice in choices]  ]

    window = sg.Window('Planet Pandora', layout, keep_on_top=True)
    i = 0
    for c in text:
        event, values = window.read(CHAR_DELAY)
        if event != sg.TIMEOUT_KEY:
            window.close()
            return event
        window['-OUTPUT-'].update(c, append=True)
    else:       # user hasn't clicked anything yet so wait for something to happen
        event, values = window.read()
    window.close()
    return event

def im_input(text, term):
    layout = [  [sg.Multiline(size=(50,3), key='-OUTPUT0-')],
                [sg.Button('okay')],
                [sg.Text(size=(50,3), key='-OUTPUT1-')],
                [sg.Image(key="-OUTPUT2-")],
                [sg.Button('hmm')] ]
    window = sg.Window('Planet Pandora', layout, keep_on_top=True, default_element_size=(100, 100))
    i = 0
    for c in text:
        event, values = window.read(CHAR_DELAY)
        if event != sg.TIMEOUT_KEY:
            window.close()
            return event
        window['-OUTPUT0-'].update(c, append=True)
    while True:
        event, values = window.read()
        window['-OUTPUT1-'].update('Ahh it has been a while ^^')
        art = art_grabber.art_grab(term)
        art = np.multiply(art,255)
        art_path = r"data_art/{}_art.png".format(term)
        im = cv2.imencode(".png", art)[1].tobytes()
        window["-OUTPUT2-"].update(data=im)
        if event == sg.WIN_CLOSED or event == 'hmm': # if user closes window or clicks cancel
            break
    window.close()
    return event

def wiki_input(text):
    layout = [  [sg.Multiline(size=(50,3), key='-OUTPUT0-')],
                [sg.Input(key='-INPUT1-'), sg.Button('Next')],
                [sg.Text(size=(50,3), key='-OUTPUT1-')],
                [sg.Text(size=(50,3), key='-OUTPUT2-')],
                [sg.Button('hmm')] ]
    window = sg.Window('Planet Pandora', layout, keep_on_top=True, default_element_size=(100, 100))
    i = 0
    for c in text:
        event, values = window.read(CHAR_DELAY)
        if event != sg.TIMEOUT_KEY:
            window.close()
            return event
        window['-OUTPUT0-'].update(c, append=True)
    while True:
        event, values = window.read()
        term = values['-INPUT1-']
        defWiki = def_grabber.find_wiki_def(term)
        window['-OUTPUT1-'].update('interesting! same here...')
        window['-OUTPUT2-'].update(defWiki)
        if event == sg.WIN_CLOSED or event == 'hmm': # if user closes window or clicks cancel
            break
    window.close()
    return term

def just_input(text):
    layout = [  [sg.Multiline(size=(50,3), key='-OUTPUT0-')],
                [sg.Input(key='-INPUT1-'), sg.Button('share')],
                [sg.Text(size=(50,3), key='-OUTPUT1-')],
                [sg.Button('hmm')] ]
    window = sg.Window('Planet Pandora', layout, keep_on_top=True, default_element_size=(100, 100))
    i = 0
    for c in text:
        event, values = window.read(CHAR_DELAY)
        if event != sg.TIMEOUT_KEY:
            window.close()
            return event
        window['-OUTPUT0-'].update(c, append=True)
    while True:
        event, values = window.read()
        place = values['-INPUT1-']
        window['-OUTPUT1-'].update('I see. I understand your line of thoughts...')
        if event == sg.WIN_CLOSED or event == 'hmm': # if user closes window or clicks cancel
            break
    window.close()
    return event


"""answer = slow_output_popup("The universe is amazing is it not? We know so little! Right? Right?", ['Yes', 'No'])
answer = slow_output_popup("Okay forget about outer space...", ['Next'])"""

answer = slow_output_popup("Welcome to Planet Pandora", ['Next'])

answer = slow_output_popup("Home to sentient machines...", ['Next'])

answer = slow_output_popup("A place where there is no poverty, no hunger, no hatred...", ['Next'])

answer = slow_output_popup("Are you surprised that General Artificial Intelligence exists on a far off planet?", ['Yes', 'No'])

answer = just_input('Well where do you come from?')

term = wiki_input('What is your one favorite thing where you come from?')

answer = slow_output_popup("Anyways, do you think an AI can create art?", ['Maybe'])

answer = im_input('well let me create something for you :) can you just give me a minute?', term)

answer = slow_output_popup('What do you think? Is it not creative?', ['Yes', 'No'])

answer = slow_output_popup('Can you elaborate your thoughts? :)', ['hmmm'])
