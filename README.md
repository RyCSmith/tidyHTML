tidyHTML
========

Design: This concept was created as an assignment by Professor Dave Matuszek at the University of Pennsylvania. All implementation details and code developed by Ryan Smith and Theresa Breiner.

Overview: Formats an unorganized HTML file into a correct and more visually-appealing layout.

Use: This file does not have a GUI. It can be run from the command line by navigating to the containing folder and running python tidyHTML.py. 

Other Info: The program and unit tests are written in Python. 
-The program will make two temporary files that will only exist during execution; a file with a randomly generated integer name and postcut.html. These will be deleted before execution concludes. 
-The program will preserve the original file submitted for editing in the same folder from which it was selected with the .bak extension.
-The reformatted file will overwrite the file submitted for editing.