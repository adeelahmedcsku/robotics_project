from pathlib import Path
import re, csv, textwrap
from xml.sax.saxutils import escape
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
    Spacer, PageBreak, Preformatted, Table, TableStyle, Image, KeepTogether, CondPageBreak)
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.graphics.shapes import Drawing, Rect, Line, String, Polygon

ROOT=Path('/data/Robotics_Project')
OUT=ROOT/'AI_Humanoid_Robotics_Engineering_Book.pdf'
W,H=A4; WIDTH=W-96
NAVY=colors.HexColor('#172E45'); TEAL=colors.HexColor('#007E87')
LIGHT=colors.HexColor('#EAF3F5'); GRAY=colors.HexColor('#546779')
for name,file in [('Body','DejaVuSerif.ttf'),('Body-Bold','DejaVuSerif-Bold.ttf'),
                  ('Sans','DejaVuSans.ttf'),('Sans-Bold','DejaVuSans-Bold.ttf'),
                  ('Mono','DejaVuSansMono.ttf')]:
    pdfmetrics.registerFont(TTFont(name,'/usr/share/fonts/truetype/dejavu/'+file))
for family in ['Body','Sans']:
    pdfmetrics.registerFontFamily(family,normal=family,bold=family+'-Bold',italic=family,boldItalic=family+'-Bold')
styles={
 'body':ParagraphStyle('body',fontName='Body',fontSize=9.3,leading=14.5,spaceAfter=7.5,textColor=NAVY),
 'part':ParagraphStyle('part',fontName='Sans-Bold',fontSize=23,leading=29,textColor=TEAL,spaceAfter=21,keepWithNext=True),
 'chapter':ParagraphStyle('chapter',fontName='Sans-Bold',fontSize=18,leading=24,textColor=NAVY,spaceAfter=16,keepWithNext=True),
 'section':ParagraphStyle('section',fontName='Sans-Bold',fontSize=10.5,leading=15,textColor=TEAL,spaceBefore=12,spaceAfter=7,keepWithNext=True),
 'code':ParagraphStyle('code',fontName='Mono',fontSize=8,leading=11.5,textColor=NAVY,spaceBefore=6,spaceAfter=12),
 'cell':ParagraphStyle('cell',fontName='Sans',fontSize=7.6,leading=10.6,textColor=NAVY),
 'caption':ParagraphStyle('caption',fontName='Sans',fontSize=8,leading=12,textColor=GRAY,spaceAfter=12),
 'file':ParagraphStyle('file',fontName='Sans-Bold',fontSize=8,leading=12,textColor=GRAY,spaceBefore=8,spaceAfter=4,keepWithNext=True),
 'bullet':ParagraphStyle('bullet',fontName='Body',fontSize=9.3,leading=14.5,leftIndent=14,firstLineIndent=-11,spaceAfter=6,textColor=NAVY)
}

def normalize(s):
    for c in ['—','–','‑','−']:s=s.replace(c,'-')
    return s.replace('\t','    ')

def fmt(s):
    s=escape(normalize(s))
    s=re.sub(r'\*\*(.+?)\*\*',r'<b>\1</b>',s)
    s=re.sub(r'`([^`]+)`',r'<font name="Mono">\1</font>',s)
    s=re.sub(r'(https://[^\s<]+)',r'<link href="\1" color="#007E87">\1</link>',s)
    return s

def code(text):
    rows=[]
    for line in normalize(text).splitlines():
        if len(line)<=103: rows.append(line)
        else: rows.extend(textwrap.wrap(line,width=103,subsequent_indent='    ',
            replace_whitespace=False,drop_whitespace=False,break_long_words=True,break_on_hyphens=False))
    return Preformatted('\n'.join(rows),styles['code'])

class Book(BaseDocTemplate):
    def beforeDocument(self):
        self.heading_number=0
    def afterFlowable(self,f):
        if isinstance(f,Paragraph) and f.style.name in ['part','chapter']:
            level=0 if f.style.name=='part' else 1
            self.heading_number+=1; key='h'+str(self.heading_number)
            self.canv.bookmarkPage(key)
            self.canv.addOutlineEntry(f.getPlainText(),key,level,False)
            self.notify('TOCEntry',(level,f.getPlainText(),self.page,key))

def header(c,doc):
    if doc.page==1:
        c.setFillColor(NAVY);c.rect(0,H-20,W,20,fill=1,stroke=0)
        return
    c.setStrokeColor(colors.HexColor('#B9CCD5'));c.setLineWidth(.4)
    c.line(48,H-40,W-48,H-40)
    c.setFont('Sans',7);c.setFillColor(TEAL)
    c.drawString(48,H-30,'ENGINEERING AN AI HUMANOID ROBOT')
    c.setFillColor(GRAY);c.drawString(48,28,'Asimov 1 / Simulation first / Research edition 2026')
    c.drawRightString(W-48,28,str(doc.page))

def box(d,x,y,w,h,title,sub=''):
    d.add(Rect(x,y,w,h,rx=5,fillColor=LIGHT,strokeColor=TEAL,strokeWidth=.7))
    d.add(String(x+w/2,y+h-19,title,fontName='Sans-Bold',fontSize=9,textAnchor='middle',fillColor=NAVY))
    for j,line in enumerate(sub.split('\n')):
        d.add(String(x+w/2,y+h-34-j*11,line,fontName='Sans',fontSize=7.5,textAnchor='middle',fillColor=GRAY))

def arrow(d,x1,y1,x2,y2):
    d.add(Line(x1,y1,x2,y2,strokeColor=GRAY,strokeWidth=.9))
    import math
    a=math.atan2(y2-y1,x2-x1);sz=5
    points=[x2,y2,x2-sz*math.cos(a-.5),y2-sz*math.sin(a-.5),x2-sz*math.cos(a+.5),y2-sz*math.sin(a+.5)]
    d.add(Polygon(points,fillColor=GRAY,strokeColor=GRAY))

def diagram(kind):
    if kind=='architecture':
        d=Drawing(WIDTH,330)
        box(d,140,264,220,56,'Human + task planner','Instruction -> permitted skill')
        box(d,140,178,220,61,'Safety + control','Limits, deadlines, policy/PD authority')
        box(d,0,88,220,60,'Simulation backend','MuJoCo + modeled sensors')
        box(d,278,88,220,60,'Physical backend','Verified HAL + embedded watchdogs')
        box(d,140,0,220,58,'State estimate + evidence','Feedback, telemetry, experiment logs')
        arrow(d,250,264,250,239);arrow(d,180,178,110,148);arrow(d,320,178,388,148)
        arrow(d,110,88,200,58);arrow(d,388,88,300,58)
        arrow(d,140,28,40,28);arrow(d,40,28,40,208);arrow(d,40,208,140,208)
        return d
    if kind=='sequence':
        d=Drawing(WIDTH,285);xs=[35,140,250,355,460]
        for x,label in zip(xs,['Human','Planner','Gate','Controller','Plant']):
            d.add(String(x,268,label,fontName='Sans-Bold',fontSize=8,textAnchor='middle',fillColor=TEAL))
            d.add(Line(x,250,x,15,strokeColor=colors.HexColor('#B9CCD5'),strokeWidth=.5))
        items=[(0,1,230,'Skill request'),(1,2,198,'Bounded, fresh request'),(2,3,166,'Authorized trajectory'),(3,4,134,'Limited command'),(4,3,102,'Timed feedback'),(3,2,70,'Health + tracking'),(2,1,38,'Complete / fault')]
        for a,b,y,label in items:
            arrow(d,xs[a],y,xs[b],y)
            d.add(String((xs[a]+xs[b])/2,y+6,label,fontName='Sans',fontSize=6.7,textAnchor='middle',fillColor=NAVY))
        return d
    if kind=='telemetry':
        d=Drawing(WIDTH,215)
        box(d,0,140,150,60,'Sensors','Joint / IMU / camera')
        box(d,175,140,150,60,'Timestamp + frame','Sample time != arrival time')
        box(d,350,140,148,60,'Estimator','State + uncertainty')
        box(d,65,25,170,60,'Decimated telemetry','Dashboard + persistent logs')
        box(d,300,25,170,60,'Local control','Fresh feedback + bounded output')
        arrow(d,150,170,175,170);arrow(d,325,170,350,170)
        arrow(d,250,140,150,85);arrow(d,424,140,385,85)
        return d
    d=Drawing(WIDTH,230)
    box(d,0,150,145,62,'Energy source','Approved supply / protection')
    box(d,175,150,145,62,'Isolation + distribution','DC-rated reviewed design')
    box(d,350,150,148,62,'Driver + motor','Guarded supported load')
    box(d,50,25,180,62,'Independent stop chain','Available when host fails')
    box(d,285,25,190,62,'Local controller','CAN + feedback + watchdog')
    arrow(d,145,181,175,181);arrow(d,320,181,350,181)
    arrow(d,140,87,247,150);arrow(d,380,87,424,150)
    return d

def table(rows,widths=None):
    cells=[[Paragraph(fmt(x),styles['cell']) for x in row] for row in rows]
    n=len(rows[0]);widths=widths or [WIDTH/n]*n
    t=Table(cells,colWidths=widths,repeatRows=1,hAlign='LEFT')
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),LIGHT),('VALIGN',(0,0),(-1,-1),'TOP'),
       ('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),
       ('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),
       ('LINEBELOW',(0,0),(-1,0),.7,TEAL),('LINEBELOW',(0,1),(-1,-1),.3,colors.HexColor('#CDDBE1'))]))
    return t

doc=Book(str(OUT),pagesize=A4,leftMargin=48,rightMargin=48,topMargin=58,bottomMargin=48,
         title='Engineering an AI Humanoid Robot - Simulation to Physical Asimov 1',
         author='Robotics Project - instructional research edition',subject='Hands-on simulation, control, embodied AI and staged hardware engineering')
doc.addPageTemplates(PageTemplate('pages',[Frame(48,48,WIDTH,H-106,id='body',leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0)],onPage=header))
story=[Spacer(1,26),Paragraph('A HANDS-ON ROBOTICS LABORATORY',ParagraphStyle('eyebrow',fontName='Sans-Bold',fontSize=10,leading=14,textColor=TEAL,spaceAfter=24)),
 Paragraph('Engineering an<br/>AI Humanoid<br/>Robot',ParagraphStyle('cover',fontName='Sans-Bold',fontSize=34,leading=42,textColor=NAVY,spaceAfter=19)),
 Paragraph('From first simulation to a safely<br/>commissioned physical research platform',ParagraphStyle('strap',fontName='Sans',fontSize=15,leading=22,textColor=TEAL,spaceAfter=25))]
cover_rows=[[Paragraph('Menlo Research Asimov 1<br/><br/>17 progressive lessons<br/>Complete runnable teaching code<br/>Numerical tests and measured results<br/>ROS 2, kinematics, control and PPO<br/>Perception and bounded skills<br/>Staged EUR 6,000 hardware planning',styles['body']),Image(str(ROOT/'humanoid_lab/logs/asimov_model.png'),width=174,height=232)]]
t=Table(cover_rows,colWidths=[WIDTH-190,190]);t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),0)]));story.append(t)
story += [Spacer(1,22),Paragraph('Research edition / 25 October 2026',styles['file']),Paragraph('Prepared for an experienced software engineer beginning robotics. Platform facts are source-linked; exercise assumptions and physical deployment gates are explicit.',styles['caption']),PageBreak()]
story.append(Paragraph('Contents',ParagraphStyle('contents_title',parent=styles['chapter'])))
toc=TableOfContents();toc.levelStyles=[ParagraphStyle('toc0',fontName='Sans-Bold',fontSize=10,leading=15,spaceBefore=11,textColor=TEAL),ParagraphStyle('toc1',fontName='Sans',fontSize=8.6,leading=13,leftIndent=10,spaceBefore=5,textColor=NAVY)]
story += [toc,PageBreak()]
firstpart=True; afterpart=False
for path in sorted((ROOT/'book_source').glob('[0-9][0-9]_*.md')):
    lines=path.read_text().splitlines();i=0
    while i<len(lines):
        line=lines[i].strip();i+=1
        if not line:continue
        if line.startswith('```'):
            body=[]
            while i<len(lines) and not lines[i].strip().startswith('```'):
                body.append(lines[i]);i+=1
            i+=1;story.append(code('\n'.join(body)));continue
        if line.startswith('!code '):
            target=ROOT/line[6:]
            if not target.exists():raise FileNotFoundError(target)
            story.append(Paragraph(fmt(str(target)),styles['file']))
            story.append(code(target.read_text()));continue
        if line.startswith('!csv '):
            rows=list(csv.DictReader((ROOT/line[5:]).open()))
            data=[['Item / quantity','Specification','Price evidence / supplier','Compatibility / priority']]
            for r in rows:
                data.append([r['component']+' / '+r['quantity'],r['specification'],
                    ('EUR '+r['verified_eur'] if r['verified_eur'] else 'Unquoted')+' / '+r['supplier'],r['compatibility']+' / '+r['priority']])
            story.extend([table(data,[118,112,137,WIDTH-367]),Spacer(1,12)]);continue
        if line.startswith('!diagram '):
            story.extend([diagram(line[9:]),Spacer(1,12)]);continue
        if line.startswith('!image '):
            from PIL import Image as PILImage
            target=ROOT/line[7:]; im=PILImage.open(target);w,h=im.size
            scale=min(WIDTH/w,470/h)
            story.extend([Image(str(target),width=w*scale,height=h*scale),Spacer(1,8)]);continue
        if line.startswith('# '):
            if not firstpart:story.append(PageBreak())
            firstpart=False;afterpart=True
            story.append(Paragraph(fmt(line[2:]),styles['part']));continue
        if line.startswith('## '):
            if not afterpart:story.extend([CondPageBreak(210),Spacer(1,18)])
            afterpart=False;story.append(Paragraph(fmt(line[3:]),styles['chapter']));continue
        if line.startswith('### '):
            story.append(Paragraph(fmt(line[4:]),styles['section']));continue
        if line.startswith('|'):
            data=[line]
            while i<len(lines) and lines[i].strip().startswith('|'):
                data.append(lines[i].strip());i+=1
            rows=[]
            for row in data:
                if re.match(r'^\|[\s:|\-]+\|$',row):continue
                rows.append([x.strip() for x in row.strip('|').split('|')])
            n=len(rows[0]); widths=None
            if n==3:widths=[102,200,WIDTH-302]
            if n==4:widths=[35,218,60,WIDTH-313]
            story.extend([table(rows,widths),Spacer(1,12)]);continue
        if line.startswith('File: '):
            story.append(Paragraph(fmt(line),styles['file']));continue
        if re.match(r'^\d+\. ',line) or line.startswith('- '):
            story.append(Paragraph(fmt(line),styles['bullet']));continue
        para=[line]
        while i<len(lines) and lines[i].strip() and not lines[i].strip().startswith(('#','!','```','|','File: ')) and not re.match(r'^\d+\. ',lines[i].strip()):
            para.append(lines[i].strip());i+=1
        style=styles['caption'] if line.startswith('Figure ') else styles['body']
        story.append(Paragraph(fmt(' '.join(para)),style))

for style in styles.values():
    style.allowWidows=0
    style.allowOrphans=0
doc.multiBuild(story)
print(OUT)
