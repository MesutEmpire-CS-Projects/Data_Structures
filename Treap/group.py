import csv

from treap import Treap


class Groupmaking(Treap):
    def __init__(self, csv_file_path):
        super().__init__()
        self.csv_file_path = csv_file_path
        self.load_students_from_csv()

    def insert_student(self, admission_number, name):
        self.insert(name)
        self.save_students_to_csv()

    def delete_student(self, name):
        self.delete(name)
        self.save_students_to_csv()

    def split_group(self, name):
        left, right = self.split(name)

        left_group = Groupmaking("left_split.csv")
        right_group = Groupmaking("right_split.csv")

        left_group.root = left.root
        right_group.root = right.root

        left_group.save_students_to_csv()
        right_group.save_students_to_csv()

        return iter(left), iter(right)

    def merge_groups(self, left_treap, right_treap):
        merged_group = Groupmaking("final_merge.csv")
        treap = self.merge(left_treap, right_treap)
        merged_group.root = treap.root
        merged_group.save_students_to_csv()
        return iter(merged_group)

    def load_students_from_csv(self):
        try:
            with open(self.csv_file_path, 'r') as file:
                reader = csv.reader(file, delimiter=',')
                index = 0
                for row in reader:
                    if index > 0:
                        name, admission_number = row
                        self.insert_student(admission_number, name)
                        print(f'Inserted : {name}')
                    index += 1

                print(f'Inserted {index} students to treap ')
        except FileNotFoundError:
            pass

    def save_students_to_csv(self):
        print(f"{self.csv_file_path}")
        if self.root is not None:
            with open(self.csv_file_path, 'w', newline='') as file:
                fieldnames = ['NAME', 'PRIORITY']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()

                for student in self:
                    print(f"Student : {student}")
                    writer.writerow({'NAME': student['key'], "PRIORITY": student['priority']})
        else:
            print("Treap is empty. No data to save to the CSV file.")
