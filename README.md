# Google-Docking-Tool


Google Dorking Tool
Google Dorking Tool is a powerful cybersecurity tool that leverages advanced Google search queries (also known as "Google Dorks") to find sensitive information, vulnerabilities, or misconfigurations on websites indexed by Google. This tool can be used for penetration testing, vulnerability assessment, or to enhance web security by identifying exposed data.

Features
Automated Dork Search: Perform automated searches using predefined or custom Google Dorks.
Custom Dork Input: Enter your own Google Dork queries for specific information retrieval.
Filtering Options: Filter results based on various parameters (e.g., file type, domain).
Export Results: Export search results to CSV or other formats for further analysis.
Easy-to-Use Interface: Simple command-line interface (CLI) for ease of use.

# Prerequisites
Python 3.x
Required Python packages (e.g., requests, BeautifulSoup4, etc.)
Installation
# Clone the repository:
git clone https://github.com/Devil9630/Google-Docking-Tool.git

cd google-dorking-tool
# Install the required dependencies:
pip install -r requirements.txt
# Usage
To run the tool, use the following command:
python google_dorking_tool.py
# Options
-d, --dork : Specify a custom Google Dork query.
-f, --file : Load dorks from a file.
-o, --output : Specify an output file to save the results.
-h, --help : Show help message and exit.
# Example:
python google_dorking_tool.py -d "intitle:index of" -o results.csv
# Disclaimer
This tool is intended for educational and ethical purposes only. Use it responsibly and ensure you have proper authorization before performing any tests on websites or systems. The author is not responsible for any misuse or damage caused by this tool.

# Contributing
Contributions are welcome! If you'd like to contribute, please fork the repository and submit a pull request.
