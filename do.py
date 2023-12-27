import requests
import time
import json
import os
import argparse


def load_progress(file_path):
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                print("Loading progress from file...")
                data = json.load(file)
                return set(data.get('available_domains', [])), data.get('last_checked')
        else:
            print("No progress file found, starting fresh.")
        return set(), None
    except Exception as e:
        print(f"Error loading progress file: {e}")
        return set(), None


def save_progress(file_path, available_domains, last_checked):
    try:
        data = {'available_domains': list(
            available_domains), 'last_checked': last_checked}
        print(f"Attempting to save progress to {file_path}...")  # Debug print
        with open(file_path, 'w') as file:
            json.dump(data, file)
        print(f"Progress saved to {file_path}")
    except Exception as e:
        print(f"Error saving progress file: {e}")


def get_next_domain(last_checked, alphabet, tld):
    if last_checked is None:
        return f'{alphabet[0]}{alphabet[0]}{alphabet[0]}.{tld}'

    parts = last_checked.split('.')[0]  # Get the domain part without the TLD
    if len(parts) != 3:
        return None

    first_letter, second_letter, third_letter = parts

    third_index = alphabet.find(third_letter)
    second_index = alphabet.find(second_letter)
    first_index = alphabet.find(first_letter)

    if third_index < len(alphabet) - 1:
        return f'{first_letter}{second_letter}{alphabet[third_index + 1]}.{tld}'
    elif second_index < len(alphabet) - 1:
        return f'{first_letter}{alphabet[second_index + 1]}{alphabet[0]}.{tld}'
    elif first_index < len(alphabet) - 1:
        return f'{alphabet[first_index + 1]}{alphabet[0]}{alphabet[0]}.{tld}'
    else:
        return None


def check_3_letter_domains_tld(tld, rapidapi_key, output_file):
    available_domains, last_checked = load_progress(output_file)
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    headers = {
        "X-RapidAPI-Key": rapidapi_key
    }
    request_count = 0
    max_requests = 9000

    print("Starting domain check...")
    domain_query = get_next_domain(last_checked, alphabet, tld)
    while domain_query and request_count < max_requests:
        try:
            response = requests.get(
                f"https://domainr.p.rapidapi.com/v2/status?mashape-key={rapidapi_key}&domain={domain_query}",
                headers=headers
            )
            request_count += 1

            if response.status_code == 200:
                data = response.json()
                for status in data.get('status', []):
                    if 'undelegated' in status.get('status') and domain_query not in available_domains:
                        available_domains.add(domain_query)
                        print(f"Domain {domain_query} is available!")
                        save_progress(
                            output_file, available_domains, domain_query)
                    else:
                        print(f"Domain {domain_query} is not available.")

            else:
                print(
                    f"Failed to check domain {domain_query}. HTTP status: {response.status_code}")

        except requests.RequestException as e:
            print(f"An error occurred: {e}")

        if request_count % 100 == 0:
            save_progress(output_file, available_domains, domain_query)

        last_checked = domain_query
        domain_query = get_next_domain(last_checked, alphabet, tld)

    save_progress(output_file, available_domains, last_checked)
    print("Domain check completed.")


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Check availability of 3-letter domains for a specific TLD.")
    parser.add_argument("--api_key", required=True,
                        help="RapidAPI key for the Domainr API.")
    parser.add_argument("--tld", default='co.za',
                        help="The top-level domain to search for, e.g., 'co.za'.")
    parser.add_argument("--output_file", default='domain_check_progress.json',
                        help="File path to save the progress.")
    return parser.parse_args()


def main():
    args = parse_arguments()
    check_3_letter_domains_tld(args.tld, args.api_key, args.output_file)


if __name__ == "__main__":
    main()
