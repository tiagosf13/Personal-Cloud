import re


def is_valid_input(text_list):
    # Define a regular expression pattern to match valid characters
    valid_characters_pattern = re.compile(r'^[a-zA-Z0-9,.!?()\'" @]+$')

    for review_text in text_list:
        # Check if the review contains only characters not in the valid pattern

        valid = valid_characters_pattern.match(review_text) or \
                re.search(r"<script>", review_text) or \
                re.search(r"onload=", review_text) or \
                re.search(r"<img", review_text) or \
                "'" in review_text

        if not valid:
            return False
    # If none of the checks above returned False, the review is valid
    return True

def is_valid_input(text_list):

    for review_text in text_list:
        # Check if the review contains only characters not in the valid pattern

        not_valid = re.search(r"<script>", review_text) or \
                re.search(r"onload=", review_text) or \
                re.search(r"<img", review_text) or \
                "'" in review_text
        if not_valid:
            return False
    # If none of the checks above returned False, the review is valid
    return True