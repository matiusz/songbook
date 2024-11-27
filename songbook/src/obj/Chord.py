from ..tools import chordGen as cg
import svg2tikz

class Chord:
    def __init__(self, name, frets):
        self.name = name
        self.frets: tuple = frets
    def saveDiagram(self):
        cg.chord(name = self.name, notes = self.frets).drawToFile()
    def toTikz(self, i=0):
        tikzCode = svg2tikz.convert_svg(cg.chord(name = self.name, notes = self.frets).draw(), codeoutput="figonly")
        tikzCodeLines = tikzCode.splitlines()
        outLines = []
        for line in tikzCodeLines:
            if r"\end{tikzpicture}" in line:
                outLines.append("}")
            if r"\begin{tikzpicture}" in line:
                outLines.append(line.replace("[y=1cm", "[overlay, y=1cm"))
                outLines.append(rf"\hspace*{{{5*i}cm}}\raisebox{{-20cm}}{{")
            else:
                outLines.append(line)
        return "\n".join(outLines)

    def toJSON(self):
        return {
            "name": self.name,
            "frets": self.frets,
        }
    @classmethod
    def fromJSON(cls, json):
        return cls(name = json["name"], frets = json["frets"])
