import datetime
import pickle


_svgStyle = """<style type="text/css"><![CDATA[
    .finger {{ 
        stroke: black; fill:  black; stroke-width: 1;
    }}
    .string {{ 
        stroke: black; stroke-width: {stringstroke}; 
    }}
    .fret {{ 
        stroke: black; stroke-width: {fretstroke}; 
    }}
    .barre {{ 
        fill:none; stroke:black; stroke-width: {barrestroke}; 
    }}
    .nut {{ 
        stroke: black; stroke-width: 2; 
    }}
    .chordname {{ 
        fill: black; font-size: {fontsize}px; 
    }}
    .fretmark {{ 
        fill: black; font-style: italic; font-size: 24; 
    }}
    .dot {{
        font-size: {fontsize}px; fill: {fontmarkfill}; font-style: italic; 
    }}
    .unplayed {{  
        fill:black; font-size:{OSIFontSize}px; 
    }}
  ]]></style>\n"""

_templates = {
    'nut_or_capo_position': "<line class='nut' x1='{nutX1}' y1='{nutY1}' x2='{nutX2}' y2='{nutY2}'/>\n",
    'chord_text': "<text class='chordname' x='{x}' y='{y}' dominant-baseline='middle' text-anchor='middle' font-style='italic'>{name}</text>\n",
    'capo_text': "<text class='fretmark' x='{x}' y='{y}'>{fretstarttext}</text>",
    'header': "<svg xmlns='http://www.w3.org/2000/svg' version='1.1' width='{w}' height='{h}'>\n",
    'fret_dot_text': "<text class='dot' x='{x}' y='{y}'>{nFret}fr</text>\n",
    'open_and_unplayed_string_markers': "<text class='unplayed' x='{sx}' y='{OSIY}'>{xOr0}</text>\n",
    'finger_positions': "<circle class='finger' cx='{cx}' cy='{cy}' r='{r}'/>\n",
    'barre': "<path class='barre' d='M {nutX1} {cy} a 50 5 0 1,1 {cx2} 0'/>\n",
    'diagram_frets': "<line class='fret' x1='{x1}' y1='{y}' x2='{x2}' y2='{y}'/>\n",
    'diagram_strings': "<line class='string' x1='{x}'  y1='{y1}' x2='{x}'  y2='{y2}'/>\n"
    }


class chord():
    """Class for generating a chord and drawing a diagram"""
    def __init__(self, notes=[0,0,0,0,0,0], **kwargs):
        """Initialise chord diagram

        KWargs:
        - capo :: Fret for capo (default 0)
        - cut :: Fret for diagram cut (default None)
        - hand :: 'L'eft or 'R'ight handed (default 'R')
        - name :: Name of chord (default NoName)
        - comment :: Comment for file (default 'name')
        - fname :: Filename for SVG (defaults to 'name'.svg)
        - scale :: Factor to scale by (default 2.0)"""
        self.barre = False
        self.barrepos = 25 # a very high fret posn
        self.scale = kwargs.get('scale', 2.0)
        self.chord = notes
        self.Capo = kwargs.get('capo', 0)
        self.hand = kwargs.get('hand', 'R')
        self.Chordname = kwargs.get('name', '')
        self.Myfile = kwargs.get('fname', 'chord.svg')
        self.style = self.set_styles(scaleFactor=self.scale)

    def set_styles(self, scaleFactor=1.0):
        """Scale all necessary parameters in the diagram."""
        miniscaleFactor = scaleFactor if scaleFactor > 1.0 else 1.0
        self.dimensions = {
                'scale': 200, # Percentage scaling
                'width':80*scaleFactor,   # Bounding rectangle for shape
                'height':75*scaleFactor,  # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                'numstrings':6, 'numfrets':5
        }

        self.coords = {
                'ChordName': {'x': 10*miniscaleFactor, 'y': 10*miniscaleFactor},
                'nut': {'x1': 5*miniscaleFactor} # Top left corner of fretboard (for right handed player)
        }

        self.spacing = {
            'string': {'x': 6*scaleFactor}, # X distance between each string
            'fret': {'y': 8*scaleFactor,    # Y distance between each fret
            'startcxdiff': 4*miniscaleFactor},
            'OpenStringIndicator': {'ytochordnameY': 7*scaleFactor, 'ytofirstfretY': 2*scaleFactor},
            'centrefontonstringX': 2.5
        }

        gstringStrokeWidth = 0.3*miniscaleFactor
        gfretStrokeWidth = 0.3*miniscaleFactor
        gfretFontSize = 12*scaleFactor
        gfretMarkFill = 'black'
        gbarreStrokeWidth = 1*miniscaleFactor
        gOSIFontSize = 12*scaleFactor

        self.circleradius = 2 * scaleFactor
        self.fontsize = gfretFontSize

        return _svgStyle.format(
                stringstroke=gstringStrokeWidth, 
                fretstroke=gfretStrokeWidth, 
                barrestroke=gbarreStrokeWidth,
                fontsize=gfretFontSize, 
                fontmarkfill=gfretMarkFill, 
                OSIFontSize=gOSIFontSize)

                        

    def draw(self):
        """Actually draw the chord."""
        OSI_y = self.coords['ChordName']['y'] + self.spacing['OpenStringIndicator']['ytochordnameY']

        FretFirstY = OSI_y + self.spacing['OpenStringIndicator']['ytofirstfretY']

        nut_y1 = FretFirstY

        # top right corner of fretboard (on RH player's guitar)
        nut_x2 = self.coords['nut']['x1'] + ((self.dimensions['numstrings'] - 1) * self.spacing['string']['x'])
        #derived nutY2
        nut_y2 = nut_y1

        # for fret string info posn.
        FretStart_X = nut_x2 + 5 # !!!!!
        FretStart_Y = FretFirstY + 2 # !!!

        nutLineCFG = {'nutX1': self.coords['nut']['x1'], 'nutY1': nut_y1, 'nutX2': nut_x2, 'nutY2': nut_y2}
        nut_or_capo_position =  "<line class='nut' x1='{nutX1}' y1='{nutY1}' x2='{nutX2}' y2='{nutY2}'/>\n".format(**nutLineCFG)

        # Left and Right edge of the fretboard
        Frets_x1 = self.coords['nut']['x1']
        Frets_x2 = self.coords['nut']['x1'] + (self.spacing['string']['x'] * 5)

        # Top and bottom edge of the fretboard
        Strings_y1 = FretFirstY
        Strings_y2 = Strings_y1 + (self.spacing['fret']['y'] * (self.dimensions['numfrets'] - 1))

        # derived output line for Chord name.
        cfg = {'x': self.coords['ChordName']['x']+23, 'y': self.coords['ChordName']['y']-5, 'name': self.Chordname}
        chord_text = _templates['chord_text'].format(**cfg)

        # form text indicating capo position, if any
        FretStartText = str(self.Capo) if self.Capo != 0 else ""

        cfg = {'x': FretStart_X, 'y': FretStart_Y, 'fretstarttext': FretStartText}
        capo_text = _templates['capo_text'].format(**cfg) if self.Capo else ""

        self.barre = 1

        if self.barre: # Find the lowest finger position
            self.barrepos = 25 # way, way up fretboard
            for i in range(self.dimensions['numstrings']):
                if not isinstance(self.chord[i], str) and (0 < self.chord[i] < self.barrepos):
                    self.barrepos = self.chord[i]
            self.lowestfingerpos = self.barrepos # take a copy as barrepos will get adjusted

        for i in range(self.dimensions['numstrings']):
            if self.chord[i] not in ['x', 'X', 0]:
                spos = self.chord[i]
                if self.Capo:
                    spos = spos - self.Capo
                if self.barre:
                    if self.lowestfingerpos > 2:
                        spos = spos - self.lowestfingerpos + 1
                cx = self.coords['nut']['x1'] + (i * self.spacing['string']['x'])
                cy = (nut_y1 - 5) + (spos * self.spacing['fret']['y']) # !!! literal alert!
                while cy > Strings_y2: # need to lengthen chord?
                    self.dimensions['numfrets'] += 1 # adjust num of frets needed
                    # calculate new length of strings
                    Strings_y2 = Strings_y1 + (self.spacing['fret']['y'] * (self.dimensions['numfrets'] - 1))
                    # following is important - changes rectangle chord shape sits in, otherwise chord will only partially render
                    self.dimensions['height'] = self.dimensions['height'] + self.spacing['fret']['y']

        # Generate header
        cfg = {'w': self.dimensions['width'], 'h': self.dimensions['height']}
        header = _templates['header'].format(**cfg)

        # Generate fretboard
        fret_dot_text = ""



        # Generate open_and_unplayed_string_markers string icons
        open_and_unplayed_string_markers = ""
        right_handed = self.hand in ['r', 'R']
        nutX = self.coords['nut']['x1'] if right_handed else nut_x2
        shift = 1 if right_handed else -1
        for i in range(self.dimensions['numstrings']):
            if self.chord[i] in ['x', 'X', 0]:
                sx = (nutX - self.spacing['centrefontonstringX'] ) + (shift * i * self.spacing['string']['x'])
                xOr0 = 'x' if self.chord[i] in ['x', 'X'] else 'o'
                cfg = {'sx': sx, 'OSIY': OSI_y, 'xOr0': xOr0}
                open_and_unplayed_string_markers += _templates['open_and_unplayed_string_markers'].format(**cfg)



        finger_positions = ""
        # Handles both left and right handed
        for i in range(self.dimensions['numstrings']):
            if self.chord[i] not in ['x', 'X', 0]:
                spos = self.chord[i]
                if self.barre:
                    if self.lowestfingerpos > 2:
                        spos = spos - self.lowestfingerpos + 1
                elif self.Capo:
                    spos = spos - self.Capo
                circleCFG = { 'cx': nut_x2 - (i * self.spacing['string']['x']),
                        'cy': (nut_y1 - (self.spacing['fret']['y'] / 2)) + (spos * self.spacing['fret']['y']),
                        'r': self.circleradius}
                if right_handed:
                    circleCFG['cx'] = self.coords['nut']['x1'] + (i * self.spacing['string']['x'])
                finger_positions += _templates['finger_positions'].format(**circleCFG)

        barre_chord_position = ""
        if self.barre:
            cy = (nut_y1 - 5) + (1 * self.spacing['fret']['y'])
            cx2 = (self.dimensions['numstrings'] - 1) * self.spacing['string']['x']
            # The following draws an elliptical arc, which works well even when scaled
            pathCFG = {'nutX1': self.coords['nut']['x1'], 'cy': cy-5, 'cx2': cx2}
            if not any(el in ['x', 'X', 0] for el in self.chord):
                barre_chord_position += _templates['barre'].format(**pathCFG)
            frLineCFG = {'x': FretStart_X, 'nFret': self.barrepos,
                    'y': FretStart_Y + (1 * self.spacing['fret']['y'])}
            if self.barrepos > 2 or not any(el in ['x', 'X', 0] for el in self.chord):
                fret_dot_text += _templates['fret_dot_text'].format(**frLineCFG)
        cut_position = ""

        CutStartText = ""
        FretStartY = 0 #local use only


        diagram_frets = ""
        for i in range(self.dimensions['numfrets']):
            y = FretFirstY + (i * self.spacing['fret']['y'])
            fretCFG = {'x1': Frets_x1, 'x2': Frets_x2,
                        'y': FretFirstY + (i * self.spacing['fret']['y'])}
            diagram_frets += _templates['diagram_frets'].format(**fretCFG)

        # now decide how strings must be drawn
        # taking account of a 'cut' fretboard format
        diagram_strings = ""

        for i in range(self.dimensions['numstrings']):
            x = self.coords['nut']['x1'] + (i * self.spacing['string']['x'])
            noCutCFG = {'x': x, 'y1': Strings_y1, 'y2': Strings_y2}
            diagram_strings += _templates['diagram_strings'].format(**noCutCFG)
        outStr = f"""{header}
            {self.style}
            {chord_text}
            {capo_text}
            {fret_dot_text}
            {open_and_unplayed_string_markers}
            {finger_positions}
            {barre_chord_position}
            {nut_or_capo_position}
            {cut_position}
            {diagram_frets}
            {diagram_strings}
            \n</svg>\n
        """
        return outStr
    
    def drawToFile(self):
        with open(self.Myfile, 'w') as svgFile:
            svgFile.write(self.draw())

if __name__ == "__main__":
    chords=[
        {"name":'Open', "notes":[0, 0, 0, 0, 0, 0]},
        {"name":'Silent', "notes":['x', 'x', 'x', 'x', 'x', 'x'], "fname":"1.svg"},
        {"name":'A11', "notes":[5,4,5,'X',3,'X'], "fname":"2.svg"},
        {"name":'A5', "notes":['X',0,2,2,'x','x'], "fname":"3.svg"},
        {"name":'A6', "notes":[0,0,2,2,2,2], "fname":"4.svg"},
        {"name":'A7', "notes":[0,0,2,0,2,0], "fname":"5.svg"},
        {"name":'A7', "notes":[0,0,2,2,2,3], "fname":"A7_var2.svg"},
        {"name":'A7sus4', "notes":['X',0,2,0,3,0], "fname":"6.svg"},
        {"name":'A9', "notes":['X',0,2,4,2,3], "fname":"7.svg"},
        {"name":'D2/4', "notes":[0,5,4,0,3,0], "fname":"Dadd.svg"},
        {"name":'A', "notes":[5,7,7,6,5,5], "fname":"A_pos5.svg"},
        {"name":'A', "notes":[5,7,7,6,5,5],"capo":2, "fname":"Acapo2.svg"},
        {"name":'Amaj7', "notes":[0,0,2,2,2,4], "fname":"9.svg"},
        {"name":'Asus4', "notes":[0,0,2,2,3,0], "fname":"10.svg"},
        {"name":'Bb', "notes":["x",8,8,7,6,6], "fname":"Bb.svg"},
        {"name":'B', "notes":[7,9,9,8,7,7],"cut":6, "fname":"B_cut.svg"},
        {"name":'B', "notes":['X','X',4,4,4,7],"fname":"11.svg"},
        {"name":'E11', "notes":[0,7,6,7,5,5],"fname":"12.svg"},
        {"name":'E5', "notes":[0,2,2,'x','x','x'], "fname":"13.svg"},
        {"name":'E6', "notes":[0,2,2,1,2,0], "fname":"14.svg"},
        {"name":'E7', "notes":[0,2,0,1,0,0], "fname":"15.svg"},
        {"name":'E7', "notes":[0,2,0,1,3,0], "fname":"E7_var2.svg"},
        {"name":'E7sus4', "notes":[0,2,0,2,0,0], "fname":"16.svg"},
        {"name":'E9', "notes":[0,2,0,1,3,2], "fname":"17.svg"},
        {"name":'E', "notes":[0,2,2,1,0,0], "fname":"18.svg"},
        {"name":'Emaj7', "notes":[0,2,1,1,0,0], "fname":"19.svg"},
        {"name":'Esus4', "notes":[0,2,2,2,0,0], "fname":"20.svg"},
        {"name":'F', "notes":[1,3,3,2,1,1], "fname":"21.svg"},
        {"name":'G', "notes":[3,5,5,4,3,3], "fname":"22.svg"}
    ]

    with open("Chords.html",'w') as f:
        f.write("<div style='display:flex; flex-wrap:wrap'>\n")
        for i, val in enumerate(chords):
            f_out = '{}.svg'.format(val['name'])
            if 'fname' in val:
                f_out = val['fname']
            f.write("<div>{}: <img src='{}'/></div>\n".format(i, f_out))
            val['scale'] = 2.0
            chord(**val).draw()
        f.write("</div>")
