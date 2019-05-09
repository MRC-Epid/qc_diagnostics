## QC Diagnostics 

### Introduction
A standalone script that takes a job list, performs a fast load of the file and checks for timeseries discrepancies.  It also returns pwear values for quadrants of the day and device battery levels.  It performs estimates of ENMO and non-wear, and has the functionality to return this a graph, along with battery percentage.

### Prerequisites
*  Python 3.6 or higher
*  Pampro Python module installed ([https://gitlab.mrc-epid.cam.ac.uk/PATT/pampro](url))
*  Batch-processing capacity (Recommended)

### Downloading and preparing the environment
There are two options available for downloading the code, depending on whether you wish to use Git.  Option 1 requires Git to be installed in your environment - [https://git-scm.com/](url).
1.  From the command line, navigate to your desired folder location and execute the following command:
`git clone https://gitlab.mrc-epid.cam.ac.uk/PATT/qc_diagnostics/`
