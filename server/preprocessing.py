import datetime
import ast
import json


def preprocess(message):
    data = []
    for item in message:
        data.append(ast.literal_eval(item))

    sum_dict = {}
    last_timestamp = None
    last_DeviceID = None
    for d in data:
        for key, value in d.items():
            if key == 'DeviceID':
                last_DeviceID = value
                continue
            elif key == 'TimeStamp':
                last_timestamp = value
                continue
            sum_dict[key] = sum_dict.get(key, 0) + value

    num_dicts = len(data)
    avg_dict = {}
    for key, value in sum_dict.items():
        if key != 'TimeStamp':
            avg_dict[key] = value / num_dicts

    avg_dict['TimeStamp'] = last_timestamp
    avg_dict['DeviceID'] = last_DeviceID
    return avg_dict