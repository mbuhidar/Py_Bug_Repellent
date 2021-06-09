import re
# Import try/except used because different path to basic_to_chr module is
# used depending on if pybug is loaded or imported
try:
    from pybugrepellent.basic_to_chr import chr_dict
except ModuleNotFoundError:
    from basic_to_chr import chr_dict


def ahoy_text_to_line_strings():
    '''
    Function to read Ahoy typed in text and convert to individual
    line strings with line number stripped off.  Output as list for
    iteration and execution of code flow for each line.
    Mocked until checksum algorithm is worked out.
    '''
    code_lines1 = ["AA", "BB", "AA1", "BB1", "CC1", "DD1"]
    key_lines1 = ["IE", "IE", "LO", "LO", "LK", "LK"]
    # Alternate mock code lines and corresponding keys
    # code_lines2 = ["G", "GG", "GGG", "GGGG"]
    # key_lines2 = ["EL", "JA", "NM", "CB"]

    return list(zip(code_lines1, key_lines1))


def charlist_to_code_list(charlist):
    '''
    Function to accept a line of code as a string and return
    a list of corresponding c64 petscii codes as integers.
    '''
    # Split charlist at special character entries of form '{xx}', store in list
    str_split = re.split(r"\{\w{2}\}", charlist)
    # Check for loose braces in each substring, return error statement if found
    for sub_str in str_split:
        loose_brace = re.search(r"\}|\{", sub_str)
        if loose_brace is not None:
            return "Loose brace error."
    # Create list of special character code strings
    code_split = re.findall(r"\{\w{2}\}", charlist)
    # Set proper list length to use count enumerate
    code_split.append('')

    # Create list of codes corresponding to each character in string passed in
    codelist = []

    # Build list of ascii codes for string segments with codes for special
    # characters inserted at the string splits
    for count, segment in enumerate(str_split):
        for char in segment:
            codelist.append(int(chr_dict[char]))
        codelist.append(int(chr_dict[code_split[count]]))
    # Remove codes for "" in found in the string
    codelist = [x for x in codelist if x != int(chr_dict[""])]
    return codelist


def int_list_to_hilo_bytes(int_list):
    '''
    Function to take a list of integers, add them, and convert result into
    high and low bytes.  Guess at this point.
    '''
    num_total = 0
    for num in int_list:
        num_total += num
        # hi_byte = int(num_total/256)
        hi_byte = int(num_total >> 8)
        lo_byte = num_total - hi_byte * 256
    return (hi_byte, lo_byte)


def int_list_to_XOR_csum(int_list):
    '''
    '''
    num_xor = 0
    for num in int_list:
        num_xor ^= num
    return num_xor


def hex_to_repellent_code(hex_value):
    '''
    Function to convert hex to alpha only representation that the
    Ahoy Bug Repellent tool uses - guess at this point.
    '''
    hex_alpha_dict = {"0": "A", "1": "B", "2": "C", "3": "D",
                      "4": "E", "5": "F", "6": "G", "7": "H",
                      "8": "I", "9": "J", "a": "K", "b": "L",
                      "c": "M", "d": "N", "e": "O", "f": "P",
                      }
    right_two = str(hex_value)[-2:]
    return hex_alpha_dict[right_two[0]] + hex_alpha_dict[right_two[1]]


def repellent_code_to_hex(code):
    '''
    Function to convert alpha code representation that the
    Ahoy Bug Repellent tool uses to hex - guess at this point.
    '''
    hex_alpha_dict = {"0": "A", "1": "B", "2": "C", "3": "D",
                      "4": "E", "5": "F", "6": "G", "7": "H",
                      "8": "I", "9": "J", "a": "K", "b": "L",
                      "c": "M", "d": "N", "e": "O", "f": "P",
                      }

    alpha_hex_dict = {value: key for (key, value) in hex_alpha_dict.items()}

    return "0x" + alpha_hex_dict[code[0]] + alpha_hex_dict[code[1]]


def main():
    '''
    Manual test execution flow - seed lines of code and corresponding
    checksum generated by the Bug Repellent line checker in the
    ahoy_text_to_line_strings() function for testing.
    '''
    for codeline, keyline in ahoy_text_to_line_strings():
        code_list = charlist_to_code_list(codeline)
        if code_list == "Loose brace error.":
            print("Loose brace error in", codeline)
            break 
        hilo_bytes = int_list_to_hilo_bytes(code_list)
        xor_hilo = hilo_bytes[0] ^ hilo_bytes[1]
        hex_xor_hilo = hex(xor_hilo)
        hex_to_repellent = hex_to_repellent_code(hex_xor_hilo)

        key_hex = repellent_code_to_hex(keyline)
        key_int = int(key_hex, 16)

        row = [xor_hilo, hex_xor_hilo, hex_to_repellent, key_int, key_hex, 
               keyline]

        print(codeline, hilo_bytes)
        print("{:4} {:4} {:4} {:4} {:4} {:4}".format(*row))
        print(int_list_to_XOR_csum(code_list))

if __name__ == "__main__":
    main()
