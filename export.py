import csv


def save_to_file(stack_result, wework_result, remoteok_result):
    file = open("Magic_Report.csv", mode="w", encoding="utf-8")
    writer = csv.writer(file)
    writer.writerow(["title", "company", "link"])

    combined_result = []
    for stack in stack_result:
        combined_result.append(stack)

    for wework in wework_result:
        combined_result.append(wework)

    for remoteok in remoteok_result:
        combined_result.append(remoteok)

    for result in combined_result:
        writer.writerow(list(result.values()))

    return
