import streamlit as st
import sqlite3
from datetime import datetime
import pandas as pd
import plotly.graph_objects as go


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="ChangeWise",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(
            circle at 85% 5%,
            rgba(56,189,248,0.07),
            transparent 25%
        ),
        radial-gradient(
            circle at 5% 90%,
            rgba(99,102,241,0.07),
            transparent 25%
        ),
        #080b12;
    color: #f8fafc;
}

/* ================= SIDEBAR ================= */

section[data-testid="stSidebar"] {
    background: #090d15;
    border-right: 1px solid #1e293b;
}

section[data-testid="stSidebar"] > div {
    padding-top: 25px;
}

/* ================= TEXT ================= */

h1, h2, h3 {
    color: #f8fafc !important;
}

.page-heading {
    font-size: 34px;
    font-weight: 800;
    letter-spacing: -1px;
}

.page-description {
    color: #64748b;
    font-size: 14px;
    margin-bottom: 25px;
}

/* ================= CARDS ================= */

div[data-testid="stMetric"] {
    background: linear-gradient(
        145deg,
        #111827,
        #0d121c
    );

    border: 1px solid #1e293b;
    border-radius: 16px;
    padding: 18px;

    min-height: 115px;

    box-shadow:
        0 8px 30px rgba(0,0,0,.18);
}

div[data-testid="stMetric"]:hover {
    border-color: #334155;
}

div[data-testid="stMetricLabel"] {
    color: #64748b !important;
    font-size: 11px !important;
    font-weight: 700 !important;
    text-transform: uppercase;
    letter-spacing: 1px;
}

div[data-testid="stMetricValue"] {
    color: #f8fafc !important;
    font-size: 30px !important;
    font-weight: 800 !important;
}

/* ================= CONTAINERS ================= */

div[data-testid="stVerticalBlockBorderWrapper"] {
    background: #0d121c;
    border-color: #1e293b !important;
    border-radius: 16px !important;
}

/* ================= BUTTONS ================= */

.stButton > button {
    background: #111827;
    color: #e2e8f0;

    border: 1px solid #263244;
    border-radius: 9px;

    font-weight: 600;

    transition: .2s;
}

.stButton > button:hover {
    border-color: #38bdf8;
    color: #38bdf8;
    background: #111827;
}

.stFormSubmitButton > button {
    background: linear-gradient(
        135deg,
        #0ea5e9,
        #6366f1
    );

    border: none;
    color: white;
    font-weight: 700;
}

/* ================= INPUTS ================= */

.stTextInput input,
.stTextArea textarea {

    background: #0b1018 !important;

    color: #f8fafc !important;

    border: 1px solid #1e293b !important;

    border-radius: 9px !important;
}

.stTextInput input:focus,
.stTextArea textarea:focus {
    border-color: #38bdf8 !important;
}

/* SELECT */

div[data-baseweb="select"] > div {
    background: #0b1018 !important;
    color: #f8fafc !important;
    border-color: #1e293b !important;
}

/* ================= SIDEBAR BRAND ================= */

.sidebar-title {
    font-size: 24px;
    font-weight: 800;
    color: #f8fafc;
}

.sidebar-subtitle {
    color: #64748b;
    font-size: 10px;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: 1px;
}

/* ================= STATUS ================= */

.status-pending {
    color: #fbbf24;
}

.status-approved {
    color: #4ade80;
}

.status-rejected {
    color: #f87171;
}

.status-implemented {
    color: #38bdf8;
}

/* ================= CODE / TERMINAL ================= */

.terminal-box {
    background: #05070b;
    border: 1px solid #1e293b;
    border-radius: 10px;
    padding: 15px;

    font-family: 'JetBrains Mono', monospace;

    color: #64748b;
    font-size: 11px;
}

/* ================= DIVIDER ================= */

hr {
    border-color: #1e293b !important;
}

/* ================= DATAFRAME ================= */

[data-testid="stDataFrame"] {
    border: 1px solid #1e293b;
    border-radius: 10px;
}

/* ================= HIDE STREAMLIT ================= */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# DATABASE
# ============================================================

DATABASE = "changewise.db"


def get_connection():

    return sqlite3.connect(DATABASE)


def initialize_database():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS change_requests (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            title TEXT NOT NULL,

            description TEXT,

            requested_by TEXT,

            priority TEXT,

            impact TEXT,

            reason TEXT,

            status TEXT,

            created_at TEXT

        )
    """)

    connection.commit()

    connection.close()


initialize_database()


# ============================================================
# DATABASE OPERATIONS
# ============================================================

def add_change_request(
    title,
    description,
    requested_by,
    priority,
    impact,
    reason
):

    connection = get_connection()

    connection.execute("""
        INSERT INTO change_requests
        (
            title,
            description,
            requested_by,
            priority,
            impact,
            reason,
            status,
            created_at
        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?)

    """, (
        title,
        description,
        requested_by,
        priority,
        impact,
        reason,
        "Pending",
        datetime.now().strftime("%Y-%m-%d %H:%M")
    ))

    connection.commit()

    connection.close()


def get_change_requests():

    connection = get_connection()

    data = pd.read_sql_query(
        """
        SELECT *
        FROM change_requests
        ORDER BY id DESC
        """,
        connection
    )

    connection.close()

    return data


def update_status(change_id, status):

    connection = get_connection()

    connection.execute(
        """
        UPDATE change_requests
        SET status = ?
        WHERE id = ?
        """,
        (status, change_id)
    )

    connection.commit()

    connection.close()


# ============================================================
# HELPER
# ============================================================

def priority_icon(priority):

    if priority == "Critical":
        return "🔴"

    if priority == "High":
        return "🟠"

    if priority == "Medium":
        return "🟡"

    return "🟢"


def status_icon(status):

    if status == "Pending":
        return "🟡"

    if status == "Approved":
        return "🟢"

    if status == "Rejected":
        return "🔴"

    if status == "Implemented":
        return "🔵"

    return "⚪"


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        "⚙️",
        unsafe_allow_html=False
    )

    st.markdown(
        '<div class="sidebar-title">ChangeWise</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-subtitle">SOFTWARE CHANGE CONTROL</div>',
        unsafe_allow_html=True
    )

    st.divider()

    page = st.radio(
        "WORKSPACE",
        [
            "Dashboard",
            "Submit Change",
            "Change Requests",
            "Change Approval"
        ]
    )

    st.divider()

    st.markdown(
        """
        <div class="terminal-box">

        <span style="color:#4ade80;">
        ● SYSTEM ONLINE
        </span>

        <br><br>

        MODULE<br>
        <span style="color:#38bdf8;">
        SCM / CHANGE CONTROL
        </span>

        <br><br>

        DATABASE<br>
        <span style="color:#38bdf8;">
        SQLite
        </span>

        <br><br>

        VERSION<br>
        <span style="color:#38bdf8;">
        v1.0.0
        </span>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    st.caption("Software Engineering")
    st.caption("Mini Project")


# ============================================================
# LOAD DATA
# ============================================================

data = get_change_requests()


# ============================================================
# DASHBOARD
# ============================================================

if page == "Dashboard":

    st.markdown(
        '<div class="page-heading">Change Control Dashboard</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="page-description">'
        'Monitor and control software changes across the project lifecycle.'
        '</div>',
        unsafe_allow_html=True
    )

    total = len(data)

    pending = (
        len(data[data["status"] == "Pending"])
        if total else 0
    )

    approved = (
        len(data[data["status"] == "Approved"])
        if total else 0
    )

    rejected = (
        len(data[data["status"] == "Rejected"])
        if total else 0
    )

    implemented = (
        len(data[data["status"] == "Implemented"])
        if total else 0
    )


    # METRICS

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "TOTAL CHANGES",
        total,
        "Change Requests"
    )

    c2.metric(
        "PENDING REVIEW",
        pending,
        "Awaiting decision"
    )

    c3.metric(
        "APPROVED",
        approved,
        "Authorized changes"
    )

    c4.metric(
        "IMPLEMENTED",
        implemented,
        "Completed changes"
    )


    st.write("")


    # WORKFLOW

    with st.container(border=True):

        st.subheader("Change Lifecycle")

        st.caption(
            "Controlled Software Configuration Management workflow"
        )

        workflow = st.columns(7)

        steps = [
            "REQUEST",
            "→",
            "IMPACT",
            "→",
            "REVIEW",
            "→",
            "APPROVAL"
        ]

        for column, step in zip(workflow, steps):

            with column:

                if step == "→":

                    st.markdown(
                        "<h3 style='text-align:center;color:#334155;'>→</h3>",
                        unsafe_allow_html=True
                    )

                else:

                    st.markdown(
                        f"""
                        <div style="
                            background:#111827;
                            border:1px solid #263244;
                            border-radius:9px;
                            padding:12px 4px;
                            text-align:center;
                            color:#38bdf8;
                            font-size:10px;
                            font-weight:700;
                        ">
                        {step}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )


    st.write("")


    # TWO COLUMN AREA

    left, right = st.columns([1.4, 1])


    # RECENT REQUESTS

    with left:

        with st.container(border=True):

            st.subheader("Recent Change Requests")

            st.caption(
                "Latest modifications submitted to the change register"
            )

            if total == 0:

                st.info(
                    "No change requests yet."
                )

            else:

                for _, row in data.head(5).iterrows():

                    st.markdown(
                        f"""
                        **CR-{row['id']:03d}**
                        {priority_icon(row['priority'])}
                        **{row['title']}**

                        `{row['status']}` •
                        {row['requested_by'] or 'Unknown'} •
                        {row['created_at']}
                        """,
                    )

                    st.divider()


    # STATUS CHART

    with right:

        with st.container(border=True):

            st.subheader("Request Status")

            st.caption(
                "Current distribution"
            )

            if total:

                counts = data["status"].value_counts()

                fig = go.Figure(
                    data=[
                        go.Pie(
                            labels=counts.index,
                            values=counts.values,
                            hole=.65
                        )
                    ]
                )

                fig.update_layout(
                    height=300,
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(
                        color="#94a3b8"
                    ),
                    margin=dict(
                        l=5,
                        r=5,
                        t=10,
                        b=5
                    )
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

            else:

                st.info(
                    "No data available."
                )


# ============================================================
# SUBMIT CHANGE
# ============================================================

elif page == "Submit Change":

    st.markdown(
        '<div class="page-heading">Submit Change Request</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="page-description">'
        'Create a controlled request for a software modification.'
        '</div>',
        unsafe_allow_html=True
    )


    left, right = st.columns([1.4, 1])


    with left:

        with st.container(border=True):

            st.subheader(
                "Change Request Details"
            )

            st.caption(
                "Provide information required for technical review."
            )

            with st.form("change_form"):

                title = st.text_input(
                    "Change Title",
                    placeholder="Add Face Recognition Attendance"
                )

                description = st.text_area(
                    "Description",
                    placeholder="Describe the proposed change..."
                )

                requested_by = st.text_input(
                    "Requested By",
                    placeholder="Client / Developer / Tester"
                )

                col1, col2 = st.columns(2)

                with col1:

                    priority = st.selectbox(
                        "Priority",
                        [
                            "Low",
                            "Medium",
                            "High",
                            "Critical"
                        ]
                    )

                with col2:

                    impact = st.selectbox(
                        "Estimated Impact",
                        [
                            "Low",
                            "Medium",
                            "High"
                        ]
                    )

                reason = st.text_area(
                    "Reason for Change",
                    placeholder="Why is this change required?"
                )

                submit = st.form_submit_button(
                    "Submit Change Request",
                    use_container_width=True
                )

                if submit:

                    if not title.strip():

                        st.error(
                            "Please enter a change title."
                        )

                    else:

                        add_change_request(
                            title,
                            description,
                            requested_by,
                            priority,
                            impact,
                            reason
                        )

                        st.success(
                            "Change request successfully created!"
                        )

                        st.balloons()


    with right:

        with st.container(border=True):

            st.subheader(
                "Change Control Process"
            )

            st.caption(
                "Every change follows a controlled lifecycle."
            )

            st.markdown(
                """
                ### 01
                **Submit Request**

                ↓

                ### 02
                **Impact Analysis**

                ↓

                ### 03
                **Technical Review**

                ↓

                ### 04
                **Approve / Reject**

                ↓

                ### 05
                **Implementation**

                ↓

                ### 06
                **Verification**
                """
            )


# ============================================================
# CHANGE REQUESTS
# ============================================================

elif page == "Change Requests":

    st.markdown(
        '<div class="page-heading">Change Request Register</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="page-description">'
        'Centralized record of all software changes.'
        '</div>',
        unsafe_allow_html=True
    )

    if len(data) == 0:

        st.info(
            "No change requests available."
        )

    else:

        search = st.text_input(
            "Search Change Requests",
            placeholder="Search by title, requester or status..."
        )

        filtered = data.copy()

        if search:

            mask = (
                filtered.astype(str)
                .apply(
                    lambda row:
                    row.str.contains(
                        search,
                        case=False,
                        na=False
                    ).any(),
                    axis=1
                )
            )

            filtered = filtered[mask]


        st.caption(
            f"{len(filtered)} change request(s)"
        )


        for _, row in filtered.iterrows():

            with st.container(border=True):

                c1, c2, c3 = st.columns(
                    [4, 1, 1]
                )

                with c1:

                    st.markdown(
                        f"### CR-{row['id']:03d} — {row['title']}"
                    )

                    st.caption(
                        f"Requested by: "
                        f"{row['requested_by'] or 'Unknown'}"
                        f" • {row['created_at']}"
                    )

                    st.write(
                        row["description"]
                        or "No description provided."
                    )

                with c2:

                    st.write("Priority")

                    st.write(
                        f"{priority_icon(row['priority'])} "
                        f"**{row['priority']}**"
                    )

                with c3:

                    st.write("Status")

                    st.write(
                        f"{status_icon(row['status'])} "
                        f"**{row['status']}**"
                    )


# ============================================================
# CHANGE APPROVAL
# ============================================================

elif page == "Change Approval":

    st.markdown(
        '<div class="page-heading">Change Review Center</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="page-description">'
        'Perform impact analysis and control change approval.'
        '</div>',
        unsafe_allow_html=True
    )


    if len(data) == 0:

        st.info(
            "No change requests available."
        )

    else:

        selected_id = st.selectbox(
            "Select Change Request",
            data["id"].tolist(),
            format_func=lambda x:
            f"CR-{x:03d}"
        )

        selected = data[
            data["id"] == selected_id
        ].iloc[0]


        st.write("")


        c1, c2, c3 = st.columns(3)

        c1.metric(
            "PRIORITY",
            selected["priority"]
        )

        c2.metric(
            "IMPACT",
            selected["impact"]
        )

        c3.metric(
            "STATUS",
            selected["status"]
        )


        st.write("")


        left, right = st.columns(
            [1.4, 1]
        )


        # IMPACT ANALYSIS

        with left:

            with st.container(border=True):

                st.subheader(
                    "Technical Impact Analysis"
                )

                st.caption(
                    "Assessment of the proposed software modification."
                )

                st.markdown(
                    f"""
                    **Change Request**

                    CR-{selected['id']:03d}

                    **Description**

                    {selected['description'] or 'Not provided'}

                    **Reason**

                    {selected['reason'] or 'Not provided'}

                    **Requested By**

                    {selected['requested_by'] or 'Unknown'}
                    """
                )

                st.divider()

                if selected["impact"] == "High":

                    st.error(
                        "HIGH IMPACT — Detailed technical review and regression testing recommended."
                    )

                elif selected["impact"] == "Medium":

                    st.warning(
                        "MEDIUM IMPACT — Review affected components before implementation."
                    )

                else:

                    st.success(
                        "LOW IMPACT — Limited system effect expected."
                    )


        # DECISION

        with right:

            with st.container(border=True):

                st.subheader(
                    "Change Decision"
                )

                st.caption(
                    "Update the controlled lifecycle state."
                )


                if st.button(
                    "✓ Approve Change",
                    use_container_width=True
                ):

                    update_status(
                        selected_id,
                        "Approved"
                    )

                    st.success(
                        "Change approved."
                    )

                    st.rerun()


                if st.button(
                    "✕ Reject Change",
                    use_container_width=True
                ):

                    update_status(
                        selected_id,
                        "Rejected"
                    )

                    st.error(
                        "Change rejected."
                    )

                    st.rerun()


                if st.button(
                    "◆ Mark Implemented",
                    use_container_width=True
                ):

                    update_status(
                        selected_id,
                        "Implemented"
                    )

                    st.success(
                        "Change marked as implemented."
                    )

                    st.rerun()


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "CHANGEWISE  •  SOFTWARE CONFIGURATION MANAGEMENT  •  CHANGE CONTROL  •  v1.0.0"
)