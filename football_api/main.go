package main

import (
	"database/sql"
	"fmt"
	"net/http"

	"github.com/gin-gonic/gin"
	_ "github.com/lib/pq"
)

type fixture struct {
	TotalPoints  float64 `json:"total_points"`
	GoalsFavour  float64 `json:"goals_favour"`
	GoalsAgainst float64 `json:"goals_against"`
	TeamName     string  `json:"team_name"`
	Country      string  `json:"country"`
}

var db *sql.DB

func main() {
	var err error
	//create the psql pbject to connect to postgres
	psqlInfo := "postgresql://cantuaria.marco1@gmail.com:rnZihcBHl1m6@ep-purple-term-a5pg9xu6.us-east-2.aws.neon.tech/neondb?sslmode=require"
	db, err = sql.Open("postgres", psqlInfo)
	if err != nil {
		panic(err)
	}
	//check if everything was good
	fmt.Println("Successfully connected")
	//start our server
	router := gin.Default()
	router.GET("/fixtures", getFixture)
	router.GET("/", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{"data": "hello_world"})
	})
	router.Run("localhost:8080")
}

func getFixture(c *gin.Context) {
	c.Header("Content-Type", "application/json")

	rows, err := db.Query("SELECT total_points, goals_favour, goals_against, team_name, country from updated_ranking_table")
	if err != nil {
		panic("Error trying to execute query.")
	}
	//close it
	var all_fixtures []fixture
	for rows.Next() {
		var match_day fixture
		err := rows.Scan(&match_day.TotalPoints, &match_day.GoalsFavour, &match_day.GoalsAgainst, &match_day.TeamName, &match_day.Country)
		if err != nil {
			panic("Error trying to read query.")
		}
		all_fixtures = append(all_fixtures, match_day)
	}
	err = rows.Err()
	if err != nil {
		panic("Error associated to the query.")
	}
	c.JSON(http.StatusOK, all_fixtures)
}
