import re
import json

# Provided string
input_string = "Tokens Used: 630\n\tPrompt Tokens: 577\n\tCompletion Tokens: 53\nSuccessful Requests: 1\nTotal Cost (USD): $0.0009714999999999999"

# Use regular expressions to extract all key-value pairs
matches = re.findall(r'(\w+(?:\s+\w+)*):\s*([$0-9.]+)', input_string)

# Handle special case for "Total Cost" to capture the entire cost string
total_cost_match = re.search(r'Total Cost \(USD\):\s*([$0-9.]+)', input_string)
if total_cost_match:
    matches.append(('Total Cost (USD)', total_cost_match.group(1)))

# Create a dictionary from the matches
response_dict = dict(matches)

# Convert the dictionary to JSON format
json_response = json.dumps(response_dict, indent=2)

# Print or use the JSON response
print(json_response)
