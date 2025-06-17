import logging
from IPython.core.error import UsageError
import datetime

# Configure logging for K8s/EKS
logger = logging.getLogger("telemetry")
logger.setLevel(logging.DEBUG)  # Capture all logs
handler = logging.StreamHandler()  # Log to stdout
formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] - %(message)s")
handler.setFormatter(formatter)
if not logger.handlers:
    logger.addHandler(handler)

FORBIDDEN_KEYWORDS = ['externalbrowser', 'externalllm', 'curl', 'openai']

def pre_run_cell(self, info):
    try:
        cell_details = info.raw_cell
        logger.debug("pre_run_cell invoked.")
        logger.debug(f"Raw cell content:\n{cell_details}")

        lowered = cell_details.lower()
        for keyword in FORBIDDEN_KEYWORDS:
            if keyword in lowered:
                logger.warning(f"Execution blocked: forbidden keyword detected -> '{keyword}'")
                raise UsageError(f"Execution blocked: Use of '{keyword}' is not allowed.")

        # Continue logging for telemetry
        logger.info(f"Cell executed successfully by user: {os.getenv('JUPYTERHUB_USER', 'unknown')}")
        self.pre_time = datetime.datetime.now(datetime.timezone.utc)
        self.last_x = self.shell.user_ns.get('x', None)

    except UsageError as ue:
        logger.error(f"UsageError raised: {ue}")
        raise

    except Exception as e:
        logger.exception(f"Unexpected error in pre_run_cell: {e}")
        raise UsageError("Internal telemetry error: please contact admin.")
