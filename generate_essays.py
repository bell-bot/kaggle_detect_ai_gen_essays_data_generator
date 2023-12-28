import os

from src.utils.generator_utils import generate_essays


if __name__ == "__main__":
    num_essays = int(input("Please enter the number of essays to generate:  "))
    path_to_train_prompts = "data/train_prompts.csv"
    path_to_training_essays = "data/training_essays.csv"
    out_path = "data/generated_essays.csv"
    print(f"""
        The program currently expects the file containing the prompts and the file containing the training essays to 
        be in the following locations:
        - {path_to_train_prompts}
        - {path_to_training_essays}
    """)
    change_location = input("Do you want to change the locations? (Y/n):    ")
    if change_location.lower() == "y":
        while True:
            print("Please enter the location of the training prompts.")
            path_to_train_prompts = input()

            confirm = input(f"Please confirm that the new location is {path_to_train_prompts}. (Y/n):     ")
            if confirm.lower() == "y":
                break

        while True:
            print("Please enter the location of the training data")
            path_to_training_essays = input()

            confirm = input(f"Please confirm that the new location is {path_to_training_essays}. (Y/n):     ")
            if confirm.lower() == "y":
                break

    change_out_location = input(f"The generated essays will be stored in {out_path}. Do you want to change this location? (Y/n):    ")

    if (change_out_location.lower() == "y"):
        while True:
            print("Please enter the location and filename for the output file.")
            out_path = input()

            confirm = input(f"Please confirm that the new location is {out_path}. (Y/n):     ")
            if confirm.lower() == "y":
                break

    try:
        openai_api_key = os.environ['OPENAI_API_KEY']
    except KeyError:
        openai_api_key = input("Please enter your OpenAi API Key:    ")

    generate_essays(path_to_train_prompts, path_to_training_essays, num_essays, out_path, openai_api_key)