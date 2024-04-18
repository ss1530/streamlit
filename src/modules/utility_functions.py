import re
import json


def to_pascal_case(text):
    """
    Converts a given text to Pascal Case, treating underscores as word separators.

    Args:
        text (str): The text to convert.

    Returns:
        str: The text converted to Pascal Case.
    """
    return " ".join(word.capitalize() for word in text.replace("_", " ").split())


def annotate_abbreviations(text, abbrev_dict):
    """Annotate abbreviations in text with HTML tooltips, adding color and background styling."""
    # Regex to find abbreviations, matching whole words only
    regex_pattern = (
        r"\b(" + "|".join(re.escape(abbrev) for abbrev in abbrev_dict.keys()) + r")\b"
    )

    # Replacement function to add tooltips and style
    def replace(match):
        abbrev = match.group(0)
        title = abbrev_dict.get(abbrev.upper(), "Unknown abbreviation")
        # Added background color (light yellow) and text color (dark red) for emphasis
        return f'<span title="{title}" style="text-decoration: underline; font-style: italic; background-color: #FFFF99; color: #CC0000;">{abbrev}</span>'
    return re.sub(regex_pattern, replace, text, flags=re.IGNORECASE)

def load_file(filepath):
    """Loads JSON data from a file.

    Args:
        filepath (str): The path to the JSON file.

    Returns:
        dict: The loaded JSON data as a Python dictionary.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        json.JSONDecodeError: If the file contains invalid JSON data.
    """

    with open(filepath, "r") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(f"Failed to parse JSON from '{filepath}': {e}")


def get_abbreviations_dict(filepath):
    """
    Load abbreviation data from a JSON file and convert it into a dictionary.

    Args:
        filepath (str): The path to the JSON file containing abbreviations.

    Returns:
        dict: A dictionary where keys are abbreviations and values are their meanings.
    """
    data = load_file(
        filepath
    )  # Load the JSON data using the previously defined load_file method
    abbreviations_dict = {item["Abbreviation"]: item["Meaning"] for item in data}
    return abbreviations_dict
