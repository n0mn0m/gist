"""
Airflow creates ALOT of logs. The first thing you should check is changing your
log level and dag bag refresh rate. If that solves your space issue great! If
not the below should be able to help by scheduling the script to run via cron
at a given interval cleaning up the local airflow logs.
"""

import os
from datetime import datetime

# subtracting timestamps returns milliseconds
HOUR_IN_MILLISECONDS = 3600000

def truncate_process_manager_log(log_base_path):
    """
    The scheduler records all acitivty related to dag processing in the same file.
    This file can grow large fast, and is actively in use. Intead of unlinking the
    file and pulling it out from under the scheduler truncate.
    """
    dag_process_manager_log = os.path.join(
        log_base_path, "dag_processor_manager", "dag_processor_manager.log"
    )
    open(dag_process_manager_log, "w").close()


def traverse_and_unlink(fobject):
    """
    Traverse the log directory on the given airflow instance (webserver, scheduler,
    worker, etc) and remove any logs not modified in the last hour.
    """
    for entry in os.scandir(fobject):
        new_fobject = os.path.join(fobject, entry)
        if os.path.isfile(new_fobject):
            last_modified = os.stat(new_fobject).st_mtime
            delta = datetime.utcnow().timestamp() - last_modified
            if delta > HOURS_IN_MILLISECONDS:
                print(
                    f"{new_fobject} has not been used in the last hour.\nCleaning up."
                )
                os.unlink(new_fobject)
            elif os.path.isdir(new_fobject):
                traverse_and_unlink(new_fobject)


def cleanup_logs():
    """
    Remove all logs not used within the last hour.

    Truncate the dag processor log.
    """
    base_dir = os.environ["AIRFLOW_HOME"]
    log_dir = os.path.join(base_dir, "logs")

    truncate_process_manager_log(log_dir)


if __name__ == "__main__":
    cleanup_logs()

