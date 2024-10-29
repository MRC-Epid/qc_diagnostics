#################################################################################
# This script finds all .cwa files in a specified data directory and creates a job_file, that are listen all .cwa files. This job_file can be used when running qc_diagnostics
# Author: CAS254
# Date: 10/09/2024
# Version: 1.0

import os
import pandas as pd
import glob
import setup


#DATA_DIR = 'file_path_data_dir'    # Replace with the directory for where the data is saved
#OUTPUT_DIR = 'file_path_job_file'   # Replace with the directory where you want the job_file to be saved
#PROJECT_NAME = 'example_project_name'  # Replace with the name of the project

# --- CREATING A FILELIST OF ALL FILES IN THE RESULTS FOLDER --- #
def create_filelist():
    file_list = glob.glob(os.path.join(setup.PROJECT_DIR, setup.DATA_DIR, setup.file_extension))
    file_list = [f.replace('\\', '/') for f in file_list]
    filenames = [os.path.basename(f) for f in file_list]
    df = pd.DataFrame(file_list, columns=['filename'])
    df['pid'] = filenames
    df['pid'] = df['pid'].apply(lambda x: x.rsplit('_')[0])
    df = df[['pid', 'filename']]

    output_path = os.path.join(setup.PROJECT_DIR, setup.JOB_FILE_DIR, f'job_file_{setup.NAME_JOB_LIST}.csv')
    df.to_csv(output_path, index=False)


if __name__ == "__main__":
    create_filelist()