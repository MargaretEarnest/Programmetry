from math import floor


# all possible colors for command line printing
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

startPhrase = ["Angels", "descend", "down", "from", "heaven"]
endPhrase = ["Demons", "ascend", "up", "to", "earth"]

# returns the integer representation of the n-th Gray code
def grayCode(n):
    return n ^ floor(n / 2)

# generates the n-th line of the poem using the n-th Gray code
def poemLine(n):
    gray = grayCode(n)
    # cycles through the bits in the Gray code and prints the
    # appropriate word with a space after it in the appropriate color
    for bit in reversed(range(len(startPhrase))):
        i = len(startPhrase) - 1 - bit
        print((bcolors.FAIL + (endPhrase[i].center(len(startPhrase[i]), " ") + bcolors.ENDC) if (gray >> bit) & 1 else (bcolors.OKCYAN + startPhrase[i].center(len(endPhrase[i]), " ") + bcolors.ENDC)), end=" ")
    print()

# prints out each line of the poem
for n in range(pow(2, len(startPhrase))):
    poemLine(n)
