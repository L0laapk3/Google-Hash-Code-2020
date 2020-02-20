import sys
import itertools
import multiprocessing as mp




PRINTBOOKS = False

def main(infile):



	class Book:
		def __init__(self, index, score):
			self.index = index
			self.originalIndex = index
			self.score = score
			self.rarity = 1



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



	class Lib:
		def __init__(self, index, signupDays, troughput, books):
			self.originalIndex = index
			self.index = index
			self.signupDays = signupDays
			self.troughput = troughput

			self.books = books
			self.booksByIndex = dict()
			for bookI, book in enumerate(books):
				self.booksByIndex[book.index] = bookI
			

			
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
		
		numBooks = int(info[1])
		numLib = int(info[1])
		
		bookToLib = list(map(lambda x: list(), [None] * numBooks))

		deadline = int(info[2])

		allBooks = list(map(Book, enumerate(inf.readline().split(" "))))

		libs = []
		for libIndex in range(0, numLib):
			libInfo = inf.readline().split(" ")

			books = map(lambda x: allBooks[int(x)], inf.readline().split(" "))
			for book in books:
				book.rarity += 1
				bookToLib[book.index].append(libIndex)

			lib = Lib(libIndex, int(libInfo[1]), int(libInfo[2]), list(books))
			libs.append(lib)



	# print(deadline)
	# print(libs)
	# print(bookScores)




	# initial book values berekenen
	for book in allBooks:
		book.value = book.score / book.rarity


	for lib in libs:
		# initial sort
		lib.books.sort(key=lambda b: b.value, reversed=True)
		
		# initial lib value
		lib.value = 0
		for book in lib.books[0:(deadline - lib.signupDays)*lib.troughput]:
			lib.value += book.value

			
		# initial lib book sort order berekenen


	solution = []
	while deadline < 0:


		# 1. beste lib vinden
		bestLib = None
		bestLibScore = 0
		for lib in libs:

			# TODO: rekening houden met deadline
			libScore = lib.value / lib.signupDays
			if libScore > bestLibScore:
				bestLibScore = libScore
				bestLib = lib
		
		solution.append(lib)



		# 2. lib eruithalen
		libs[bestLib.index] = libs.pop()
		libs[bestLib.index].index = bestLib.index


		for book in bestLib.books:

			# 4. boeken er uit alle andere libs uithalen
			for lib in bookToLib[book.index]:
				bookI = lib.booksByIndex[book.index]
				removedBook = lib.books.pop(bookI)
				lib.value -= removedBook

				# moet ook nog boeken in libs hersorteren


				
			# 3. book rarities aanpassen, zou eigenlijk nie nodig moeten zijn..
			book.score = 0
			book.value = 0





	print(libs)

	solution = libs


	with open("out" + infile, "w") as txt_file:
		txt_file.write(str(len(solution)))
		for lib in solution:
			txt_file.write(f"\n{lib.originalIndex} {len(lib.books)}")
			txt_file.write("\n" + " ".join(map(lambda x: str(x.originalIndex), lib.books)) )
