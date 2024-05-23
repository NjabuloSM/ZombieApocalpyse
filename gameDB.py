class Records():
    def __init__(self, name, score, numKills, accuracy, controls):
        self.name = name
        self.score = score
        self.numKills = numKills
        self.accuracy = accuracy
        self.controls =controls

    def __str__(self):
        return "({0}, {1}, {2}, {3})".format(self.name, str(self.numKills), str(self.accuracy), str(self.controls))

dataList = []

dataList.append(Records('Steve',3762.0,47,82.46,1)) 
dataList.append(Records('Njabulo',19199.0,180,100.0,2)) 
dataList.append(Records('Andile',310.0,15,53.57,1)) 
dataList.append(Records('Cypher',11660.0,142,100.0,2)) 
dataList.append(Records('DryMeat',506.0,21,77.78,1)) 
dataList.append(Records('QhiteSponge',950.0,27,77.14,2)) 
dataList.append(Records('CCyFa',14837.0,172,100.0,1)) 
dataList.append(Records('Dickson',63.0,3,60.0,2)) 
dataList.append(Records('RazorSharp',25585.0,208,100.0,1)) 
dataList.append(Records('StickDull',4319.0,48,56.47,2)) 
dataList.append(Records('kILLErBoy',3091.0,62,79.49,1)) 
dataList.append(Records('ABC',863.0,24,63.16,2)) 
dataList.append(Records('GreatMuta',39982.0,252,100.0,1)) 
dataList.append(Records('SuperNove',4490.0,59,74.68,2)) 
dataList.append(Records('SmellyBum',891.0,15,51.72,1)) 
dataList.append(Records('TeethLess',8240.0,128,100.0,2)) 
dataList.append(Records('drytongue',876.0,24,88.89,1)) 
dataList.append(Records('sassypants',3369.0,59,75.64,2)) 
dataList.append(Records('Nicole',614.0,20,86.96,1)) 
dataList.append(Records('Mee',26443.0,241,100.0,2)) 
dataList.append(Records('TheOnly1',4948.0,103,100.0,1)) 
dataList.append(Records('m',0,0,0.0,2)) 
