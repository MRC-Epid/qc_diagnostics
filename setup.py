# This setup.py file holds the variables that needs editing before being able to run the .py scripts from the qc_diagnostics repository.
# The variables are commented to explain their use and how to edit them

# --- VARIABLES THAT NEEDS EDITING --- #

# Name of project #
PROJECT_NAME = "example_project_name" # Replace with the name of the project

# File settings #
filetype = "Axivity"            # raw data file filetype ("GeneActiv" or "Axivity")

# Folder settings #
PROJECT_DIR = 'example_project_directory' # Replace with the directory for the overall folder for the project (Note that you have to use "/" and not "/")

# Job list name #
NAME_JOB_LIST = '' # Replace with the name you wish for the job list file. E.g., if you have you data saved in subfolders (e.g., January, February etc.) the job list for files from January could be 'study_name_Jan'. If you leave it blank ('') it will be named job_file_projectname.

# --- VARIABLES THAT SHOULD NOT NEED EDITING --- #
# The folders below do not need editing, if you have setup you project directory with the standard foldernames as below (These folders should be within your project folder). Edit if you have named the folders differently
DATA_DIR = '_data'          # The folder where the accelerometer files should be stored (.cwa for axivity or .bin for GeneActiv). If data are saved in subfolders, add the name of the subfolder that you wish to run for after the /, e.g., '_analysis/January'.
JOB_FILE_DIR = '_analysis'  # The job_files created through the filelist_generation.py will be stored here.
RESULTS_FOLDER = '_results' # The results from the QC_Diagnostics will be saved here. If your data was saved in subfolders and you also wish to save the results in subfolders these can be added, e.g., '_results/January' (remember to add it below as well)
QC_OUTPUT = '_results/_combined'    # Once the QC_diagnostic results have been combined into one it will be saved in the _combined folder within the _results folder. The QC_log will also be saved here. NOTE if have saved the results in subfolders and want this outputtet in the subfolder as well this needs adding here as well, e.g., '_results/January/_combined'
CHARTS_DIR = '_charts'      # If Charts are generated these will be saved here
ANOMALIES_DIR = '_anomalies'    # If any files had anomalies a file will be saved here.

# Creating the file extension to look for when creating job list - this is created from the filetype to either look for .cwa or .bin files
if filetype.lower() == 'axivity':
    file_extension = '*.cwa'
if filetype.lower() == 'geneactiv':
    file_extension = '*.bin'

# Creating the name of the job file if this was not added above:
if NAME_JOB_LIST == '':
    NAME_JOB_LIST = f'{PROJECT_NAME}'
