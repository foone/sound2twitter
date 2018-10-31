import sys, subprocess, json, os, math, pdb, glob
from PIL import Image
FRAMERATE = 15*2
W=640
H=240
PRETWIT = 'PRETWIT.mkv'
PRETWIT2 = 'PRETWIT2.mkv'
MONO = 'mono.wav'
SILENT='silence.wav'
MINLENGTH=7
PADDING=True

def erase_temp_files():
	paths = [PRETWIT, PRETWIT2, MONO, 'out.wav','out.mp4', 'waveform.png','greyform.png', SILENT]+glob.glob('frames/*.png')
	for path in paths:
		try:
			os.unlink(path)
		except OSError:
			pass
	if os.path.exists('frames'):
		try:
			os.rmdir('frames')
		except OSError:
			pass

erase_temp_files()
path=sys.argv[1]
OUTFILE=os.path.splitext(path)[0]+'.mp4'
info = json.loads(subprocess.check_output(['ffprobe','-v','quiet','-print_format','json','-show_format','-show_streams',path]))

seconds = float(info['format']['duration'])
frames = int(seconds * FRAMERATE)
waveform_path = path
if info['streams'][0]['channels']>1:
	print 'Stereo input found! Downmixing to mono for images, will retain stereo for output video'
	subprocess.check_call(['ffmpeg','-v','quiet','-i',path,'-ac','1', MONO])
	waveform_path = MONO
subprocess.check_call(['ffmpeg','-v','quiet','-i',waveform_path,'-lavfi','showwavespic=split_channels=1:s={}x{}:scale=lin'.format(W,H),'-y','waveform.png'])
subprocess.check_call(['magick','convert','waveform.png','-modulate','140,0,100','png32:greyform.png'])
spot_width = int(math.ceil(float(W)/frames))
background = Image.open('greyform.png')
foreground = Image.open('waveform.png')

subprocess.check_call(['ffmpeg','-v','quiet','-f','lavfi','-i','anullsrc','-t','7','-c:a','pcm_s16le',SILENT])
subprocess.check_call(['ffmpeg','-v','quiet','-i',SILENT,'-i',path,'-filter_complex','amerge','-ac','1','-c:a','pcm_s16le','out.wav'])
paths=[]
try:
	os.mkdir('frames')
except OSError:
	pass
for i in range(frames):
	out = Image.new('RGBA',(W,H))
	out.paste((255,255,255),(0,0,W,H))
	out.paste(background,(0,0),background)
	#out.alpha_composite(background)
	box = (0,0,i*spot_width,H-1)
	forecrop = foreground.crop(box)
	out.paste(forecrop,box,forecrop)
	outpath='frames/im%08d.png' % i
	paths.append(outpath)
	out.convert('RGB').save(outpath)

subprocess.check_call(['ffmpeg','-y','-v','quiet','-r',str(FRAMERATE),'-i','frames/im%08d.png','-i',path,'-acodec','copy',PRETWIT])

addlength=int(math.ceil(MINLENGTH-seconds))

if PADDING and addlength>0:
	subprocess.check_call(['ffmpeg','-y','-v','quiet','-loop','1','-y','-i',paths[-1],'-t',str(addlength),'padding.mkv'])

	with open('concat.txt','w') as f:
		print >>f,'file',PRETWIT
		print >>f,'file','padding.mkv'

	subprocess.check_call(['ffmpeg','-y','-v','quiet','-f','concat','-safe','0','-i','concat.txt','-c','copy',PRETWIT2])
else:
	PRETWIT2=PRETWIT
subprocess.check_call("ffmpeg -y -v quiet -i {} -pix_fmt yuv420p -vcodec libx264 -vf scale=640:-1 -acodec aac -vb 1024k -minrate 1024k -maxrate 1024k -bufsize 1024k -ar 44100  -ac 2  -strict experimental -r 30  \"{}\"".format(PRETWIT2,OUTFILE))


erase_temp_files()