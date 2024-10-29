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

### Output
The process produces output for each raw accelerometer file processed, as a wide-format 'qc_meta' .csv file. The variables come from both the metadata contained in the file itself (which varies between the AX3 and GENEActiv files) and the derived output from the QC process. These files can be consolidated and reviewed accordingly.  If an output file already exists for the current raw file being processed it will be overwritten with the results from the current process.  In addition, if there are any “anomalies” detected in the raw files processed, an ‘anomalies’ .csv file will be created in the specified folder.  

### Further notes
The repository futhermore provides a script that creates a job file list that is needed to run the QC_Diagnostics script as well as a script that combines the QC_Diagnostics output and generates a log with any issues to review. Navigate to the qc_diagnostics [wiki](https://github.com/MRC-Epid/qc_diagnostics/wiki) on further guidance on how to prepare and run the scripts. 

