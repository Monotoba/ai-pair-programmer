# AI Pair Programmer User Guide


## Overview
AI Pair Programmer was developed as an applet that is run as 
a standalone tool. The module is backed by ChatGPT and allows 
the user to query ChatGPT for help and code suggestions.

The main window provides a simple text input for queries, a text 
window for response display, and a crude, but workable history 
mechanism. The user may use the prev and next buttons to view 
previous responses from ChatGPT. 

## Running The Software
Download, Copy, Install, or Git the software on your machine. If 
compressed, expand the project in a suitable location on your 
filesystem. cd into the root project folder and run: 
 > python main.py

If you wish to alter the software use git to clone the project from
the github repository:

 > git clone https://github.com/Monotoba/ai-pair-programmer.git

Then installed the project dependencies:

 > python -m pip install -r requirements.txt

You will find the code for this project in the aipairprogrammer module.


## Configuration
As stated above, AI Pair Programmer is a standalone tool. As standalone 
tool, simply cd into the directory containing main.py and run: 

 ~> python3 main.py

Once the window opens, click on the 'Config' button in the bottom-right
corner of the window. This will open a small dialog box asking for an 
API Key. You can obtain a ChatGPT API key from OpenAI at: 

http://openai.com/signup

Once you are signed up generate your API key and copy it from the OpenAI 
website. Then paste it into the Config dialog. Next click 'Ok'. This will
save your API key in the application settings.

You can select various AI Models from the 'model' dropdown. The currently 
selected model will be saved to the application settings and will be 
automatically selected the next time you open the application.

## Usage
When AI Pair Programmer makes a request and gets a response from ChatGPT,
the query, date and time, as well as the response are saved in a history 
file. This history is loaded the next time you open the application. You 
can use the 'Prev' and 'Next' buttons above the 'Response' window to 
scroll through back and forth, through previous responses. The crude 
history mechanism does not support sessions at the moment. So, all 
responses are kept in chronological order.

A 'Clear' button at the bottom-center of the main window allows for 
clearing all text in the 'query' and 'Response' windows.

## Motivation
The motivation for this project was all the hype around ChatGPT lately, 
and the fact that I too found myself constantly asking question about 
my coding, or libraries and tools I was only vaguely failure with. I
quickly found ChatGPT to be a useful tool for a solo developer looking 
for additional input and perspectives on projects. While this is a 
very simple project, I hope ever solo developer finds it useful and 
engaging.

## Code Structure
The code in AI Pair Programmer is very simple and straight forward. 
Almost all the code is in the appairprogrammer module. The bulk of the 
code there is in ai_pair_programmer.py file. This file contains most
of the GUI code. The only exception being a custom dialog box contained 
in the qt_custom_dialog.py file. This is included because the standard 
PyQT5 dialog does not seem to support loading text in to the lineEdit
contained within the dialog. It has a method for setting the text but 
when called no action occurs. I didn't want to waste too much time on
this issue since it was quicker for me to just create a new custom 
dialog with the features I needed. If you know how to do this with the 
PyQT5 QInputDialog, please let me know.

All the settings storage and retrieval methods are handled by the code
in the ai_pair_programmer_settings.py file. This code uses the Python
ConfigParser module to handle settings management.


## Going Further
- I can see some areas this project can be improved. First, the history
feature needs to be reworked to allow the creation of 'sessions'. A 
session in this context is single subject of conversation over short 
period of time, perhaps a few minutes, hours, or a few days, similar 
to how ChatGPT handles history.
- It would also be nice to support multiple providers and their multiple
AI models. 
- Support for various color schemes and visual themes could be added.
I suffer from Chronic migraines and having a dark theme allows me to
work for longer periods of time. Other accessibility features could be
added as well.
- The settings for the applet leave the user's API key stored in the
settings.ini file in plain text. If security is an issue, using one of 
the many encryption methods is suggested. 


Happy Coding!
- Randall Morgan
