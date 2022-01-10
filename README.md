# SPTT (SPEECH TO TEXT) 

  

### Video Demo:  <https://youtu.be/qpbrwMxOnfs> 

  

### Description: 

  

#### Name of project: SPTT (SPEECH TO TEXT) 

#### Language: Python

### How to use:
Sign up from the main window to create your account.
After creating your account or if you already have an account, login from the main window using the username and password you provided during signing up.
Once you click submit on the login page, you will be directed to your main page.
The SPTT console is there to help you!
Enter the no. of seconds you want to record in the field provided below the console and use RECORD button to record your voice.
Use the RECOGNIZE button to recognize the text.
Remember to speak clearly and slowly for the best results.
Use the SAVE button to save your work.
Remember to alwyas save your work.
Your saved work will be present each time you open your main page.
Use the editor to edit your work.
WORK ON! :D

- FUNDAMENTALS
  
  - GENERAL OVERVIEW OF ALL OBJECTS: 

    - The interface is so designed that a user, upon opening the app, would be greeted at the frame, internally defined as homepage. From there they have the option to quit, login or signup. 
    - Clicking login will take them to the frame, internally defined as loginpage. 
    - Clicking signup will take them to the frame, internally defined as signuppage. 
    - Clicking exit will quit the app. 
    - The loginpage has fields to enter login credentials (username and password) and a submit button. 
    - The signuppage has fields to enter signup credentials (name, username and password and confirm password) for signing up a new user and a submit button. 
    - The main page can be accessed through the login frame. 
    - The main page has one entry field for inputting text from the user and acts as a text editor, a console for aiding the user and keeping them updated on the progress of the app and a small entry window for user input (internally represented as seconds). It has a back button, a save button, a record button and a recognize button.
  
  - FOLDERS AND UTILITY: 
      - The app is housed in a folder called SPTT. And the folder contains the .py file (SPTT.py), that contains the code for the working of the app; a users folder, that keeps track of all the signed up users; a assets folder, that contains pictures required for the code to work; and this readme file. 

Since their inception, computers have revolutionized human society. Their advent 
has fueled changes and improvements in life and helped us achieve things that 
were previously unthinkable. CS requires logical thinking along non-conventional 
routes and non-linear problem-solving abilities. 

I wanted to create something new, something different, something that would 
challenge me – hence, I decided to develop an app to convert speech to text 
efficiently. In the fast-paced and ever developing world, people do not have time 
to type out large documents. This app would aid them, by using speech 
recognition and type out these documents. I had never worked on such a large 
project before, especially such a complex one. I didn’t know most of the 
intricacies required to accomplish it to fruition, and that's what made it all the 
more attractive to me. Considering that I was working alone, I had to put in added 
effort, and I had to work upon every aspect of the app myself. 

I started reading up resources to help me complete the project. Firstly, I needed 
to create the GUI. Tkinter was the most popular and accessible option, so I studied its functionalities and read up online resources for it. I also used the 
FIGMA app to help with the technical part of the design (placing the widgets and 
deriving the hexadecimal values for colors). It helped me understand how the app 
would look. 

The next step was deciding upon the method for speech recognition. I decided to 
use Google. In the code, I have first imported all the required libraries. I have 
dedicated a variable called USERNAME to store the username of the person 
logging in. For the app to work, obviously, each different user account needed to 
have different mainframes as per their files. But initially I had not accounted for it. 
I have used a list for the purpose because of its mutability. This made it possible 
to update the login username every time a new login happened, from within the 
check login function, even though the scope becomes limited for a variable 
updated inside a function. 

This went through three main development stages. Initially, I had developed each 
frame independently so that I could test that they were working properly, and I 
could add new functionality and test them. Then I had made a draft for the 
finished work and finally the main thing has been completed. I wanted my 
buttons to have a hover effect (color change upon hover), but Tkinter didn’t have 
any direct method to do so, so I defined functions for it. 

Some buttons required different function for hover because the colors are 
different on them. I had initially tried to loop over a list of all buttons and then 
with if-else statements assigned the colors within one single function, but it didn’t 
work. I couldn’t understand why. So, I had to define a function, every time I 
wanted a different set of colors. Then I defined the login check function which is 
executed on a button click on the login frame. For storage purposes I have used a 
database using MySQL (SPTT1) and a table (userdata). 

For incorrect entries I’ve created an empty label, which is updated with new text 
as per user actions. The login function also calls other functions to set up the 
mainframe. 

I have used break statements in a multitude of places to ensure that, even after 
failing a check condition, the code was not executed to full completion. 
Then I wrote the real working code using the defined functions and bound each 
function to the required buttons. During my second development cycle, another 
problem I faced was that every time I backed from a frame, all the images I had 
used for the frame disappeared. Tkinter was automatically deleting them to 
prevent memory loss. So, I had to add a reference to the image, so that this 
doesn’t happen.

 Finally, after so much hard-work and toil, I was presented with the fully 
functional app, and the joy that rushed over me was indescribable. The 
experience taught me many things: how to deal with problems, finding solutions, 
and innovating on your feet. It enhanced my coding skills, my intellectual 
capabilities, my capability to research and work for efficient solutions, and my 
determination and hard work to accomplish my self-started projects to fruition. 
Most importantly, it gave me the confidence and inspiration to work harder and 
learn more advanced concepts. 
