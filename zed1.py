from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.units import mm
from reportlab.platypus import Image, PageBreak, Table
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

Width, Height = letter
styles = getSampleStyleSheet()
Title = "Comparison Index"
pageinfo = "platypus example"
BTRLogo = '/home/samuelitwaru/Pictures/mvara.png'
PartnerLogo = '/home/samuelitwaru/Pictures/mvara.jpg'
ClientLogo = '/home/samuelitwaru/Pictures/mvara.jpg'
Graph1 = '/home/samuelitwaru/Pictures/mvara.jpg'



# Define the fixed features of the first page of the document
def myFirstPage(canvas, doc):
    canvas.saveState()

    # canvas.setFillColorCMYK(0.68, 0.44, 0, 0.41)
    # canvas.setFontSize(22)
    # canvas.setFont('Helvetica-Bold', 36)
    # canvas.drawString(40, 670, 'Health & Welfare')
    canvas.drawImage(BTRLogo,100,400,width=400,height=400,mask='auto') 

    # canvas.setFont('Helvetica-Bold', 24)
    # canvas.drawString(40, 625, 'Benchmark Comparison Report')

    # canvas.setFont('Helvetica', 16)
    # canvas.drawString(40, 550, 'Prepared for:')
    # canvas.drawString(40, 400, 'Prepared on:') #INSERY DYNAMIC DATE****

    # #Logo is measured and good to go

    # canvas.drawImage(PartnerLogo, 10, Height/5, width=Width/1.2, 
    # preserveAspectRatio=True, mask='auto') #MAKE SURE IMAGE IS DYNAMIC AND HAS MAX SETS

    # canvas.setStrokeColorCMYK(0.68,0.44,0,0.41)
    # canvas.setLineWidth(7)
    # canvas.line(40,112,570,112)



# Since we want pages after the first to look different from the first we define an alternate layout for
# the fixed features of the other pages.
# Note that the two functions use the pdfgen level canvas operations to paint the annotations for the pages.
def myLaterPages(canvas, doc):
    canvas.saveState()
    canvas.setFont('Times-Roman', 23)
    page_num = canvas.getPageNumber()
    text = "Page #%s" % page_num
    canvas.drawRightString(200 * mm, 20 * mm, text)
    canvas.restoreState()

def myThirdPages(canvas, doc):
    canvas.saveState()
    canvas.setFont('Times-Roman', 9)
    canvas.drawString(inch, 0.75 * inch, "Page %d %s")
    canvas.restoreState()

# Create a story and build the document
def createMultiPage():

    doc = SimpleDocTemplate("Comparison Index.pdf", pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
    # style = styles["Normal"]
    # styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))

    Story = [Spacer(1, 2 * inch)]

    doc.build(Story, onFirstPage=myFirstPage, onLaterPages=myFirstPage)
    table = Table([[i for i in range(10)] for i in range(10)])
    doc.build([table, PageBreak(), table, PageBreak(), table])
    # doc.build([PageBreak(),PageBreak()])

if __name__ == "__main__":
    createMultiPage()