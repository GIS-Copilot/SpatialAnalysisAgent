import os
import sys
import importlib
import subprocess
from qgis.PyQt.QtWidgets import QMessageBox
from qgis.PyQt.QtCore import QSettings
from concurrent.futures import ThreadPoolExecutor

def check_and_install_libraries(filename):
    """Check and install required third-party Python libraries."""
    settings = QSettings()
    # Read the list of required libraries from the file
    required_libraries = read_libraries_from_file(filename)

    # Check if the list of required libraries is stored
    cached_libraries = settings.value("cached_libraries", [])

    # If no cached libraries exist or libraries have changed, perform a full check
    if not cached_libraries or cached_libraries != required_libraries:
        missing_packages = check_missing_libraries(required_libraries)

    # if settings.value("libraries_installed", False, type=bool):
    #     return  # Skip the check if libraries are already installed
    # required_libraries = read_libraries_from_file(filename)
    # # Collect missing libraries in parallel
    # missing_packages = check_missing_libraries(required_libraries)


    # If there are missing packages, prompt the user to install them
    if missing_packages:
        message = "The following Python packages are required to use the plugin:\n\n"
        message += "\n".join(missing_packages)
        message += "\n\nWould you like to install them now? After installation, please restart QGIS."

        # Display the message box to the user
        reply = QMessageBox.question(None, 'Missing Dependencies', message,
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            # Install the missing packages
            install_libraries(missing_packages)
            # settings.setValue("libraries_installed", True)  # Mark libraries as installed
            settings.setValue("cached_libraries", required_libraries)  # Cache the list of installed libraries

        elif reply == QMessageBox.No:
            # Close the current dialog or window when the user clicks "No"
            return  # Stop installation if user declines
    else:
        # settings.setValue("libraries_installed", True)  # Mark libraries as installed if none are missing
        settings.setValue("cached_libraries", required_libraries)

def check_missing_libraries(libraries):
        """Function to install missing libraries using pip."""
        missing_packages = []

        # Use ThreadPoolExecutor for parallel checking
        with ThreadPoolExecutor() as executor:
            results = executor.map(check_library, libraries)

        for library, missing in results:
            if missing:
                missing_packages.append(library)

        return missing_packages
def check_library(library_info):
    """Check if a library is installed, return (library, is_missing)."""
    library, module = library_info
    try:
        importlib.import_module(module)
        return (library, False)  # Library is installed
    except ImportError:
        return (library, True)  # Library is missing

def install_libraries(libraries):
    """Install missing libraries using pip."""

    try:
        print(f"Installing missing libraries: {libraries}")
        subprocess.check_call(['python3', '-m', 'pip', 'install'] + libraries)
        print("Libraries installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error installing missing libraries: {e}")


def read_libraries_from_file(filename):
    """Read the list of libraries and their import paths from a text file."""
    libraries = []
    with open(filename, 'r') as file:
        for line in file:
            if line.strip():  # Skip empty lines
                # Each line is in the format: library_name:module_name
                library, module = line.strip().split(':')
                libraries.append((library, module))
    return libraries






















# import os
# import sys
# import importlib
# import subprocess
# from qgis.PyQt.QtWidgets import QMessageBox
# from qgis.PyQt.QtCore import QSettings
#
# # Check and install required third-party Python libraries
# def check_and_install_libraries(filename):
#     """Check and install required third-party Python libraries."""
#     required_libraries = read_libraries_from_file(filename)
#
#     def install_missing_libraries(libraries):
#         """Function to install missing libraries using pip."""
#         missing_packages = []
#
#
#         for library, module in libraries:
#             try:
#                 # Use importlib to check if the module can be imported
#                 importlib.import_module(module)
#                 # print(f"{library} is already installed.")
#             except ImportError:
#                 # If the module isn't installed, use pip to install the library
#                 # print(f"{library} is not installed. Installing...")
#                 missing_packages.append(library)
#         # If there are missing packages, prompt the user to install them
#         if missing_packages:
#             message = "The following Python packages are required to use the plugin:\n\n"
#             message += "\n".join(missing_packages)
#             message += "\n\nWould you like to install them now? After installation, please restart QGIS."
#
#             # Display the message box to the user
#             reply = QMessageBox.question(None, 'Missing Dependencies', message,
#                                          QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
#             if reply == QMessageBox.Yes:
#                 # Install the missing packages
#                 for package in missing_packages:
#                     # print(f"Installing {package}...")
#                     subprocess.check_call(['python3', '-m', 'pip', 'install', package])
#
#             elif reply == QMessageBox.No:
#                 # Close the current dialog or window when the user clicks "No"
#                 return  # Assuming this is in a dialog or window that should be closed
#             # else:
#             #     print("User chose not to install the missing packages.")
#
#     install_missing_libraries(required_libraries)
#
# def read_libraries_from_file(filename):
#     """Read the list of libraries and their import paths from a text file."""
#     libraries = []
#     with open(filename, 'r') as file:
#         for line in file:
#             if line.strip():  # Skip empty lines
#                 # Each line is in the format: library_name:module_name
#                 library, module = line.strip().split(':')
#                 libraries.append((library, module))
#     return libraries
#
#
#
#
#
























# def check(required_packages):
#     # Check if required packages are installed
#     missing_packages = []
#     for package in required_packages:
#         try:
#             importlib.import_module(package)
#         except ImportError:
#             missing_packages.append(package)
#     if missing_packages:
#         message = "The following Python packages are required to use the plugin Spatial Analysis Agent:\n\n"
#         message += "\n".join(missing_packages)
#         message += "\n\nWould you like to install them now? After installation please restart QGIS."
#
#         reply = QMessageBox.question(None, 'Missing Dependencies', message,
#                                      QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
#
#         if reply == QMessageBox.No:
#             return False
#
#         for package in missing_packages:
#             try:
#                 subprocess.check_call(['python3', '-m', 'pip', 'install', package])
#             except Exception as e:
#                 QMessageBox.warning(None, "Error", f"Failed to install {package}: {str(e)}")
#                 return False
#
#         # Set the flag that packages have been installed
#         settings = QSettings()
#         settings.setValue('SAA/PackagesInstalled', True)
#         return True
#
#     #Set flag to indicate packages have been installed
#     settings = QSettings()
#     settings.setValue('SAA/PackagesInstalled', True)
#     return True








# import os
# import sys
# import importlib
# from qgis.PyQt.QtWidgets import QMessageBox
# from qgis.PyQt.QtCore import QSettings
#
#
# def check(required_packages):
#     # Check if required packages are installed
#     missing_packages = []
#     for package in required_packages:
#         try:
#             importlib.import_module(package)
#         except ImportError:
#             missing_packages.append(package)
#         if missing_packages:
#             message = "The following Python packages are required to use the plugin Spatial Analysis Agent:\n\n"
#             message += "\n".join(missing_packages)
#             message += "\n\nWould you like to install them now? After installation please restart QGIS."
#
#             reply = QMessageBox.question(None, 'Missing Dependencies', message,
#                                          QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
#
#             if reply == QMessageBox.No:
#                 return
#
#             for package in missing_packages:
#                 update = False
#                 try:
#                     os.system('"' + os.path.join(sys.prefix, 'scripts', 'pip') + f'" install {package}')
#                     update = True
#                 finally:
#                     if not update:
#                         try:
#                             importlib.import_module(package)
#                             import subprocess
#                             subprocess.check_call(['python3', '-m', 'pip', 'install', package])
#                         except:
#                             importlib.import_module(package)
#
#             update = False
#             try:
#                 os.system('"' + os.path.join(sys.prefix, 'scripts', 'pip') + f'" install --upgrade openai')
#                 update = True
#             finally:
#                 if not update:
#                     try:
#                         import subprocess
#                         subprocess.check_call(['python3', '-m', 'pip', 'install', f'" --upgrade openai'])
#                     except:
#                         pass
#
#                     # Set flag to indicate packages have been installed
#             settings = QSettings()
#             settings.setValue('SAA/PackagesInstalled', True)
#         else:
#             # Set flag to indicate packages are already installed
#             settings = QSettings()
#             settings.setValue('SAA/PackagesInstalled', True)