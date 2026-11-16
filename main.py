from pathlib import Path
import os
import requests


processed = {}

def readFile(filepath:str):
	with open(file=filepath,mode='r') as data:
		return data.read()

def getListFiles(path:str):
	return os.listdir(path)

def getFileFromUrl(url,timeout=3000):
	response = requests.get(url=url,timeout=timeout)
	response.raise_for_status()
	return response.text

def proceseUrls(file,namefile:str):
	for line in file.split('\n'):
		if not line.startswith('0.0.0.0'):
			continue
		if line in processed:
			processed[line].append(namefile)
		if line not in processed:
			processed[line]=[]
	
def saveFile(conten:str, filPahtSave:str):
	with open(filPahtSave,'w',encoding='utf-8') as file:
		file.write(conten)

listRepositories=[
    "https://raw.githubusercontent.com/crazy-max/WindowsSpyBlocker/master/data/hosts/spy.txt",
    "https://raw.githubusercontent.com/crazy-max/WindowsSpyBlocker/master/data/hosts/update.txt",
    "https://raw.githubusercontent.com/Strappazzon/teleme7ry/master/src/rules.txt",
    "https://media.githubusercontent.com/media/zachlagden/Pi-hole-Optimized-Blocklists/main/lists/advertising.txt",
    "https://raw.githubusercontent.com/crazy-max/WindowsSpyBlocker/master/data/hosts/extra.txt",
    "https://media.githubusercontent.com/media/zachlagden/Pi-hole-Optimized-Blocklists/main/lists/malicious.txt",
    "https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts",
    "https://media.githubusercontent.com/media/zachlagden/Pi-hole-Optimized-Blocklists/main/lists/nsfw.txt",
    "https://media.githubusercontent.com/media/zachlagden/Pi-hole-Optimized-Blocklists/main/lists/tracking.txt"
]
baseroute = Path.cwd()
filesfolder = 'files'
resultfolder = 'results'
filespath = Path.joinpath(baseroute,filesfolder)
resultpath = Path.joinpath(baseroute,resultfolder)

if not filespath.exists():
	os.mkdir(str(filespath))

if not resultpath.exists():
	os.mkdir(str(resultpath))

filesSaved=getListFiles(str(filespath))
filesProceced=getListFiles(str(resultpath))

print("##### PROSESSING #####")
for repository in listRepositories:

	namefile =repository.split('/')[-1]
	print(namefile)
	alreadysaved=namefile in filesSaved

	file = filesSaved[alreadysaved] if alreadysaved else None
	if namefile in filesProceced:
		print('skiping file: ',namefile,'already exists.')
		continue

	if not file :
		file = getFileFromUrl(repository)
		saveFile(file,str(filespath.joinpath(namefile)))
	else:
		file = readFile(str(filespath.joinpath(namefile)))

	proceseUrls(file,namefile)

archivos={}

def existsFile(file:str):
	return file in archivos

def processFile(file:str,url:str):
	if  not existsFile(file):
		archivos[file]=[url]
	if existsFile(file):
		archivos[file].append(url)

print('### generating files ###')
for url,files in processed.items():
	if len(files)>1:
		processFile('duplicated.txt',url)
	elif len(files)==1:
		processFile(files[0],url)

print('### saving files ###')

for file,urls in archivos.items():
	urlslist='\n'.join(urls)
	saveFile(urlslist,str(resultpath.joinpath(file)))
	print('saved: ',str(resultpath.joinpath(file)))
