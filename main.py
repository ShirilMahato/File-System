import unittest
from test import TestFile, TestDirectory, TestFileSystem, TestLocalSystem 
import local_system
import virtual_system

def run_tests():
    # Load the tests
    test_classes_to_run = [TestFile, TestDirectory, TestFileSystem, TestLocalSystem]
    loader = unittest.TestLoader()

    suites_list = []
    for test_class in test_classes_to_run:
        suite = loader.loadTestsFromTestCase(test_class)
        suites_list.append(suite)

    big_suite = unittest.TestSuite(suites_list)
    runner = unittest.TextTestRunner()
    results = runner.run(big_suite)

    # Return whether the tests were successful
    return results.wasSuccessful()

def main():
    print("Running unit tests...")
    if run_tests():
        print("All unit tests passed!")
        while True:
            print("Choose the execution environment:")
            print("1. Local System")
            print("2. Virtual System")
            print("3. Exit")
            choice = input("Enter your choice (1/2/3): ")

            if choice == "1":
                local_system.run_local_system()
            elif choice == "2":
                virtual_system.run_virtual_system()
            elif choice == "3":
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please try again.")
    else:
        print("Some unit tests failed. Exiting...")

if __name__ == "__main__":
    main()
