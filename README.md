# 3-Letter Domain Checker for .co.za TLD

This Python script checks the availability of 3-letter domains for the `.co.za` top-level domain (TLD) using the Domainr API via RapidAPI. It's designed to automate the process of finding available short domain names, which can be particularly useful for branding or URL shortening purposes.

## Features

- Checks all possible 3-letter combinations for the specified TLD.
- Pauses after every 100 API requests to comply with rate limits.
- Stops after 49,000 requests to prevent excessive API usage.
- Saves progress to a file, allowing the process to be paused and resumed.
- Securely passes the API key as a command-line argument.

## Prerequisites

Before running the script, ensure you have the following:

- Python 3 installed on your system.
- `requests` library installed in Python (`pip install requests`).
- A valid RapidAPI key for the Domainr API.

## Usage

To use the script, run it from the command line with the necessary arguments.

python do.py --api_key YOUR_RAPIDAPI_KEY

Replace `script_name.py` with the name of your script file and `YOUR_RAPIDAPI_KEY` with your actual RapidAPI key.

### Command Line Arguments

- `--api_key` (required): Your RapidAPI key for the Domainr API.
- `--tld` (optional): The top-level domain to search for. Default is 'co.za'.
- `--output_file` (optional): The file path where the script's progress will be saved. Default is 'domain_check_progress.json'.

## Output

The script will output the available 3-letter domains for the specified TLD and save this information in the specified output file. This file is also used to resume the process in case of interruption.

## License

This project is open source and available under the [MIT License](LICENSE).

## Contributing

Contributions to this project are welcome! Please fork the repository and submit a pull request with your changes or improvements.

## Contact

For any queries or suggestions, please open an issue in the GitHub repository.

## Acknowledgments

This script uses the Domainr API provided via RapidAPI.

---

_Note: This script is for educational and development purposes. Please ensure compliance with the API provider's terms of service._
