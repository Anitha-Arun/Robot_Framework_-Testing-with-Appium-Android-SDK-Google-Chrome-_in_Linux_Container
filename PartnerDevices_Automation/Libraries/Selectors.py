"""
Global get-JSON-from-file implementation.
"""
import os
import json
import traceback

# Use BuiltIn().log_to_console() for debugging - load_json_file() is called
#   at module load, not runtime, so 'print()' is not active yet:
# from robot.libraries.BuiltIn import BuiltIn


def load_json_file(filename):
    """
    Return the JSON from JSON a file.
    Params:
        filename: The JSON file to open and read.
    """

    def _loadit(fullfilename):
        with open(fullfilename) as reader:
            return json.loads(reader.read())

    # Use abspath() so failures show the actual path used.
    fullfilename = os.path.abspath(filename)
    return _loadit(fullfilename)


# """
# Only test code follows
# """
class _Tester:
    """
    Command-line tester for this module
    """

    def __init__(self):
        # print("Tester.__init__()")
        pass

    def test_load_json_file(self):
        print("Tester.test_load_json_file()")

        # Any real JSON file to test with:
        json_test_file = "resources/Page_objects/Calls.json"

        json_1 = load_json_file(json_test_file)
        assert len(json_1) > 100
        json_2 = load_json_file(json_test_file)
        assert len(json_2) > 100
        assert json_1 == json_2
        print("Tester.test_load_json_file() PASS")

    def get_robot_dir(self):
        # Assuming this file is in Libraries, directly under the 'robot dir'.
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def main(self):
        print("Tester.main()")
        robot_dir = self.get_robot_dir()
        os.chdir(robot_dir)

        self.test_load_json_file()
        print("Tester.main() PASS")


if __name__ == "__main__":
    tester = _Tester()
    try:
        tester.main()
        print("Success")
    except Exception:
        traceback.print_exc()
