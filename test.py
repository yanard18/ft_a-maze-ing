from typing import Generator
# print("hello")


def gen() -> Generator[int, None, None]:
    i = 0
    while True:
        i += 1
        yield i


if __name__ == "__main__":
    g = gen()
    for _ in range(3):
        print(next(g))
