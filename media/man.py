import csv

def read_file():
    with open("2.csv") as file:
        numbers = csv.reader(file)
        country_code="91"
        next(numbers)
        lst=[]
        for number in numbers:
            number=str(number)
            a=country_code+str(number[2:12])
            a=int(a)
            lst.append(a)

    return lst


if __name__ == '__main__':
    lst = read_file()
    print(lst)
