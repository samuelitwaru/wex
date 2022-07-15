from reportlab.pdfgen import canvas
from reportlab.lib.units import mm


class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        """add page info to each page (page x of y)"""
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            page_num = self._pageNumber
            self.drawImage
            self.drawImage('/home/samuelitwaru/Pictures/mvara.jpg', 100,
                           700, width=None, height=None, 
                           mask='auto')
            # mybarcode = createBarcodeDrawing('QR', value= 'www.mousevspython.com - Page %s'%page_num)
            # self.drawInlineImage(mybarcode,20,20)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)


def main():
    import sys
    # import urllib2
    # from cStringIO import StringIO
    from reportlab.platypus import SimpleDocTemplate, Image, Paragraph, PageBreak
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet

    # This is needed because ReportLab accepts the StringIO as a file-like object,
    # but doesn't accept urllib2.urlopen's return value
    # def get_image(url):
    #     u = urllib2.urlopen(url)
    #     return StringIO(u.read())

    styles = getSampleStyleSheet()
    styleN = ParagraphStyle(styles['Normal'])

    # build doc

    if len(sys.argv) > 1:
        fn = sys.argv[1]
    else:
        fn = "filename.pdf"
    doc = SimpleDocTemplate(open(fn, "wb"))
    elements = [
        Paragraph(
            "Hellodfdfdfdfdfddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd,", styleN),
        Image("/home/samuelitwaru/Pictures/mvara.jpg"),
        Paragraph("world!", styleN),
        Image("/home/samuelitwaru/Pictures/mvara.jpg"),
    ]
    doc.build(elements, canvasmaker=NumberedCanvas)


if __name__ == "__main__":
    main()
