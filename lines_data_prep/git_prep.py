"""
Reading the a customised git log output

To get files touched by commits:
	log --no-merges --name-only --pretty=oneline --after="2017-01-01" > ~/Desktop/email2git_data/raw_data/git_file_map.txt

To get the commit diffs:
	git log -p --no-merges --pretty=format:"%H,%an,%ae" --after="2017-01-01" > ~/Desktop/email2git_data/raw_data/commits_short.txt

"""
import re
import cPickle as pickle

class Commit:
	def __innit__(self,cid,name,email,lines):
		self.cid = cid
		self.name = name
		self.email = email
		self.lines = lines


INPUT_CID_FILE_MAP = "/Users/alexandrecourouble/Desktop/email2git_data/raw_data/git_file_map.txt"
INPUT_COMMIT_FILE = "/Users/alexandrecourouble/Desktop/email2git_data/raw_data/commits_short.txt"

OUTPUT_MAP = "/Users/alexandrecourouble/Desktop/email2git_data/COMMIT_MAP_PICKLED.txt"
OUTPUT_COMMITS = "/Users/alexandrecourouble/Desktop/email2git_data/COMMITS_PICKLED.txt"

COMMIT_FILE_MAP = {}

COMMITS = {}

def readCIDMap():
	with open(INPUT_CID_FILE_MAP) as f:
		currentCommit = ""
		for i in f:
			line = i.strip("\n")
			if re.match(r'\b[0-9a-f]{40}\b', line):
				currentCommit = line[:40]
				COMMIT_FILE_MAP[currentCommit] = []
			else:
				COMMIT_FILE_MAP[currentCommit].append(line)


def readCommits():
	with open(INPUT_COMMIT_FILE) as f:
		cid = ""
		authorName = ""
		authorEmail = ""
		lines = []

		for i in f:
			line = i.strip("\n")
			if re.match(r'\b[0-9a-f]{40}\b', line):
				# submit previously found data
				if cid != "":
					# COMMITS[cid] = Commit(cid,authorName,authorEmail,lines)
					COMMITS[cid] = {"name":authorName,"email":authorEmail,"lines":lines}
				# create next commit and reset LINES
				split = line.split(",")
				cid = split[0]
				authorName = split[1]
				authorEmail = split[2]
				lines = []
			elif line.startswith("+++") or line.startswith("---"):
				pass
			elif line.startswith("+") or line.startswith("-"):
				lines.append(line)




if __name__ == '__main__':
	readCIDMap()
	readCommits()

	with open(OUTPUT_MAP,"w") as f:
		f.write(pickle.dumps(COMMIT_FILE_MAP))

	with open(OUTPUT_COMMITS,"w") as f:
		f.write(pickle.dumps(COMMITS))	


	print COMMIT_FILE_MAP
	print len(COMMIT_FILE_MAP)