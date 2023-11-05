from Treap.group import Groupmaking


def main():
    csv_file_path = input("Enter the CSV file path: ")
    groupmaker = Groupmaking(csv_file_path)
    while True:
        choice = input(
            "1. Insert Student\n2. Delete Student\n3. Split Group\n4. Merge Groups\n5. Exit\nEnter your choice: ")

        if choice == '1':
            admission_number = input("Enter admission number: ").upper()
            name = input("Enter student name: ").upper()
            groupmaker.insert_student(admission_number, name)
        elif choice == '2':
            name = input("Enter name to delete: ").upper()
            groupmaker.delete_student(name)
        elif choice == '3':
            name = input("Enter name for split: ").upper()
            left_group, right_group = groupmaker.split_group(name)
            print("Left Group:", left_group)
            print("Right Group:", right_group)
        elif choice == '4':
            left_csv_file_path = input("Enter the CSV file path for the left group: ")
            right_csv_file_path = input("Enter the CSV file path for the right group: ")
            left_treap = Groupmaking(left_csv_file_path)
            right_treap = Groupmaking(right_csv_file_path)
            merged_treap = groupmaker.merge_groups(left_treap, right_treap)
        elif choice == '5':
            break


if __name__ == "__main__":
    main()

