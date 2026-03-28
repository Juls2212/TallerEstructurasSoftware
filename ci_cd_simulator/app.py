import streamlit as st

from core import CICDSimulator


st.set_page_config(page_title="CI/CD Simulator", page_icon=":gear:", layout="wide")


def get_simulator() -> CICDSimulator:
    if "simulator" not in st.session_state:
        st.session_state.simulator = CICDSimulator()
    return st.session_state.simulator


simulator = get_simulator()

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
    st.subheader("Execution Agents")
    st.caption("Array: fixed execution agents.")
    st.table(simulator.get_agents_status())

with top_right:
    st.subheader("Waiting Queue")
    st.caption("Queue: jobs waiting for the first free agent.")
    queue_status = simulator.get_queue_status()
    if queue_status:
        st.table(queue_status)
    else:
        st.warning("The waiting queue is empty.")

middle_left, middle_right = st.columns(2)

with middle_left:
    st.subheader("Pipeline Stages")
    st.caption("Singly linked list: each stage points to the next stage.")
    stage_rows = []
    pipeline_stages = simulator.get_pipeline_stages()
    for index, stage_name in enumerate(pipeline_stages, start=1):
        next_stage = pipeline_stages[index] if index < len(pipeline_stages) else "None"
        stage_rows.append(
            {
                "Node": index,
                "Stage": stage_name,
                "Next": next_stage,
            }
        )
    st.table(stage_rows)

with middle_right:
    st.subheader("Deployed Versions Stack")
    st.caption("Stack: top version appears first.")
    versions_stack = simulator.get_versions_stack()
    if versions_stack:
        version_rows = []
        for index, version in enumerate(versions_stack, start=1):
            version_rows.append(
                {
                    "Position": index,
                    "Version": version,
                    "State": "Top" if index == 1 else "Stored",
                }
            )
        st.table(version_rows)
    else:
        st.warning("No versions have been deployed yet.")

st.divider()

action_left, action_right = st.columns(2)

with action_left:
    st.subheader("Job Processing")
    st.caption("The first queued job is assigned to the first free agent.")
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

st.subheader("Logs Console")
st.caption("List: logs stored in a Python list and displayed like console output.")
logs_filter = st.text_input("Filter logs", value="")
filtered_logs = simulator.get_logs(logs_filter)

with st.container(border=True):
    if filtered_logs:
        console_output = "\n".join(filtered_logs)
        st.code(console_output, language="text")
    else:
        st.warning("No logs match the current filter.")
