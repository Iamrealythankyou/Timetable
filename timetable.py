
def add_event(events_dir: list[dict], week: str, when: str, where: str, detail: str | None = None) -> list[dict]:
    input_list = [week, when, where, detail]
    item = {}
    # exist overlap
    while (len(search_event(events_dir, input_list[0], input_list[1])) != 0):
        input_str = input(
            "Please, input event time again, existing overlap in event time")
        input_list = [n for n in input_str.replace('\n', "").split(',')]
    for x in range(0, 4):
        item.update({list(events_dir[0].keys())[x]: input_list[x]})
    events_dir.append(item)
    return events_dir


def search_event(events_dir: list[dict], week: str | None = None, when: str | None = None, where: str | None = None, detail: str | None = None) -> list:
    def f(events: list[dict], x: str): return [
        n for n in events if x in n.values()]
    argues_list = [n for n in [week, where, detail] if n != None]
    for n in argues_list:
        events_dir = f(events_dir, n)
    if when != None:

    return events_dir


test_dir1 = {'week': 'week1', 'when': '11:29',
             'where': 'unisa', 'detail': 'study geography'}

test_dir8 = {'week': 'week1', 'when': '11:2900',
             'where': 'F1 building', 'detail': 'study python'}
test_dir2 = {'week': 'week2', 'when': '10:29',
             'where': 'unisa', 'detail': 'study manage'}
test_dir3 = {'week': 'week3', 'when': '1:29',
             'where': 'unisa', 'detail': 'study computers'}
test_dir4 = {'week': 'week4', 'when': '1:39',
             'where': 'unisa', 'detail': 'study Math'}
test_dir5 = {'week': 'week5', 'when': '12:29',
             'where': 'unisa', 'detail': 'study programming'}
test_dir6 = {'week': 'week6', 'when': '21:29',
             'where': 'unisa', 'detail': 'study practice'}
test_dir7 = {'week': 'week7', 'when': '11:59',
             'where': 'unisa', 'detail': 'study security'}
test_list = [test_dir1, test_dir2, test_dir3,
             test_dir4, test_dir5, test_dir6, test_dir7, test_dir8]
print(search_event(test_list, "week1", "11:29"))
print(add_event(test_list, "week7", "22:50", "home", "sleeping at home"))
