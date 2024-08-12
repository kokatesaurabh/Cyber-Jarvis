# shodan.py

import shodan

SHODAN_API_KEY = 'pHHlgpFt8Ka3Stb5UlTxcaEwciOeF2QM'  # Replace with your Shodan API key

def get_shodan_info(query):
    try:
        api = shodan.Shodan(SHODAN_API_KEY)
        result = api.search(query)
        return result
    except shodan.APIError as e:
        if e.value == '403 Forbidden':
            return "Access to Shodan API is denied. Please check your API key."
        else:
            print(f"Shodan API error: {e}")
            return None

def extract_specific_info(shodan_result):
    # Extract specific information like IP addresses, etc.
    info_list = []
    for match in shodan_result['matches']:
        ip_address = match.get('ip_str', 'N/A')
        info_list.append(f"IP Address: {ip_address}")

        # Add more specific information as needed

    return '\n'.join(info_list)

def save_to_txt(query, shodan_result):
    try:
        with open(f'shodan_{query}.txt', 'w', encoding='utf-8') as txtfile:
            specific_info = extract_specific_info(shodan_result)
            txtfile.write(f"Query: {query}\n")
            txtfile.write(f"Shodan Result: {shodan_result['total']} matches found.\n")
            txtfile.write(specific_info)
    except Exception as e:
        print(f"Error saving to TXT: {e}")


class Shodan:
    pass