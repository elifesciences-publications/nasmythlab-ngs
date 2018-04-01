from __future__ import division
import re
from os import listdir
from os.path import isfile, join

#change this to the occupancy ratio derived for your sample.
occupancyRatio = 0.357608555
path = './'
files = [ f for f in listdir(path) if isfile(join(path,f)) ]
files = [ f for f in files if re.search("\.tabular$", f) ]

chromosome_filters = {
	'chrI': [91558, 211582],
	'chrII': [178299, 298323],
	'chrIII': [54477, 174501],
	'chrIV': [389821, 509821],
	'chrV': [92080, 212104],
	'chrVI': [88603, 208627],
	'chrVII': [436920, 556944],
	'chrVIII': [45586, 165610],
	'chrIX': [295721, 415745],
	'chrX': [376307, 496331],
	'chrXI': [380129, 500153],
	'chrXII': [90828, 210852],
	'chrXIII': [208125, 328875],
	'chrXIV': [568851, 688875],
	'chrXV': [266584, 386608],
	'chrXVI': [496049, 616073]
}

chromosome_names = [
	'chrI',
	'chrII',
	'chrIII',
	'chrIV',
	'chrV',
	'chrVI',
	'chrVII',
	'chrVIII',
	'chrIX',
	'chrX',
	'chrXI',
	'chrXII',
	'chrXIII',
	'chrXIV',
	'chrXV',
	'chrXVI'
]

filtered_chromosomes = {}

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

	 	chromosome_library[data[1]] = data[3]

	chromosome_name = chromosomes[0].split('\t')[0]
	chromosome_filter = chromosome_filters.get(chromosome_name, 0)

	filtered_chromosomes[chromosome_name] = []
	for base in range(chromosome_filter[0],chromosome_filter[1]+1):
		filtered_chromosomes[chromosome_name].append(chromosome_library.get(str(base), 0))

output = []
for index in range(0, 120000):
	output.append([])
	for chromosome_name in chromosome_names:
		output[index].append(int(filtered_chromosomes[chromosome_name][index]))
	
	average = sum(output[index]) / len(output[index])
	output[index].append(average)
	output[index].append(average * occupancyRatio)
	output[index].insert(0, index - 60000)

	for position, value in enumerate(output[index]):
		output[index][position] = str(value)

	output[index] = '\t'.join(output[index])

results = open('avgchr60.tabular', 'w')
results.write('\n'.join(output))
results.close
