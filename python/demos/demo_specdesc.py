#! /usr/bin/env python

import sys
from aubio import fvec, source, pvoc, specdesc
from numpy import hstack

win_s = 512                 # fft size
hop_s = win_s / 4           # hop size

if len(sys.argv) < 2:
    print "Usage: %s <filename> [samplerate]" % sys.argv[0]
    sys.exit(1)

filename = sys.argv[1]

samplerate = 0
if len( sys.argv ) > 2: samplerate = int(sys.argv[2])

s = source(filename, samplerate, hop_s)
samplerate = s.samplerate

pv = pvoc(win_s, hop_s)

methods = ['default', 'energy', 'hfc', 'complex', 'phase', 'specdiff', 'kl', 'mkl',
    'specflux', 'centroid', 'spread', 'skewness', 'kurtosis', 'slope', 'decrease',
    'rolloff', ]

all_descs = {}
o = {}

for method in methods:
    cands = []
    all_descs[method] = fvec(0)
    o[method] = specdesc(method, win_s)

total_frames = 0
downsample = 2

while True:
    samples, read = s()
    fftgrain = pv(samples)
    print "%f" % ( total_frames / float(samplerate) ),
    for method in methods:
        specdesc_val = o[method](fftgrain)[0]
        all_descs[method] = hstack ( [all_descs[method], specdesc_val] )
        print "%f" % specdesc_val,
    print
    total_frames += read
    if read < hop_s: break

if 1:
    print "done computing, now plotting"
    import matplotlib.pyplot as plt
    from demo_waveform_plot import get_waveform_plot
    fig = plt.figure()
    plt.rc('lines',linewidth='.8')
    wave = plt.axes([0.1, 0.75, 0.8, 0.19])
    get_waveform_plot(filename, samplerate, ax = wave )
    wave.yaxis.set_visible(False)
    wave.xaxis.set_visible(False)

    all_desc_times = [ x * hop_s  for x in range(len(all_descs["default"])) ]
    n_methods = len(methods)
    for i, method in enumerate(methods):
        #ax = fig.add_subplot (n_methods, 1, i)
        #plt2 = plt.axes([0.1, 0.1, 0.8, 0.65], sharex = plt1)
        ax = plt.axes ( [0.1, 0.75 - ((i+1) * 0.65 / n_methods),  0.8, 0.65 / n_methods], sharex = wave )
        ax.plot(all_desc_times, all_descs[method], '-', label = method)
        #ax.set_ylabel(method, rotation = 0)
        ax.xaxis.set_visible(False)
        ax.yaxis.set_visible(False)
        ax.axis(xmax = all_desc_times[-1], xmin = all_desc_times[0])
        ax.annotate(method, xy=(-10, 10),  xycoords='axes points',
                horizontalalignment='right', verticalalignment='bottom',
                )
    if all_desc_times[-1] / float(samplerate) > 60:
        plt.xlabel('time (mm:ss)')
        ax.set_xticklabels([ "%02d:%02d" % (t/float(samplerate)/60, (t/float(samplerate))%60) for t in ax.get_xticks()[:-1]], rotation = 50)
    else:
        plt.xlabel('time (ss.mm)')
        ax.set_xticklabels([ "%02d.%02d" % (t/float(samplerate), 100*((t/float(samplerate))%1) ) for t in ax.get_xticks()[:-1]], rotation = 50)
    #plt.ylabel('spectral descriptor value')
    ax.xaxis.set_visible(True)
    plt.show()