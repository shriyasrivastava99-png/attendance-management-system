# attendance-management-system
An AI-powered attendance management system built with Python and Hugging Face.
# AI Attendance Management System

## About the Project
The AI Attendance Management System is a Python-based project that helps manage and track student attendance using natural language requests. It uses the Hugging Face Inference API to understand user commands and perform attendance-related operations.

## Features
- View all registered students.
- Check individual student attendance.
- Mark students as present or absent for a specific date.
- Calculate individual attendance percentages.
- Calculate the class attendance average.
- View student details.
- Remove a student from the records.
- Store and update attendance data in a JSON file.
- Interact with the system using simple text requests.

## Technologies Used
- **Python** – Main programming language.
- **Hugging Face** – AI-powered natural language understanding.
- **huggingface_hub** – Python library for Hugging Face API access.
- **python-dotenv** – Loads environment variables securely.
- **JSON** – Stores student and attendance data.

## Project Structure
```text
attendance-management-system/
├── app.py
├── students.json
├── requirement.txt
├── .env
├── .gitignore
└── README.md
```

**Note:** The `.env` file is used locally to store the Hugging Face API token. It must not be uploaded to GitHub.

## Installation and Setup

### 1. Clone the Repository
```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd attendance-management-system
```

Replace `YOUR_GITHUB_REPOSITORY_URL` with your actual repository URL.

### 2. Create a Virtual Environment
```bash
python -m venv venv
```

Activate it on Windows:
```bash
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
python -m pip install -r requirement.txt
```

### 4. Configure the Hugging Face Token
Create a `.env` file in the project folder and add:

```text
HF_TOKEN=your_hugging_face_token
```

Replace the example value with your own Hugging Face access token. Never share or upload your token.

### 5. Run the Application
```bash
python app.py
```

## How to Use
After starting the program, enter a request when prompted:

```text
Enter your request:
```

Example requests:

```text
Show all students
Check attendance of Aarav Sharma
What is the attendance percentage of Diya Verma?
Mark Aarav Sharma present on 2026-10-09
Mark Rohan Singh absent on 2026-10-09
Show class attendance average
Show details of Ananya Gupta
```

Type `exit` to close the program.

## Data Storage
Student names, roll numbers, daily attendance records, present days, total days, and attendance percentages are stored in `students.json`. Attendance calculations can be updated when records change.

## Security
- Keep API tokens in the local `.env` file.
- Add `.env` and `venv/` to `.gitignore`.
- Use sample student data in public repositories.
- Never publish confidential student information or API credentials.

## Future Improvements
- Add a graphical user interface.
- Support attendance reports and CSV exports.
- Add student search and date-wise summaries.
- Improve input validation and error handling.

## Conclusion
The AI Attendance Management System combines Python, JSON data storage, and Hugging Face AI to make attendance management easier through simple text-based commands.

## Author
Developed as a Python and AI-based project to explore attendance automation and natural language processing.

