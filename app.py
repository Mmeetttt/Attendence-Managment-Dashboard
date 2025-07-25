# enhanced_attendance_app.py
import streamlit as st
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import io
import warnings
warnings.filterwarnings('ignore')

# Your credentials
SENDER_EMAIL = "meet.patel060@nmims.eud.in"
APP_PASSWORD = "fbvx fxmy chkm gdyh"

class AttendanceApp:
    def __init__(self):
        self.init_session_state()
    
    def init_session_state(self):
        """Initialize session state variables"""
        if 'attendance_data' not in st.session_state:
            st.session_state.attendance_data = None
        if 'parent_emails' not in st.session_state:
            st.session_state.parent_emails = {}
        if 'email_logs' not in st.session_state:
            st.session_state.email_logs = []
        if 'threshold' not in st.session_state:
            st.session_state.threshold = 80.0
    
    def load_attendance_data(self, file_path=None, uploaded_file=None):
        """Load attendance data from file or upload"""
        try:
            if uploaded_file is not None:
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_csv(file_path)
            
            # Process attendance data
            day_cols = [col for col in df.columns if "Day" in col]
            df["Total_Classes"] = len(day_cols)
            df["Classes_Attended"] = df[day_cols].sum(axis=1)
            df["Attendance_Percentage"] = (df["Classes_Attended"] / df["Total_Classes"]) * 100
            
            def get_status(percentage):
                if percentage >= st.session_state.threshold:
                    return "Good"
                elif percentage >= 60:
                    return "Warning"
                else:
                    return "Debarr"
            
            df["Status"] = df["Attendance_Percentage"].apply(get_status)
            
            # Monthly breakdown
            months = ['June', 'July', 'August']
            for month in months:
                month_cols = [col for col in df.columns if month in col and "Day" in col]
                if month_cols:
                    df[f"{month}_Attendance"] = (df[month_cols].sum(axis=1) / len(month_cols)) * 100
            
            st.session_state.attendance_data = df
            return True
            
        except Exception as e:
            st.error(f"Error loading data: {e}")
            return False
    
    def send_email(self, to_email, student_name, attendance_pct, subject_name, roll_no):
        """Send email to parent"""
        try:
            msg = MIMEMultipart()
            msg['From'] = SENDER_EMAIL
            msg['To'] = to_email
            msg['Subject'] = f"Attendance Alert - {student_name} (Roll No: {roll_no})"
            
            body = f"""
Dear Parent/Guardian,

This is to inform you about your child's attendance status.

Student Details:
- Name: {student_name}
- Roll Number: {roll_no}
- Subject: {subject_name}
- Current Attendance: {attendance_pct:.2f}%

Your child's attendance is below the required threshold of {st.session_state.threshold}%. 
Please ensure regular attendance to maintain academic performance.

Best regards,
Academic Department
NMIMS
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(SENDER_EMAIL, APP_PASSWORD.replace(" ", ""))
                server.send_message(msg)
            
            # Log the email
            log_entry = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "student_name": student_name,
                "roll_no": roll_no,
                "parent_email": to_email,
                "attendance": attendance_pct,
                "status": "Sent Successfully"
            }
            st.session_state.email_logs.append(log_entry)
            
            return True
            
        except Exception as e:
            log_entry = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "student_name": student_name,
                "roll_no": roll_no,
                "parent_email": to_email,
                "attendance": attendance_pct,
                "status": f"Failed: {str(e)}"
            }
            st.session_state.email_logs.append(log_entry)
            return False

def main():
    st.set_page_config(
        page_title="Attendance Management System",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    app = AttendanceApp()
    
    # Sidebar
    st.sidebar.title("📚 Attendance System")
    st.sidebar.markdown("---")
    
    # Navigation
    page = st.sidebar.selectbox(
        "Choose a page",
        ["📋 Manage Data","🏠 Dashboard", "👨‍👩‍👧‍👦 Parent Emails", "📧 Send Notifications", "📊 Analytics", "📈 Reports", "⚙️ Settings"]
    )
    
    # Threshold setting in sidebar
    st.sidebar.markdown("### Settings")
    new_threshold = st.sidebar.slider(
        "Attendance Threshold (%)",
        min_value=50.0,
        max_value=100.0,
        value=st.session_state.threshold,
        step=1.0
    )
    
    if new_threshold != st.session_state.threshold:
        st.session_state.threshold = new_threshold
        if st.session_state.attendance_data is not None:
            # Recalculate status with new threshold
            def get_status(percentage):
                if percentage >= st.session_state.threshold:
                    return "Good"
                elif percentage >= 60:
                    return "Warning"
                else:
                    return "Debarr"
            st.session_state.attendance_data["Status"] = st.session_state.attendance_data["Attendance_Percentage"].apply(get_status)
    
    # Main content based on page selection
    if page == "🏠 Dashboard":
        show_dashboard(app)
    elif page == "📋 Manage Data":
        show_data_management(app)
    elif page == "👨‍👩‍👧‍👦 Parent Emails":
        show_parent_email_management(app)
    elif page == "📧 Send Notifications":
        show_email_notifications(app)
    elif page == "📊 Analytics":
        show_analytics(app)
    elif page == "📈 Reports":
        show_reports(app)
    elif page == "⚙️ Settings":
        show_settings(app)

def show_dashboard(app):
    st.title("📊 Attendance Dashboard")
    
    if st.session_state.attendance_data is None:
        st.warning("Please load attendance data first from the 'Manage Data' page.")
        return
    
    df = st.session_state.attendance_data
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Students", len(df))
    
    with col2:
        good_students = len(df[df['Status'] == 'Good'])
        st.metric("Good Attendance", good_students, f"{good_students/len(df)*100:.1f}%")
    
    with col3:
        low_attendance = len(df[df['Status'] != 'Good'])
        st.metric("Below Threshold", low_attendance, f"{low_attendance/len(df)*100:.1f}%")
    
    with col4:
        avg_attendance = df['Attendance_Percentage'].mean()
        st.metric("Average Attendance", f"{avg_attendance:.1f}%")
    
    # Quick visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Status Distribution")
        status_counts = df['Status'].value_counts()
        fig = px.pie(
            values=status_counts.values,
            names=status_counts.index,
            color_discrete_map={'Good': 'green', 'Warning': 'orange', 'Debarr': 'red'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Attendance Distribution")
        fig = px.histogram(
            df,
            x='Attendance_Percentage',
            nbins=20,
            title="Attendance Distribution"
        )
        fig.add_vline(x=st.session_state.threshold, line_dash="dash", line_color="red")
        st.plotly_chart(fig, use_container_width=True)
    
    # Students requiring attention
    st.subheader("Students Requiring Attention")
    low_attendance_df = df[df['Status'] != 'Good'].sort_values('Attendance_Percentage')
    
    if not low_attendance_df.empty:
        st.dataframe(
            low_attendance_df[['Roll No', 'Name', 'Subject', 'Attendance_Percentage', 'Status']],
            use_container_width=True
        )
    else:
        st.success("All students have good attendance!")

def show_data_management(app):
    st.title("📋 Data Management")
    
    tab1, tab2 = st.tabs(["📤 Upload Data", "📝 View/Edit Data"])
    
    with tab1:
        st.subheader("Upload Attendance Data")
        
        uploaded_file = st.file_uploader(
            "Choose CSV file",
            type=['csv'],
            help="Upload your attendance data CSV file"
        )
        
        if uploaded_file is not None:
            if st.button("Load Data", type="primary"):
                if app.load_attendance_data(uploaded_file=uploaded_file):
                    st.success("Data loaded successfully!")
                    st.rerun()
        
        st.markdown("### Sample Data Format")
        sample_data = {
            'Roll No': [101, 102, 103],
            'Name': ['John Doe', 'Jane Smith', 'Bob Johnson'],
            'Subject': ['Math', 'Physics', 'Chemistry'],
            'June_Day1': [1, 0, 1],
            'June_Day2': [1, 1, 0],
            'July_Day1': [0, 1, 1]
        }
        st.dataframe(pd.DataFrame(sample_data))
    
    with tab2:
        if st.session_state.attendance_data is not None:
            st.subheader("Current Data")
            
            # Search and filter options
            col1, col2 = st.columns(2)
            with col1:
                search_term = st.text_input("Search by name or roll number")
            with col2:
                status_filter = st.selectbox("Filter by status", ["All", "Good", "Warning", "Debarr"])
            
            df = st.session_state.attendance_data.copy()
            
            # Apply filters
            if search_term:
                df = df[
                    df['Name'].str.contains(search_term, case=False, na=False) |
                    df['Roll No'].astype(str).str.contains(search_term, na=False)
                ]
            
            if status_filter != "All":
                df = df[df['Status'] == status_filter]
            
            st.dataframe(df, use_container_width=True)
            
            # Download processed data
            csv = df.to_csv(index=False)
            st.download_button(
                label="Download processed data as CSV",
                data=csv,
                file_name=f"processed_attendance_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        else:
            st.info("No data loaded yet.")

def show_parent_email_management(app):
    st.title("👨‍👩‍👧‍👦 Parent Email Management")
    
    if st.session_state.attendance_data is None:
        st.warning("Please load attendance data first.")
        return
    
    df = st.session_state.attendance_data
    
    tab1, tab2 = st.tabs(["➕ Add/Edit Emails", "📋 View All Emails"])
    
    with tab1:
        st.subheader("Add or Update Parent Emails")
        
        # Select student
        students = df[['Roll No', 'Name']].drop_duplicates()
        student_options = [f"{row['Roll No']} - {row['Name']}" for _, row in students.iterrows()]
        
        selected_student = st.selectbox("Select Student", student_options)
        
        if selected_student:
            roll_no = int(selected_student.split(' - ')[0])
            student_name = selected_student.split(' - ')[1]
            
            # Current email (if exists)
            current_email = st.session_state.parent_emails.get(roll_no, "")
            
            if current_email:
                st.info(f"Current email: {current_email}")
            
            # Email input
            new_email = st.text_input(
                "Parent Email Address",
                value=current_email,
                placeholder="parent@example.com"
            )
            
            if st.button("Save Email"):
                if new_email and "@" in new_email:
                    st.session_state.parent_emails[roll_no] = new_email
                    st.success(f"Email saved for {student_name}")
                else:
                    st.error("Please enter a valid email address")
    
    with tab2:
        st.subheader("All Parent Emails")
        
        if st.session_state.parent_emails:
            email_df = pd.DataFrame([
                {
                    "Roll No": roll_no,
                    "Student Name": df[df['Roll No'] == roll_no]['Name'].iloc[0] if len(df[df['Roll No'] == roll_no]) > 0 else "Unknown",
                    "Parent Email": email
                }
                for roll_no, email in st.session_state.parent_emails.items()
            ])
            
            st.dataframe(email_df, use_container_width=True)
            
            # Bulk email upload
            st.subheader("Bulk Email Upload")
            uploaded_emails = st.file_uploader(
                "Upload CSV with Roll No and Parent Email columns",
                type=['csv'],
                key="email_upload"
            )
            
            if uploaded_emails is not None:
                try:
                    email_data = pd.read_csv(uploaded_emails)
                    if 'Roll No' in email_data.columns and 'Parent Email' in email_data.columns:
                        if st.button("Import Emails"):
                            for _, row in email_data.iterrows():
                                st.session_state.parent_emails[int(row['Roll No'])] = row['Parent Email']
                            st.success(f"Imported {len(email_data)} emails")
                    else:
                        st.error("CSV must have 'Roll No' and 'Parent Email' columns")
                except Exception as e:
                    st.error(f"Error reading file: {e}")
        else:
            st.info("No parent emails stored yet.")

def show_email_notifications(app):
    st.title("📧 Email Notifications")
    
    if st.session_state.attendance_data is None:
        st.warning("Please load attendance data first.")
        return
    
    df = st.session_state.attendance_data
    low_attendance_students = df[df['Status'] != 'Good'].sort_values('Attendance_Percentage')
    
    if low_attendance_students.empty:
        st.success("No students require email notifications!")
        return
    
    st.subheader("Students Requiring Notifications")
    
    # Show students who need emails
    students_needing_emails = []
    for _, student in low_attendance_students.iterrows():
        roll_no = student['Roll No']
        if roll_no in st.session_state.parent_emails:
            students_needing_emails.append({
                "Roll No": roll_no,
                "Name": student['Name'],
                "Subject": student['Subject'],
                "Attendance": student['Attendance_Percentage'],
                "Parent Email": st.session_state.parent_emails[roll_no],
                "Status": student['Status']
            })
    
    if not students_needing_emails:
        st.warning("No parent emails found for students with low attendance. Please add emails first.")
        return
    
    email_df = pd.DataFrame(students_needing_emails)
    st.dataframe(email_df, use_container_width=True)
    
    # Send options
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Send All Emails", type="primary"):
            progress_bar = st.progress(0)
            sent_count = 0
            
            for i, student in enumerate(students_needing_emails):
                if app.send_email(
                    student['Parent Email'],
                    student['Name'],
                    student['Attendance'],
                    student['Subject'],
                    student['Roll No']
                ):
                    sent_count += 1
                
                progress_bar.progress((i + 1) / len(students_needing_emails))
            
            st.success(f"Sent {sent_count} out of {len(students_needing_emails)} emails")
    
    with col2:
        # Individual email sending
        st.subheader("Send Individual Email")
        selected_student_email = st.selectbox(
            "Select student",
            [f"{s['Roll No']} - {s['Name']}" for s in students_needing_emails]
        )
        
        if st.button("Send Individual Email"):
            selected_roll = int(selected_student_email.split(' - ')[0])
            student_data = next(s for s in students_needing_emails if s['Roll No'] == selected_roll)
            
            if app.send_email(
                student_data['Parent Email'],
                student_data['Name'],
                student_data['Attendance'],
                student_data['Subject'],
                student_data['Roll No']
            ):
                st.success(f"Email sent to {student_data['Name']}'s parent")
            else:
                st.error("Failed to send email")

def show_analytics(app):
    st.title("📊 Advanced Analytics")
    
    if st.session_state.attendance_data is None:
        st.warning("Please load attendance data first.")
        return
    
    df = st.session_state.attendance_data
    
    # Subject-wise analysis
    st.subheader("Subject-wise Analysis")
    
    if 'Subject' in df.columns:
        subject_stats = df.groupby('Subject').agg({
            'Attendance_Percentage': ['mean', 'min', 'max', 'count']
        }).round(2)
        subject_stats.columns = ['Average', 'Minimum', 'Maximum', 'Student Count']
        st.dataframe(subject_stats, use_container_width=True)
        
        # Subject-wise box plot
        fig = px.box(df, x='Subject', y='Attendance_Percentage', title="Attendance Distribution by Subject")
        fig.add_hline(y=st.session_state.threshold, line_dash="dash", line_color="red")
        st.plotly_chart(fig, use_container_width=True)
    
    # Monthly trend analysis
    st.subheader("Monthly Trend Analysis")
    monthly_cols = [col for col in df.columns if col.endswith('_Attendance')]
    
    if monthly_cols:
        monthly_data = df[monthly_cols].mean()
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=[col.replace('_Attendance', '') for col in monthly_cols],
            y=monthly_data.values,
            mode='lines+markers',
            name='Average Attendance'
        ))
        fig.add_hline(y=st.session_state.threshold, line_dash="dash", line_color="red", annotation_text="Threshold")
        fig.update_layout(title="Monthly Attendance Trend", xaxis_title="Month", yaxis_title="Attendance %")
        st.plotly_chart(fig, use_container_width=True)

def show_reports(app):
    st.title("📈 Reports")
    
    if st.session_state.attendance_data is None:
        st.warning("Please load attendance data first.")
        return
    
    # Email logs
    st.subheader("Email Logs")
    if st.session_state.email_logs:
        logs_df = pd.DataFrame(st.session_state.email_logs)
        st.dataframe(logs_df, use_container_width=True)
        
        # Download email logs
        csv = logs_df.to_csv(index=False)
        st.download_button(
            label="Download Email Logs",
            data=csv,
            file_name=f"email_logs_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    else:
        st.info("No email logs available yet.")
    
    # Generate comprehensive report
    st.subheader("Generate Comprehensive Report")
    if st.button("Generate Report"):
        df = st.session_state.attendance_data
        
        report = f"""
# Attendance Report - {datetime.now().strftime('%Y-%m-%d')}

## Summary Statistics
- Total Students: {len(df)}
- Average Attendance: {df['Attendance_Percentage'].mean():.2f}%
- Students with Good Attendance: {len(df[df['Status'] == 'Good'])}
- Students Needing Attention: {len(df[df['Status'] != 'Good'])}

## Low Attendance Students
"""
        
        low_attendance = df[df['Status'] != 'Good']
        for _, student in low_attendance.iterrows():
            report += f"- {student['Name']} (Roll: {student['Roll No']}): {student['Attendance_Percentage']:.2f}%\n"
        
        st.download_button(
            label="Download Report",
            data=report,
            file_name=f"attendance_report_{datetime.now().strftime('%Y%m%d')}.md",
            mime="text/markdown"
        )

def show_settings(app):
    st.title("⚙️ Settings")
    
    # Email configuration
    st.subheader("Email Configuration")
    st.info(f"Sender Email: {SENDER_EMAIL}")
    st.warning("Email credentials are pre-configured. Contact admin to change.")
    
    # Data management
    st.subheader("Data Management")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Clear All Data", type="secondary"):
            if st.checkbox("I confirm I want to clear all data"):
                st.session_state.attendance_data = None
                st.session_state.parent_emails = {}
                st.session_state.email_logs = []
                st.success("All data cleared!")
                st.rerun()
    
    with col2:
        if st.button("Export All Settings"):
            settings = {
                "parent_emails": st.session_state.parent_emails,
                "threshold": st.session_state.threshold,
                "email_logs": st.session_state.email_logs
            }
            st.download_button(
                label="Download Settings",
                data=str(settings),
                file_name=f"settings_backup_{datetime.now().strftime('%Y%m%d')}.json",
                mime="application/json"
            )

if __name__ == "__main__":
    main()
