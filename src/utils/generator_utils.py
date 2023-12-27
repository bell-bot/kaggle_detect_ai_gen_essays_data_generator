import os
import uuid

import pandas as pd
from openai import OpenAI

from src.utils.placeholder_utils import get_missing_placeholders, provide_missing_placeholders, \
    sub_placeholders_in_essays
from src.utils.prompt_utils import prepare_prompts
from src.utils.query_openai_api import query_chatgpt
from src.utils.utils import get_choices_per_request


def generate_ids(num_essays, train_df):
    existing_ids = train_df["id"].tolist()
    ids = []
    for i in range(0, num_essays):
        new_id = str(uuid.uuid4())[0:8]

        while new_id in existing_ids:
            new_id = str(uuid.uuid4())[0:8]

        existing_ids.append(new_id)
        ids.append(new_id)

    return ids


def generate_essays_for_prompt(prompt, num, prompt_id, client):
    essays = query_chatgpt(prompt, num, client)
    return [[prompt_id, choice.message.content, 1] for choice in essays.choices]


def generate_essays(path_to_training_prompts, path_to_training_data, num_essays, filename):
    # Define your own OpenAI API key here or store it as environment variable
    openai_api_key = os.environ['OPENAI_API_KEY']

    # Initialize OpenAI client
    client = OpenAI(api_key=openai_api_key)

    print("Formatting the prompts.")
    # Format the prompts to contain instructions for the model
    formatted_prompts = prepare_prompts(path_to_training_prompts)
    train_df = pd.read_csv(path_to_training_data)

    # OpenAI generates a maximum of 128 choices per request.
    # The def_choices_per_request creates a list of the length of the number of requires requests to generate num_essays and the number
    # of choices (i.e. essays) per request
    choices_per_requests = get_choices_per_request(num_essays)

    # Iterate over the list containing the number of choices for each request an generate the essays.
    # Results are flattened and stored in the responses list
    responses = []

    print("Generating essays.")
    for num_choices in choices_per_requests:
        response = formatted_prompts.apply(
            lambda row: generate_essays_for_prompt(row["prompt"], num_choices, row["index"], client), 'columns')
        # response currently contains a dataframe where each cell contains a list of lists.
        # We require a simple list of lists so flatten this dataframe
        response = [essay for essays_per_prompt in response.to_list() for essay in essays_per_prompt]
        # add the response to the responses list
        responses += response

    missing_placeholders_dict = provide_missing_placeholders(responses)

    # The essays written by the gpt model may contain placeholders. This method substitutes them with fake values
    responses_with_substitutions = sub_placeholders_in_essays(responses, missing_placeholders_dict)

    # Create a dataframe from the list of lists
    generated_essays_df = pd.DataFrame(responses_with_substitutions, columns=["prompt_id", "text", "generated"])

    # The training dataframe contains a unique id for each essay generated. This method generates unique ids for the generated essays
    generated_essays_df["id"] = generate_ids(num_essays, train_df)

    print("Writing data to file.")
    # Write the data to a csv file
    generated_essays_df.to_csv(filename, index=False)
    print("Done!")
