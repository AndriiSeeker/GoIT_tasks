from time import time
from multiprocessing import Pool, cpu_count


def factorize(*number):
    res = []
    for num in number:
        temp = []
        for i in range(1, num+1):
            if num % i == 0:
                temp.append(i)
        res.append(temp)
    return res


numbers = 128, 255, 99999, 10651060


def factorize2(num):
    res = []
    for i in range(1, num + 1):
        if num % i == 0:
            res.append(i)
    return res


if __name__ == '__main__':
    timer = time()
    a, b, c, d = factorize(128, 255, 99999, 10651060)
    print(f"Done by a loop {round(time() - timer, 4)}")

    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106,
                 1521580, 2130212, 2662765, 5325530, 10651060]

    timer = time()
    with Pool(cpu_count()) as pool:
        r = pool.map(factorize2, numbers)
    print(f"Done using multiprocessing {round(time() - timer, 4)} (Logical processors: {cpu_count()})")

    a, b, c, d = [i for i in r]
    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106,
                 1521580, 2130212, 2662765, 5325530, 10651060]
