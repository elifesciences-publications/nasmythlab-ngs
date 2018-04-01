import re
from os import listdir
from os.path import isfile, join

# Replace with the path to your pileups
path = './'
files = [ f for f in listdir(path) if isfile(join(path,f)) ]
files = [ f for f in files if re.search("\.pileup$", f) ]


for f in files:

	chromosome = re.split("\r\n|\r|\n", open(join(path, f)).read())

	#Remove all lines that start with hash that have data in them (list comprehension)
	chromosomes = [line for line in chromosome if line and line[0] != '#']

	# Make dictionary (keys -> chromosomes)
	chromosome_library = {}
	for line in chromosomes:
		data = line.split('\t')

		if chromosome_library.get(data[1]):
			raise Exception("Duplicate key: " + data[1])

		if len(data) < 4:
			print f
			print data
	 	chromosome_library[data[1]] = data[3]

	# Read chromosome length
	chromosome_lengths = {
		'chrI': 230218,
		'chrII': 813184,
		'chrIII': 316620,
		'chrIV': 1531933,
		'chrV': 576874,
		'chrVI': 270161,
		'chrVII': 1090940,
		'chrVIII': 562643,
		'chrIX': 439888,
		'chrX': 745751,
		'chrXI': 666816,
		'chrXII': 1078177,
		'chrXIII': 924431,
		'chrXIV': 784333,
		'chrXV': 1091291,
		'chrXVI': 948066
	}
	chromosome_name = chromosomes[0].split('\t')[0]
	chromosome_length = chromosome_lengths.get(chromosome_name, 0)

	# Create new chromosome array with padded values
	padded_chromosome = []
	for base in range(1, chromosome_length + 1):
		padded_chromosome.append('\t'.join([
			chromosome_name, 
			str(base),
			'',
			str(chromosome_library.get(str(base), 0))
		]))
	
	output = join(path, chromosome_name+'.tabular')

	if isfile(output):
		raise Exception("Duplicate chromosome "+chromosome_name)

	results = open(output, 'w')
	results.write('\n'.join(padded_chromosome))
	results.close