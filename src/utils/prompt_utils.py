import pandas as pd


def format_prompt(row):
    prompt_name = row["prompt_name"]
    instructions = row["instructions"]
    source_text = row["source_text"]
    return f"""You are given the following excerpts discussing the topic '{prompt_name}':
            {source_text}

            Instructions: {instructions}.

            The essay must contain at least 1486 words and at most 8400 words.

            Output:\n"""


def prepare_prompts(path_to_training_prompts):
    prompts_df = pd.read_csv(path_to_training_prompts)
    # Format each prompt and store the result in a pandas Series with column name "prompt"
    formatted_prompts = prompts_df.apply(lambda row: pd.Series({"prompt": format_prompt(row)}), 'columns')
    # Add an index column using the index of the prompt in the original data frame
    formatted_prompts["index"] = formatted_prompts.index

    return formatted_prompts
