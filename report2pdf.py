from reportlab.platypus.doctemplate import PageTemplate, BaseDocTemplate, Frame, FrameBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter, A4, inch
from reportlab.graphics.charts.linecharts import HorizontalLineChart, Drawing
from reportlab.platypus import PageBreak, Spacer
from reportlab.platypus.paragraph import Paragraph
from reportlab.lib.units import cm
from reportlab.lib.styles import ParagraphStyle as PS
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont('heiti', 'simsun.ttf'))
import time
from reportlab.graphics.samples import radar


class MyPdfReport:
    def __init__(self, filename):
        self.doc = BaseDocTemplate(
                filename=filename,
                pagesize=letter
        )

        header = Frame(
                x1=0,
                y1=27 * cm,
                width=self.doc.width,
                height=2 * cm,
                id='header',
                showBoundary=0
        )

        body = Frame(
                x1=1.5 * cm,
                y1=2 * cm,
                width=self.doc._rightMargin - 1 * cm,
                height=self.doc.height,
                id='body',
                showBoundary=0
        )

        self.doc.addPageTemplates(PageTemplate(id='reportPage', frames=[header, body]))

        self.story = []

        self.titleStyle = PS(name='Title', fontSize=24, fontName='heiti', alignment=1, leading=22)
        self.timeStyle = PS(name='Title', fontSize=20, fontName='heiti', alignment=1, leading=40)
        self.h1Style = PS(name='Heading1', fontSize=18, fontName='heiti', leading=30, leftIndent=20)
        self.h2Style = PS(name='Heading2', fontSize=16, fontName='heiti', leading=30, leftIndent=20)
        self.h3Style = PS(name='Heading3', fontSize=14, fontName='heiti', leading=20, leftIndent=20)
        self.lineBreak = Spacer(self.doc.width, 20)

    def usageChart(self, metric, width=400, height=200):
        # data = metric['data']
        # catNames = metric['catNames']
        data = [
            (13, 5, 20, 22, 37, 45, 19, 4),
            (5, 20, 46, 38, 23, 21, 6, 14)
        ]

        drawing = Drawing(width, height)
        lc = HorizontalLineChart()
        lc.x = 50
        lc.y = 50
        lc.height = height * 0.8
        lc.width = width * 0.8
        lc.data = data
        lc.joinedLines = 1
        catNames = 'Jan Feb Mar Apr May Jun Jul Aug'.split(' ')
        lc.categoryAxis.categoryNames = catNames
        lc.categoryAxis.labels.boxAnchor = 'n'
        lc.valueAxis.valueMin = 0
        lc.valueAxis.valueMax = 100
        lc.valueAxis.valueStep = 20
        lc.lines[0].strokeWidth = 2
        lc.lines[0].fillColor = colors.brown
        lc.lines[0].name = 'line1'
        lc.lines[1].strokeWidth = 1.5
        lc.lines[1].fillColor = colors.whitesmoke
        lc.lines[1].name = 'line2'

        drawing.add(lc)

        return drawing

    def frontPage(self):
        strNow = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        reportTitle = Paragraph("氢氪出行XXX接口测试报告", self.titleStyle)
        timeTitle = Paragraph("报告时间", self.timeStyle)
        reportTime = Paragraph(strNow, self.timeStyle)

        # 切换页眉
        self.story.append(FrameBreak())
        # 标题距页眉间隔
        self.story.append(Spacer(self.doc.width, 8 * cm))
        # 标题
        self.story.append(reportTitle)
        # 间隔
        self.story.append(Spacer(self.doc.width, 6 * cm))
        # 报告时间
        self.story.append(timeTitle)
        self.story.append(reportTime)
        # 换页
        self.story.append(PageBreak())

    def hostInfoPage(self, cpuMetric, memMetric, diskMetric):
        hostTitle = Paragraph("主机运行状态信息", self.h1Style)
        cpuTitle = Paragraph("主机CPU状态", self.h3Style)
        cpuChart = self.usageChart(cpuMetric, 400, 150)
        memTitle = Paragraph("主机内存状态", self.h3Style)
        memChart = self.usageChart(memMetric, 400, 150)
        diskTitle = Paragraph("主机磁盘状态", self.h3Style)
        diskChart = self.usageChart(diskMetric, 400, 150)

        self.story.append(FrameBreak())
        self.story.append(hostTitle)
        self.story.append(cpuTitle)
        self.story.append(self.lineBreak)
        self.story.append(cpuChart)
        self.story.append(memTitle)
        self.story.append(self.lineBreak)
        self.story.append(memChart)
        # self.story.append(FrameBreak())
        self.story.append(diskTitle)
        self.story.append(self.lineBreak)
        self.story.append(diskChart)

    def build(self):
        self.frontPage()
        self.hostInfoPage(None, None, None)
        self.doc.build(self.story)


if __name__ == '__main__':
    myReport = MyPdfReport('report.pdf')

    myReport.build()
