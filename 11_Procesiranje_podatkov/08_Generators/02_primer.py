# iterable - an object that has the __iter__ method defined
# iterator - an object that has both __iter__ and __next__ defined

if __name__ == "__main__":
    my_list = [1, 2, 3]
    my_list = iter(my_list)
    print(my_list)
    print(next(my_list))
    print(next(my_list))
    print(next(my_list))
    # print(next(my_list)) # dobimo  StopIteration napako

    # my_list = [1, 2, 3]

    # for el in iter(my_list):
    #     try:
    #         next(my_list)
    #         next(my_list)
    #         next(my_list)
    #     except StopIteration:
    #         pass
