"""
Rough driver code for a student group maker
"""
from Treap.student_group_maker import StudentGroupMaker


def main():
    print("Student Group Maker")
    path = input("Enter the path to the student information file: ")
    try:
        group_maker = StudentGroupMaker(path)
    except IOError:
        print(f"The file {path}, cannot be opened.")
        exit(1)
    except StudentGroupMaker.InvalidFileException:
        print("The file must be a csv file")
        exit(2)

    try:
        students_per_group = int(input("Enter the number of students per group: "))
    except ValueError:
        # TODO: Handle this case appropriately
        print("Please enter a valid number")
        exit(3)

    group_maker.make_groups(students_per_group)
    print(f"The file with groups is at ./{StudentGroupMaker.OUTPUT_FILE}")


if __name__ == "__main__":
    main()
