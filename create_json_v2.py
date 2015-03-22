import json
import string
import tempfile
name_file = open('/data/MM1/corpora/SBU/SBU_captioned_photo_dataset_urls.txt')
caption_file = open('/data/MM1/corpora/SBU/SBU_captioned_photo_dataset_captions.txt')
roster_fin = open('/data/MM1/corpora/SBU/CrawlByUrl/roster')
train_size = 100
val_size = 10
i = 0
namelist = []
imgdic = {}
for line in roster_fin:
	imgdic[line.strip()] = 1
roster_fin.close()
cnt = 0
for i,line in enumerate(name_file):
	
	line = line.replace('\n','')
	s = line.split('/')
	namelist.append(s[-2]+'_'+s[-1])
	if imgdic.has_key(namelist[i]):
		cnt = cnt + 1
	if cnt >= train_size+val_size:
		break
images = []
cnt = 0
for i,line in enumerate(caption_file):
	#print 'i = '+str(i) + '\t len(namelist) = '+str(len(namelist))
	filename = namelist[i]
	if imgdic.has_key(filename):
		
		line = line.replace('\n','')
		temp = {}
		temp['filename'] = namelist[i]
		temp['imgid'] = cnt
		sen = [{}]
		s = line.replace(string.punctuation,' ')
		tokens = s.split()
		sen[0]['tokens'] = tokens
		sen[0]['raw'] = line
		sen[0]['imgid'] = cnt
		sen[0]['sentid'] = cnt
		temp['sentences'] = sen
		if cnt < train_size:
			temp['split'] = 'train'
		else:
			temp['split'] = 'val'
		temp['sentids'] = [cnt]
		images.append(temp)
		cnt = cnt + 1
	if cnt >= train_size+val_size:
		break
result = {}
result['images'] = images
result['dataset'] = 'toyset'

f = tempfile.NamedTemporaryFile(mode='w+')
json.dump(result, f)
f.flush()

print open(f.name, 'r').read()
