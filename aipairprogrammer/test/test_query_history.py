import os

import pytest

from aipairprogrammer.query_history import QueryHistory, HistoryItem


@pytest.fixture()
def history():
    #cwd = os.getcwd()
    #filename = f"{cwd}/historytest.txt"
    filename = '/historytest.txt'
    hist = QueryHistory(filename=filename)
    return hist


def test_history_item(history):
    date = '2023-04-05'
    query = "Help Me"
    response = "I can't help you!"
    item = HistoryItem(date=date, query=query, response=response)
    assert item.date == date
    assert item.query == query
    assert item.response == response

    item.date = '2003-09-12'
    item.query = 'Can a drive a car?'
    item.response = "Yes, a cat can drive a car!"
    assert item.date == '2003-09-12'
    assert item.query == 'Can a drive a car?'
    assert item.response == "Yes, a cat can drive a car!"


def test_add(history):
    date = '2022-03-12'
    query = 'Can a cat walk?'
    response = 'A cat can walk on four feet'
    history.add(date=date, query=query, response=response)
    item = history.last()
    assert item.date == date
    assert item.query == query
    assert item.response == response
    date = '2022-06-21'
    query = 'What is a credenza'
    response = 'A credenza is a dining room sideboard.'
    assert item.date == date
    assert item.query == query
    assert item.response == response


def test_add_item(history):
    date = '2023-02-07'
    query = 'Tell me about the current weather conditions in Omaha'
    response = 'It is currently 66 degrees F and clear in Omaha Ne, USA'
    item = HistoryItem(date=date, query=query, response=response)
    history.add_item(item=item)
    new_item = history.last()
    print(f"Old: {item}, New: {new_item}")
    assert new_item.date == date
    assert new_item.query == query
    assert new_item.response == response


def test_count(history):
    num = 0
    cnt = history.count()
    assert cnt == num
    date = '2023-02-07'
    query = 'Tell me about the current weather conditions in Omaha'
    response = 'It is currently 66 degrees F and clear in Omaha Ne, USA'
    history.add(date=date, query=query, response=response)
    num = 1
    cnt = history.count()
    assert cnt == num


def test_limit(history):
    # Test zero case
    sent = 0
    lim = history.limit(sent)
    assert lim == sent
    # Test over limit
    sent = 999
    lim = history.limit(sent)
    assert lim == history.count()
    # Test under limit
    sent = -45
    lim = history.limit(sent)
    assert lim == 0


def test_is_in_bounds(history):
    # When the history dict is empty,
    # limit will return an index value
    # of zero, but the 0th element does
    # not exist. For this case we must
    # check is_in_bounds() which will
    # return False if the history dict
    # is empty and the index is 0 or
    # if the index < 0 or
    # index > len(history)
    index = 0
    cnt = history.count()
    res = history.is_in_bounds(index)
    # Make sure we have zero items in history
    assert index == cnt
    query = 'What is the color purple?'
    response = 'The color purple is a movie released in 1985'
    history.add(query=query, response=response)
    cnt = history.count()
    assert cnt == 1
    index = 0
    res = history.is_in_bounds(index)
    assert res == True
    query = 'What makes the sky blue?'
    response = 'Light refracting through the atmosphere.'
    history.add(query=query, response=response)
    cnt = history.count()
    assert cnt == 2
    index = 0
    res = history.is_in_bounds(index)
    assert res == True
    index = 1
    res = history.is_in_bounds(index)
    assert res == True
    index = 2
    res = history.is_in_bounds(index)
    assert res == False


def test_first(history):
    date = '2023-02-14'
    query = 'What is the color purple?'
    response = 'The color purple is a movie released in 1985'
    item1 = HistoryItem(date=date, query=query, response=response)
    history.add_item(item=item1)
    date = '2023-03-22'
    query = 'What makes the sky blue?'
    response = 'Light refracting through the atmosphere.'
    item2 = HistoryItem(date=date, query=query, response=response)
    history.add_item(item=item2)
    first = history.first()
    assert first.date == item1.date
    last = history.last()
    assert last.date == item2.date


def test_last(history):
    date = '2023-02-14'
    query = 'What is the color purple?'
    response = 'The color purple is a movie released in 1985'
    item1 = HistoryItem(date=date, query=query, response=response)
    history.add_item(item=item1)
    date = '2023-03-22'
    query = 'What makes the sky blue?'
    response = 'Light refracting through the atmosphere.'
    item2 = HistoryItem(date=date, query=query, response=response)
    history.add_item(item=item2)
    first = history.first()
    assert first.date == item1.date
    last = history.last()
    assert last.date == item2.date


def test_next(history):
    date = '2023-02-14'
    query = 'What is the color purple?'
    response = 'The color purple is a movie released in 1985'
    item1 = HistoryItem(date=date, query=query, response=response)
    history.add_item(item=item1)
    date = '2023-03-22'
    query = 'What makes the sky blue?'
    response = 'Light refracting through the atmosphere.'
    item2 = HistoryItem(date=date, query=query, response=response)
    history.add_item(item=item2)
    first = history.first()
    assert first.date == item1.date
    next = history.next()
    assert next == item2



def test_prev(history):
    date = '2023-02-14'
    query = 'What is the color purple?'
    response = 'The color purple is a movie released in 1985'
    item1 = HistoryItem(date=date, query=query, response=response)
    history.add_item(item=item1)
    date = '2023-03-22'
    query = 'What makes the sky blue?'
    response = 'Light refracting through the atmosphere.'
    item2 = HistoryItem(date=date, query=query, response=response)
    history.add_item(item=item2)
    last = history.last()
    assert last == item2
    prev = history.prev()
    assert prev == item1


def test_save_history(history):
    date = '2023-02-14'
    query = 'What is the color purple?'
    response = 'The color purple is a movie released in 1985'
    item1 = HistoryItem(date=date, query=query, response=response)
    history.add_item(item=item1)
    date = '2023-03-22'
    query = 'What makes the sky blue?'
    response = 'Light refracting through the atmosphere.'
    item2 = HistoryItem(date=date, query=query, response=response)
    history.add_item(item=item2)
    history.save_history()
    history.load_history()
    cnt = history.count()
    assert cnt == 2
    first = history.first()
    last = history.last()
    assert item1.date == first.date
    assert item2.date == last.date

def test_clear(history):
    cnt = history.count()
    assert cnt == 0
    date = '2023-02-14'
    query = 'What is the color purple?'
    response = 'The color purple is a movie released in 1985'
    item1 = HistoryItem(date=date, query=query, response=response)
    history.add_item(item=item1)
    date = '2023-03-22'
    query = 'What makes the sky blue?'
    response = 'Light refracting through the atmosphere.'
    item2 = HistoryItem(date=date, query=query, response=response)
    history.add_item(item=item2)
    cnt = history.count()
    assert cnt == 2
    history.clear()
    cnt = history.count()
    assert cnt == 0
