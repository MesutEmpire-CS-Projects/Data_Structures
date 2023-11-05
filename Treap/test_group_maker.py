import unittest

from Treap.student_group_maker import StudentGroupMaker, GroupMode


class TestConstructor(unittest.TestCase):
    def test_constructor_with_non_csv_file(self):
        with self.assertRaises(StudentGroupMaker.InvalidFileException):
            StudentGroupMaker("./file.cs")

    def test_constructor_with_valid_csv(self):
        group_maker = StudentGroupMaker("./file.csv")

        # The number of students should be one less than the number of lines
        # in the file
        with open("./file.csv") as file:
            self.assertEqual(len(file.readlines()) - 1, len(group_maker))

    def test_with_non_existent_csv(self):
        with self.assertRaises(IOError):
            StudentGroupMaker("./file1.csv")

    def test_with_csv_containing_duplicate_reg_no(self):
        with self.assertRaises(StudentGroupMaker.DuplicateKeyException):
            StudentGroupMaker("./containing_duplicates.csv")

    def test_with_csv_with_invalid_shape(self):
        with self.assertRaises(StudentGroupMaker.InvalidShapeException):
            StudentGroupMaker("./invalid_shape.csv")


class TestMakeGroupsMethod(unittest.TestCase):
    def test_output_file_created(self):
        group_maker = StudentGroupMaker("file.csv")
        group_maker.make_groups(5)

        with open("grouped.csv"):
            pass

    def test_output_file_valid(self):
        # TODO: Make this test more granular
        group_maker = StudentGroupMaker("file.csv")
        group_maker.make_groups(5)

        with open("grouped.csv") as file:
            self.assertEqual(len(group_maker) + 1, len(file.readlines()))
            i = 0
            for line in file.readlines():
                with self.subTest(line=i):
                    # Confirm that the groups column has been created
                    self.assertEqual(3, len(line.split(",")))
                    i += 1

    def test_group_modes(self):
        group_maker = StudentGroupMaker("file.csv")
        group_maker.make_groups(5, GroupMode.ASCENDING)

        with self.subTest(group_mode=GroupMode.ASCENDING):
            with open(StudentGroupMaker.OUTPUT_FILE) as file:
                lines = file.readlines()
                for i in range(1, len(lines) - 1):
                    with self.subTest(line_number=i):
                        (_, current_reg, _) = self._split_output_line(lines[i])
                        (_, next_reg, _) = self._split_output_line(lines[i + 1])
                        self.assertTrue(current_reg < next_reg)

        group_maker.make_groups(5, GroupMode.DESCENDING)

        with self.subTest(group_mode=GroupMode.DESCENDING):
            with open(StudentGroupMaker.OUTPUT_FILE) as file:
                lines = file.readlines()
                for i in range(1, len(lines) - 1):
                    with self.subTest(current_reg=lines[i], next_reg=lines[i + 1]):
                        (_, current_reg, _) = self._split_output_line(lines[i])
                        (_, next_reg, _) = self._split_output_line(lines[i + 1])
                        self.assertTrue(current_reg > next_reg)

    @staticmethod
    def _split_output_line(line: str) -> (str, str, str):
        (name, reg_no, group) = line.replace("\n", "").split(",")

        return name, reg_no, group


if __name__ == '__main__':
    unittest.main()
