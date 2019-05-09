## QC Diagnostics 

### Introduction
A standalone script that takes a job list, performs a fast load of the file and checks for timeseries discrepancies.  It also returns pwear values for quadrants of the day and device battery levels.  It performs estimates of ENMO and non-wear, and has the functionality to return this in a graph, along with battery percentage, per file processed.

### Prerequisites
*  Python 3.6 or higher
*  Pampro Python module installed ([https://gitlab.mrc-epid.cam.ac.uk/PATT/pampro](url))
*  Batch-processing capacity (Recommended)

### Downloading and preparing the environment
There are two options available for downloading the code, depending on whether you wish to use Git.  Option 1 requires Git to be installed in your environment ([https://git-scm.com/](url)).
1.  EITHER use the command line to navigate to your desired folder location and execute the following command:
`git clone https://gitlab.mrc-epid.cam.ac.uk/PATT/qc_diagnostics/`

2.  OR select the 'Repository' option from the lefthand sidebar, and select the download icon on the top-right of the Repository page.  You can select from different formats of download.
3.  Regardless of whether you used step 1 or 2 above, you should now have a folder that contains the required files.  Wherever you will be executing the script from you'll need to create a folder named "_logs", this is where log files will be created by the process.
4.  Included in the downloaded files is a blank job file containing the required column headings "id" and "filename".  The id column must contain unique values and the filename column must contain the complete path for each file requiring processing.

### Editing the script
As this is a self-contained process, all the settings are found at the top of the processing script QC_Diagnostics_v1.0.py.

The settings are commented to explain their usage, and as a minimum the filetype setting should be checked and the 'charts', 'visualisation' and 'anomalies' folder locations must be provided.

The plotting functionality can be turned off by changing the 'PLOT' variable to "NO".

'Processing_epoch' and 'noise_cutoff_mg' are set to standard defualt values, but can be altered if required.

### Executing the script
The processing script takes a 'job number' and 'number of jobs' from the command line as arguments.  These are used in the script to split the job list into sections.  Submitting the job can be done in a number of ways, depending on your environment.

1.  If you do not have the capacity to submit multiple jobs then the simplest way to run the script is to give these both as "1" when submitting the script. Use the command line to navigate to the folder containing the script and issue the following command: `ipython QC_Diagnostics_v1.0.py 1 1` This will run the script as one process.
2.  If, however, you do have multiple-process capability you could submit the script in batches in this way: `ipython QC_Diagnostics_v1.0.py 1 3 & ipython QC_Diagnostics_v1.0.py 2 3 $ ipython QC_Diagnostics_v1.0.py 3 3` This would execute the python script three times, each process using one third of the job list.
3.  Anotehr option would be to use a scheduling engine, such as Sun Grid Engine.  The shell script 'qc_batch_sge.sh' has been written to take the processing script's relative path, and the number of batches required.  It then uses the python environment (in this case provided by Anaconda3) in order to automatically submit the required number of jobs.  In order to submit three jobs, it would be executed from the command line thus: `./qc_batch_sge.sh QC_Diagnostics_v1.0.py 3`