import sys
import multiprocessing as mp
from multiprocessing import Pool
from main import main


if __name__ == '__main__':
    with Pool(6) as p:
        p.map(main,["a.txt", "b.txt", "c.txt","d.txt","e.txt","f.txt"])