import os,sys
import json
import string
import tempfile
name_file = open('/data/MM1/corpora/SBU/SBU_captioned_photo_dataset_urls.txt')
caption_file = open('/data/MM1/corpora/SBU/SBU_captioned_photo_dataset_captions.txt')
roster_fin = open('/data/MM1/corpora/SBU/CrawlByUrl/roster')
image_dir = '/data/MM1/corpora/SBU/CrawlByUrl/sbu_images_crawled'
train_size = 400000
val_size = 100000

i = 0
namelist = []
imgdic = {}
for line in roster_fin:
	if os.path.isfile(os.path.join(image_dir,line.strip())):
		imgdic[line.strip()] = 1
roster_fin.close()

cnt = 0
i = 0
for line in name_file:
        line = line.replace('\n','')
        s = line.split('/')
        namelist.append(s[-2]+'_'+s[-1])

        if imgdic.has_key(namelist[i]):
                cnt = cnt + 1
        i = i + 1
        if cnt >= train_size+val_size:
                break
name_file.close()
sys.stderr.write('finished reading roster file\n')
print '{"images":[',
cnt = 0
i = 0
for line in caption_file:
        filename = namelist[i]
        if i%1000 == 0:
                sys.stderr.write(str(i)+'\n')
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
                cnt = cnt + 1
                f = tempfile.NamedTemporaryFile(mode='w+')
                json.dump(temp, f)
                f.flush()
                print open(f.name, 'r').read(),
                if cnt < train_size+val_size:
                        print ',',
                if cnt >= train_size+val_size:
                        break
        i = i + 1
caption_file.close()
print '], "dataset": "toyset"}'
