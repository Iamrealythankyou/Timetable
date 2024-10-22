# 3 22:30  30

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
    print(end_week)
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


print(test(1, "23:30,00:50", "F3", "studying"))
