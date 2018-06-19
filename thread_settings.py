from fbmq import Template
from app import page
# Greeting text
page.greeting("Welcome to Find Me Bot! My Mission is help you to easy find the pitch. :)")

page.show_starting_button("START")

@page.callback(['START'])
def start_callback(payload, event):
    print("Let's start!")

page.show_persistent_menu([Template.ButtonPostBack('Find Pitch', 'FIND_PITCH'),
                           Template.ButtonPostBack('Reminder', 'REMINDER'),
                           Template.ButtonPostBack('Help', 'HELP')])

@page.callback(['FIND_PITCH'])
def click_persistent_menu_find_pitch(payload, event):
    sender_id = event.sender_id
    page.send(sender_id, "you clicked %s menu" % payload)
    print("you clicked %s menu" % payload)

@page.callback(['REMINDER'])
def click_persistent_menu_reminder(payload, event):
    sender_id = event.sender_id
    page.send(sender_id, "you clicked %s menu" % payload)
    print("you clicked %s menu" % payload)

@page.callback(['HELP'])
def click_persistent_menu_help(payload, event):
    sender_id = event.sender_id
    page.send(sender_id, "you clicked %s menu" % payload)
    print("you clicked %s menu" % payload)