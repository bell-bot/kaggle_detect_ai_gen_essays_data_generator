import re

from faker import Faker

fake = Faker()


def get_placeholder_dict(additional_values=None):
    if additional_values is None:
        additional_values = {}
    your_first_name = fake.first_name()
    your_last_name = fake.last_name()
    your_name = f"{your_first_name} {your_last_name}"
    your_address = fake.street_address()
    your_city = fake.city()
    your_state = fake.country_code()
    your_zip = fake.postcode()
    your_email = fake.ascii_free_email()
    your_phone = fake.phone_number()
    date = str(fake.date_between(start_date="-10y"))
    senator_first_name = fake.first_name()
    senator_last_name = fake.last_name()
    senator_name = f"{senator_first_name} {senator_last_name}"
    senators_address = fake.street_address()

    placeholder_dict = {
        "name": your_name,
        "firstname": your_first_name,
        "lastname": your_last_name,
        "lastnam": your_last_name,
        "addressline": your_address,
        "address": your_address,
        "officaddress": your_address,
        "officiaddress": your_address,
        "officisenataddress": your_address,
        "senataddress": your_address,
        "senateofficaddress": your_address,
        "senatorioofficaddress": your_address,
        "senat": senator_name,
        "statesenat": senator_name,
        "titl": fake.sentence(),
        "citi": your_city,
        "insertstate": your_state,
        "date": date,
        "zip": your_zip,
        "zipcode": your_zip,
        "currentdate": date,
        "todaydate": date,
        "senatname": senator_name,
        "senatfullname": senator_name,
        "statesenatname": senator_name,
        "statesenataddress": senators_address,
        "senatlastname": senator_last_name,
        'statesenatlastname': senator_last_name,
        "phonenumber": your_phone,
        "emailaddress": your_email,
        "contactinform": your_email,
        "state": your_state,
        "sourc": fake.url(),
        'addresssenatoroffic': senators_address,
        'insertstatename': your_state,
        'senatofficaddress': senators_address,
        'phonenumberemailaddress': your_email,
    }

    for (key, value) in additional_values.items():
        components = re.split("\s+", value)
        evaluated_values = []
        for component in components:
            try:
                evaluated_values.append(eval(component))
            except SyntaxError:
                evaluated_values.append(component)
            except NameError:
                evaluated_values.append(component)
        placeholder_dict[key] = " ".join(evaluated_values)

    return placeholder_dict