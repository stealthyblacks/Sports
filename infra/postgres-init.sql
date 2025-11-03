CREATE TABLE matches (
  id SERIAL PRIMARY KEY,
  provider_id TEXT UNIQUE,
  league TEXT,
  home TEXT,
  away TEXT,
  kickoff TIMESTAMP,
  status TEXT,
  provider_payload JSONB,
  created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE odds (
  id SERIAL PRIMARY KEY,
  match_id INTEGER,
  provider TEXT,
  market TEXT,
  selection TEXT,
  odd NUMERIC,
  retrieved_at TIMESTAMP DEFAULT now()
);