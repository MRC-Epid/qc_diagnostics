# This setup.py file holds the variables that needs editing before being able to run the .py scripts from the qc_diagnostics repository.
# The variables are commented to explain their use and how to edit them

# --- VARIABLES THAT NEEDS EDITING --- #

# Name of project #
PROJECT_NAME = "example_project_name" # Replace with the name of the project

# File settings #
filetype = "Axivity"            # raw data file filetype ("GeneActiv" or "Axivity")

# Folder settings #
PROJECT_DIR = 'example_file_path_project_directory' # Replace with the directory for the overall folder for the project


# --- VARIABLES THAT SHOULD NOT NEED EDITING --- #
# The folders below do not need editing, if you have setup you project directory with the standard foldernames as below (These folders should be within your project folder). Edit if you have named the folders differently
DATA_DIR = '_data'          # The folder where the accelerometer files should be stored (.cwa for axivity or .bin for GeneActiv)
JOB_FILE_DIR = '_analysis'  # The job_files created through the filelist_generation.py will be stored here.
RESULTS_FOLDER = '_results' # The results from the QC_Diagnostics will be saved here
QC_OUTPUT = '_results/_combined'    # Once the QC_diagnostic results have been combined into one it will be saved in the _combined folder within the _results folder. The QC_log will also be saved here.
CHARTS_DIR = '_charts'      # If Charts are generated these will be saved here
ANOMALIES_DIR = '_anomalies'    # If any files had anomalies a file will be saved here.
