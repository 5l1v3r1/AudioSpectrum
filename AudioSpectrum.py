import librosa
import pygame
import numpy as np
from os import path
from librosa import display
import matplotlib.pyplot as plt

from Modules.audioBars import A_Bar

def clear():
    print (u"{}[2J{}[;H".format(chr(27), chr(27)))

mainWin = True
while mainWin:
    clear()
    print('''
 __                 _
/ _\_ __   ___  ___| |_ _ __ _   _ _ __ ___    _ __  _   _
\ \| '_ \ / _ \/ __| __| '__| | | | '_ ` _ \  | '_ \| | | |
_\ \ |_) |  __/ (__| |_| |  | |_| | | | | | |_| |_) | |_| |
\__/ .__/ \___|\___|\__|_|   \__,_|_| |_| |_(_) .__/ \__, |
   |_|                                        |_|    |___/
    ''')
    filename = str(input('Enter the song name: (Must be in Songs folder): '))
    filename_dir = 'Songs/{}'.format(filename)
    if path.exists(filename_dir):
        clear()
        break
    else:
        continue


print('\nAnalysing the song...')
time_series, sample_rate = librosa.load(filename_dir)
stft = np.abs(librosa.stft(time_series, hop_length=512, n_fft=2048*4))
spectrogram = librosa.amplitude_to_db(stft, ref=np.max)
frequencies = librosa.core.fft_frequencies(n_fft=2048*4)

times = librosa.core.frames_to_time(np.arange(spectrogram.shape[1]), sr=sample_rate, hop_length=512, n_fft=2048*4)
time_index_ratio = len(times)/times[len(times) - 1]
frequencies_index_ratio = len(frequencies)/frequencies[len(frequencies)-1]

if path.exists('plotImages/{}_plot.png'.format(filename.title())):
    print('')
else:
    print('\nSaving spectrum plot image in plotImages folder...')
    librosa.display.specshow(spectrogram,
                         y_axis='log', x_axis='time')
    plt.title('{} Spectrum.'.format(filename.title()))
    plt.colorbar(format='%+2.0f dB')
    plt.tight_layout()
    plt.savefig('plotImages/{}_plot.png'.format(filename.title()), dpi=300, bbox_inches='tight')
    print('Plot image saved.')


def get_decibel(target_time, freq):
    return spectrogram[int(freq * frequencies_index_ratio)][int(target_time * time_index_ratio)]

pygame.init()
pygame.display.set_caption('{} Spectrum'.format(filename.title()))
programIcon = pygame.image.load('Icons/gitCat.png')
pygame.display.set_icon(programIcon)



infoObject = pygame.display.Info()
screen_w = int(infoObject.current_w/2.5)
screen_h = int(infoObject.current_w/2.5)
screen = pygame.display.set_mode([screen_w, screen_h])

bars = []
frequencies = np.arange(100, 8000, 100)
r = len(frequencies)
width = screen_w/r

x = (screen_w - width*r)/2
for c in frequencies:
    bars.append(A_Bar(x, 300, c, (32, 105, 224) , max_height=500, width=width))
    x += width

t = pygame.time.get_ticks()
getTicksLastFrame = t
pygame.mixer.music.load(filename_dir)
pygame.mixer.music.play(0)

pyGameWin = True
while pyGameWin:

    t = pygame.time.get_ticks()
    deltaTime = (t - getTicksLastFrame) / 1000.0
    getTicksLastFrame = t


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pyGameWin = False

    #Change background color:
    screen.fill((0, 0, 0))

    for b in bars:
        b.update(deltaTime, get_decibel(pygame.mixer.music.get_pos()/1000.0, b.freq))
        b.render(screen)

    pygame.display.flip()

pygame.quit()
