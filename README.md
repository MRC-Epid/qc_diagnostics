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
4.  