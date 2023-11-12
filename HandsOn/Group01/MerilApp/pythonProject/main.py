# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def format_waste_type(waste_type):
    # Replace hyphens with spaces
    waste_type = waste_type.replace('-', ' ')
    # Split camel case to words and capitalize each
    waste_type = ' '.join(re.sub('([A-Z][a-z]+)', r' \1', re.sub('([A-Z]+)', r' \1', waste_type)).split())
    return waste_type.capitalize()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    import re

    waste_types = [
        "CDW",
        "biomedicalWaste",
        "clothing",
        "glass",
        "non-recyclable-waste",
        "organicFood",
        "packagingProductsOfPlastics",
        "wastePaper",
        "wasteContainer",
        "horseBed"
    ]




    formatted_waste_types = {waste_type: format_waste_type(waste_type) for waste_type in waste_types}

    print(formatted_waste_types)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
