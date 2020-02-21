# Audit Samples
Script for creating samples to be used for auditing.

## Requirements

All required packages are in the requirements.txt file. There is also an included environment.yml file for setting up a conda environment. Requires paceutils package to be installed in environment - use pip install e <local_path/to/pace_utils>.

### PaceUtils

Requires that the paceutils package to be installed. Can be found at http://github.com/whatscottcodes/paceutils.

Requires a SQLite database set up to the specifications in https://github.com/whatscottcodes/database_mgmt

## Use

Script can be run with no parameters to create sample files for a review period of the month prior to the month the script is being run in.
To run for other months the following parameters can be passed:
    start_date: YYYY-MM-DD
    end_date: YYYY-MM-DD
    audit_type: initial-closed, cos, or documentation – allows the script to be run for just one type of sample (initial and closed are linked)

The script outputs 4 csv files.
The documents are each of the form “audit_name_start_date_end_date.csv”
    i.e. careplan_audit_2020_01_01_2020_01_31.csv.
These files are saved in “V:\CMT\_Audits\month_num_monthName YYYY\Ppt Samples”, where the month values are the month during which you ran the script.
    i.e. V:\CMT\_Audits\2_February 2020\Ppt Samples

