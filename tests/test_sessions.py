#falta testear las sessions

def test_create_study_session(client, auth_headers):
    subject_payload = {
        "name": "Physics",
        "description": "Basic physics course",
        "total_hours_goal": 50,
        "total_hours_completed": 0,
        "priority_level": "MEDIUM",
        "status": "ACTIVE"
    }
    subject_res = client.post("/subjects", headers=auth_headers, json=subject_payload)
    assert subject_res.status_code == 201

    subject_data = subject_res.get_json()
    subject_id = subject_data["id"]

    session_payload = {
        "subject_id": subject_id,
        "start_time": "03:30PM",
        "end_time": "04:30PM",
        "notes": "Studied chapters 1 to 3"
    }
    session_res = client.post("/sessions", headers=auth_headers, json=session_payload)
    assert session_res.status_code == 201

    session_data = session_res.get_json()
    assert session_data["subject_id"] == subject_id

def test_get_study_sessions(client, auth_headers):
    res = client.get("/sessions", headers=auth_headers)
    assert res.status_code == 200
    data = res.get_json()
    assert "sessions" in data

def test_put_study_sessions(client, auth_headers):
    subject_payload = {
        "name": "Physics",
        "description": "Basic physics course",
        "total_hours_goal": 50,
        "total_hours_completed": 0,
        "priority_level": "MEDIUM",
        "status": "ACTIVE"
    }
    subject_res = client.post("/subjects", headers=auth_headers, json=subject_payload)
    assert subject_res.status_code == 201

    subject_data = subject_res.get_json()
    subject_id = subject_data["id"]

    session_payload = {
        "subject_id": subject_id,
        "start_time": "03:00PM",
        "end_time": "04:30PM",
        "notes": "Studied chapters 1 to 5"
    }
    session_res = client.post("/sessions", headers=auth_headers, json=session_payload)
    assert session_res.status_code == 201

    session_data = session_res.get_json()
    assert session_data["subject_id"] == subject_id

    payload_put = {
        "subject_id": subject_id,
        "start_time": "05:00PM",
        "end_time": "06:00PM",
        "notes": "Studied chapters 6 to 15"
    }
    session_put_res = client.put(f"/sessions/{session_data['id']}", headers=auth_headers, json=payload_put)
    assert session_put_res.status_code == 200
    put_data = session_put_res.get_json()
    assert put_data["message"] == "Session updated successfully"

def test_delete_study_sessions(client, auth_headers):
    subject_payload = {
        "name": "Physics",
        "description": "Basic physics course",
        "total_hours_goal": 50,
        "total_hours_completed": 0,
        "priority_level": "MEDIUM",
        "status": "ACTIVE"
    }
    subject_res = client.post("/subjects", headers=auth_headers, json=subject_payload)
    assert subject_res.status_code == 201

    subject_data = subject_res.get_json()
    subject_id = subject_data["id"]

    session_payload = {
        "subject_id": subject_id,
        "start_time": "03:30PM",
        "end_time": "04:30PM",
        "notes": "Studied chapters 1 to 5"
    }
    session_res = client.post("/sessions", headers=auth_headers, json=session_payload)
    assert session_res.status_code == 201

    session_data = session_res.get_json()
    assert session_data["subject_id"] == subject_id

    delete_res = client.delete(f"/sessions/{session_data['id']}", headers=auth_headers)
    assert delete_res.status_code == 200
    delete_data = delete_res.get_json()
    assert delete_data["message"] == "Session deleted" 
