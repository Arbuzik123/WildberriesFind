import re
def extract_model_name(input_string):
    second_capital_index = -1
    # Найти вторую большую букву
    first_capital_index = -1
    count_capitals = 0
    parenthesis_index = -1
    comma_index = -1
    slash_index = -1
    for i, char in enumerate(input_string):
        if char.isupper():
            count_capitals += 1
            if count_capitals == 2:
                second_capital_index = i
        if char == ')':
            parenthesis_index = i
        if char == ',':
            comma_index = i
        if char == '/':
            slash_index = i
    if second_capital_index != -1:
        if parenthesis_index != -1:
            target_index = parenthesis_index
        elif comma_index != -1:
            target_index = comma_index
        elif slash_index != -1:
            target_index = slash_index
        else:
            target_index = len(input_string)
        modified_text = input_string[:second_capital_index] + input_string[second_capital_index:target_index].replace(' ', '') + input_string[target_index:]
        print(modified_text)
    else:
        modified_text = input_string
    match = re.search(r'[A-Z].*[A-Z]', modified_text)
    if match:
        start_index = match.start()
        print(start_index)
        second_capital_index = match.start() + match.group().rfind(match.group()[-1])
        open_parenthesis_index = modified_text.find('(', second_capital_index)
        if open_parenthesis_index != -1 and open_parenthesis_index - second_capital_index > 10:
            space_index = modified_text.find(' ', second_capital_index)
            comma_index = modified_text.find(',', second_capital_index)
            slash_index = modified_text.find('/', second_capital_index)
            end_index = min(space_index, comma_index, slash_index) if (
                    space_index != -1 and comma_index != -1 and slash_index != -1
            ) else max(space_index, comma_index, slash_index)
            if end_index != -1:
                print("return1")
                return modified_text[second_capital_index:end_index].replace(" ", "")
            else:
                print("return2")
                return modified_text[second_capital_index:].replace(" ", "")
        if open_parenthesis_index != -1:
            close_parenthesis_index = modified_text.find(')', open_parenthesis_index)
            if close_parenthesis_index != -1:
                if close_parenthesis_index - open_parenthesis_index <= 4:
                    print("return3")
                    return modified_text[start_index:close_parenthesis_index + 1].replace(" ", "")
                else:
                    print("return4")
                    return modified_text[start_index:open_parenthesis_index].replace(" ", "")
            else:
                return modified_text[start_index:].replace(" ", "")
        else:
            space_index = modified_text.find(' ', start_index)
            comma_index = modified_text.find(',', start_index)
            another_index = modified_text.find('(', start_index)
            if space_index != -1 and comma_index != -1:
                print("return5")
                return modified_text[start_index:min(space_index, comma_index, another_index)].replace(" ", "")
            elif another_index != -1:
                return modified_text[start_index:another_index].replace(" ", "")
            elif space_index != -1:
                print("return6")
                return modified_text[start_index:space_index].replace(" ", "")
            elif comma_index != -1:
                print("return7")
                return modified_text[start_index:comma_index].replace(" ", "")
            else:
                print("return8")
                return modified_text[start_index:].replace(" ", "")
    else:
        return None