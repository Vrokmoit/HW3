from multiprocessing import Pool, cpu_count
import time

def factorize_sync(*numbers):
    # Реалізація синхронної версії функції factorize
    results = []
    for number in numbers:
        factors = []
        for i in range(1, number + 1):
            if number % i == 0:
                factors.append(i)
        results.append(factors)
    return results

def factorize_single(number):
    # Допоміжна функція для паралельного обчислення factorize
    factors = []
    for i in range(1, number + 1):
        if number % i == 0:
            factors.append(i)
    return factors

def factorize_parallel(*numbers):
    # Реалізація паралельної версії функції factorize
    with Pool(processes=cpu_count()) as pool:
        return pool.map(factorize_single, numbers)

def test_factorize():
    a, b, c, d  = factorize_sync(128, 255, 99999, 10651060)
    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]
    print("All tests passed!")

if __name__ == "__main__":
    start_time = time.time()
    test_factorize()
    end_time = time.time()
    print(f"Sync execution time: {end_time - start_time:.6f} seconds")

    start_time = time.time()
    result = factorize_parallel(128, 255, 99999, 10651060)
    end_time = time.time()
    print(f"Parallel execution time: {end_time - start_time:.6f} seconds")
