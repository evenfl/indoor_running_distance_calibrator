import xml.etree.ElementTree as ET

trueFullDistance = 10000 # [m]
filename = "activity.tcx"

tcxFile = open(filename, "r+")
FileString = tcxFile.read()
tcxFile.close()

occurrences = FileString.count("Track>")

def getText(nodelist):
    # Iterate all Nodes aggregate TEXT_NODE
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
        else:
            # Recursive
            rc.append(getText(node.childNodes))
    return ''.join(rc)



# Xml parsing.
tree = ET.parse(filename)
root = tree.getroot()

#Access the nodes you want by treating root as an array of arrays
# roots children = root[x]
# roots children's children root[x][y]etc
nrOfLaps = len(root[0][0])-2
nrOfTracks = len(root[0][0][1])-2
nrOfTrackPoints = []
for h in range(1,int(occurrences/2) + 1):
    nrOfTrackPoints.append(len(root[0][0][h][8]))

# nrOfTrackPoints.append(len(root[0][0][1][8]))
# nrOfTrackPoints.append(len(root[0][0][2][8]))
# nrOfTrackPoints.append(len(root[0][0][3][8]))
# nrOfTrackPoints.append(len(root[0][0][4][8]))
# nrOfTrackPoints.append(len(root[0][0][5][8]))
# nrOfTrackPoints.append(len(root[0][0][6][8]))
# nrOfTrackPoints.append(len(root[0][0][7][8]))
# nrOfTrackPoints.append(len(root[0][0][8][8]))
# nrOfTrackPoints.append(len(root[0][0][9][8]))
# nrOfTrackPoints.append(len(root[0][0][10][8]))
# nrOfTrackPoints.append(len(root[0][0][11][8]))
# nrOfTrackPoints.append(len(root[0][0][12][8]))
nrOfTrackPointsLastTrack = len(root[0][0][nrOfLaps][nrOfTracks])-1
nrOfTracksLastLap = len(root[0][0][nrOfLaps])-2


print("Initial full distance: " + root[0][0][nrOfLaps][nrOfTracks][nrOfTrackPointsLastTrack][1].text)
print("Corrected full distance: " + str(trueFullDistance))
falseFullDistance = float(root[0][0][nrOfLaps][nrOfTracks][nrOfTrackPointsLastTrack][1].text)
C = trueFullDistance/falseFullDistance

DistanceMeters = []

for i in range(1,nrOfLaps+1):
    for k in range(0, nrOfTrackPoints[i-1]):
        DistanceMeters.append(float(root[0][0][i][8][k][1].text)*C)
        root[0][0][i][8][k][1].text = str(float(root[0][0][i][8][k][1].text)*C)
        # print(str(len(DistanceMeters)) + " " + str(DistanceMeters[len(DistanceMeters)-1]))

ET.register_namespace('schemaLocation', "http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2 http://www.garmin.com/xmlschemas/TrainingCenterDatabasev2.xsd")
ET.register_namespace('', "http://www.garmin.com/xmlschemas/ActivityGoals/v1")
ET.register_namespace('', "http://www.garmin.com/xmlschemas/ActivityExtension/v2")
ET.register_namespace('', "http://www.garmin.com/xmlschemas/UserProfile/v2")
ET.register_namespace('', "http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2")
ET.register_namespace('xsi', "http://www.w3.org/2001/XMLSchema-instance")

#Open the xml file and rewrite it
xmlFileHandle = open(filename,'wb')
xmlFileHandle.write(ET.tostring(root, encoding='utf8', method='xml'))
xmlFileHandle.close()

#Remove all occurances of ns2:
tcxFile = open(filename, "r+")
newFileString = tcxFile.read()
tcxFile.close()

tcxFile = open(filename, "r+")
tcxFile.truncate(0)
newFileString = str(newFileString).replace("ns2:","")

tcxFile.write(newFileString)
tcxFile.close()