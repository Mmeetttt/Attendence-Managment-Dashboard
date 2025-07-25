# Enhanced Attendance Management Dashboard

## 📊 Overview

This is a comprehensive and interactive web application built with Streamlit designed to simplify and enhance the process of managing student attendance. It allows educators and administrators to easily upload attendance data, track student performance, identify at-risk students, automate parent notifications, and gain insights through various analytics and reports.

## ✨ Features

  * **CSV Data Upload:** Easily import your attendance records from a CSV file.
  * **Automated Calculations:** Automatically calculates total classes, classes attended, and attendance percentages.
  * **Dynamic Status Assignment:** Categorizes students into "Good," "Warning," or "Debarr" based on a configurable attendance threshold.
  * **Interactive Dashboard:** Provides a quick overview of key metrics, status distribution, and attendance trends.
  * **Parent Email Management:** Add, edit, and bulk upload parent email addresses for targeted communication.
  * **Automated Email Notifications:** Send personalized attendance alerts to parents of students below the set threshold.
  * **Advanced Analytics:** Visualize attendance trends by subject and over different months.
  * **Comprehensive Reports:** Generate and download detailed reports, including email logs.
  * **Configurable Threshold:** Adjust the attendance percentage threshold directly from the sidebar.
  * **Search & Filter:** Easily find and filter student data within the app.

## 🚀 Try the App Live\!

Experience the Enhanced Attendance Management Dashboard yourself.
Click on the link below to access the deployed application:

👉 [**Launch the Attendance App**](https://mmeetttt-attendence-managment-dashboard-app-jdjrwz.streamlit.app/)

## 📸 Screenshots
<img width="2879" height="1455" alt="image" src="https://github.com/user-attachments/assets/67dd024d-89bb-4314-9dd8-3575f5c1fb73" />


## ⚙️ How to Run Locally

If you want to run this application on your local machine for development or testing, follow these steps:

1.  **Clone the Repository:**

    ```bash
    git clone https://github.com/mmeetttt/attendence-managment-dashboard-app.git # Replace with your actual repo URL
    cd attendence-managment-dashboard-app
    ```

2.  **Create a Virtual Environment (Recommended):**

    ```bash
    python -m venv venv
    # On Windows:
    .\venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
    ```

3.  **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Set Up Environment Variables (for email sending):**
    For security, email credentials are not hardcoded. Create a `.streamlit` folder in your project root, and inside it, create a file named `secrets.toml`. Add your sender email and app password (or an application-specific password generated for your email provider) to this file:

    ```toml
    # .streamlit/secrets.toml
    SENDER_EMAIL = "your_sender_email@example.com"
    APP_PASSWORD = "your_app_password"
    ```

    **Important:** Do **NOT** commit `secrets.toml` to your public GitHub repository\! Add `.streamlit/secrets.toml` to your `.gitignore` file.

5.  **Run the Streamlit App:**

    ```bash
    streamlit run enhanced_attendance_app.py
    ```

    This will open the application in your web browser.

## 🛠️ Technologies Used

  * [Streamlit](https://streamlit.io/)
  * [Pandas](https://pandas.pydata.org/)
  * [Plotly](https://plotly.com/python/)
  * [Matplotlib](https://matplotlib.org/)
  * [Seaborn](https://seaborn.pydata.org/)
  * [smtplib](https://docs.python.org/3/library/smtplib.html) (for email)

## 🤝 Contributing

Contributions are welcome\! If you have suggestions for improvements, new features, or find any bugs, please feel free to:

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/your-feature-name`).
3.  Make your changes.
4.  Commit your changes (`git commit -m 'Add new feature'`).
5.  Push to the branch (`git push origin feature/your-feature-name`).
6.  Open a Pull Request.

## 📄 License

This project is open source and available under the [MIT License](https://www.google.com/search?q=LICENSE).

-----
