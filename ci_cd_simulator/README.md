# CI/CD Simulator

## Short Description

This project is a small CI/CD simulator built with Python and Streamlit for a university data structures workshop. It models a simple continuous integration and delivery workflow using in-memory data structures that are easy to explain in class.

## Data Structures Used

- Array
- Queue
- Stack
- List
- Singly linked list

## How Each Required Structure Is Represented in the Code

### Array

The execution agents are stored in a fixed Python list inside `CICDSimulator`. This list acts as the array of available agents: `Ubuntu`, `Windows`, `macOS`, and `Alpine`.

### Queue

The waiting jobs are stored in a Python list used with FIFO behavior. New jobs are added at the end of the list, and the next job is removed from the front.

### Stack

The deployed versions are stored in a Python list used as a stack. Each new version is pushed to the end of the list, and rollback pops the current version from the top.

### List

The execution logs are stored in a normal Python list. Each simulator event adds a new text message to this list.

### Singly Linked List

The pipeline stages are implemented with `StageNode` and `PipelineStages`. Each node stores a stage name and a reference to the next node.

## Project Structure

```text
ci_cd_simulator/
|-- app.py
|-- core.py
|-- requirements.txt
`-- README.md
```

- `app.py`: Streamlit user interface
- `core.py`: simulator logic and data structures
- `requirements.txt`: minimal dependency list
- `README.md`: project documentation

## Installation

Download or clone the project and open the `ci_cd_simulator` folder in your editor or terminal.

## Virtual Environment Setup

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

Activate it on Linux or macOS:

```bash
source .venv/bin/activate
```

## Dependency Installation

Install the required dependency with:

```bash
pip install -r requirements.txt
```

## How to Run the App

From inside the `ci_cd_simulator` folder, run:

```bash
streamlit run app.py
```

Streamlit will open the dashboard in the browser.

## What Can Be Tested in the UI

- Create jobs with a name and branch
- Add jobs to the waiting queue
- Observe the fixed array of execution agents
- Process the next queued job
- Watch the job move through the pipeline stages in order
- Review the log messages generated during execution
- Deploy a version manually
- Inspect the deployed versions stack from top to bottom
- Trigger emergency rollback and verify whether a previous version can be restored

## Notes

The simulator works completely in memory. If the app session restarts, the current jobs, logs, and deployed versions are reset.

The project does not use databases, external services, or real deployment infrastructure. All deployment behavior is simulated locally for teaching purposes.
