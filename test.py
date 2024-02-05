def convert_comma_to_period(input_string):
    if isinstance(input_string, str):
        result_string = input_string.replace(",", ".")
        return result_string
    else:
        raise ValueError("Input must be a string.")


# Example usage:
input_string = "1,000,000.50"
output_string = convert_comma_to_period(input_string)
print(output_string)
