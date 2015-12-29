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

type FederationTmuser struct {
	Federation  int64     `db:"federation" json:"federation"`
	TmUser      int64     `db:"tm_user" json:"tmUser"`
	Role        int64     `db:"role" json:"role"`
	LastUpdated time.Time `db:"last_updated" json:"lastUpdated"`
}

func handleFederationTmuser(method string, id int, payload []byte) (interface{}, error) {
	if method == "GET" {
		return getFederationTmuser(id)
	} else if method == "POST" {
		return postFederationTmuser(payload)
	} else if method == "PUT" {
		return putFederationTmuser(id, payload)
	} else if method == "DELETE" {
		return delFederationTmuser(id)
	}
	return nil, nil
}

func getFederationTmuser(id int) (interface{}, error) {
	ret := []FederationTmuser{}
	if id >= 0 {
		err := globalDB.Select(&ret, "select * from federation_tmuser where id=$1", id)
		if err != nil {
			fmt.Println(err)
			return nil, err
		}
	} else {
		queryStr := "select * from federation_tmuser"
		err := globalDB.Select(&ret, queryStr)
		if err != nil {
			fmt.Println(err)
			return nil, err
		}
	}
	return ret, nil
}

func postFederationTmuser(payload []byte) (interface{}, error) {
	var v Asn
	err := json.Unmarshal(payload, &v)
	if err != nil {
		fmt.Println(err)
	}
	sqlString := "INSERT INTO federation_tmuser("
	sqlString += "federation"
	sqlString += ",tm_user"
	sqlString += ",role"
	sqlString += ") VALUES ("
	sqlString += ":federation"
	sqlString += ",:tm_user"
	sqlString += ",:role"
	sqlString += ")"
	result, err := globalDB.NamedExec(sqlString, v)
	if err != nil {
		fmt.Println(err)
		return nil, err
	}
	return result, err
}

func putFederationTmuser(id int, payload []byte) (interface{}, error) {
	// Note this depends on the json having the correct id!
	var v Asn
	err := json.Unmarshal(payload, &v)
	if err != nil {
		fmt.Println(err)
		return nil, err
	}
	sqlString := "UPDATE federation_tmuser SET "
	sqlString += "federation = :federation"
	sqlString += ",tm_user = :tm_user"
	sqlString += ",role = :role"
	sqlString += " WHERE id=:id"
	result, err := globalDB.NamedExec(sqlString, v)
	if err != nil {
		fmt.Println(err)
		return nil, err
	}
	return result, err
}

func delFederationTmuser(id int) (interface{}, error) {
	result, err := globalDB.NamedExec("DELETE FROM federation_tmuser WHERE id=:id", id)
	if err != nil {
		fmt.Println(err)
		return nil, err
	}
	return result, err
}
