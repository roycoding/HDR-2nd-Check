# result2pdf.py

# Write HDR 2nd check output to a PDF report.

# Started 18 July 2012
# Roy Keyes (roy.coding@gmail.com)

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate,Spacer
from reportlab.pdfgen.canvas import Canvas
from math import ceil

# def result2pdf(result,reportfilename):
    # '''Write HDR 2nd check output to a PDF report.
    # Input: list of strings (report text) and output file name.'''
    
    # pdf = SimpleDocTemplate(reportfilename, pagesize = letter)
    ##pdf = Canvas(reportfilename, pagesize = letter)
    # report = []
    # style = getSampleStyleSheet()
    
    # for line in result:
        # report.append(Paragraph(line, style["Normal"]))
        ##report.append(Spacer(0, inch * .1))
    
    # pdf.build(report)
    
def result2pdf(result,reportfilename):
    '''Write HDR 2nd check output to a PDF report.
    Input: list of strings (report text).'''
    
    # Lines per page
    lpp = 48
    # Pages needed in report
    pages = ceil(len(result)/float(lpp))
    print '# of pages:',pages
    
    pdf = Canvas(reportfilename, pagesize = letter)
    report = pdf.beginText(inch * 1, inch * 10)
    
    # Single page report
    if len(result) < lpp:

        for line in result:
            report.textLine(line)
    
        pdf.drawText(report)
        pdf.showPage()

    # Or create a multi-page report
    else:
        page = 1
        l = 0
        while page < pages:
            # Reset page contents
            report = pdf.beginText(inch * 1, inch * 10)
        
            while l < lpp*page:
                print 'l:',l
                report.textLine(result[l])
                l += 1
            pdf.drawText(report)
            pdf.showPage()
            page += 1
        
        # Print last page
        # Reset page contents
        report = pdf.beginText(inch * 1, inch * 10)
        for line in result[int(pages-1)*lpp:]:
            report.textLine(line)
    
        pdf.drawText(report)
        pdf.showPage()
        
    pdf.save()
