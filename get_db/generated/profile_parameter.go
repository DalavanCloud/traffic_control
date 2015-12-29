// Copyright 2015 Comcast Cable Communications Management, LLC

// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at

// http://www.apache.org/licenses/LICENSE-2.0

// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

// This file was initially generated by gen_goto2.go (add link), as a start
// of the Traffic Ops golang data model

package todb

import (
	"encoding/json"
	"fmt"
	"time"
)

type ProfileParameter struct {
	Profile     int64     `db:"profile" json:"profile"`
	Parameter   int64     `db:"parameter" json:"parameter"`
	LastUpdated time.Time `db:"last_updated" json:"lastUpdated"`
}

func handleProfileParameter(method string, id int, payload []byte) (interface{}, error) {
	if method == "GET" {
		return getProfileParameter(id)
	} else if method == "POST" {
		return postProfileParameter(payload)
	} else if method == "PUT" {
		return putProfileParameter(id, payload)
	} else if method == "DELETE" {
		return delProfileParameter(id)
	}
	return nil, nil
}

func getProfileParameter(id int) (interface{}, error) {
	ret := []ProfileParameter{}
	if id >= 0 {
		err := globalDB.Select(&ret, "select * from profile_parameter where id=$1", id)
		if err != nil {
			fmt.Println(err)
			return nil, err
		}
	} else {
		queryStr := "select * from profile_parameter"
		err := globalDB.Select(&ret, queryStr)
		if err != nil {
			fmt.Println(err)
			return nil, err
		}
	}
	return ret, nil
}

func postProfileParameter(payload []byte) (interface{}, error) {
	var v Asn
	err := json.Unmarshal(payload, &v)
	if err != nil {
		fmt.Println(err)
	}
	sqlString := "INSERT INTO profile_parameter("
	sqlString += "profile"
	sqlString += ",parameter"
	sqlString += ") VALUES ("
	sqlString += ":profile"
	sqlString += ",:parameter"
	sqlString += ")"
	result, err := globalDB.NamedExec(sqlString, v)
	if err != nil {
		fmt.Println(err)
		return nil, err
	}
	return result, err
}

func putProfileParameter(id int, payload []byte) (interface{}, error) {
	// Note this depends on the json having the correct id!
	var v Asn
	err := json.Unmarshal(payload, &v)
	if err != nil {
		fmt.Println(err)
		return nil, err
	}
	sqlString := "UPDATE profile_parameter SET "
	sqlString += "profile = :profile"
	sqlString += ",parameter = :parameter"
	sqlString += " WHERE id=:id"
	result, err := globalDB.NamedExec(sqlString, v)
	if err != nil {
		fmt.Println(err)
		return nil, err
	}
	return result, err
}

func delProfileParameter(id int) (interface{}, error) {
	result, err := globalDB.NamedExec("DELETE FROM profile_parameter WHERE id=:id", id)
	if err != nil {
		fmt.Println(err)
		return nil, err
	}
	return result, err
}
