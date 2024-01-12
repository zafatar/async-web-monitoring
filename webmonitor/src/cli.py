# This is a client for the webmonitor server.

import argparse

from tabulate import tabulate

from src.config import settings
from src.configs.logs import logging
from src.database.repositories.link_access_logs import LinkAccessLogsRepository
from src.database.repositories.links import LinksRepository
from src.entities.mappers import LinkMapper


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def _parse_cli():
    parser = argparse.ArgumentParser(
        description="Webmonitor client",
        epilog="Version {}".format(settings.PROJECT_VERSION),
    )
    parser.add_argument("--offset", help="starting offset", default=0)
    parser.add_argument("--limit", help="limit of links to fetch", default=10)
    args = parser.parse_args()

    return args


def main():
    """CLI entrypoint."""
    args = _parse_cli()
    logger.info(
        f"Fetching the url from db with offset {args.offset} and limit {args.limit}"
    )

    # Get all links from the database
    links_repo = LinksRepository()
    raw_links = links_repo.get_all(offset=args.offset, limit=args.limit)
    links = list(map(LinkMapper.to_object, raw_links))

    if len(links) == 0:
        logger.error("No links found in the database.")
        return

    # Get Link stats for all links
    link_access_logs_repo = LinkAccessLogsRepository()
    link_stats = link_access_logs_repo.get_all_stats()

    # build array of arrays for tabulate
    link_stats_table = []
    for link in links:
        # check if the link has stats
        if link.id not in link_stats:
            link_stats_table.append([link.id, link.url, "N/A", "N/A", "N/A"])
            continue

        link_stats_table.append(
            [
                link.id,
                link.url,
                link_stats[link.id]["first_accessed_at"],
                link_stats[link.id]["last_accessed_at"],
                link_stats[link.id]["total_access"],
            ]
        )

    # display links and link_access_logs as a table (tabulate)
    tabulated_view = tabulate(
        tabular_data=link_stats_table,
        showindex=True,
        headers=[
            "ID",
            "URL",
            "First accessed at",
            "Last accessed at",
            "Total Access",
        ],
        tablefmt="fancy_grid",
    )

    logger.info("Stats for the links:\n" + tabulated_view)


if __name__ == "__main__":
    main()
