from datetime import datetime
import configparser, re, os

timestamp = datetime.now().strftime("%Y_%m_%d-%I_%M_%S")

# Load configuration file
config = configparser.ConfigParser()
config.read('config.ini')

# Read in parameters from configuration file
log_file = (config['Paths']['logfile'])
#regex_list = (config['Patterns']['Regex'].replace(",","").split())
regex_list = [r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})", r"(?:[0-9a-fA-F]:?){12}", r"Number", r"character", r"effects", r"Giants"]

changes = 0
# Count Lines in logfile and do pattern matching
with open(log_file,"r") as file:
    linecount = len(file.readlines())
    file.seek(0)
    data = file.read()
    for regex in regex_list:
        data = re.sub(regex, "XXXXX", data, flags=re.IGNORECASE)
changes = data.count("XXXXX")

# Create new redacted log file
output = (os.path.splitext(config['Paths']['logfile'])[0]) + " " + timestamp + ".txt"
with open(output, "w") as output_file:
    output_file.write(data)

# Create summary report file
summary = "Summary" + " " + timestamp + ".txt"
with open(summary, "w") as summary_file:
    summary_file.write("Matching on following patterns: " + regex_list.__str__() + '\n')
    summary_file.write("Number of items in list to match: " + len(regex_list).__str__() + '\n')
    summary_file.write(file.name + " lines processed: " + linecount.__str__() + '\n')
    summary_file.write("Redactions in file: " + changes.__str__() +'\n')