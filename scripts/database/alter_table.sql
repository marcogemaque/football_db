alter table teams_aliases 
	drop column uuid
alter table teams_aliases 
	add column team_name varchar(200) primary key
alter table team_keys 
	add constraint unique_team_name_constraint
	unique(team_name)
alter table teams_aliases
	add constraint constraint_fk
	foreign key (team_name)
		references team_keys (team_name)
alter table teams_aliases 
	alter column alias type text[] using array[alias]