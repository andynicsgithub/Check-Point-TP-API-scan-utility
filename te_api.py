"""
te_api
    A Python client side utility for using Threat Emulation API calls to an appliance.
    You may either set the global variables below (some or all), or assigning their optional
      arguments when running the utility.  Run  te_api --help  for the arguments details.
"""

from te_file_handler import TE
import os
import argparse
import concurrent.futures
import zipfile

# Following variables can be assigned and used instead of adding them as arguments when running the te_api.py .
#  input_directory and reports_directory have the following default settings.
#  Using the following input directory default setting means - assuming that the input files to handle are in
#   already existing folder :  ..appliance_tpapi/te_api/input_files
#  Using the following reports_directory default setting means - creating/using the output directory :
#   ..appliance_tpapi/te_api/te_response_data
input_directory = "input_files"
reports_directory = "te_response_data"
appliance_ip = ""
benign_directory = ""
quarantine_directory = ""

def main():
    """
    1. Get the optional arguments (if any): the input-directory, the output-directory and appliance-ip.
    2. Accordingly set the api-url, and create the output directory.
    3. Go though all input files in the input directory.
        Handling each input file is described in TE class in te_file_handler.py:
    """
    global input_directory
    global reports_directory
    global appliance_ip
    global benign_directory
    global quarantine_directory
    global concurrency
    global url
    parser = argparse.ArgumentParser()
    parser.add_argument("-in", "--input_directory", help="the input files folder to be scanned by TE")
    parser.add_argument("-rep", "--reports_directory", help="the output folder with TE results")
    parser.add_argument("-ip", "--appliance_ip", help="the appliance ip address")
    parser.add_argument('-n', '--concurrency', type=int, help='Number of concurrent loops')
    parser.add_argument('-out', '--benign_directory', help='the directory to move Benign files after scanning')
    parser.add_argument('-jail', '--quarantine_directory', help='the directory to move Malicious files after scanning')
    args = parser.parse_args()
    if args.input_directory:
        input_directory = args.input_directory
    print("The input files directory to be scanned by TE : {}".format(input_directory))
    if not os.path.exists(input_directory):
        print("\n\n  --> The input files directory {} does not exist !\n\n".format(input_directory))
        parser.print_help()
        return
    if args.reports_directory:
        reports_directory = args.reports_directory
    print("The output directory with TE results : {}".format(reports_directory))
    if not os.path.exists(reports_directory):
        print("Pre-processing: creating te_api output directory {}".format(reports_directory))
        try:
            os.mkdir(reports_directory)
        except Exception as E1:
            print("could not create te_api output directory, because: {}".format(E1))
            return
    if args.appliance_ip:
        appliance_ip = args.appliance_ip
    if not appliance_ip:
        print("\n\n  --> Missing appliance_ip !\n\n")
        parser.print_help()
        return
    print("The appliance ip address : {}".format(appliance_ip))
    url = "https://" + appliance_ip + ":18194/tecloud/api/v1/file/"
    if args.benign_directory:
        benign_directory = args.benign_directory
    print("The output directory for Benign files: {}".format(benign_directory))
    if not os.path.exists(benign_directory):
        print("Pre-processing: creating Benign directory {}".format(benign_directory))
        try:
            os.mkdir(benign_directory)
        except Exception as E1:
            print("could not create Benign directory because: {}".format(E1))
            return
    if args.quarantine_directory:
        quarantine_directory = args.quarantine_directory
    print("The output directory for Malicious files: {}".format(quarantine_directory))
    if not os.path.exists(quarantine_directory):
        print("Pre-processing: creating Benign directory {}".format(quarantine_directory))
        try:
            os.mkdir(quarantine_directory)
        except Exception as E1:
            print("could not create Quarantine directory because: {}".format(E1))
            return


    # Define the list of archive file extensions
    archive_extensions = [".7z", ".arj", ".bz2", ".CAB", ".gz", ".rar", ".tar", ".tbz2", ".tbz", ".tb2", ".tgz", ".xz", ".zip", ".udf", ".qcow2"]

    # A loop over the files in the input folder
    files = os.listdir(input_directory)
    print("Begin handling input files by TE")

    # Separate archive files and other files
    archive_files = []
    other_files = []

    for file_name in files:
        full_path = os.path.join(input_directory, file_name)
        extension = os.path.splitext(file_name)[1]
        if extension.lower() in archive_extensions:
            archive_files.append(file_name)
        else:
            other_files.append(file_name)

    # Process other files concurrently
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.concurrency) as executor:
        executor.map(process_files, other_files)

    # Process archive files sequentially
    for file_name in archive_files:
        process_files(file_name)


def process_files(file_name):
    try:
        full_path = os.path.join(input_directory, file_name)
        print("Handling file: {} by TE".format(file_name))
        te = TE(url, file_name, full_path, reports_directory, benign_directory, quarantine_directory)
        te.handle_file()
    except Exception as E:
        print("Could not handle file: {} because: {}. Continue to handle the next file.".format(file_name, E))

if __name__ == '__main__':
    main()


