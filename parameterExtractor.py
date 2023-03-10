import sys
from rdkit import Chem
from rdkit.Chem import Draw
from mordred import Calculator, Autocorrelation, Constitutional, Weight, MoeType, EState, InformationContent
import numpy as np
import pickle

smileString= sys.argv[1]
imageID = sys.argv[2]
uploadImagePath = "uploads/"+imageID+".png"

try:

    model = pickle.load(open("public/savedModel/GBReg_20230303.pkl", "rb"))

    featureList = ["CIC0", "ATSC0v", "Mv", "ATSC3v", "Mare", "AMW", "SMR_VSA9", "MATS1c", "IC0", "MATS2c", "SsSiH3"]
    mol = Chem.MolFromSmiles(smileString)
    Draw.MolToFile(mol, uploadImagePath)
    
    calc = Calculator([
        InformationContent.ComplementaryIC(order=0),
        Autocorrelation.ATSC(order=0,prop='v'),
        Constitutional.ConstitutionalMean(prop='v'),
        Autocorrelation.ATSC(order=3,prop='v'),
        Constitutional.ConstitutionalMean(prop='are'),
        Weight.Weight(),
        MoeType.SMR_VSA(k=9),
        Autocorrelation.MATS(order=1,prop='c'),
        InformationContent.InformationContent(order=0),
        Autocorrelation.MATS(order=2,prop='c'),
        EState.AtomTypeEState(type='count',estate='sSiH3')
    ])
    descrip = list(calc(mol))
    output = model.predict([descrip])
    print(round(output[0],2))
    
except Exception as e:
    print("ERROR") #print(e) # for troubleshooting
