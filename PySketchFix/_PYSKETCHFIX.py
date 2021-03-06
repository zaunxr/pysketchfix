# At first you have to make sure the package ast tokens is installed in your python directory
# Therefore: pip install asttokens from https://pypi.org/project/asttokens/.
# AT FIRST PLEASE SET UP THE CONFIGURATIONS FILE!

import PatchFinder
import SketchMaker

# Here you have to configure your Python Interpreter with which you want to run the process.
python_interpreter = "/Users/daniel/Bachelorarbeit/Python/bin/python"
# And also here you have to insert the directory to this project.
project_folder_location = "/Users/daniel/Bachelorarbeit/pysketchfix/PySketchFix/"

# The location where the sketch generator, ochiai and the patch finder are located.
sketch_generator = project_folder_location + "SketchMaker.py"
patch_finder = project_folder_location + "PatchFinder.py"

# Debuggers which are possible:
fault_localizer = project_folder_location + "FaultLocalizer.py"
OCHIAI = "ochiai"
TARANTULA = "tarantula"

# The buggy lines of the maximum bug file.
maximum_buggy_lines = "4,5"
maximum_bug_file = project_folder_location + "BugFile/maximum/maximum.py"
maximum_bug_file_test = project_folder_location + "BugFile/maximum/testsuite/test_maximum.py"
maximum_test_input = project_folder_location + "BugFile/maximum/tests_for_fault_localization/input_tests.txt"
# buggy_lines = maximum_buggy_lines
# bug_file = maximum_bug_file
# bug_file_test = maximum_bug_file_test
# test_input = maximum_test_input

# The buggy lines of the minimum bug file.
minimum_buggy_lines = "4,5"
minimum_bug_file = project_folder_location + "BugFile/minimum/minimum.py"
minimum_bug_file_test = project_folder_location + "BugFile/minimum/testsuite/test_minimum.py"
minimum_test_input = project_folder_location + "BugFile/minimum/tests_for_fault_localization/input_tests.txt"
# buggy_lines = minimum_buggy_lines
# bug_file = minimum_bug_file
# bug_file_test = minimum_bug_file_test
# test_input = minimum_test_input

# The buggy lines of the is prime bug file.
is_prime_buggy_lines = "6,5,3"
is_prime_bug_file = project_folder_location + "BugFile/is_prime/is_prime.py"
is_prime_bug_file_test = project_folder_location + "BugFile/is_prime/testsuite/test_is_prime.py"
is_prime_test_input = project_folder_location + "BugFile/is_prime/tests_for_fault_localization/input_tests.txt"
buggy_lines = is_prime_buggy_lines
bug_file = is_prime_bug_file
bug_file_test = is_prime_bug_file_test
test_input = is_prime_test_input

# The buggy lines of the positive indicator function.
positive_indicator_buggy_lines = "2,3"
positive_indicator_bug_file = project_folder_location + "BugFile/positive_indicator/" \
                                                         "positive_indicator.py"
positive_indicator_bug_file_test = project_folder_location + "BugFile/positive_indicator/testsuite/" \
                                                              "test_positive_indictator.py"
positive_indicator_test_input = project_folder_location + "BugFile/tests_for_fault_localization/tests_for_" \
                                                           "ochiai/input_tests.txt"
# buggy_lines = positive_indicator_buggy_lines
# bug_file = positive_indicator_bug_file
# bug_file_test = positive_indicator_bug_file_test
# test_input = positive_indicator_test_input

# The buggy lines of the mid bug file.
mid_buggy_lines = "6,2,1"
mid_bug_file = project_folder_location + "BugFile/mid/mid.py"
mid_bug_file_test = project_folder_location + "BugFile/mid/testsuite/test_mid.py"
mid_test_input = project_folder_location + "BugFile/mid/tests_for_ochiai/input_tests.txt"
# buggy_lines = mid_buggy_lines
# bug_file = mid_bug_file
# bug_file_test = mid_bug_file_test
# test_input = mid_test_input

# First run the fault localizer (Ochiai, Tarantula) to get the buggy lines (if you don't want to use your own).
# buggy_lines = FaultLocalizer.start_fault_localization(bug_file, test_input, OCHIAI)
# buggy_lines = FaultLocalizer.start_fault_localization(bug_file, test_input, TARANTULA)
# Run SketchFix
SketchMaker.generate_sketches(bug_file, buggy_lines)
PatchFinder.run_sketches(bug_file, bug_file_test)
# os.system(python_interpreter + " " + fault_localizer + " " + bug_file + " " + test_input + " " + TARANTULA)
# os.system(python_interpreter + " " + fault_localizer + " " + bug_file + " " + test_input + " " + OCHIAI)
# os.system(python_interpreter + " " + sketch_generator + " " + bug_file + " " + buggy_lines)
# os.system(python_interpreter + " " + sketch_runner + " " + bug_file + " " + bug_file_test)
