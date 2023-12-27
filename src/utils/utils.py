MAX_CHOICES = 128


def get_choices_per_request(num_essays):
    num_requests_required = num_essays // MAX_CHOICES
    choices_in_last_request = num_essays % MAX_CHOICES
    if choices_in_last_request > 0:
        return [MAX_CHOICES] * num_requests_required + [choices_in_last_request]

    return [MAX_CHOICES] * num_requests_required
