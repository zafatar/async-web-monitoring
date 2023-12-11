from src.entities.links import Link, LinkAccessLog


class LinkMapper:
    @staticmethod
    def to_dict(link):
        return {
            "id": link.id,
            "title": link.title,
            "description": link.description,
            "url": link.url,
            "search_regex": link.search_regex,
            "access_interval": link.access_interval,
            "created_at": link.created_at,
            "updated_at": link.updated_at,
        }

    @staticmethod
    def to_object(link):
        return Link(
            id=link["id"],
            title=link["title"],
            description=link["description"],
            url=link["url"],
            search_regex=link["search_regex"],
            access_interval=link["access_interval"],
            created_at=link["created_at"],
            updated_at=link["updated_at"],
        )


class LinkAccessLogMapper:
    @staticmethod
    def to_dict(link_access_log):
        return {
            "link_id": link_access_log.link_id,
            "status_code": link_access_log.status_code,
            "content": link_access_log.content,
            "created_at": link_access_log.created_at,
            "updated_at": link_access_log.updated_at,
        }

    @staticmethod
    def to_object(link_access_log):
        return LinkAccessLog(
            link_id=link_access_log["link_id"],
            status_code=link_access_log["status_code"],
            content=link_access_log["content"],
            created_at=link_access_log["created_at"],
            updated_at=link_access_log["updated_at"],
        )
