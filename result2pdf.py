# result2pdf.py

# Write HDR 2nd check output to a PDF report.

# Started 18 July 2012
# Roy Keyes (roy.coding@gmail.com)

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate,Spacer
from reportlab.pdfgen.canvas import Canvas

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
    Input: list of strings (report text) and output file name.'''
    
    pdf = Canvas(reportfilename, pagesize = letter)
    report = pdf.beginText(inch * 1, inch * 10)
    
    for line in result:
        report.textLine(line)
    
    pdf.drawText(report)
    pdf.showPage()
    pdf.save()