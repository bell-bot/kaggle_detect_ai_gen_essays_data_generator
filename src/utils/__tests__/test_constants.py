from src.utils.placeholder_utils import FAKER_DOCS_LINK

ESSAY_WITH_PLACEHOLDERS_1 = [
    1,
    'Lorem ipsum dolor sit amet, [Placeholder 1] adipiscing elit. Aenean id erat commodo, egestas enim ac, scelerisque '
    'enim. Nulla vestibulum neque vitae augue placerat tempor. Proin condimentum vel enim sit amet molestie. Nullam '
    'ut sem bibendum ligula pretium facilisis. Aliquam eget erat ut libero tristique euismod. Ut at nisl at felis '
    'dapibus pharetra id posuere sapien. Pellentesque lobortis velit orci, ornare iaculis nibh varius a. In laoreet '
    'ac lacus sit amet aliquam. Praesent sodales odio nisi, in [Your Name] tortor sagittis et. Morbi luctus et ante at '
    'porttitor. Integer elementum eu arcu non vulputate. Praesent sit amet neque ac tellus vulputate facilisis ac '
    'aliquet elit. Morbi nec urna laoreet, euismod eros ut, dignissim velit.',
    0
]

ESSAY_WITH_SUBBED_PLACEHOLDERS_1 = (
    1,
    'Lorem ipsum dolor sit amet, Cool Placeholder adipiscing elit. Aenean id erat commodo, egestas enim ac, scelerisque'
    ' enim. Nulla vestibulum neque vitae augue placerat tempor. Proin condimentum vel enim sit amet molestie. Nullam '
    'ut sem bibendum ligula pretium facilisis. Aliquam eget erat ut libero tristique euismod. Ut at nisl at felis '
    'dapibus pharetra id posuere sapien. Pellentesque lobortis velit orci, ornare iaculis nibh varius a. In laoreet '
    'ac lacus sit amet aliquam. Praesent sodales odio nisi, in Alicia Keys tortor sagittis et. Morbi luctus et ante at '
    'porttitor. Integer elementum eu arcu non vulputate. Praesent sit amet neque ac tellus vulputate facilisis ac '
    'aliquet elit. Morbi nec urna laoreet, euismod eros ut, dignissim velit.',
    0
)

ESSAY_WITH_PLACEHOLDERS_2 = [
    4,
    'No opinions answered oh felicity is resolved hastened. Produced it friendly my if opinions [Adjective]. Enjoy is '
    'wrong folly no taken. It [Company Name, Street Name] insipidity simplicity at interested. Law pleasure attended '
    'differed mrs fat and formerly. Merely thrown garret her law danger him son better excuse. Effect extent narrow '
    'in up chatty. Small are his chief offer happy had.',
    0
]

ESSAY_WITH_MISSING_PLACEHOLDERS = (
    5,
    'Letter wooded direct two men indeed income sister. Impression up admiration he by partiality is. Instantly '
    'immediate his saw one day perceived. Old blushes respect but offices hearted minutes effects. Written parties '
    'winding oh as in without on started. Residence [Missing Placeholder] yet preserved few convinced. Coming regret '
    'simple'
    'longer little am sister on. Do danger in to adieus ladies houses oh eldest. Gone pure late gay ham. They sigh '
    'were not find are rent.',
    0
)

ESSAY_WITH_PLACEHOLDERS_3 = (
    5,
    'Letter wooded direct [Your Name] indeed income sister. Impression up admiration he by partiality is. Instantly '
    'immediate his saw one day perceived. Old blushes respect but offices hearted minutes effects. Written parties '
    'winding oh as in without on started. Residence [Missing Placeholder, Adjective] yet preserved few convinced. '
    'Coming regret simple '
    'longer little am sister on. Do danger in to adieus ladies houses oh eldest. Gone pure late gay ham. They sigh '
    'were not find are rent.',
    0
)

ESSAY_WITH_SUBBED_PLACEHOLDERS_3 = (
    5,
    'Letter wooded direct Alicia Keys indeed income sister. Impression up admiration he by partiality is. Instantly '
    'immediate his saw one day perceived. Old blushes respect but offices hearted minutes effects. Written parties '
    'winding oh as in without on started. Residence [missplacehold], bombastic yet preserved few convinced. Coming '
    'regret simple '
    'longer little am sister on. Do danger in to adieus ladies houses oh eldest. Gone pure late gay ham. They sigh '
    'were not find are rent.',
    0
)

ESSAY_WITHOUT_PLACEHOLDERS = [
    99,
    'Greatly cottage thought fortune no mention he. Of mr certainty arranging am smallness by conveying. Him plate '
    'you allow built grave. Sigh sang nay sex high yet door game. She dissimilar was favourable unreserved nay '
    'expression contrasted saw. Past her find she like bore pain open. Shy lose need eyes son not shot. Jennings '
    'removing are his eat dashwood. Middleton as pretended listening he smallness perceived. Now his but two green '
    'spoil drift. ',
    0
]

STATIC_PLACEHOLDER_DICT = {
    'placehold1': 'Cool Placeholder',
    'name': 'Alicia Keys',
    'companiname': 'Footbook',
    'streetname': 'Sesame Street',
    'adject': 'bombastic'
}

EXPECTED_PRINT_STATEMENTS = [
    "Reply 'mmm' not recognized. Please try again.",
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
    ,
    "2 provided. Proceeding."
]