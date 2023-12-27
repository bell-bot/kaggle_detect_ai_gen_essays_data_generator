import re
import urllib.parse

from typing import Tuple

from src.utils.placeholder_dict import get_placeholder_dict

import nltk

from src.utils.parser import soft_remove_non_alphanum

from nltk.stem import PorterStemmer

from nltk.tokenize import word_tokenize

from nltk.corpus import stopwords

from faker import Faker


class printcolours:
    highlight = '\033[96m'
    none = '\033[0m'


nltk.download('punkt')
nltk.download('stopwords')

PLACEHOLDER_REGEX = r"\[[’,\'A-Za-z0-9\s\w]+\]"
POSITIVE_RESPONSE = ["y", "yes", "ye"]
NEGATIVE_RESPONSE = ["n", "no", "non"]
STOPWORDS = stopwords.words('english')
ps = PorterStemmer()
fake = Faker()
FAKER_DOCS_URL = urllib.parse.quote("faker.readthedocs.io/en/master/")
FAKER_DOCS_LINK = f"https://{FAKER_DOCS_URL}"


def parse_placeholder(placeholder_name: str):
    """
    Parse a string containing of one or more placeholders. Return a list of
    normalized placeholder names
    :param placeholder_name: A string containing the placeholder name, e.g. [Your name] or [Street Name, State, ZIP Code]
    :return: str[]. A list of normalized placeholder names, e.g. [yourname] or [streetname, state, zipcode]
    """
    placeholders = soft_remove_non_alphanum(placeholder_name)
    placeholders = placeholders.split(',')
    parsed_placeholders = []
    for placeholder in placeholders:
        # Split placeholders consisting of multiple terms into a list of strings
        placeholder_components = word_tokenize(placeholder)
        parsed_placeholder_components = ""

        for placeholder_component in placeholder_components:
            if placeholder_component.lower() in STOPWORDS:
                continue
            placeholder_component = ps.stem(placeholder_component)
            parsed_placeholder_components += placeholder_component

        parsed_placeholders.append(parsed_placeholder_components)

    return parsed_placeholders


def get_all_placeholders(responses: [Tuple[int, str, int]]):
    """
    Iterate over a list of essays and return a list containing all the normalized placeholders used without duplicates.
    :param responses: List containing tuples of the form (prompt_id: int, text: str, generated: int) representing the
    ID of the prompt the essay responds to, the essay, and if the essay was AI-generated.
    :return: A list of strings containing the normalized names of placeholders used in the essays.
    """

    # From manual inspection, we know that the placeholders will look like [placeholder name]. Thus, we will use a
    # regex to get all placeholders from the samples first.

    placeholders = [re.findall(PLACEHOLDER_REGEX, text) for (_, text, _) in responses]
    # flatten the list. Using set also removes the duplicates
    placeholders = set([placeholder for placeholder_group in placeholders for placeholder in placeholder_group])

    # Normalize the placeholders
    placeholders = [
        parsed_placeholder for placeholder in placeholders for parsed_placeholder in parse_placeholder(placeholder)
    ]
    return set(placeholders)


def sub_placeholder(placeholder_name: str, placeholder_dict: {str: str}):
    """
    Substitute a single placeholder instance containing one or more placeholder names
    :param placeholder_name: A string representing a placeholder instance. E.g. ["Your name"] or
    ["Your Street Name", "Your City", "Your ZIP Code"]
    :param placeholder_dict: :return:
    """

    placeholders = parse_placeholder(placeholder_name)
    placeholder_values = []

    for placeholder in placeholders:
        try:
            placeholder_value = placeholder_dict[placeholder]
            placeholder_values.append(placeholder_value)
        except KeyError:
            print(f"Placeholder {placeholder} not in dict. Skipping value.")
            placeholder_values.append(f"[{placeholder}]")
    print(f"Substituting {printcolours.highlight}{placeholder_name}{printcolours.none} with {printcolours.highlight}{', '.join(placeholder_values)}{printcolours.none}\n")
    return ", ".join(placeholder_values)


def sub_placeholders_in_essays(responses: [Tuple[int, str, int]], missing_placeholders: {str: str}):
    """
    Substitute all placeholders in a list of essays
    :param responses: A list containing tuples of the form (prompt_id, text, generated) where prompt_id refers to the
    id of the prompt for which the essay way written, text refers to the essay text, and generated is 0 if the essay was
    not AI-generated and 0 if the essay was AI-generated.
    :param missing_placeholders: A dictionary containing any placeholders missing from the standard placeholder
    dictionary as key-value pairs where the key is the placeholder name and the value will substitute the placeholder
    name.
    :return: An object of type [Tuple[prompt_id:int, text: str, generated:int]] containing the same prompt_id and
    generated value as the input but the placeholders in text are substituted with the values defined in the placeholder
    dictionary.
    """

    responses_with_substitutions = []

    for (prompt_id, essay, generated) in responses:
        # Instantiate a new placeholder dictionary and add the missing placeholders
        placeholder_dict = get_placeholder_dict(additional_values=missing_placeholders)

        sub_essay = re.sub(PLACEHOLDER_REGEX, lambda match: sub_placeholder(match.group(), placeholder_dict), essay)
        responses_with_substitutions.append((prompt_id, sub_essay, generated))

    return responses_with_substitutions


def get_missing_placeholders(responses: [Tuple[int, str, int]]):
    """
    Get a list of placeholders used in the essays but not defined in the placeholder dictionary
    :param responses: A list containing tuples of the form (prompt_id, text, generated) where prompt_id refers to the
    id of the prompt for which the essay way written, text refers to the essay text, and generated is 0 if the essay was
    not AI-generated and 0 if the essay was AI-generated.
    :return: A list containing the normalised names of the missing placeholders
    """

    placeholders = get_all_placeholders(responses)
    defined_placeholders = set(get_placeholder_dict().keys())
    missing_placeholders = placeholders - defined_placeholders

    return missing_placeholders


def print_missing_placeholders(missing_placeholders):
    """
    Prints a list of missing placeholders
    :param missing_placeholders: [str]
    :return: None
    """
    print(
        f"""No substitution values are defined for the following {len(missing_placeholders)} placeholders:
    """)

    for placeholder in missing_placeholders: print(f"{placeholder}")
    print()


def request_missing_placeholders(missing_placeholders):
    """
    User interaction that allows the user to provide values for a missing placeholder.
    :param missing_placeholders: [str] containing the names of placeholders
    :return: {str: str} containing the placeholder names as key and replacement value as value.
    """

    while True:

        define_subs = input("Do you want to define substitutions for the missing placeholders now? (y/N)\t")

        if define_subs.lower() in POSITIVE_RESPONSE:

            print(
                f"""
                You will now be asked to provide a value definition for the missing placeholders one by one.
            
                Unless you want to use the same value for each essay, use the python faker package ({FAKER_DOCS_LINK}).
                To call a faker method, use the already initialised `fake` object. E.g. to generate a fake name, enter fake.name()
                
                The placeholder dictionary contains a number of variables that are used to build the replacement values. 
                Use the same name as the pre-defined value if you want the placeholder substitution to be consistent within 
                an essay. 
                For instance, the placeholder dictionary contains a variable `\"your_last_name\"` which returns a random fake
                last name and is used to build the value for the `\"name\"` placeholder. You may have a missing placeholder 
                called `\"yoursistername\"` and want to use the same last name in \"yoursistername\" as in the `\"name\"` placeholder.
                When prompted, you could provide the value in the following way:
                \"yoursistername\": f\"{'{fake.first_name()}'} {'{your_last_name}'}\"
                The example above creates a string composed of a randomly generated and last name where the last name will
                be consistent across the essay.
                
                Here is a list of the variables defined in the placeholder dictionary:
                
                your_first_name = fake.first_name()
                your_last_name = fake.last_name()
                your_name = f"{'{your_first_name}'} {'{your_last_name}'}"
                your_address = fake.street_address()
                your_city = fake.city()
                your_state = fake.country_code()
                your_zip = fake.postcode()
                your_email = fake.ascii_free_email()
                your_phone = fake.phone_number()
                date = str(fake.date_between(start_date="-10y"))
                senator_first_name = fake.first_name()
                senator_last_name = fake.last_name()
                senator_name = f"{'{senator_first_name}'} {'{senator_last_name}'}"
                senators_address = fake.street_address()
                
                """
            )

            missing_placeholders_dict = {}
            for placeholder in missing_placeholders:
                placeholder_value = input(f"{placeholder}:  ")
                missing_placeholders_dict[placeholder] = placeholder_value
            print()
            print(f"{len(missing_placeholders_dict)} placeholder(s) provided. Proceeding.")

            return missing_placeholders_dict

        elif define_subs.lower() in NEGATIVE_RESPONSE:
            print("No substitution values provided for missing placeholders. Proceeding.")
            return {}

        else:
            print(f"Reply '{define_subs}' not recognized. Please try again.")


def provide_missing_placeholders(responses: [Tuple[int, str, int]]):
    """
    Find all placeholders in a list of essays that are not defined in the placeholder dictionary and allow the user
    to define values for them is desired.
    :param responses: A list containing tuples of the form (prompt_id, text, generated) where prompt_id refers to the
    id of the prompt for which the essay way written, text refers to the essay text, and generated is 0 if the essay was
    not AI-generated and 0 if the essay was AI-generated.
    :return: None
    """

    missing_placeholders = get_missing_placeholders(responses)

    if len(missing_placeholders) > 0:
        print_missing_placeholders(missing_placeholders)

        return request_missing_placeholders(missing_placeholders)

    return {}
