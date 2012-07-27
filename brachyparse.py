# brachyparse.py

# Read a "QA Export Report" text file produced by Eclipse 11 brachytherapy planning
#    and exctract the information useful for secondary physics checks.

# Started: 11 July 2012
# Roy Keyes - roy.coding@gmail.com

import re

class Applicator:
    '''A class defining the source positions, dwell times, and source strength for HDR.'''
    
    def __init__(self):
        self.sourcestrength = 0.0  # cGy cm^2 / hr
        self.sourceactivity = 0.0  # Ci
        
def sanitize(data):
    '''Sanitize text file before parsing for HDR data.
    Input a list. Return a list.'''
    
    # Remove unwanted characters and phrases:
    phrases = ['\x00','\x0c','%%[Page: 1]%%','%%[Page: 2]%%',]
    
    k = 0
    while k < len(data):
        for phrase in phrases:
            data[k] = data[k].replace(phrase,'')
        k += 1
    
    # Remove empty lines.
    data = [x for x in data if x != '\n']

    return data
    
def bparse(fname):
    '''Read in Eclipse 11 Brachytherapy QA Export Report text file. Return applicator object.'''
    
    d = open(fname,'U').readlines()
    
    # Sanitize file before parsing data.
    d = sanitize(d)
    
    # print d
    
    # Initialize applicator object and channels.
    applicator = Applicator()
    applicator.channels = []
    
    # i = 0
    # while i < len(d):
        # if re.match('Applicator:',d[i].split()[0]) is not None: # Brief Report style
            # print d[i+1]
            # pos = d[i].split()[1:]
            # pos[0] = pos[0][4:] # remove [cm] from first value
            # applicator.channels += [float(x) for x in pos]
        # i += 1
        
    i = 0
    while i < len(d):
        # Parse treatment information
        if re.search('Treatment activity',d[i]) is not None:
            applicator.sourceactivity = float(d[i].split()[-1][:-3])
        
        if re.search('Treatment Strength',d[i]) is not None:
            applicator.sourcestrength = float(d[i].split()[2])
            
        if re.match('Last name',d[i]) is not None:
            applicator.lastname = d[i].split()[2][:-1]
            
        if re.match('First name',d[i]) is not None:
            applicator.firstname = d[i].split()[2][:-1]
        
        if re.match('IDs',d[i]) is not None:
            applicator.ID = d[i].split()[1][:-1]
            
        if re.match('Treatment date',d[i]) is not None:
            applicator.date = ' '.join(d[i].split()[3:6])
        
        # Parse channel information
        if re.match('Channel',d[i].split()[0]) is not None: # QAexport style
            j = i + 3

            while (re.match('Channel',d[j]) is None) and (re.match('Fraction',d[j]) is None):
                #print 'j:',j
                try:
                    float(d[j].split()[0][:-1]) # Keep loading numerical channel data until you hit a non-numberical line.
                    applicator.channels += [[float(x[:-1]) for x in d[j].split()[1:5]]]
                    j += 1
                except:
                    break
        i += 1
        
    return applicator
