import sys
import itertools
import multiprocessing as mp
import math



PRINTBOOKS = True

def main(infile):

	print(f"start {infile}")

	class Book:
		def __init__(self, index, score):
			self.index = index
			self.score = score
			self.rarity = 1



		def __repr__(self):
			return self.__str__()
		def __str__(self):
			stuff = dict(vars(self))
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
			self.booksMemory = tuple(books)
			# self.booksByIndex = dict()
			# for bookI, book in enumerate(books):
			# 	self.booksByIndex[book.index] = bookI
			

			
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





	rarityOffset = None




	with open("in/" + infile, 'r') as inf:

		infoLine = inf.readline().rstrip("\n")
		info = infoLine.split(" ")
		
		numBooks = int(info[0])
		numLib = int(info[1])
		
		bookToLib = list(map(lambda x: list(), [None] * numBooks))

		deadline = int(info[2])

		allBooks = list(map(lambda x: Book(x[0], int(x[1])), enumerate(inf.readline().rstrip("\n").split(" "))))

		libs = []
		for libIndex in range(0, numLib):
			libInfo = inf.readline().rstrip("\n").split(" ")

			books = list(map(lambda x: allBooks[int(x)], inf.readline().rstrip("\n").split(" ")))

			
			lib = Lib(libIndex, int(libInfo[1]), int(libInfo[2]), books)
			libs.append(lib)

			for book in books:
				bookToLib[book.index].append(lib)
				book.rarity += 1



	if rarityOffset == None:
		rarityOffset = [1] * numBooks
	else:
		for bookI, offset in enumerate(rarityOffset):
			allBooks[bookI].score *= offset



	for book in allBooks:
		book.score /= book.rarity


	# print(deadline)
	# print(libs)
	# print(bookScores)




	# initial book values berekenen


	for lib in libs:
		# initial sort
		lib.books.sort(key=lambda b: b.score, reverse=True)
		
		# initial lib value
		lib.score = sum(map(lambda b: b.score, lib.books[0:(deadline - lib.signupDays)*lib.troughput]))

			
		# initial lib book sort order berekenen


	solution = []
	while deadline > 0 and len(libs) > 0:


		# 1. beste lib vinden
		bestLib = None
		bestLibScore = 0
		for lib in libs:

			# TODO: rekening houden met deadline
			libScore = lib.score / lib.signupDays
			
			daysToProcessAll = lib.signupDays + len(lib.books) * lib.troughput
			if daysToProcessAll < deadline:
				libScore *= daysToProcessAll / deadline


			if libScore > bestLibScore:
				bestLibScore = libScore
				bestLib = lib










				

		if bestLib == None:
			break
		
		solution.append((bestLib.originalIndex, tuple(bestLib.books)))#, bestLib, bestLib.score))



		# 2. lib eruithalen
		if bestLib.index  == len(libs) - 1:
			libs.pop()
		else:
			libs[bestLib.index] = libs.pop()
			libs[bestLib.index].index = bestLib.index


		for book in bestLib.books:

			# 3. boeken er uit alle andere libs uithalen
			for lib in bookToLib[book.index]:
				# bookI = lib.booksByIndex[book.index]
				lib.books.remove(book)
				# TODO: here iets da nie remove is zoda het sneller is

				# boek weg, andere slechtere boek erbij
				lib.score -= book.score
				nextBookJustOutOfRangeIndex = (deadline - lib.signupDays)*lib.troughput
				if nextBookJustOutOfRangeIndex < len(lib.books) and nextBookJustOutOfRangeIndex >= 0:
					lib.score += lib.books[nextBookJustOutOfRangeIndex].score



		# 4. alle libs score aanpassen om het minder aantal dagen aan te geven:
		newDeadline = deadline - bestLib.signupDays
		for lib in libs:
			newDays = max(0, newDeadline - lib.signupDays)
			lib.score -= sum(map(lambda b: b.score, lib.books[newDays*lib.troughput:(deadline - lib.signupDays)*lib.troughput]))

		deadline = newDeadline





	


	# WORK IN PRORGESS: check duplicates of books
	# never finished this part:
	# the idea is that if a book comes in multiple libraries, penalize the worst libraries in the next
	# bookCount = [0] * numBooks
	# for (_, submittedBooks, lib) in solution:
	# 	for book in submittedBooks:
	# 		bookCount[book.index] += 1

	
	# for (_, submittedBooks, lib) in solution:
	# 	lib.subtractScore = 0

	# 	for book in submittedBooks:
	# 		if bookCount[book.index] > 1:
	# 			lib.subtractScore += book.score

	
	# lowestScoreLib = None
	# lowestScore = math.inf
	# for (_, submittedBooks, lib, submittedScore) in solution:

	# 	newScore = submittedScore - lib.subtractScore
	# 	if newScore < lowestScore:
	# 		lowestScoreLib = (_, submittedBooks, lib, submittedScore)
	# 		lowestScore = newScore

	
	





	# print(solution)


	with open("out" + infile, "w") as txt_file:
		txt_file.write(str(len(solution)))
		for s in solution:
			txt_file.write(f"\n{s[0]} {len(s[1])}")
			txt_file.write("\n" + " ".join(map(lambda x: str(x.index), s[1])) )


	print(f"done {infile}")






	for lib in libs:
		for book in lib.books:
			rarityOffset[book.index] *= 1.5


if __name__ == "__main__":
	main("b.txt")