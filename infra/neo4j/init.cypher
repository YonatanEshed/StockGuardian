// Constraints
CREATE CONSTRAINT event_unique_id IF NOT EXISTS 
FOR (e:Event) REQUIRE e.event_node_id IS UNIQUE;

CREATE CONSTRAINT ticker_unique_id IF NOT EXISTS 
FOR (t:Ticker) REQUIRE t.ticker IS UNIQUE;

CREATE CONSTRAINT sector_unique_name IF NOT EXISTS 
FOR (s:Sector) REQUIRE s.name IS UNIQUE;

CREATE CONSTRAINT keyword_unique_term IF NOT EXISTS 
FOR (k:Keyword) REQUIRE k.term IS UNIQUE;


// Indexes
CREATE INDEX event_added_at_index IF NOT EXISTS 
FOR (e:Event) ON (e.added_at);

