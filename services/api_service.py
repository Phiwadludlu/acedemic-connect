from flask import jsonify

def format_timeslot_data(timeslots):
    tmp = []

    for slot in timeslots:
        schema = {
            "day" : slot.day,
            "timeslots" : {
                "timeslot_id" : slot.id, 
                "period" : {
                    "start_time" : slot.start_time.isoformat(), 
                    "end_time" : slot.end_time.isoformat()
                }
            }
        }
        tmp.append(schema)

    result = merge_timeslots(tmp)
    return jsonify(result)

def merge_timeslots(data):
    merged_data = {}  # Dictionary to store merged data
    for item in data:
        day = item['day']
        if day not in merged_data:
            # If 'day' is not in merged_data, initialize it with the current item's 'timeslots'
            merged_data[day] = {'day': day, 'timeslots': [item['timeslots']]}
        else:
            # If 'day' is already in merged_data, append the 'timeslots' to the existing list
            merged_data[day]['timeslots'].append(item['timeslots'])

    # Convert the values of the merged_data dictionary to a list
    result = list(merged_data.values())
    return result

def format_module_data(data):

    result = []
    for item in data:
        schema = {
            "id" : item.id,
            "code" : item.code,
            "name" : item.name,
            "type" : "module",
        }
        result.append(schema)

    return jsonify(result)