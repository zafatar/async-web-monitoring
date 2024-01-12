# Ingest the bootstrap data into the database

from src.configs.logs import logging
from src.database.bootstrap_data.links import links
from src.database.repositories.links import LinksRepository


logger = logging.getLogger(__name__)


def ingest_bootstrap_data():
    """
    Ingest the bootstrap data into the database
    :param conn: The database connection object
    :return: None
    """
    ingest_links()


def ingest_links():
    """
    Ingest the links into the database
    :param conn: The database connection object
    :return: None
    """
    links_repo = LinksRepository()

    for link in links:
        existing_link = links_repo.get_by_url(link["url"])

        if existing_link:
            logger.info(
                f"Link {link['url']} already exists with ID {existing_link['id']}"
            )
            continue

        try:
            links_repo.insert(
                title=link["title"],
                description=link["description"],
                url=link["url"],
                search_regex=link["search_regex"],
                access_interval=link["access_interval"],
            )
        except Exception as e:
            logger.error("Error({0}): {1}".format(e.pgcode, e.pgerror))


if __name__ == "__main__":
    ingest_bootstrap_data()
