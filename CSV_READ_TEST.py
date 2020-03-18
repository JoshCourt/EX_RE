# CSV READING TEST
import csv



def csv_read(CSV_Path):
    TCs = set()
    with open(CSV_Path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            print(row)
            for _ in row:
                print(_)
                TCs.add(_)
    return TCs

csv_read("Template_2.csv")
