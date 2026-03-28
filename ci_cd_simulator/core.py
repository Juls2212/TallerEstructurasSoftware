from dataclasses import dataclass
from typing import Generator, List, Optional


@dataclass
class Agent:
    name: str
    status: str = "Free"
    current_job: Optional[str] = None


@dataclass
class Job:
    id: int
    name: str
    branch: str
    status: str = "Queued"


class StageNode:
    """Node used by the singly linked list of pipeline stages."""

    def __init__(self, name: str) -> None:
        self.name = name
        self.next: Optional["StageNode"] = None


class PipelineStages:
    """Singly linked list used to store pipeline stages in order."""

    def __init__(self) -> None:
        self.head: Optional[StageNode] = None

    def append(self, stage_name: str) -> None:
        new_node = StageNode(stage_name)

        if self.head is None:
            self.head = new_node
            return

        current = self.head
        while current.next is not None:
            current = current.next
        current.next = new_node

    def __iter__(self) -> Generator[StageNode, None, None]:
        current = self.head
        while current is not None:
            yield current
            current = current.next

    def to_list(self) -> List[str]:
        return [node.name for node in self]


class CICDSimulator:
    def __init__(self) -> None:
        # Array: fixed Python list of execution agents.
        self.agents: List[Agent] = [
            Agent("Ubuntu"),
            Agent("Windows"),
            Agent("macOS"),
            Agent("Alpine"),
        ]

        # Queue: Python list used as a FIFO queue for waiting jobs.
        self.waiting_jobs: List[Job] = []

        # List: Python list used to store execution logs.
        self.logs: List[str] = []

        # Stack: Python list used to store deployed versions for rollback.
        self.deployed_versions: List[str] = []

        # Singly linked list: stores pipeline stages in execution order.
        self.pipeline_stages = PipelineStages()
        for stage_name in [
            "Checkout",
            "Install Dependencies",
            "Linter",
            "Unit Tests",
            "Deployment",
        ]:
            self.pipeline_stages.append(stage_name)

        self.next_job_id = 1

    def create_job(self, name: str, branch: str) -> Job:
        job = Job(
            id=self.next_job_id,
            name=name.strip(),
            branch=branch.strip(),
        )
        self.next_job_id += 1
        return job

    def enqueue_job(self, job: Job) -> str:
        self.waiting_jobs.append(job)
        self.add_log(
            f"Job #{job.id} for {job.name} on branch {job.branch} entered the queue."
        )
        return f"Job #{job.id} added to the queue."

    def add_log(self, message: str) -> None:
        self.logs.append(message)

    def get_logs(self, filter_text: Optional[str] = None) -> List[str]:
        if not filter_text:
            return list(self.logs)

        normalized_filter = filter_text.lower()
        return [
            log_message
            for log_message in self.logs
            if normalized_filter in log_message.lower()
        ]

    def get_agents_status(self) -> List[dict]:
        return [
            {
                "name": agent.name,
                "status": agent.status,
                "current_job": agent.current_job,
            }
            for agent in self.agents
        ]

    def get_queue_status(self) -> List[dict]:
        return [
            {
                "id": job.id,
                "name": job.name,
                "branch": job.branch,
                "status": job.status,
            }
            for job in self.waiting_jobs
        ]

    def get_versions_stack(self) -> List[str]:
        return list(reversed(self.deployed_versions))

    def get_pipeline_stages(self) -> List[str]:
        return self.pipeline_stages.to_list()

    def process_next_job(self) -> str:
        if not self.waiting_jobs:
            message = "There are no jobs waiting in the queue."
            self.add_log(message)
            return message

        free_agent = self._get_free_agent()
        if free_agent is None:
            message = "No free agent is available. The next job stays in the queue."
            self.add_log(message)
            return message

        job = self.waiting_jobs.pop(0)
        job.status = "Running"
        free_agent.status = "Busy"
        free_agent.current_job = f"Job #{job.id}"
        self.add_log(
            f"Agent {free_agent.name} started job #{job.id} for {job.name}."
        )

        for stage_name in self.get_pipeline_stages():
            self.add_log(
                f"Job #{job.id} is running stage: {stage_name}."
            )

        job.status = "Completed"
        deployed_version = f"{job.name} - {job.branch}"
        self.add_log(f"Job #{job.id} completed successfully.")
        self.deploy_version(deployed_version)

        free_agent.status = "Free"
        free_agent.current_job = None
        self.add_log(f"Agent {free_agent.name} is now free.")

        return f"Job #{job.id} completed and deployed as {deployed_version}."

    def deploy_version(self, version: str) -> str:
        self.deployed_versions.append(version)
        self.add_log(f"Version deployed: {version}.")
        return f"Version {version} deployed."

    def rollback(self) -> str:
        if len(self.deployed_versions) < 2:
            message = "Rollback is not possible because there is no previous version."
            self.add_log(message)
            return message

        removed_version = self.deployed_versions.pop()
        restored_version = self.deployed_versions[-1]
        self.add_log(
            f"Rollback completed. Removed {removed_version} and restored {restored_version}."
        )
        return f"Rollback completed. Active version: {restored_version}."

    def _get_free_agent(self) -> Optional[Agent]:
        for agent in self.agents:
            if agent.status == "Free":
                return agent
        return None
