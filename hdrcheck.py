# hdrcheck.py

# Independent dose calculation from a BrachyVision HDR plan. Following the methodology used in 
#    HDR Handcalc (Nathan Childress) / Mauceri, et al, 1999.

# Started 16 July 2012
# Roy Keyes (roy.coding@gmail.com)

import brachyparse
from math import exp, sqrt

# Exposure rate constant in (R-cm^2 / mCi-hr)
Gamma = 4.69

# fmed
fmed = 0.971

# mu
mu = 0.092

# ka
ka = 1.59

# kb
kb = 1.23



def h2oRatio(r):
    '''Estimate ratio of dose-to-water to dose-to-air.'''
    # Ratio of dose to water/air
    # This uses the formulism:
    # Dwater/Dair = Br*e^(-mu*r)
    # where r is distance in cm and Br is calculated by:
    # Br = 1 + ka*(mu*r)^kb
    # The default data comes from Mauceri (Medical Physics, 01/99, Vol. 26, Issue 1, pp. 97-99).
    # This is fairly reliable up to depths of 50 cm.
    
    return (1 + ka*(mu*r)**kb)*exp(-mu*r)
    
def pointdose(r, A, dwell):
    '''Estimate dose from a point radioactive source to distance r. Result in Gy.'''
    
    dose = 10 * Gamma * (A / (r*r)) * (dwell/3600.) * fmed * h2oRatio(r)
    return dose
    
# Calculate total dose from HDR applicator.
def calcdose(applicator, target):
    '''Calculate total dose from all dwell positions in HDR applicator.
    Return total dose, total dwell time, and list of report strings.'''
    
    A = applicator.sourceactivity # Ci
    
    # Total dose
    dose = 0.0
    
    # Total time
    time = 0.0
    
    # Report text output lines
    reportlines = ['Locations (cm)                   Distance (cm)  Dwell time (s)  Dose (Gy)']
    
    print 'Locations (cm) \t\t\tDistance (cm) \tDwell time (s) \tDose (Gy)'
    
    for c in applicator.channels:
        r = sqrt((c[1]-target[0])**2+(c[2]-target[1])**2+(c[3]-target[2])**2)
        d = pointdose(r,A,c[0])
        
        # Print out per channel data and dose.
        print 'x,y,z:','%.2f' % c[1], '%.2f'%c[2], '%.2f'%c[3],'\t','%.2f'%r,'\t\t',c[0],'\t\t','%.3f'%d
        reportline = 'x,y,z: '+('%.2f' % c[1])+'  '+str('%.2f'%c[2])+'  '+str('%.2f'%c[3])+'         '+str('%.2f'%r)+'               '+str(c[0])+'                '+str('%.3f'%d)
        
        time += c[0]
        reportlines += [reportline]
        dose += d
        
    return dose, time, reportlines
    

def hdrcheck(x,y,z,targetdose,filename):
    '''Perform independent HDR dose calculation at target point.
    Return total dose and list of report strings.'''
    
    # Load applicator data
    applicator = brachyparse.bparse(filename)
    
    # Report text
    report = ['Patient: ' + applicator.firstname + ' ' + applicator.lastname.upper()]
    print 'Patient: ' + applicator.firstname + ' ' + applicator.lastname.upper()
    
    report += ['Patient ID: ' + applicator.ID]
    print 'Patient ID: ' + applicator.ID
    
    report += ['Treatment date: ' + applicator.date]
    print 'Treatment date: ' + applicator.date
    
    report += [' '] # Blank line in report
    report += ['Source activity: '+str(applicator.sourceactivity)+' (Ci)']
    print '\nSource activity:',applicator.sourceactivity,'(Ci)'
    
    report += ['Source strength: '+str(applicator.sourcestrength)+' (cGy cm^2 / hr)']
    print 'Source strength:',applicator.sourcestrength,'(cGy cm^2 / hr)\n'
    
    target = (x,y,z)
    
    dose, time, reportlines = calcdose(applicator,target)
    
    report += [' '] # Blank line in report
    report += reportlines
    
    print '\nTotal treatment time:',time,'(s)'
    report += [' '] # Blank line in report
    report += ['Total treatment time: '+str(time)+' (s)']
    
    report += [' '] # Blank line in report
    print '\nExpected dose to target point: ',targetdose,'(Gy)'
    print 'Estimated dose to target point:','%.3f'%dose,'(Gy)'
    print '\nDifference between expected and estimated:', '%.2f' % (100.*(dose-targetdose)/targetdose), '%'
    
    report += ['Expected dose to target point:  '+str(targetdose)+' (Gy)']
    report += ['Estimated dose to target point: '+str('%.3f'%dose)+' (Gy)']
    
    report += [' '] # Blank line in report
    report += ['Difference between expected and estimated: '+str('%.2f' % (100.*(dose-targetdose)/targetdose))+' %']
    
    return dose, report

if __name__ == '__main__':
    import sys

    x = float(sys.argv[1])
    y = float(sys.argv[2])
    z = float(sys.argv[3])
    targetdose = float(sys.argv[4])
    fname = sys.argv[5]
    
    hdrcheck(x,y,z,targetdose,fname)
