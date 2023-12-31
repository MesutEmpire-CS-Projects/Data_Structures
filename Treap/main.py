"""
Rough driver code for a student group maker
"""
import os

from Treap.student_group_maker import StudentGroupMaker, GroupMode


def main():
    print("Student Group Maker")
    print("-" * 20)
    path = input("Enter the path to the student information file: ")
    try:
        group_maker = StudentGroupMaker(path)
    except IOError:
        print(f"The file at '{path}', cannot be opened. Please check if the path is typed correctly")
        exit(1)
    except StudentGroupMaker.InvalidFileException:
        print(f"The file at '{path}' is not a csv file")
        exit(2)
    except StudentGroupMaker.DuplicateKeyException:
        print("The file has duplicate registration numbers. Please correct this first.")
        exit(3)
    except StudentGroupMaker.InvalidShapeException as e:
        print(e.args[0])
        exit(4)

    try:
        students_per_group = int(input("Enter the number of students per group: "))
        print("Group modes")
        print("-" * 10)
        print("1. Random")
        print("2. Ascending")
        print("3. Descending")

        group_mode_input = int(input("Enter group mode: "))
        if 1 <= group_mode_input <= 3:
            group_mode = GroupMode(group_mode_input)
        else:
            print("Invalid choice. Please choose 1, 2 or 3 for group mode")
            exit(5)

    except ValueError:
        # TODO: Handle this case appropriately, probably by forcing a loop until a valid value is entered
        print("Please enter a valid number")
        exit(6)

    group_maker.make_groups(students_per_group, group_mode)
    print(f"The file with groups is at .{os.sep}{StudentGroupMaker.OUTPUT_FILE}")


if __name__ == "__main__":
    main()
