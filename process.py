import calendar
import datetime
import io
import json


def wrap_text(text):
    return f"{{\"content\": \"{text}\"}}"


def filter_through_list(obj):
    with io.StringIO() as string:
        type_ = obj["type"]
        string.write(f"-# {type_["effect"]} \\* {type_["group"]} (pg. {type_["page"]})\\n")
        # The first line looks like '-# $EFFECT \* $GROUP (pg. $PAGE)'

        string.write(f"**{obj["name"]}**\\n")

        for point in obj["points"]:
            string.write(f"- {point}\\n")

        if "comment" in obj:
            string.write(f"\"{obj["comment"]}\"")

        return string.getvalue()


def determine_date():
    timezone = datetime.timezone(datetime.timedelta(hours=-8))  # I set this to
    # Pacific Time, one hour before Mountain Time, where I live, on the
    # off-chance I'm up just past midnight.
    current_time = datetime.datetime.now(tz=timezone)

    with io.StringIO() as string:
        string.write(f"## {current_time.day}")

        mod = current_time.day % 10
        if mod == 1 and current_time.day != 11:
            string.write("st ")  # "1st", "21st", etc.
        elif mod == 2 and current_time.day != 12:
            string.write("nd ")  # "2nd", "22nd", etc.
        elif mod == 3 and current_time.day != 13:
            string.write("rd ")  # "3rd", "23rd", etc.
        else:
            string.write("th ")  # "4th", "12th", "20th", etc.

        string.write(f"{calendar.month_name[current_time.month]}, {current_time.year}")
        return string.getvalue()


def primary():
    with open("data.json") as file_pointer:
        obj = json.loads(json.load(file_pointer)["body"])

    with open("messages.txt", "x") as file_pointer:
        header = determine_date()
        file_pointer.write(f"{wrap_text(header)}\n")

        for sub_obj in obj:
            line = filter_through_list(sub_obj)
            file_pointer.write(f"{wrap_text(line)}\n")


if __name__ == "__main__":
    primary()
