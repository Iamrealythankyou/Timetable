# Timetable
# Username:HengSheng Zhou
# Student ID: 110427517
# Email ID: Zhohy042@mymail.unisa.edu.au
# This is my own work as defined by
# the university's academic misconduct policy.
def delet_event(events_dir: list[dict], week: str, when: str) -> list[dict]:
    events_dir.remove(search_event(events_dir, week, when)[0])
    return events_dir


def update_event(events_dir: list[dict], originalweek: str, originalwhen: str, week: str | None = None, when: str | None = None, where: str | None = None, detail: str | None = None) -> list[dict]:
    one_week_events_when = []
    for n in search_event(events_dir, originalweek):
        one_week_events_when.append(
            [n['when'].split(",")[0], n['when'].split(",")[1]])
    target_event = {}
    for n in one_week_events_when:
        if originalwhen in n[0]:
            target_event = search_event(
                events_dir, originalweek, originalwhen)[0]
    deleted_events = delet_event(events_dir, originalweek, originalwhen)
    print(target_event)
    if week != None:
        target_event['week'] = week
    if when != None:
        target_event['when'] = when
    if where != None:
        target_event['where'] = where
    if detail != None:
        target_event['detail'] = detail
    print(target_event)
    return add_event(deleted_events, target_event['week'], target_event['when'], target_event['where'], target_event['detail'])


def legal_checker(week: str, when: str) -> bool:
    flag = True
    legal_week = []
    for n in range(1, 8):
        legal_week.append("week"+str(n))
    flag = False if week not in legal_week else flag
    if flag == True:
        flag = False if when.count(",") != 1 or when.count(
            ":") != 2 or when.count(".") != 0 else flag
    if flag == True:
        flag = False if when[2] != ":" and when[5] != "," and when[8] != ":" else flag
    first_num = second_num = third_num = fourth_num = ""
    if flag == True:
        first_num = when.split(",")[0].split(":")[0]
        second_num = when.split(",")[0].split(":")[1]
        third_num = when.split(",")[1].split(":")[0]
        fourth_num = when.split(",")[1].split(":")[1]
        flag = False if (
            first_num).isnumeric == False or third_num.isnumeric == False or second_num.isnumeric == False or fourth_num.isnumeric == False else flag

    if flag == True:
        flag = False if int(first_num) > 24 or int(first_num) < 0 or int(
            second_num) > 60 or int(second_num) < 0 or int(fourth_num) > 60 or int(fourth_num) < 0 or (int(week[4])-1)*1440 + get_minits(when)[0]+get_minits(when)[1] > 10080 else flag

    return flag


def add_event(events_dir: list[dict], week: str, when: str, where: str, detail: str | None = None) -> list[dict]:
    input_list = [week, when, where, detail]
    item = {}
    flag: bool = True
    iner_flag: bool = True
    # exist overlap
    check_week = week
    check_when = when
    flag = legal_checker(check_week, check_when)
    is_overlap = False
    while (flag != True):
        input_str = input(
            "Please, input event time again, invalid input:  ")
        input_list = [n for n in input_str.replace('\n', "").split(';')]
        if len(input_list) != 3 or len(input_list) != 4:
            flag = False
        flag = legal_checker(input_list[0], input_list[1])
    n = -1
    while (is_overlap != True):
        n += 1
        currentevent_lis = (search_event(events_dir, input_list[0]))
        if len(currentevent_lis) != 0:
            currentevent = (search_event(events_dir, input_list[0]))[n]
            current_event_starttime = get_minits(currentevent['when'])[0]
            current_event_endtime = get_minits(currentevent['when'])[
                1]+current_event_starttime
            input_event_starttime = get_minits(input_list[1])[0]
            input_event_endtime = get_minits(input_list[1])[
                1]+input_event_starttime
            if (input_event_starttime >= current_event_starttime and input_event_starttime <= current_event_endtime) or (input_event_endtime >= current_event_starttime and input_event_endtime <= current_event_endtime) or (input_event_starttime < current_event_starttime and input_event_endtime > current_event_endtime):
                is_formate = False
                while (is_formate == False):
                    input_str = input(
                        "Please, input event time again, existing overlap in event time:  ")
                    input_list = [n for n in input_str.replace(
                        '\n', "").split(';')]
                    if len(input_list) >= 2:
                        is_formate = legal_checker(
                            input_list[0], input_list[1])
                n = -1
            if n+1 == len(search_event(events_dir, input_list[0])):
                is_overlap = True
        else:
            is_overlap = True
    prepare_append = test(
        int(input_list[0][4:5]), input_list[1], input_list[2], input_list[3])
    for y in prepare_append:
        # print(y)
        # for x in range(0, 4):
        #    item.update({list(events_dir[0].keys())[
        #                x]: list(y.values())[x]})
        events_dir.append(y)

    return events_dir


def get_time_str(time: int) -> str:
    hour = int(time/60)
    mini = time % 60
    hour_str = ""
    mini_str = ""
    if hour < 10:
        hour_str = "0"+str(hour)
    else:
        hour_str = str(hour)
    if mini < 10:
        mini_str = "0"+str(mini)
    else:
        mini_str = str(mini)
    return hour_str+":"+mini_str


def test(week: int, when: str, where: str, detail: str) -> list[dict]:
    tiemlist = when.split(",")[0].split(":")
    duration_list = when.split(",")[1].split(":")
    hour = int(tiemlist[0])
    min = int(tiemlist[1])
    minits = hour*60+min
    duration = int(duration_list[0])*60+int(duration_list[1])
    item_list = []
    end_week = week
    gap = 0
    if 1440-minits < duration:
        end_week = week+1
        gap = int((duration-1440+minits) / 1440)
        end_week += gap
    if (end_week-week-1 > 0):
        print("setnersnt")
        for x in range(week+1, gap+week+1):
            item_list.append({'week': "week"+str(x), 'when': "00:00,24:00",
                             'where': where, 'detail': detail})
        s = when.split(",")[0]+","+get_time_str(1440-minits)
        item_list.append({'week': "week"+str(week), 'when': s,
                         'where': where, 'detail': detail})
        s = "00:00"+","
        s += get_time_str((duration-1440+minits-(end_week-week-1)*1440))

        item_list.append({'week': "week"+str(end_week), 'when': s,
                         'where': where, 'detail': detail})
    elif (end_week-week-1 == 0):

        s = when.split(",")[0]+","+get_time_str(1440-minits)
        item_list.append({'week': "week"+str(week), 'when': s,
                         'where': where, 'detail': detail})
        # item_list.append({'week': "week3"+str(3), 'when': s,
        #                  'where': where, 'detail': detail})
        s = "00:00"+"," + get_time_str((duration-1440+minits -
                                        (end_week-week-1)*1440) % 60)

        item_list.append({'week': "week"+str(end_week), 'when': s,
                         'where': where, 'detail': detail})
    else:
        item_list.append({'week': "week"+str(end_week), 'when': when,
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


def print_arrow(time: int, gap: int) -> None:
    for n in range(1, time):
        print("{0:>8}".format("||   "), end="")
        print(" "*gap, end="")
    print()
    for n in range(1, time):
        print("{0:>8}".format("\\  ||  /"), end="")
        print(" "*gap, end="")
    print()
    for n in range(1, time):
        print("{0:>8}".format("\\ || / "), end="")
        print(" "*gap, end="")
    print()
    for n in range(1, time):
        print("{0:>8}".format("\\||/  "), end="")
        print(" "*gap, end="")
    print()
    for n in range(1, time):
        print("{0:>8}".format("\\/   "), end="")
        print(" "*gap, end="")
    print()


def printer(events_dir: list[dict]) -> None:
    def get_hour(a): return int(a/60)
    def get_min(b): return int(b % 60)
    number = 0
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
    # print((all_print_data))
    update_colck = upcolck-1
    time_list = []
    time_list1 = []
    printed_week_list = []
    all_time_duration = []
    for n in all_print_data:
        for m in n:
            time_list.append(m[0])
    time_list1 = []
    plag = False
    print("-"*140)
    print("|Time |"+"{0:18}".format("     Monday"), "{0:18}".format("     Tuesday"), "{0:18}".format("     Wednesday"),
          "{0:18}".format("     Thursday"), "{0:18}".format("     Friday"), "{0:18}".format("     Saturday"), "{0:18}".format("     Sunday"), end="")
    print("|")
    print("-"*140)
    for n in time_list:
        start = get_minits(n)[0]
        end = get_minits(n)[0]+get_minits(n)[1]
        if start + end not in time_list1:
            time_list1.append(get_minits(n)[0]+get_minits(n)[1]
                              )
        if [start, end] not in all_time_duration:
            all_time_duration.append([start, end])
    while (update_colck <= endcolck):
        i = -1
        update_colck += 1
        tempp_start_list = []

        tempp_end_list = []
        is_true = True
        for n in all_time_duration:
            tempp_start_list.append(n[0])
            tempp_end_list.append(n[1])

        for n in all_time_duration:
            if update_colck >= n[0] and update_colck <= n[1]:
                is_true = False
        uplevel = lowlevel = 0
        if is_true:
            if len([n for n in tempp_end_list if n < update_colck]) != 0 and len([n for n in tempp_start_list if n > update_colck]) != 0:
                uplevel = quick_sort(
                    [n for n in tempp_end_list if n < update_colck])[-1]
                lowlevel = quick_sort(
                    [n for n in tempp_start_list if n > update_colck])[0]
            if lowlevel-uplevel > 10:
                print_arrow(7, 15)
                update_colck = lowlevel-1

        print("|", end="")
        for n in time_list:
            if update_colck == get_minits(n)[0]:
                if n.split(",")[0] not in printed_week_list:
                    print(n.split(",")[0]+"|", end="")
                    printed_week_list.append(n.split(",")[0])
                del time_list[time_list.index(n)]
                plag = True
        if update_colck in time_list1:
            print("{0:0=2d}".format(get_hour(update_colck))+":" +
                  "{0:0=2d}".format(get_min(update_colck))+"|", end="")
            del time_list1[time_list1.index(update_colck)]
            plag = True

        if (plag == True):
            plag = False
        elif plag == False:
            print("     |", end="")
            plag = False
        for y in all_print_data:
            i += 1
            tar = ""
            if len(y) != 0:
                listx = get_text(y, update_colck)
                tar = listx[1]
                all_print_data[i] = listx[0]
            print('{0:<18}'.format(tar)+"|", end="")

        print()

    print("-"*140)
    print(all_print_data)


def get_text(weekly_event: list[dict], update_time: int) -> list:
    if (update_time < get_minits(weekly_event[0][0])[0]):
        return [weekly_event, ""]
    elif get_minits(weekly_event[0][0])[0] == update_time:
        return [weekly_event, "="*18]
    elif ((update_time >= get_minits(weekly_event[0][0])[0]) and (update_time < get_minits(weekly_event[0][0])[0]+get_minits(weekly_event[0][0])[1])):
        if len(weekly_event[0]) == 1:
            return [weekly_event, "        +"]
        elif len(weekly_event[0]) != 1 and update_time == get_minits(weekly_event[0][0])[0]+get_minits(weekly_event[0][0])[1]-1:
            return [weekly_event, ">>>"]
        else:
            tempstr = weekly_event[0][1]
            weekly_event[0] = [weekly_event[0][0]]+weekly_event[0][2:]
            return [weekly_event, tempstr]
    else:
        weekly_event = weekly_event[1:]
        return [weekly_event, "="*18]


test_dir1 = {'week': 'week1', 'when': '11:29,01:05',
             'where': 'unisa in Mawson Lakes campus', 'detail': 'study geography'}

test_dir2 = {'week': 'week2', 'when': '10:29,00:05',
             'where': 'unisa', 'detail': 'study manage'}
test_dir12 = {'week': 'week4', 'when': '05:38,00:6',
              'where': 'unisa', 'detail': 'building home enst aen stesrnt'}
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
test_list1 = [test_dir1]
test_dir13 = {'week': 'week3', 'when': '01:59',
              'where': 'Home', 'detail': 'Rush B'}

# printer(test_list1)
# print(add_event(test_list1, "week1", "11:49,00:35", "Home", "Rush B"))
# print(get_information(search_event(test_list, "week1"), 3, False))
# printer(add_event(test_list1, "week3", "23:55,48:30",
#                  "Groge street", "Playing computer games"))
# printer(update_event(test_list1, "week1", "11:29",
#        week='week2', when="12:29,00:20"))
# print(search_event(test_list1, "week1", "11:29"))


# printer(add_event(test_list1, "week1", "11:49,00:35", "Home", "Rush B"))
# print(legal_checker("week1", "20:30,20:10"))
def main() -> None:
    events_lis = []
    operation = input(
        "A for add events;D for delete a events;U for update a event;S for search events;Q for exit ;P for print current events; C for create an example list: ")
    while (operation != 'Q'):
        while (operation not in ['A', 'D', 'U', 'S', 'C', 'P']):
            operation = input("Type in again, invalid input")
        if operation == "A":
            argument = input("Type in an event: ")
            argument_lis = argument.split(";")
            print(len(argument_lis))
            if len(argument_lis) == 4 and legal_checker(argument_lis[0], argument_lis[1]) != False:
                events_lis = add_event(
                    events_lis, argument_lis[0], argument_lis[1], argument_lis[2], argument_lis[3])
                print(events_lis)
        if operation == 'D':
            argument = input("Type in the event you want to delete: ")
            argument_lis = argument.split(";")
            if len(argument_lis) == 2 and legal_checker(argument_lis[0], argument_lis[1]) != False:
                events_lis = delet_event(
                    events_lis, argument_lis[0], argument_lis[1])
        if operation == 'U':
            argument = input("Type in the event you want to change: ")
            argument_lis = argument.split(";")
            if len(argument_lis) == 6 and legal_checker(argument_lis[0], argument_lis[1]) != False:
                events_lis = update_event(
                    events_lis, argument_lis[0], argument_lis[1], argument_lis[2], argument_lis[3], argument_lis[4], argument_lis[5])
        if operation == 'S':
            argument = input("Type in the event you want to search: ")
            argument_lis = argument.split(";")
            if len(argument_lis) == 4 and legal_checker(argument_lis[0], argument_lis[1]) != False:
                print(search_event(
                    events_lis, argument_lis[0], argument_lis[1], argument_lis[2], argument_lis[3]))
        if operation == 'P':
            printer(events_lis)
        if operation == 'C':
            printer(test_list1)

        operation = input(
            "A for add events;D for delete a events;U for update a event;S for search events;Q for exit ;P for print current events; C for create an example list: ")


main()
