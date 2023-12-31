import os
import random
from enum import Enum, auto
from typing import Union

from Treap.treap import Treap, TreapNode


class GroupMode(Enum):
    RANDOM = auto()
    ASCENDING = auto()
    DESCENDING = auto()


class Student:
    """
    A class representing a student
    This class overrides the __lt__, __gt__ and __ea__ methods since its
    instances are to be used as keys
    """

    def __init__(self, name: str, reg_no: str):
        self.name = name
        self.reg_no = reg_no
        self.group = 0  # Default group

    def __lt__(self, other):
        if isinstance(other, Student):
            return self.reg_no < other.reg_no

    def __gt__(self, other):
        if isinstance(other, Student):
            return self.reg_no > other.reg_no

    def __eq__(self, other):
        if isinstance(other, Student):
            return self.name == other.name and self.reg_no == other.reg_no

    def __str__(self):
        return f"Student({self.name}, {self.reg_no}, {self.group})"

    def __repr__(self):
        return f"Student({self.name}, {self.reg_no})"


class StudentGroupMaker(Treap):
    """
    A class that can make groups from a csv file containing a list of students and their registration numbers.
    """
    OUTPUT_FILE = "grouped.csv"

    class InvalidFileException(Exception):
        pass

    class InvalidShapeException(Exception):
        pass

    def __init__(self, file_name: Union[str | os.PathLike | bytes]):
        """
        Creates a new student group maker from the file given.
        The file has to be a csv file (for now)
        """
        super().__init__()
        self.file_name = file_name
        if not self.file_name.endswith(".csv"):
            raise self.InvalidFileException("Expected a .csv file")

        if self.file_has_desired_shape():
            self.populate_from_file()

    def file_has_desired_shape(self) -> bool:
        """
        Tests whether the file has a valid shape, in this case, whether it
        consists of two columns all through.
        May also include test to see whether all the items in the reg no column are
        registration numbers, but that seems overkill
        """
        with open(self.file_name) as file:
            i = 0
            for line in file.readlines():
                # Confirm that the groups column has been created
                if len(line.split(",")) != 2:
                    raise self.InvalidShapeException("The file should only have two columns, name and reg.no")
                i += 1

        return True

    def populate_from_file(self):
        """Adds student names and registration numbers from a file"""
        with open(self.file_name) as file:
            index = 0
            for line in file:
                # This condition will ensure that we skip the header
                if index > 0:
                    fields = line.replace("\n", "").split(",")
                    if fields:
                        [name, reg_no] = fields
                        self.insert(Student(name, reg_no))

                index += 1

    def make_groups(self, students_per_group: int, mode: GroupMode = GroupMode.RANDOM):
        """
        Creates a csv file (grouped.csv) in the current directory
        populated with the groups that each student is placed.
        Groups differ in length by at most 1 member
        :param mode: Determines the order in which the students will be arranged, which,
            by default, is random (but not really random).
            The arrangement is with reference to the registration numbers.
        :param students_per_group: Denotes the number of students each group_number will have.
                Will put all the students into one group_number if it is greater
                than the number of students in the file
        """
        # This achieves randomization by performing a preorder traversal through the treap
        # in which it stores the info. Since the items are inserted with random priority
        # and the treap gets shifted many times as elements are inserted to it, there is a very
        # small chance that the order in the output file will be the same as it was in the input file
        if students_per_group <= 0:
            raise ValueError("The value of students_per_group must be a positive integer")

        student_counter = 0
        # Equals to the number of complete groups + 1
        # in the case of an oddly divisible students_per_group
        group_number = 0

        iterator = random.choice([self.preorder(), self._postorder(self.root)])
        match mode:
            case GroupMode.RANDOM:
                pass  # Already set to self.preorder()
            case GroupMode.ASCENDING:
                iterator = self.__iter__()
            case GroupMode.DESCENDING:
                iterator = self._inorder_reverse(self.root)

        student_list: list[Student] = []
        for student in iterator:
            if student_counter % students_per_group == 0:
                group_number += 1

            student.group = group_number
            student_list.append(student)
            student_counter += 1

        # Handle the adding the members of incomplete groups to random groups
        students_remaining = student_counter % students_per_group

        if 0 < students_remaining < students_per_group - 1:
            new_group = random.randrange(1, group_number)
            for i in range(students_remaining):
                student_list[(student_counter - 1) - i].group = new_group
                new_group += 1
                if new_group >= group_number:
                    new_group = 1

            student_list = sorted(student_list, key=lambda s: s.group)

        with open(self.OUTPUT_FILE, "w") as output_file:
            output_file.write(f"NAME,REG NO,GROUP\n")
            for student in student_list:
                output_file.write(f"{student.name},{student.reg_no},{student.group}\n")

    def _inorder_reverse(self, root: TreapNode):
        if root is not None:
            yield from self._inorder_reverse(root.right)
            yield root.key
            yield from self._inorder_reverse(root.left)

    def _postorder(self, root: TreapNode):
        if root is not None:
            yield from self._inorder_reverse(root.left)
            yield from self._inorder_reverse(root.right)
            yield root.key

    def number_of_students(self):
        return len(self)
