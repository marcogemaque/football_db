create table if not exists football_dwh.team_keys (
	uuid varchar(36) primary key,
	team_name varchar(200) not null,
	country varchar(200) not null
)

create table if not exists teams_aliases (
	uuid varchar(36) not null,
	alias varchar(200),
	primary key (uuid),
	foreign key (uuid)
		references team_keys (uuid)
);

create table if not exists url_to_scrape (
	uuid varchar(36) not null,
	url text,
	type_of_url varchar(99),
	primary key (uuid),
	foreign key (uuid)
		references team_keys (uuid)
);

create table if not exists player_stats (
	uuid varchar(36) not null,
	player_number varchar(100),
	player_position varchar(50) not null,
	age int not null,
	matches_played int not null,
	goals int not null,
	assists int not null,
	yellow_cards int not null,
	double_yellows int not null,
	red_cards int not null,
	subbed_in int not null,
	subbed_out int not null,
	points_per_game numeric(3,2) not null,
	minutes_played numeric(6,1),
	player_name varchar(50),
	primary key (uuid),
	foreign key (uuid)
		references team_keys (uuid)
);

create table if not exists team_value (
	uuid varchar(36) not null,
	value numeric(6) not null,
	primary key (uuid)
	foreign key (uuid)
		references team_keys (uuid)
)

--downside is we duplicate matches, upside is query is easier
create table if not exists matches_played (
	match_id serial primary key, --the sequential id
	team_uuid varchar(36) not null, --team we're referring as main
	opp_uuid varchar(36), --team played against
	goals_scored int, --goals for the main team
	goals_against int, --goals against the team
	match_day int,
	match_month int,
	match_year int,
	ground_neutrality  varchar(7), --home, away or neutral,
	competition varchar(36) --national league, cup, libertadores, etc
)