
import json
import os
from datetime import date
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()
token = os.getenv("HF_TOKEN")
client = InferenceClient(token=token) if token else None
FILE = "students.json"
MODEL = "openai/gpt-oss-120b:fastest"


def load_data():
    with open(FILE, encoding="utf-8") as f:
        return json.load(f)


def save_data(data):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def calculate(data):
    percentages = []
    for s in data["students"]:
        attendance = s["attendance"]
        s["present_days"] = sum(attendance.values())
        s["total_days"] = len(attendance)
        p = s["present_days"] / s["total_days"] * 100 if s["total_days"] else 0
        s["attendance_percentage"] = round(p, 2)
        percentages.append(p)
    data["class_attendance_average"] = round(
        sum(percentages) / len(percentages), 2
    ) if percentages else 0


def get_action(request, data):
    names = [
        {"name": s["name"], "roll_no": s["roll_no"]}
        for s in data["students"]
    ]
    result = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "Convert the attendance request into one JSON object. "
                    "Keys: action, name, date. Actions: check, present, "
                    "absent, remove, percentage, average, list. "
                    "Date format YYYY-MM-DD; use empty date if not needed. "
                    "Use only these students: " + json.dumps(names)
                )
            },
            {"role": "user", "content": request}
        ],
        max_tokens=200
    )
    text = result.choices[0].message.content.strip()
    text = text.removeprefix("```json").removesuffix("```").strip()
    return json.loads(text)


def main():
    if not client:
        print("HF_TOKEN missing. Add it to your .env file.")
        return

    data = load_data()
    calculate(data)
    print("AI ATTENDANCE MANAGEMENT SYSTEM")
    print("Type 'exit' to quit.")

    while True:
        request = input("\nEnter your request: ").strip()
        if request.lower() == "exit":
            break

        try:
            cmd = get_action(request, data)
            action = cmd.get("action", "").lower()
            name = cmd.get("name", "").strip()
            day = cmd.get("date", "").strip()

            if action == "average":
                calculate(data)
                print("Class average:", data["class_attendance_average"], "%")
                continue

            if action == "list":
                for s in data["students"]:
                    print(s["roll_no"], s["name"],
                          s["attendance_percentage"], "%")
                continue

            student = next(
                (s for s in data["students"]
                 if s["name"].lower() == name.lower()
                 or s["roll_no"] == name),
                None
            )

            if action == "percentage":
                if student:
                    print(student["name"],
                          student["attendance_percentage"], "%")
                else:
                    print("Student not found.")
                continue

            if action not in ("check", "present", "absent", "remove"):
                print("Unsupported action. Please try again.")
                continue

            if not student:
                print("Student not found.")
                continue

            date.fromisoformat(day)
            period = data["attendance_period"]
            if not period["start_date"] <= day <= period["end_date"]:
                print("Date is outside the attendance period.")
                continue

            if action == "check":
                value = student["attendance"].get(day)
                status = ("Not recorded" if value is None else
                          "Present" if value else "Absent")
                print(json.dumps({
                    "name": student["name"],
                    "date": day,
                    "present": value,
                    "status": status
                }, indent=2))
                continue

            if action == "remove":
                student["attendance"].pop(day, None)
            else:
                student["attendance"][day] = (action == "present")

            calculate(data)
            save_data(data)
            print("Updated successfully.")
            print(json.dumps({
                "name": student["name"],
                "date": day,
                "attendance": student["attendance"].get(day),
                "attendance_percentage": student["attendance_percentage"],
                "class_attendance_average": data["class_attendance_average"]
            }, indent=2))

        except Exception as e:
            print("Error:", e)


if __name__ == "__main__":
    main()
