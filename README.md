## QC Diagnostics 

### Introduction
This standalone script takes in a job list of filepaths, performs a fast load of the file (at page-level), extracts basic metadata from file and checks for time-series and axis discrepancies (“anomalies”). It also returns an **estimate** of wear time (pwear) across the file and within quadrants of the day (to aid compliance monitoring) and device battery levels (to monitor device performance). It has the functionality to produce graphs showing **approximated** ENMO and battery percentage, with shaded sections of non-wear, for each file processed. It is designed to provide a quick overview of the file, without the need for full processing. 

### Prerequisites
*  Binary files from either an AX3 or GENEActiv device (see below)
*  Python 3.6 or higher
*  pampro Python module installed ([https://github.com/MRC-Epid/pampro](url))
*  Batch-processing capacity (recommended)

The process currently only supports .cwa (AX3) or .bin (GENEActiv) binary files.

NOTE: This process has been developed on a Linux operating system, but is also compatible with Windows.  It has NOT been tested for any other operating system type, e.g. macOS.

### Downloading and preparing the environment
There are two options available for downloading the code, depending on whether you wish to use Git.  Option 1 requires Git to be installed in your environment ([https://git-scm.com/](url)).
1.  EITHER use the command line to navigate to your desired folder location and execute the following command:
`git clone https://github.com/MRC-Epid/qc_diagnostics/`

2.  OR select the 'Repository' option from the lefthand sidebar, and select the download icon on the top-right of the Repository page.  You can select from different formats of download.
3.  Regardless of whether you used step 1 or 2 above, you should now have a folder that contains the required files.  Also included is a folder named "_logs", this is where log files will be created by the process.
4.  Included in the downloaded files is an example job file with the required column headings "pid" and "filename". The pid column must contain unique values and the filename column must contain the complete filepath of each file requiring processing.

### Editing the script
As this is a self-contained process, all the settings are found at the top of the processing script QC_Diagnostics_v1.0.py.

The settings are commented to explain their usage, and, as a minimum, the ‘filetype’ setting should be checked and the job file location, 'charts', 'results' and 'anomalies' folder locations must be provided.

'Processing_epoch' and 'noise_cutoff_mg' are set to standard default values, but can be altered if required.

The plotting functionality can be turned off by changing the 'PLOT' setting to "NO".

### Executing the script
The processing script takes a 'job number' and 'number of jobs' from the command line as arguments.  These are used in the script to split the job list into sections.  Submitting the job can be done in a number of ways, depending on your environment.

1.  If you do not have the capacity to submit multiple jobs then the simplest way to run the script is to give these both as "1" when submitting the script. Use the command line to navigate to the folder containing the script and issue the following command: `ipython QC_Diagnostics_v1.0.py 1 1` 
This will run the script as one process.

2.  If, however, you do have multiple-process capability you could submit the script in batches in this way: `ipython QC_Diagnostics_v1.0.py 1 3 & ipython QC_Diagnostics_v1.0.py 2 3 & ipython QC_Diagnostics_v1.0.py 3 3` 
This would execute the python script three times, each process using one third of the job list.

3.  Another batch processing option would be to use a scheduling engine, such as Sun Grid Engine.  The shell script 'qc_batch_sge.sh' has been written to take the processing script's relative path, and the number of batches required.  It then uses the python environment (in this case provided by Anaconda3) in order to automatically submit the required number of jobs.  In order to submit three jobs, it would be executed from the command line thus: `./qc_batch_sge.sh QC_Diagnostics_v1.0.py 3`

### Output
The process produces output for each raw file processed, as a wide-format 'qc_meta' .csv file. The variables come from both the metadata contained in the file itself (which varies between the AX3 and GENEActiv files) and the derived output from the QC process. These files can be consolidated and reviewed accordingly.  If an output file already exists for the current raw file being processed it will be overwritten with the results from the current process.  In addition, if there are any “anomalies” detected in the raw files processed, an ‘anomalies’ .csv file will be created in the specified folder.  

### Executing script to combine and review QC diagnostics output files
The script combine_review_qc_variables.py combines the qc_meta files for that were produced for each file into one. It then run some checks on the main variables and outputs the checks to a qc_log named 'QC_diagnostics_log_DDMonYYYY.docx'. The checks that are run are explained in the log together with PATT recommendations on how to handle any issues. As this is a self-contained process, all the settings that needs adjusting to run the script are found at the top of the processing script combine_review_qc_variables.py. Comments are added in the script to explain how to edit the settings. 

To run the script open the combine_review_qc_variables.py file in PyCharm (If it's not already open).
To run the script click the Run 
![image](https://github.com/user-attachments/assets/15f6a26d-e15e-4d67-82cc-0ade22f03b05)
icon image at the top of the PyCharm window.


