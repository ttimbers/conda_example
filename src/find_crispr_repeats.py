# # Using Regular Expressions for finding DNA sequences of interest in Python
#
# Now that we have learned how to use regular expressions, let apply them using
# Python to find some DNA sequences of interest. In the first example we will
# look for key sequences that are part of the Crispr bacterial immune system.
#

# # Crispr - a bacterial immune system
#
# The CRISPR/Cas system is a bacterial immune system which gives bacteria
# resistance to plasmids and phages. Crispr spacers (see diagram below) from the
# Bacterium's genome recognize and help cut sequences complementary to the
# spacers in the plasmids and phages. Repeats from the bacterium's genome flank
#the spacers.
#
# load libraries
import screed
import re


# assign filename to variable
Genomefastafile = "data/Acidithiobacillus_ferrooxidans.fasta"

# Loop through all the records in fasta file and assign to
# variables (assuming only one genome is in the file)
for record in screed.open(Genomefastafile):
    Genome_seqname = record.name
    Genome_sequence = record.sequence

print "\n"
print "The Genome we are searching through for Crispr repeats is:"
print Genome_seqname
print Genome_sequence[1:100]
print "\n"

# ### Load Crispr repeat sequences
# assign filename to variable
Crisprfastafile = "data/Acidithiobacillus_ferrooxidans_Crispr.fasta"

# Create empty lists to append sequences to
Crispr_seqname = list()
Crispr_sequence = list()

# Loop through all the records in fasta file and add them the the lists
for record in screed.open(Crisprfastafile):
    Crispr_seqname.append(record.name)
    Crispr_sequence.append(record.sequence)

# zip the two lists together to make a dictionary
Crispr_repeats = dict(zip(Crispr_seqname, Crispr_sequence))

# print the dictionary to view the seqeunces and their names
print "The possible Crispr repeats to search for are in this dictionary:"
print Crispr_repeats
print "\n"

# ## Find Crispr repeats

# ### Access the sequence of a single repeat
# select the sequence from the dictionary by subsetting it's key
Crispr_repeats['NC_011761_1']




# ### Find a single repeat in genome
# use re.search to find sequence in genome, inputs are 1) pattern and 2) string
# to search for pattern
# '(' and ')' surround the string that you want to capture
first_repeat = re.search('(' + Crispr_repeats['NC_011761_1'] + ')', Genome_sequence)

# re.search object also has position information!
print 'The first occurence of the NC_011761_1 Crispr repeat is at:', first_repeat.span()
print "\n"

# ### Compile a pattern ahead of time for speed and readability
# specify and compile pattern ahead of time
NC_011761_1pattern = re.compile('(' + Crispr_repeats['NC_011761_1'] + ')')

# then use re.search
first_repeat = NC_011761_1pattern.search(Genome_sequence)


# ### Find unknown sequence between Crispr repeats
# put capture group between sequences
NC_011761_1spacerspattern = re.compile(Crispr_repeats['NC_011761_1'] + '([ATCG]+)' + Crispr_repeats['NC_011761_1'])

# search for all occurrences of pattern
first_repeat_spacers = NC_011761_1spacerspattern.search(Genome_sequence)
print 'The spacer sequence for this first repeat is:',  first_repeat_spacers.group(1)


# ### Find Crispr repeats and spacer
### Use re.findall to find multiple repeats and the spacer sequences!
NC_011761_1pattern = re.compile('(' + Crispr_repeats['NC_011761_1'] + ')' + '([ATCG]+)' + '(' + Crispr_repeats['NC_011761_1'] + ')' )

# search for all occurrences of pattern
first_repeat_matches = NC_011761_1pattern.search(Genome_sequence)
print 'The repeat sequence this first repeat is:', first_repeat_matches.group(1)
print "\n"

# ### Use re.findall to find multiple repeats
# specify and compile pattern ahead of time
NC_011761_1pattern = re.compile('(' + Crispr_repeats['NC_011761_1'] + ')')

# search for all occurrences of pattern
first_repeat_matches = NC_011761_1pattern.findall(Genome_sequence)

# ### Finding positions of multiple matches
# `re.findall()` is very useful for finding multiple sequences, but what if we
# want to find the positions of multiple sequences? For example, multiple
# repeats? To do this we need to use another function, `re.finditer()`:
# specify and compile pattern ahead of time
NC_011761_1pattern = re.compile('(' + Crispr_repeats['NC_011761_1'] + ')')

# search for all occurrences AND positions of pattern
first_repeat_matches = NC_011761_1pattern.finditer(Genome_sequence)

# loop over finditer object and print start position, end position and sequence
# (capture group)
print 'All the possible matches for this Crispr repeat are:'
for match in first_repeat_matches:
    print match.start(), match.end(), match.group(1)
