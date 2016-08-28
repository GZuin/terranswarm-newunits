import os
import sys
import xml.etree.ElementTree as ET

if __name__ == '__main__':

    expFolder = sys.argv[1]
    exp = expFolder.split('/')[-1]
    numFiles = int(sys.argv[2])

    wins = 0
    loss = 0
    draw = 0
    
    for i in range(0, numFiles):
        archive = os.path.join(expFolder, str(i) + '.chr.res.xml')
        if (os.path.exists(archive)):
            xml_tree = ET.parse(archive).getroot()
            mres = xml_tree.find('result').get('value')
            if(mres == 'loss'):
                loss = loss + 1
            elif(mres == 'draw'):
                 draw = draw + 1
            else:
                wins = wins + 1
    outp = open('results/result_' + exp + '.txt', 'w')
    outp.write('Wins: ' + str(float(wins/(wins+draw+loss)))+'\n')
    outp.write('Loss: ' + str(float(loss/(wins+draw+loss)))+'\n')
    outp.write('Draw: ' + str(float(draw/(wins+draw+loss)))+'\n')
    outp.close()
