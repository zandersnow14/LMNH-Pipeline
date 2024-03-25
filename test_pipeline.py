"""Unit tests for pipeline.py"""

from pipeline import get_ratings, get_emergencies, get_assistances, missing_key

def test_get_ratings():
    """Tests if correct rating data is retrieved."""
    test_data = {
        'at': '2023-11-14',
        'site': '3',
        'val': 4
    }

    ratings = get_ratings(test_data)[0]

    assert len(ratings) == 3
    assert ratings == ['2023-11-14', 4, 5]

def test_get_emergency():
    """Tests if correct emergency data is retrieved."""
    test_data = {
        'at': '2023-11-14',
        'site': '3',
        'val': -1,
        'type': 1
    }

    emergency = get_emergencies(test_data)[0]

    assert len(emergency) == 2
    assert emergency == ['2023-11-14', 4]


def test_get_assistances():
    """Tests if correct assistance data is retrieved."""
    test_data = {
        'at': '2023-11-14',
        'site': '3',
        'val': -1,
        'type': 0
    }

    emergency = get_assistances(test_data)[0]

    assert len(emergency) == 2
    assert emergency == ['2023-11-14', 4]

def test_no_missing_key():
    """Tests whether no missing key returns False."""
    data = {
        'at': '2023-11-14',
        'site': '3',
        'val': 4
    }

    assert missing_key(data) is False

def test_missing_key_log(caplog):
    """Checks if correct messages are logged to the terminal."""
    data = {
        'at': '2023-11-14',
        'site': '3',
    }
    missing_key(data)
    output = caplog.messages
    assert 'missing val' in output[0]
    assert "{'at': '2023-11-14', 'site': '3'}" in output[0]

def test_missing_key_true():
    """Checks if missing key returns True."""
    data = {
        'at': '2023-11-14',
        'site': '3',
    }

    assert missing_key(data)
