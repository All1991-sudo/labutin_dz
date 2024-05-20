from datetime import datetime
from typing import List
def sorted_dict(data: List[dict], EXECUTED=True) -> List[dict]:
    result = []
    for i in data:
        for k, v in i.items():
            if k == "state":
                if v == "EXECUTED" and EXECUTED:
                    result.append(i)
                else:
                    if not EXECUTED and v == "CANCELED":
                        result.append(i)
    return(result)

#print(sorted_dict([{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'}, {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}, {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'}, {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}]
#, EXECUTED=False))




def sorted_dict2(date: List[dict], sorting=False) -> List[dict]:
    return sorted(date, key=lambda x: datetime.fromisoformat(x["date"]), reverse=sorting)

print(sorted_dict2([{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'}, {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}, {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'}, {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}], sorting=True))
