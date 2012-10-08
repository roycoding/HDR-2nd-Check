# hdrcheckgui.py

# GUI for hdrcheck.py.
# Should allow you to select data file, input target x,y,z and expected dose,
#    execute calculation, return results, and optionally save report to PDF.

# Started 17 July 2012
# Roy Keyes (roy.coding@gmail.com)

import easygui as eg
import sys
import hdrcheck
import result2pdf

    
# Enter target dose and coordinates.
msg         = "Welcome to HDR 2nd Check\nEnter target x,y,z (cm) and expected dose (Gy)\nChoose 'OK' to select data file."
title       = "HDR 2nd Check"
fieldNames  = ["x (cm)","y (cm)","z (cm)","Dose (Gy)"]
fieldValues = []  # we start with blanks for the values
fieldValues = eg.multenterbox(msg,title, fieldNames)

# make sure that none of the fields was left blank
while 1:  # do forever, until we find acceptable values and break out
    if fieldValues == None: 
        break
    errmsg = ""
   
    # look for errors in the returned values
    for i in range(len(fieldNames)):
        if fieldValues[i].strip() == "":
            errmsg = errmsg + ('"%s" is a required field.\n\n' % fieldNames[i])
      
    if errmsg == "": 
        break # no problems found
    else:
        # show the box again, with the errmsg as the message    
        fieldValues = eg.multenterbox(errmsg, title, fieldNames, fieldValues)
       
msg ="Select BracyVision QAExport Report text file."
title = "HDR file import"
default = "X:\radiation/HDR_BrachyVision_Plans"
filename = eg.fileopenbox(msg, title, default)

while filename is None:
    eg.msgbox("Please choose another file!", "File error!")
    
    msg ="Select BracyVision QAExport Report text file."
    title = "HDR file import"
    default = "X:\radiation/HDR_BrachyVision_Plans"
    filename = eg.fileopenbox(msg, title, default)
    
x = float(fieldValues[0])
y = float(fieldValues[1])
z = float(fieldValues[2])
targetdose = float(fieldValues[3])
    
dose,report = hdrcheck.hdrcheck(x,y,z,targetdose,filename)
    
msg ='Expected dose to target point:  '+str(targetdose)+' (Gy)\nEstimated dose to target point: '+str('%.3f'%dose)+' (Gy) \n\nDifference between expected and estimated: '+str('%.2f' % (100.*(dose-targetdose)/targetdose))+'%'
title = "HDR 2nd Check result"
choices = ('Save PDF report','Quit')
result = eg.buttonbox(msg,title,choices)

if result == 'Save PDF report':
    msg ="Select location and name to save PDF report to file."
    title = "HDR PDF file report save"
    default = "X:\radiation/HDR_BrachyVision_Plans"
    filetypes = '*.pdf'
    reportfilename = eg.filesavebox(msg, title, default, filetypes)
    
    result2pdf.result2pdf(report,reportfilename)
    
    eg.msgbox("HDR 2nd check report saved!")
    
    
    
# if result == 'Exit': sys.exit(0)
