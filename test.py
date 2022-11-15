
import pytest

# draft

@pytest.mark.parametrize("titles,expected", [(["Chris Hemsworth","Natalie Portman"], 0.8), (["Throat singing","Black hole"], 0.2), (["Politician","Reptilian humanoid"], 1)])
def test_similar(titles,expected):
    content_1 = fetch_content(titles[0])
    content_2 = fetch_content(titles[1])

    assert abs(similarity(content_1, content_2) - expected) < 0.1


def fetch_content(title):
    return "Lorem ipsum dolor sit amet, consectetur adipiscing"

def similarity(content_1,content_2):
    return 0
