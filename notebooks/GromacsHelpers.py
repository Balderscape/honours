from IPython.core.display import Image

import os
import sys

import matplotlib as mplt
import matplotlib.pyplot as plt
import prettyplotlib as ppl


def plotXVG(ax, filename):
    infile=open(filename,'r')
    datax=[]
    datay=[]
    legends=[]
    first=True
    for line in infile:
        if line.find('@')!=-1 or line.find('#')!=-1: 
            sl=line.split()
            if len(sl)<3: continue
            if sl[2]=='legend':
                legends.append(sl[3])
            continue
            
        datax.append(float(line.split()[0]))
    
        if first:
          for i in range(1,len(line.split())):
            datay.append([])
          first=False
        
        for i in range(1,len(line.split())):
          datay[i-1].append(float(line.split()[i]))
        
    infile.close()
    
    
    for i in range(0,len(datay)):
        if len(legends)==len(datay):
           ppl.plot(ax,datax,datay[i],linewidth=2.0,label=legends[i])
#             ax.plot(datax,datay[i],linewidth=2.0,label=legends[i])
        else:
#             ax.plot(datax,datay[i],linewidth=2.0)
           ppl.plot(ax,datax,datay[i],linewidth=2.0)
        
    
def plotFigure(xvgfile):
    fig,ax = plt.subplots()
    plotXVG(ax, xvgfile)
    ppl.legend(ax)
#     plt.legend()



def pymolPlotStructure(filename):
    import __main__
    __main__.pymol_argv = ['pymol','-qc'] # Pymol: quiet and no GUI
    from time import sleep
    import pymol
    pymol.finish_launching()
    pymol.cmd.reinitialize()
    pymol.cmd.do("load %s"%filename)
    pymol.cmd.do("bg_color white")
    pymol.cmd.do("orient")
    pymol.cmd.do("show cartoon")
    pymol.cmd.do("show spheres, name CL")
    pymol.cmd.do("color yellow, name CL")
    pymol.cmd.do("dss")
    pymol.cmd.do("ray 640,480")
    pymol.cmd.do("png temp.png")
    sleep(2)
    return Image(filename='temp.png')

def pymolFlexibilityPlot(filename):
    import __main__
    __main__.pymol_argv = ['pymol','-qc'] # Pymol: quiet and no GUI
    from time import sleep
    import pymol
    pymol.finish_launching()
    pymol.cmd.reinitialize()
    pymol.cmd.do("load %s"%filename)
    pymol.cmd.do("bg_color white")
    pymol.cmd.do("intra_fit protein and (name c,n,ca)")
    pymol.cmd.do("orient")
    pymol.cmd.do("hide all")
    pymol.cmd.do("show cartoon")
    pymol.cmd.do("viewport 640,480")
    pymol.cmd.do("dss")
    pymol.cmd.do("set all_states=1")
    pymol.cmd.do("ray 640,480")
    pymol.cmd.do("png temp.png")
    sleep(10)
    return Image(filename='temp.png')


def pymolPlotGro(filename):
    os.system(". /home/ubuntu/gromacs-2016.2/bin/GMXRC; gmx editconf -f %s -o temp.pdb" % filename)
    return pymolPlotStructure("temp.pdb")