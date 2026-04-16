-- CREATE TABLE resources(
--     _id UUID PRIMARY KEY DEFAULT uuid_generate_v4() ,
--     type TEXT CHECK(type IN ('notes','videos','assessments')),
--     assesment_type TEXT,
--     name TEXT ,
--     url TEXT,
--     eligible_for TEXT,
--     unit_id UUID REFERENCES units(unit_id) ON DELETE SET NULL,
--     subject_id UUID REFERENCES subject(subject_id) ON DELETE SET NULL,
--     is_global BOOLEAN DEFAULT TRUE,
--     created_at TIME DEFAULT CURRENT_TIMESTAMP
  
-- )

-- INSERT INTO resources(
--     _id,
--     type,
--     name,
--     url,
--     eligible_for,
--     unit_id
-- ) 
-- SELECT 
--     notes_id,
--     'notes',
--     notes_name,
--     notes_url,
--     eligible_for,
--     unit_id
--  FROM notes

-- CREATE TABLE nodes(
--     _id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
--     title TEXT,
--     description TEXT,
--     eligible_for TEXT,
--     user_id UUID REFERENCES profileinfo(id) ON DELETE CASCADE,
--     status TEXT,
--     unit_id UUID REFERENCES units(unit_id) ON DELETE CASCADE,
--     subject_id UUID REFERENCES subject(subject_id) ON DELETE CASCADE

-- );

-- CREATE TABLE node_resources (
--   node_id UUID REFERENCES nodes(_id) ON DELETE CASCADE,
--   resource_id UUID REFERENCES resources(_id) ON DELETE CASCADE,
--   PRIMARY KEY (node_id, resource_id)
-- )



-- ALTER TABLE units
-- ADD COLUMN what_to_learn TEXT[]

