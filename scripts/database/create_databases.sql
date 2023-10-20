create table [if not exists] team_keys (
	uuid varchar(36) primary key,
	team_name text(200) not null,
	country text(200) not null,
	created_on TIMESTAMP not null,
	created_by TIMESTAMP not null
)

create table [if not exists] teams_aliases (
	uuid varchar(36) not null,
	alias text(200),
	created_on TIMESTAMP not null,
	created_by TIMESTAMP not null,
	foreign key (uuid)
		references team_keys (uuid)
)

create table [if not exists] url_to_scrape (
	uuid varchar(36) not null,
	url text(9999),
	type_of_url varchar(99)
	foreign key (uuid)
		references team_keys (uuid)
)

create table [if not exists] player_stats (
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
	minutes played numeric(5) not null,
	player_name varchar(50),
	foreign key (uuid)
		references team_keys (uuid)
)

create table [if not exists] team_value (
	uuid varchar(36) not null,
	value numeric(6) not null,
	foreign key (uuid)
		references team_keys (uuid)
)