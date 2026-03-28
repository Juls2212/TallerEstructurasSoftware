import streamlit as st

from core import CICDSimulator


st.set_page_config(page_title="CI/CD Simulator", page_icon=":gear:", layout="wide")


def get_simulator() -> CICDSimulator:
    if "simulator" not in st.session_state:
        st.session_state.simulator = CICDSimulator()
    return st.session_state.simulator


simulator = get_simulator()


def build_agents_array_rows() -> list[dict]:
    rows = []
    for index, agent in enumerate(simulator.agents):
        rows.append(
            {
                "Index": f"[{index}]",
                "Agent": agent.name,
                "Status": agent.status,
                "Current Job": agent.current_job or "-",
            }
        )
    return rows


def build_queue_rows() -> list[dict]:
    rows = []
    for index, job in enumerate(simulator.waiting_jobs):
        rows.append(
            {
                "Position": index + 1,
                "Queue Role": "Front" if index == 0 else "Waiting",
                "Job ID": job.id,
                "Job Name": job.name,
                "Branch": job.branch,
                "Status": job.status,
            }
        )
    return rows


def build_stack_rows() -> list[dict]:
    rows = []
    versions = simulator.get_versions_stack()
    for index, version in enumerate(versions, start=1):
        rows.append(
            {
                "Level": index,
                "Position": "Top" if index == 1 else "Below Top",
                "Version": version,
            }
        )
    return rows


def build_pipeline_rows() -> list[dict]:
    rows = []
    pipeline_stages = simulator.get_pipeline_stages()
    for index, stage_name in enumerate(pipeline_stages, start=1):
        next_stage = pipeline_stages[index] if index < len(pipeline_stages) else "None"
        rows.append(
            {
                "Node": index,
                "Current Stage": stage_name,
                "Next Stage": next_stage,
            }
        )
    return rows


def build_logs_rows(filter_text: str) -> list[dict]:
    rows = []
    for index, log_entry in enumerate(simulator.get_logs(filter_text), start=1):
        rows.append(
            {
                "Order": index,
                "Event": log_entry,
            }
        )
    return rows

st.title("CI/CD Simulator Dashboard")
st.caption("A simple classroom demo of array, queue, stack, list, and singly linked list.")

overview_columns = st.columns(4)
overview_columns[0].metric("Agents Array", len(simulator.agents))
overview_columns[1].metric("Waiting Jobs", len(simulator.get_queue_status()))
overview_columns[2].metric("Pipeline Stages", len(simulator.get_pipeline_stages()))
overview_columns[3].metric("Version Stack", len(simulator.get_versions_stack()))

st.divider()

with st.container():
    st.subheader("Create Job")
    form_columns = st.columns([2, 2, 1])

    with form_columns[0]:
        job_name = st.text_input("Job name", value="Workshop Build")

    with form_columns[1]:
        branch_name = st.text_input("Branch name", value="main")

    with form_columns[2]:
        st.write("")
        st.write("")
        add_job_clicked = st.button("Add Job", use_container_width=True)

    if add_job_clicked:
        if job_name.strip() and branch_name.strip():
            new_job = simulator.create_job(job_name, branch_name)
            message = simulator.enqueue_job(new_job)
            st.success(message)
        else:
            st.error("Job name and branch name are required.")

st.divider()

top_left, top_right = st.columns(2)

with top_left:
    st.subheader("Execution Agents Array")
    st.caption("Fixed array with indexed positions. This structure does not grow or shrink during the demo.")
    st.table(build_agents_array_rows())
    st.text("[0] Ubuntu   [1] Windows   [2] macOS   [3] Alpine")

with top_right:
    st.subheader("Job Queue (FIFO)")
    st.caption("First In, First Out")
    queue_rows = build_queue_rows()
    if queue_rows:
        st.table(queue_rows)
        first_job = simulator.waiting_jobs[0]
        st.info(f"Front of queue: Job #{first_job.id} - {first_job.name}")
    else:
        st.warning("The waiting queue is empty.")

middle_left, middle_right = st.columns(2)

with middle_left:
    st.subheader("Pipeline Stages Singly Linked List")
    st.caption("Each stage points only to the next stage.")
    st.table(build_pipeline_rows())
    linked_list_text = " -> ".join(f"[{stage}]" for stage in simulator.get_pipeline_stages())
    st.code(linked_list_text, language="text")

with middle_right:
    st.subheader("Deployment Stack (LIFO)")
    st.caption("Last In, First Out")
    stack_rows = build_stack_rows()
    if stack_rows:
        st.table(stack_rows)
        st.info(f"Top version: {stack_rows[0]['Version']}")
    else:
        st.warning("No versions have been deployed yet.")

st.divider()

action_left, action_right = st.columns(2)

with action_left:
    st.subheader("Job Processing")
    st.caption("Processing removes the front job from the queue and assigns it to the first free agent.")
    if st.button("Process Next Job", use_container_width=True):
        process_message = simulator.process_next_job()
        if "completed" in process_message.lower():
            st.success(process_message)
        else:
            st.warning(process_message)

with action_right:
    st.subheader("Deploy Version")
    deploy_columns = st.columns([3, 1])

    with deploy_columns[0]:
        version_name = st.text_input("Version name", value="release-1.0.0")

    with deploy_columns[1]:
        st.write("")
        st.write("")
        deploy_clicked = st.button("Deploy Version", use_container_width=True)

    if deploy_clicked:
        if version_name.strip():
            deploy_message = simulator.deploy_version(version_name.strip())
            st.success(deploy_message)
        else:
            st.error("Version name is required.")

rollback_message = None
if st.button("Emergency Rollback", use_container_width=True):
    rollback_message = simulator.rollback()

if rollback_message is not None:
    if "not possible" in rollback_message.lower():
        st.warning(rollback_message)
    else:
        st.success(rollback_message)

st.divider()

st.subheader("Live Logs List")
st.caption("New events are appended to the end of the list as actions happen.")
logs_filter = st.text_input("Filter logs", value="")
log_rows = build_logs_rows(logs_filter)

with st.container(border=True):
    if log_rows:
        console_output = "\n".join(
            f"{row['Order']:02d}. {row['Event']}" for row in log_rows
        )
        st.code(console_output, language="text")
        with st.expander("Show log list order"):
            st.table(log_rows)
    else:
        st.warning("No logs match the current filter.")
