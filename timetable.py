

def add_event(events_dir: list[dict], week: str, when: str, where: str, detail: str | None = None) -> list[dict]:
    input_list = [week, when, where, detail]
    item = {}
    flag: bool = True
    iner_flag: bool = True
    # exist overlap
    while (flag):
        while (len(search_event(events_dir, input_list[0], input_list[1].split(',')[0])) != 0):
            input_str = input(
                "Please, input event time again, existing overlap in event time")
            input_list = [n for n in input_str.replace('\n', "").split(';')]
        for n in events_dir:
            if (get_minits(input_list[1])[0] > get_minits(n['when'])[0] and (get_minits(input_list[1])[0] < get_minits(n["when"])[0]+get_minits(n['when'])[1])) or ((get_minits(input_list[1])[0] < get_minits(n['when'])[0]) and get_minits(n['when'])[0] < get_minits(input_list[1])[0]+get_minits(input_list[1])[1]):
                iner_flag = False
                input_str = input(
                    "Please, inpusssssst event time again, existing overlap in event time")
                input_list = [n for n in input_str.replace(
                    '\n', "").split(';')]
        if iner_flag == True:
            prepare_append = test(
                int(input_list[0][4:5]), input_list[1], input_list[2], input_list[3])
            for y in prepare_append:
                for x in range(0, 4):
                    item.update({list(events_dir[0].keys())[
                                x]: list(y.values())[x]})
                events_dir.append(item)
            flag = False
    return events_dir


def test(week: int, when: str, where: str, detail: str) -> list[dict]:
    tiemlist = when.split(",")[0].split(":")
    duration_list = when.split(",")[1].split(":")
    hour = int(tiemlist[0])
    min = int(tiemlist[1])
    minits = hour*60+min
    duration = int(duration_list[0])*60+int(duration_list[1])
    item_list = []
    end_week = week
    if 1440-minits < duration:
        end_week = week+1
        gap = int((duration-1440+minits) / 1440)
        end_week += gap
    if (end_week-week-1 > 0):
        for x in range(week+1, end_week-week-1):
            item_list.append({'week': x, 'when': "00:00,24:00",
                             'where': where, 'detail': detail})
        s = when+","+str(1440-minits)
        item_list.append({'week': week, 'when': s,
                         'where': where, 'detail': detail})
        s = "00:00"+","
        s = str((duration-1440+minits-(end_week-week-1)*1440)/60)+":" + \
            str((duration-1440+minits-(end_week-week-1)*1440) % 60)

        item_list.append({'week': end_week, 'when': s,
                         'where': where, 'detail': detail})
    elif (end_week-week-1 == 0):
        s = when+","+str(1440-minits)
        item_list.append({'week': week, 'when': s,
                         'where': where, 'detail': detail})
        hour_str = str(int((duration-1440+minits-(end_week-week-1)*1440)/60))
        if int(hour_str) < 10:
            hour_str = "0"+(hour_str)
        s = "00:00"+","+hour_str + \
            ":" + str((duration-1440+minits-(end_week-week-1)*1440) % 60)

        item_list.append({'week': end_week, 'when': s,
                         'where': where, 'detail': detail})
    else:
        item_list.append({'week': end_week, 'when': when,
                         'where': where, 'detail': detail})
    return item_list


def get_minits(when: str) -> list[int]:
    tiemlist = when.split(",")[0].split(":")
    duration_list = when.split(",")[1].split(":")
    hour = int(tiemlist[0])
    min = int(tiemlist[1])
    minits = hour*60+min
    duration = int(duration_list[0])*60+int(duration_list[1])
    return [minits, duration]


def search_event(events_dir: list[dict], week: str, when: str | None = None, where: str | None = None, detail: str | None = None) -> list:

    def f(events: list[dict], x: str): return [
        n for n in events if x in n.values()]
    argues_list = [n for n in [week, where, detail] if n != None]
    for n in argues_list:
        events_dir = f(events_dir, n)
# add overlap checking logic here
    if when != None:
        events_dir = [i for i in events_dir if i['when'].split(',')[
            0] == when]
    return events_dir


def get_information(week: list[dict], column: int, hiden: bool) -> list[dict]:
    final_suplist = []
    week = quick_sort_list(week)
    for n in week:
        final_list = []
        context = list(n.values())
        week = context[0]
        when = context[1]
        where = context[2]
        detail = context[3]
        list2 = ["Detail", ":"]
        list1 = ["Location", ":"]
        list4 = detail.split(" ")
        list3 = where.split(" ")
        final_word = list1+list3+list2+list4
        final_list.append(when)
        if hiden == True:
            final_word = list1+list3
        for x in range(0, int(len(final_word)/column)):
            tem_text = ""
            for y in final_word[x*column:x*column+column]:
                y += " "
                tem_text += y
            final_list.append(tem_text)
        tem_text = ""
        for y in final_word[int(len(final_word)/column)*column:]:
            y += " "
            tem_text += y
        if tem_text != "":
            final_list.append(tem_text)
        final_suplist.append(final_list)
    return final_suplist


def quick_sort_list(lis: list[dict]) -> list:
    if (len(lis) <= 1):
        return lis
    pivot = get_minits(lis[-1]['when'])[0]
    left = [n for n in lis[:-1] if get_minits(n['when'])[0] <= pivot]
    right = [n for n in lis[:-1] if get_minits(n['when'])[0] > pivot]
    return quick_sort_list(left) + [lis[-1]] + quick_sort_list(right)


def quick_sort(lis: list[int]) -> list:
    if (len(lis) <= 1):
        return lis
    pivot = lis[-1]
    left = [n for n in lis[:-1] if n <= pivot]
    right = [n for n in lis[:-1] if n > pivot]
    return quick_sort(left) + [pivot] + quick_sort(right)


def printer(events_dir: list[dict]) -> None:
    start_time_list = []
    end_time_list = []
    all_print_data = []
    for n in events_dir:
        start_time = get_minits(n['when'])[0]
        end_time = get_minits(n["when"])[1]+start_time
        start_time_list.append(start_time)
        end_time_list.append(end_time)
    week_list = []
    upcolck = quick_sort(start_time_list)[0]
    endcolck = quick_sort(end_time_list)[-1]
    for n in range(1, 8):
        week = ("week"+str(n))
        all_print_data.append(get_information(
            search_event(events_dir, week), 2, False)) if len(search_event(events_dir, week)) != 0 else all_print_data.append([])
    # printing
    print((all_print_data))
    update_colck = upcolck-1
    time_list = []
    printed_week_list = []
    for n in all_print_data:
        for m in n:
            time_list.append(m[0])
    plag = False
    for x in range(0, endcolck-upcolck):
        i = -1
        update_colck += 1
        for n in time_list:
            if update_colck == get_minits(n)[0]:
                if n.split(",")[0] not in printed_week_list:
                    print(n.split(",")[0], end="")
                    printed_week_list.append(n.split(",")[0])
                del time_list[time_list.index(n)]
                plag = True
        if (plag == True):
            plag = False
        elif plag == False:
            print("     ", end="")
            plag = False
        for y in all_print_data:
            i += 1
            tar = ""
            if len(y) != 0:
                listx = get_text(y, update_colck)
                tar = listx[1]
                all_print_data[i] = listx[0]
            print("|"+'{0:<15}'.format(tar)+"|", end="")

        print()

    print(all_print_data)


def get_text(weekly_event: list[dict], update_time: int) -> list:
    if (update_time < get_minits(weekly_event[0][0])[0]):
        return [weekly_event, ""]
    elif get_minits(weekly_event[0][0])[0] == update_time:
        return [weekly_event, "="*15]
    elif ((update_time >= get_minits(weekly_event[0][0])[0]) and (update_time < get_minits(weekly_event[0][0])[0]+get_minits(weekly_event[0][0])[1])):
        if len(weekly_event[0]) == 1:
            return [weekly_event, "        +"]
        else:
            tempstr = weekly_event[0][1]
            weekly_event[0] = [weekly_event[0][0]]+weekly_event[0][2:]
            return [weekly_event, tempstr]
    else:
        weekly_event = weekly_event[1:]
        return [weekly_event, "*"*15]


test_dir1 = {'week': 'week1', 'when': '11:29,01:05',
             'where': 'unisa in Mawson Lakes campus', 'detail': 'study geography'}

test_dir2 = {'week': 'week2', 'when': '10:29,00:05',
             'where': 'unisa', 'detail': 'study manage'}
test_dir12 = {'week': 'week4', 'when': '05:38,00:19',
              'where': 'unisa', 'detail': 'building home'}
test_dir9 = {'week': 'week6', 'when': '11:29,02:30',
             'where': 'unisa', 'detail': 'writing paper'}
test_dir10 = {'week': 'week1', 'when': '20:29,02:30',
              'where': 'unisa', 'detail': 'driving cars'}
test_dir11 = {'week': 'week1', 'when': '18:29,01:30',
              'where': 'unisa', 'detail': 'playing games'}
test_dir8 = {'week': 'week1', 'when': '14:29,00:30',
             'where': 'F1 building', 'detail': 'study python'}
test_dir3 = {'week': 'week3', 'when': '01:29,00:28',
             'where': 'unisa', 'detail': 'study computers'}
test_dir4 = {'week': 'week4', 'when': '01:39,00:20',
             'where': 'unisa', 'detail': 'study Math'}
test_dir5 = {'week': 'week5', 'when': '12:29,00:10',
             'where': 'unisa', 'detail': 'study programming'}
test_dir6 = {'week': 'week6', 'when': '21:29,01:05',
             'where': 'unisa', 'detail': 'study practice'}
test_dir7 = {'week': 'week7', 'when': '11:59,00:20',
             'where': 'unisa', 'detail': 'study security'}
test_list = [test_dir1, test_dir2, test_dir3,
             test_dir4, test_dir5, test_dir6, test_dir7, test_dir8, test_dir9, test_dir10, test_dir11, test_dir12]
# print(search_event(test_list, "week1", "11:29"))
test_list1 = [test_dir1, test_dir2]
test_dir13 = {'week': 'week3', 'when': '01:59',
              'where': 'Home', 'detail': 'Rush B'}

# print(add_event(test_list1, "week1", "11:49,00:35", "Home", "Rush B"))
# print(get_information(search_event(test_list, "week1"), 3, False))
printer(test_list)
