# te_api
A Python client side utility for using Threat Emulation API calls to an appliance.

It includes Upload, Query and Download API calls, using the Cloud API format ( …/tecloud/api/v#/file/..).

### The flow
Going through the input directory and handling each file in order to get its Threat Emulation results.

For each file:

      1. Querying te cache for already existing results by the file sha1.

           If results exist then goto #4, otherwise- continue to #2
    
      2. Uploading the file to the appliance for te and te_eb features.
    
      3. If upload result is upload_success then querying te and te_eb until receiving te results.

           (Note, te_eb results of early malicious verdict might be received earlier during the queries in between)
    
      4. Writing to log file - the last query/upload response info.
    
      5. If te result is found then displaying the verdict

      6. If the file is malicious then download the emulation report to the reports directory and move the file to the quarantine directory.

      7. If the file is benign, record the API response in the reports directory and move the file to the output directory.



### Usage
~~~~
python te_api.py --help

usage: te_api.py [-h] [-in INPUT_DIRECTORY] [-rep REPORTS_DIRECTORY] [-ip APPLIANCE_IP] [-n CONCURRENCY] [-out BENIGN DIRECTORY] [-jail QUARANTINE DIRECTORY]

command-line arguments:
-h, --help            show this help message and exit
-in    --input_directory        the input files folder to be scanned by TE
-rep   --reports_directory      the output folder with TE results
-ip    --appliance_ip           the appliance ip address
-n     --concurrency            Number of concurrent files to process. Tune this inline with appliance size/model for performance.
-out   --benign_directory       the directory to move Benign files after scanning
-jail  --quarantine_directory   the directory to move Malicious files after scanning

~~~~
It is also possible to change the optional arguments default values within te_api.py

### References
* Additional Threat Emulation API info: [sk167161](https://supportcenter.checkpoint.com/supportcenter/portal?eventSubmit_doGoviewsolutiondetails=&solutionid=sk167161)
* te_eb feature: [sk117168 chapter 4](https://supportcenter.checkpoint.com/supportcenter/portal?eventSubmit_doGoviewsolutiondetails=&solutionid=sk117168#New%20Public%20API%20Interface)
