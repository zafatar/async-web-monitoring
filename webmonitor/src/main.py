# Main call for the webmonitor application

import asyncio

from src.config import settings
from src.configs.logs import logging  # custom logging
from src.database.repositories.links import LinksRepository
from src.entities.mappers import LinkMapper
from src.services.monitor import Monitor


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

if settings.DEBUG:
    logger.info("*** DEBUG MODE ACTIVE ***")
    logger.setLevel(logging.DEBUG)


async def main():
    # Get all links from the database
    # TODO: Refresh links from database every X minutes with a separate thread
    links_repo = LinksRepository()
    raw_links = links_repo.get_all()
    links = list(map(LinkMapper.to_object, raw_links))

    tasks = []
    for url in links:
        task = asyncio.create_task(Monitor(link=url).run())
        tasks.append(task)

    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
