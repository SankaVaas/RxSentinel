"""Background tasks."""
import logging

from app.workers.celery_app import celery_app

logger = logging.getLogger(__name__)


@celery_app.task(name="tasks.recheck_all_active_patients")
def recheck_all_active_patients() -> None:
    """Nightly job: re-run the interaction-check agent graph for every
    patient with active medications, in case new interaction data was
    published (e.g. an FDA safety communication) since their last check.

    Structural stub — wire up an async DB session + interaction_service call
    inside an asyncio.run() here.
    """
    raise NotImplementedError


@celery_app.task(name="tasks.reingest_fda_labels")
def reingest_fda_labels() -> None:
    """Periodic refresh of the RAG literature store from OpenFDA."""
    raise NotImplementedError
