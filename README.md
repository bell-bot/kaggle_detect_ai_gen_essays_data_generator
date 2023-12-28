# kaggle_detect_ai_gen_essays_data_generator
This repository provides an easy way to generate additional training data for the "Detect AI Generated Essays" Kaggle competition using the gpt-3.5 model.

## Usage

### Set Up
During development, I was using Python 3.10. This should work for other versions too but I have not tested it.

The OpenAI API required an API key. You can obtain a key from your OpenAI account. You can store this in an environment variable called `OPENAI_API_KEY` or provide it directly when starting the program. The program will automatically ask you
to provide the api key if none is stored in the `OPENAI_API_KEY` environment variable.

This program requires several packages that may not be installed yet. 
- `pandas`: Used to read and manipulate the data
- `nltk`: Used to normalise the placeholder names
- `Faker`: Used to generate fake values for placeholders
- `uuid`: Used to generate a unique ID for each new sample
- `openai`: Used to query the gpt model

To ensure all required packages are installed, run the following commands:

```
pip install nltk Faker pandas uuid openai 
```
### Generate Essays

Generate essays by cloning this project and navigating to the top-level project directory.

Start the program using the following command:

```
python3 generate_essays.py
```

Before generating the essays, you will be requested to enter the number of essays to generate. This can be any positive integer. Keep in mind that using the gpt model-family is not free so I suggest starting with a small amount of essays to prevent unforseen costs.

The program expects the file with the training data and training prompts to be under the `/data` directory. This is also where the output file will be saved to. You will have the option to change this is you desire.
