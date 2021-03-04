## The purpose of this project is as follows:
This project, which is a work in progress, automates data entry, correction, deletion, and other actions in CUNYfirst (a peoplesoft product).
## Here's some back story on why I needed to build this:
CUNYfirst data entry, auditing, and maintenance is laborious, boring, time-consuming and necessary. Automating it is a way to free up time not only for myself and people on my team but potentially for other campuses that are in a similar position. 
This project leverages pandas, fuzzywuzzy, selenium, webdriver_manager, xlrd.
##In order to use this, you'll first need do the following:
If you are preparing to use this script, do not. Most of the functions have not yet been revised to be fully functional and may result in data damage or errors. As of this writing, the most up to date (and fully functional) portion of this is the deletion_new method for the jobpages class. Please, please, please do not attempt to use any of this so long as this readme includes this paragraph.
The expected frequency for running this code is As Needed.