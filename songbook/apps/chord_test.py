from ..src.obj.Chord import Chord

chord = {"name":'A', "notes":(5,7,7,6,5,5),"capo":2}

chord = Chord(chord["name"], chord["notes"])

print(chord.toTikz())