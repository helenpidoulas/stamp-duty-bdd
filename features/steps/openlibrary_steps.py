import unicodedata
from behave import given, then
import requests

def _norm_spaces(s: str) -> str:
    if s is None:
        return s
    s = unicodedata.normalize("NFC", s)
    # normalise narrow no-break space (U+202F) and NBSP just in case
    return s.replace("\u202F", " ").replace("\xa0", " ")

@given('I fetch the author payload for "{url}"')
def step_fetch(context, url):
    r = requests.get(url, timeout=15)
    r.raise_for_status()
    context.api_payload = r.json()

@then('the JSON field "{json_path}" should equal "{expected}"')
def step_field_equals(context, json_path, expected):
    actual = context.api_payload.get(json_path)
    assert actual is not None, f"Path {json_path} not found in payload"
    assert str(actual) == expected, f"Expected {expected!r} but got {actual!r}"

@then('the JSON array "{json_path}" should contain "{expected_value}"')
def step_array_contains(context, json_path, expected_value):
    arr = context.api_payload.get(json_path)
    assert arr is not None, f"Path {json_path} not found in payload"
    norm_expected = _norm_spaces(expected_value)
    if isinstance(arr, str):
        assert _norm_spaces(arr) == norm_expected, f"Expected {expected_value!r}, got {arr!r}"
        return
    assert isinstance(arr, list), f"Expected list at {json_path}, got {type(arr)}"
    norm_list = [_norm_spaces(x) for x in arr if isinstance(x, str)]
    assert norm_expected in norm_list, f"{expected_value!r} not found in alternate_names: {arr!r}"
