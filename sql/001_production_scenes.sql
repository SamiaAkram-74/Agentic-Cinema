CREATE TABLE IF NOT EXISTS production_scenes
(
    movie String,
    scene String,
    location String,
    shooting_day UInt16,
    complexity String,
    permit_required Bool,
    lighting String
)
ENGINE = MergeTree
ORDER BY (movie, location, shooting_day);

INSERT INTO production_scenes VALUES
('THE LAST SIGNAL', 'Sarah discovers the machine', 'Laboratory', 1, 'medium', false, 'controlled'),
('THE LAST SIGNAL', 'Sarah runs outside to meet John', 'Street', 2, 'high', true, 'natural');
