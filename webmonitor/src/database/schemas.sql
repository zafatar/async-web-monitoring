/** Links table creation */
CREATE TABLE IF NOT EXISTS links (
    id                  SERIAL PRIMARY KEY,
    title               VARCHAR(128),
    description         VARCHAR(1024),
    url                 VARCHAR(512) UNIQUE,
    search_regex        VARCHAR(128),
    access_interval     INTEGER DEFAULT 5,
    created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS link_access_logs (
    link_id             INTEGER NOT NULL,
    accessed_at         TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    status_code         INTEGER DEFAULT 200,
    is_regex_match      BOOLEAN DEFAULT FALSE,
    PRIMARY KEY         (link_id, accessed_at),
    FOREIGN KEY         (link_id) REFERENCES links (id)
);
