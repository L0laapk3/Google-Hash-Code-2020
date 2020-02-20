import sys
import itertools
import multiprocessing as mp

if len(sys.argv) > 1:
	infile = sys.argv[1] + ".txt"
else:
	infile = "b.txt"





PRINTBOOKS = False

class Lib:
	def __init__(self, index, signupDays, troughput, books):
		self.index = index
		self.signupDays = signupDays
		self.troughput = troughput
		self.books = books
		

		
	def __repr__(self):
		return self.__str__()
	def __str__(self):
		stuff = dict(vars(self))
		if not PRINTBOOKS:
			stuff["books"] = f"len({len(stuff['books'])}"
		for k in stuff:
			if isinstance(stuff[k], float):
				stuff[k] = round(stuff[k], 2)
		return str(stuff)



with open(infile, 'r') as inf:

	infoLine = inf.readline()
	info = infoLine.split(" ")
	
	numBooks = int(info[0])
	numLib = int(info[1])
	deadline = int(info[2])

	bookScores = tuple(map(lambda x: int(x), inf.readline().split(" ")))

	libs = []
	for libIndex in range(0, numLib):
		libInfo = inf.readline().split(" ")
		lib = Lib(libIndex, int(libInfo[1]), int(libInfo[2]), list(map(lambda x: int(x), inf.readline().split(" "))))
		libs.append(lib)


# print(deadline)
# print(libs)
# print(bookScores)


bookRarity = [1] * len(bookScores)
bookValue = [None] * len(bookScores)
for lib in libs:
	for bookI in lib.books:
		bookRarity[bookI] += 1



for bookI in range(len(bookScores)):
	bookValue[bookI] = bookScores[bookI] / bookRarity[bookI]

for lib in libs:
	lib.value = 0
	for bookI in lib.books:
		lib.value += bookValue[bookI]

	lib.weight = lib.value / lib.signupDays

	lib.books.sort(key=lambda b: bookValue[b], reverse=True)



libs.sort(key=lambda x: x.weight, reverse=True)


print(libs)

solution = libs


with open("out" + infile, "w") as txt_file:
    txt_file.write(str(len(solution)))
    for lib in solution:
        txt_file.write(f"\n{lib.index} {len(lib.books)}")
        txt_file.write("\n" + " ".join(map(str, lib.books)) )
