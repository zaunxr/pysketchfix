import random

from Stores.Hole import Hole
from Stores.PatchStore import PatchStore


class COMTransformation:
    """
    The COM Transformation transforms comparison operations mainly between numbers and variables. Here the type of the
    transformation are hold, their operators and the current holes in the transformation. This is stored to ensure that
    in one testsuite execution one hole has a concrete value to it and only at the next testsuite execution the value is
    changed. This ensures that the hole value doesn't change if the hole is called once again.
    """
    TYPE = "COM"
    OPERATORS = ["!=", "==", "<", ">", ">=", "<=", "is", "not is"]
    current_holes = []

    @staticmethod
    def clear_current_holes():
        """
        If the testsuite execution (iteration) is over the current holes are deleted.
        """
        COMTransformation.current_holes = []

    @staticmethod
    def add_to_current_holes(hole_new):
        """
        A hole is appended to the array. If the hole is already in the array, a value error is raised. This could not be
        possible because in one execution a hole only can be reached one single time.

        :param hole_new: The new hole which is added to the array.
        :raise: RuntimeError: if the hole could not be inserted because it is already in the current holes.
        """
        for hole in COMTransformation.current_holes:
            if hole.is_equal(hole_new):
                raise RuntimeError(
                    "The hole:" + str(hole_new.to_array()) + " could not be inserted because it is already in the "
                    + COMTransformation.TYPE + " Transformation.")
        COMTransformation.current_holes.append(hole_new)

    @staticmethod
    def find_hole(hole_number):
        """
        The current holes array is searched for a specific hole number.

        :param hole_number: The hole number of the hole which is searched in the current holes.
        :return: the hole which is searched and none, if the hole number could not be found.
        """
        for hole in COMTransformation.current_holes:
            if hole.hole_number == hole_number:
                return hole
        return None

    @staticmethod
    def call(hole_number: int, line_number: int, parent: bool, left_value_array, right_value_array):
        """
        This method is called in the code of the bug file. This is actually the code which is executed instead of the
        original buggy code. At first the current holes is searched for the hole_number. If it is not already in the
        array then the operands are fetched from the array. If the current hole is none, the operands of the operation
        are fetched from the left and right value array. On the first position there is the operand as string
        representation on the second position the value. Be careful here: left and right values could also be
        transformations or whole code statements e.g. (a==b). Then a random operator is chosen ad the changed code and
        value is calculated.

        :param hole_number: The number of the hole in the code.
        :param line_number: The line where the hole is in the code.
        :param parent: If the transformation is in another transformation.
        :param left_value_array: The first element is the string representation of the operand, the second the value.
        :param right_value_array: The first element is the string representation of the operand, the second the value.
        :return: the value of the call if it has no parent, otherwise an array of the changed code as string and the
        value of it.
        :raise RuntimeError: If a the left or right value array contains more then 2 elements.
        """
        # If the length of the array is not 2 then the array input is wrong.
        if len(left_value_array) != 2 or len(right_value_array) != 2:
            raise RuntimeError("The array of the call method of hole: " + str(hole_number) + " is bigger then 2.")

        # Get the operand and the value of the given arrays.
        left_operand = str(left_value_array[0])
        left_operand_value = left_value_array[1]
        right_operand = str(right_value_array[0])
        right_operand_value = right_value_array[1]

        # First of all is searched, if the hole has already been called, then the variable which has been taken is now
        # taken again.
        current_hole = COMTransformation.find_hole(hole_number)
        if current_hole is not None:
            operator = current_hole.varoperator
            if operator is None:
                raise RuntimeError("The current hole with hole number: " + str(hole_number) + " is not found.")
        else:
            # Choose a random operator.
            randomNumber = random.randrange(0, len(COMTransformation.OPERATORS), 1)
            operator = COMTransformation.OPERATORS[randomNumber]

        # Assign the return value and choose the operation which is performed. The code which is now executed is
        # stored with variations. The changed code array contains the operation as string where (if it is possible)
        # left and right are also swapped to ensure that this hole are also possible in this way and that they
        # are the same operation.
        value = None
        changed_code_array = []
        if operator == ">=":
            value = left_operand_value >= right_operand_value
            changed_code_array = [left_operand + " >= " + right_operand,
                                  right_operand + " <= " + left_operand]

        elif operator == "<=":
            value = left_operand_value <= right_operand_value
            changed_code_array = [left_operand + " <= " + right_operand,
                                  right_operand + " >= " + left_operand]

        elif operator == "==":
            value = left_operand_value == right_operand_value
            changed_code_array = [left_operand + " == " + right_operand,
                                  right_operand + " == " + left_operand]

        elif operator == "!=":
            value = left_operand_value != right_operand_value
            changed_code_array = [left_operand + " != " + right_operand,
                                  right_operand + " != " + left_operand]

        elif operator == ">":
            value = left_operand_value > right_operand_value
            changed_code_array = [left_operand + " > " + right_operand,
                                  right_operand + " < " + left_operand]

        elif operator == "<":
            value = left_operand_value < right_operand_value
            changed_code_array = [left_operand + " < " + right_operand,
                                  right_operand + " > " + left_operand]

        elif operator == "is":
            # If right or left operand is digit or string, the normal compare is done, otherwise the obj.
            # compare is done.
            if right_operand.isdigit() or left_operand.isdigit() or isinstance(left_operand, str) \
                    or isinstance(right_operand, str):
                value = left_operand_value == right_operand_value
                changed_code_array = [left_operand + " == " + right_operand,
                                      right_operand + " == " + left_operand]
            else:
                value = left_operand_value is right_operand_value
                changed_code_array = [left_operand + " is " + right_operand,
                                      right_operand + " is " + left_operand]

        elif operator == "not is":
            # If right or left operand is digit or string, the normal compare is done, otherwise the obj.
            # compare is done.
            if right_operand.isdigit() or left_operand.isdigit() or isinstance(left_operand, str) \
                    or isinstance(right_operand, str):
                value = left_operand_value != right_operand_value
                changed_code_array = [left_operand + " != " + right_operand,
                                      right_operand + " != " + left_operand]
            else:
                value = not (left_operand_value is right_operand_value)
                changed_code_array = ["not(" + left_operand + " is " + right_operand + ")",
                                      "not(" + right_operand + " is " + left_operand + ")"]

        # Create a new current hole and add it to the current holes (if isn't already in it).
        # Here left operands equals right operand does not make any sense as well as to compare two numbers.
        # Only True/False conditions would appear. So only if this isn't the case add the hole to the current
        # holes and to the patches in the patch store. Also if the transformation is in another transformation
        # then this transformation will add the patch to the store.
        if current_hole is None:
            current_hole = Hole(hole_number, line_number, changed_code_array, COMTransformation.TYPE, operator)
            if not (left_operand == right_operand or (left_operand.isdigit() and right_operand.isdigit())):
                COMTransformation.add_to_current_holes(current_hole)
                if not parent:
                    PatchStore.add_hole_to_patch(current_hole)

        # If it has a parent then an array is returned which code is changed otherwise only the value is returned.
        # This is done because the parent is a transformation as well and has an left and right value array. Here
        # the transformation is represented as changed code and the value of the transformation.
        if not parent:
            return value
        else:
            return [current_hole.array_of_changed_code[0], value]
