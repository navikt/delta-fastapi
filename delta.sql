-- Enable the uuid-ossp extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create Groups table
CREATE TABLE groups (
    group_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR UNIQUE NOT NULL,
    announcement TEXT,
    description TEXT,
    group_type VARCHAR(50),
    is_regular_meeting BOOLEAN DEFAULT FALSE NOT NULL,
    meeting_frequency VARCHAR(50) NOT NULL,
    default_meeting_start TIME,
    default_meeting_end TIME,
    has_private_slack BOOLEAN DEFAULT FALSE,
    slack_channel_name VARCHAR(255),
    slack_channel_url VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create Group_Updates log table
CREATE TABLE group_updates (
    update_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    group_id UUID NOT NULL REFERENCES groups(group_id) ON DELETE CASCADE,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_by UUID
);

-- Create Members table
CREATE TABLE members (
    member_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    group_id UUID NOT NULL REFERENCES groups(group_id) ON DELETE CASCADE,
    email VARCHAR NOT NULL,
    name VARCHAR NOT NULL,
    role VARCHAR(50) DEFAULT 'member' NOT NULL,
    joined_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create Meetings table
CREATE TABLE meetings (
    meeting_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    group_id UUID NOT NULL REFERENCES groups(group_id) ON DELETE CASCADE,
    meeting_date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    is_cancelled BOOLEAN DEFAULT FALSE NOT NULL,
    cancellation_reason TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(group_id, meeting_date)
);

-- Create Tags table
CREATE TABLE tags (
    tag_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(50) UNIQUE NOT NULL,
    type VARCHAR(50) NOT NULL CHECK (type IN ('audience', 'search'))
);

-- Create Group_Tags junction table
CREATE TABLE group_tags (
    group_id UUID NOT NULL REFERENCES groups(group_id) ON DELETE CASCADE,
    tag_id UUID NOT NULL REFERENCES tags(tag_id) ON DELETE CASCADE,
    PRIMARY KEY (group_id, tag_id)
);