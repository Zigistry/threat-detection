import re

def replace_github_and_codeberg_url(input_string):
    # I am doing github.com because platform really 
    # doesn't matter to the classification algorithm.
    input_string = str(input_string)
    input_string = re.sub(
        r"https?://(?:www\.)?github\.com/[^/\s]+/[^/\s]+(?:[^\s]*)?",
        "https://example.com/example/example",
        input_string
    )
    input_string = re.sub(
        r"https?://(?:www\.)?codeberg\.org/[^/\s]+/[^/\s]+(?:[^\s]*)?",
        "https://example.com/example/example",
        input_string
    )
    input_string = re.sub(
        r"github/[^/\s]+/[^/\s]+(?:[^\s]*)?",
        "example.com/example/example",
        input_string
    )

    # replace any other with example.com/2
    # I am doing this because,
    # Afaik about ML algorithms, they learn patterns.
    # So, it know like, what the url looks like.
    # Hence:
    # If github.com kind of url is there:
    # it will think it like example.com
    # And any other kind of url.
    # It will think it like https://example.com/2/
    # Why am I doing this? Because:
    # Threat repos generally have their urls like:
    # github.com/example/example/releases/malacious.zip
    # And other urls can be like:
    # img.shields.io/badge/something
    # Thats why I want my ai to know that malacious
    # urls generally look like github.com/example/example/releases/malacious.zip download,
    # which will look like:
    # https://example.com/
    # And just to treat other img.shields.io/badge/something like different urls which will look like:
    # https://example.com/2/"
    # Also, I can implement this in next commit that the repos, I am scanning also go through
    # this special tokenization for maximum accuracy, Maybe? I need to test this.
    input_string = re.sub(
        r"https?://(?!example\.com)[^\s]+",
        "https://example.com/2/",
        input_string
    )

    return input_string