from datetime import time,datetime
def mergeIntervals(intervals):
    if not intervals:
        return []
    # intervals.sort(key=lambda x : x[0])
    merged_intervals = [intervals[0]]
    for i in range(1,len(intervals)):
        curr_interval = intervals[i]
        last_interval = merged_intervals[-1]
        t1 = curr_interval[0].split(':')
        t2 = last_interval[1].split(':')
        t1 = time(int(t1[0]),int(t1[1]))
        t2 = time(int(t2[0]), int(t2[1]))
        if t1 <= t2:
            t3 = curr_interval[1].split(':')
            t3 = time(int(t3[0]),int(t3[1]))
            merged_intervals[-1] = [last_interval[0], str(max(t2,t3))[:-3]]
        else:
            merged_intervals.append(curr_interval)
    return merged_intervals
def doctor(dbt,dtl,pbt,ptl,md):
    time_format = "%H:%M"
    out = []
    if(dbt[0][0]!=dtl[0]):
        out.append([dbt[0][0]],dtl[0])
    for i in range(min(len(dbt)-1,len(pbt)-1)):
        d1 = dbt[i][1].split(':')
        d1 = time(int(d1[0]),int(d1[1]))
        d2 = dbt[i+1][0].split(':')
        d2 = time(int(d2[0]), int(d2[1]))
        p1 = pbt[i][1].split(':')
        p1 = time(int(p1[0]), int(p1[1]))
        p2 = pbt[i + 1][0].split(':')
        p2 = time(int(p2[0]), int(p2[1]))
        out.append([str(max(d1,p1))[:-3],str(min(d2,p2))[:-3]])
    return out


def find_slots(dbt,dtl,pbt,ptl,md):
    doctor_free_slots = []
    patient_free_slots = []
    #adding first free slot from doctor time limits in doctor free slots
    if dtl[0]!=dbt[0][0]:
        doctor_free_slots.append([dtl[0],dbt[0][0]])
    # adding first free slot from patient time limits in patient free slots
    if ptl[0]!=pbt[0][0]:
        patient_free_slots.append([ptl[0],pbt[0][0]])
    for i in range(len(dbt)-1):
        doctor_free_slots.append([dbt[i][1],dbt[i+1][0]])
    for i in range(len(pbt)-1):
        patient_free_slots.append([pbt[i][1],pbt[i+1][0]])
    #adding last free slot from doctor time limits in doctor free slots
    if dtl[1]!=dbt[-1][1] :
        doctor_free_slots.append([dbt[-1][1],dtl[1]])
    if ptl[1]!=pbt[-1][1]:
        patient_free_slots.append([pbt[-1][1],ptl[1]])
    return doctor_free_slots,patient_free_slots


def convert_to_time(interval):
    t = interval.split(':')
    t = time(int(t[0]),int(t[1]))
    return t

def calc_min(time1,time2):
    import math
    t1 = time1.split(':')
    t2 = time2.split(':')
    t1 = int(t1[0])*60 + int(t1[1])
    t2 = int(t2[0])*60 + int(t2[1])
    mins = math.fabs(t1-t2)
    return mins


def merge_free_slots(d_slots,p_slots,md):
    overlaps = []
    out = []
    for interval1 in d_slots:
        for interval2 in p_slots:
            start1, end1 = convert_to_time(interval1[0]), convert_to_time(interval1[1])
            start2, end2 = convert_to_time(interval2[0]), convert_to_time(interval2[1])
            if start1 < end2 and start2 < end1:
                start = max(start1, start2)
                end = min(end1, end2)
                mins = calc_min(str(start)[:-3], str(end)[:-3])
                if(mins>=md):
                    overlaps.append([str(start)[:-3], str(end)[:-3]])
                out.append([str(start)[:-3], str(end)[:-3]])
    print("total avail free slots",out)
    return overlaps
d = {"doctorBlockedTime": [["9:00", "10:30"],["12:00", "13:00"],["16:00", "18:00"]],
 "patientBlockedTime": [["10:00", "11:30"],["12:30", "14:30"],["14:30", "15:00"],["16:00", "17:00"]],
 "doctTimeLimits": ["8:00", "20:00"],
 "patientTimeLimits": ["7:00", "18:30"],
 "meetingDuration": 45 }
d["doctorBlockedTime"] = mergeIntervals(d["doctorBlockedTime"])
d["patientBlockedTime"]= mergeIntervals(d["patientBlockedTime"])

print("Merged Intervals",d["doctorBlockedTime"])
print("Merged Intervals",d["patientBlockedTime"])

doctor_slots, patient_slots = find_slots(d["doctorBlockedTime"],d["doctTimeLimits"],d["patientBlockedTime"],d["patientTimeLimits"],d["meetingDuration"])
print("Doctor Free Slots",doctor_slots)
print("Patient Free Slots", patient_slots)
free_slots = merge_free_slots(doctor_slots,patient_slots,d["meetingDuration"])
print("free slots",free_slots)
# print(doctor(d["doctorBlockedTime"],d["doctTimeLimits"],d["patientBlockedTime"],d["patientTimeLimits"],d["meetingDuration"]))





