"""
Scheduler API example
=====================

Run prioritized tasks with the Prioritized Task Scheduling API helpers.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from domonic.webapi.scheduler import Scheduler, TaskController


def build_log():
    log = []
    scheduler = Scheduler(auto_run=False)
    controller = TaskController({"priority": "background"})

    controller.signal.addEventListener(
        "prioritychange",
        lambda event: log.append(
            f"priority: {event.previousPriority} -> {event.target.priority}"
        ),
    )

    scheduler.postTask(lambda: log.append("visible"), {"priority": "user-visible"})
    scheduler.postTask(lambda: log.append("mutable"), {"signal": controller.signal})
    scheduler.postTask(lambda: log.append("blocking"), {"priority": "user-blocking"})

    controller.setPriority("user-blocking")
    scheduler.run()
    return log


if __name__ == "__main__":
    print("\n".join(build_log()))
