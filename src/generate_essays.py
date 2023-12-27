from src.utils.generator_utils import generate_essays

if __name__ == "__main__":
    num_essays = input("Please enter the number of essays to generate:  ")
    generate_essays("data/train_prompts.csv","data/training_essays.csv",num_essays,"data/generated_essays.csv")