import os
import sys
import subprocess
import logging

from IPython.core.display import Image
import matplotlib as mplt
import matplotlib.pyplot as plt
import prettyplotlib as ppl
import numpy as np

#GMXRC = '/usr/local/gromacs_gpu/bin/GMXRC';
GMXRC = '/home/ubuntu/gromacs-2016.2/bin/GMXRC';

def subprocess_cmd(command, input="", verbose=False):
    if (verbose):
        process = subprocess.Popen(command, stdin=subprocess.PIPE, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, shell=True)
    else:
        process = subprocess.Popen(command, stdin=subprocess.PIPE, stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)        
    
    (stdout, stderr) = process.communicate(input)
    print stdout.strip()

    
def gmx(command, input="", verbose=False):
    subprocess_cmd(". %s; gmx %s" % (GMXRC, command), input, verbose);

def runningMeanFast(x, N):
    return np.convolve(x, np.ones((N,))/N)[(N-1):]

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
    
    avg = runningMeanFast(datay[0], 100)
    
    for i in range(0,len(datay)):
        if len(legends)==len(datay):
           ppl.plot(ax,datax,datay[i],linewidth=2.0,label=legends[i])
           ppl.plot(ax,datax[0:-100],avg[0:-100],linewidth=2.0,label='Avg')
#             ax.plot(datax,datay[i],linewidth=2.0,label=legends[i])
        else:
#             ax.plot(datax,datay[i],linewidth=2.0)
           ppl.plot(ax,datax,datay[i],linewidth=2.0)
           ppl.plot(ax,datax[0:-100],avg[0:-100],linewidth=2.0)
        
    
def plotFigure(infile):
    fig,ax = plt.subplots()
    plotXVG(ax,infile)
    ppl.legend(ax)
    
def pymolPlotStructure(filename):
    stdout = sys.stdout
    import __main__
    __main__.pymol_argv = ['pymol','-qc'] # Pymol: quiet and no GUI
    from time import sleep
    import pymol
    pymol.finish_launching()
    sys.stdout = stdout
    pymol.cmd.reinitialize()
    pymol.cmd.do("load %s"%filename)
    pymol.cmd.do("bg_color white")
    pymol.cmd.do("orient")
    pymol.cmd.do("show cartoon")
    pymol.cmd.do("show spheres, name CL")
    pymol.cmd.do("color yellow, name CL")
    pymol.cmd.do("ray 320,240")
    pymol.cmd.do("png temp.png")
    sleep(2)
    return Image(filename='temp.png')

def pymolPlotGro(filename):
    gmx("editconf -f %s -o temp.pdb" % filename)
    return pymolPlotStructure("temp.pdb")

def video(fname, mimetype):
    """Load the video in the file `fname`, with given mimetype, and display as HTML5 video.
    """
    from IPython.display import HTML
    video_encoded = open(fname, "rb").read().encode("base64")
    video_tag = '<video controls alt="test" src="data:video/{0};base64,{1}">'.format(mimetype, video_encoded)
    return HTML(data=video_tag)

def pymolMakeMovie():
    stdout = sys.stdout
    import __main__
    __main__.pymol_argv = ['pymol','-qc'] # Pymol: quiet and no GUI
    from time import sleep
    import pymol
    pymol.finish_launching()
    sys.stdout = stdout
    pymol.cmd.reinitialize()
    pymol.cmd.do("load protein.pdb")
    pymol.cmd.do("bg_color white")
    pymol.cmd.do("intra_fit protein and (name c,n,ca)")
    pymol.cmd.do("orient")
    pymol.cmd.do("show cartoon")
    pymol.cmd.do("viewport 640,480")
    pymol.cmd.do("set ray_trace_frames,1")
    pymol.cmd.do("mpng frame_.png")
    sleep(20)
    os.system("mencoder \"mf://*.png\" -mf type=png:fps=18 -ovc lavc -o output.avi")
    os.system("ffmpeg -i output.avi -acodec libvorbis output.ogg")
    os.system("rm *.png")
    return video("output.ogg","ogg")
    
def pymolFlexibilityPlot(filename):
    stdout = sys.stdout
    import __main__
    __main__.pymol_argv = ['pymol','-qc'] # Pymol: quiet and no GUI
    from time import sleep
    import pymol
    pymol.finish_launching()
    sys.stdout = stdout
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
    pymol.cmd.do("ray 320,240")
    pymol.cmd.do("png temp.png")
    sleep(10)
    return Image(filename='temp.png')