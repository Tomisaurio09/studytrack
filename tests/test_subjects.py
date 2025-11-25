
def test_post_subjects(client, auth_headers):
    payload = {
            "name": "Complex math",
            "description": "Advanced calculus course",
            "total_hours_goal": 100,
            "total_hours_completed": 0,
            "priority_level": "HIGH",
            "status": "ACTIVE"}
    
    res = client.post("/subjects", headers=auth_headers, json=payload)
    assert res.status_code == 201

    data = res.get_json()
    assert data["name"] == "Complex math"

def test_get_subjects(client, auth_headers):
    res = client.get("/subjects", headers=auth_headers)

    assert res.status_code == 200

def test_put_subjects(client, auth_headers):
    #first i create the subject then i edit their content
    payload = {
            "name": "Complex math",
            "description": "Advanced calculus course",
            "total_hours_goal": 100,
            "total_hours_completed": 0,
            "priority_level": "HIGH",
            "status": "ACTIVE"}
    
    res = client.post("/subjects", headers=auth_headers, json=payload)

    payload_put= {
            "name": "Python",
            "description": "Advanced POO",
            "total_hours_goal": 120,
            "total_hours_completed": 0,
            "priority_level": "MEDIUM",
            "status": "COMPLETED"}
    
    res = client.put("/subjects/1", headers=auth_headers, json=payload_put)

    assert res.status_code == 200

    data = res.get_json()
    assert data["message"] == "Subject updated successfully"

def test_delete_subjects(client, auth_headers):
    #first i create the subject then i delete it 
    payload = {
            "name": "Complex math",
            "description": "Advanced calculus course",
            "total_hours_goal": 100,
            "total_hours_completed": 0,
            "priority_level": "HIGH",
            "status": "ACTIVE"}
    
    res = client.post("/subjects", headers=auth_headers, json=payload)
    res = client.delete("/subjects/1", headers=auth_headers)

    assert res.status_code == 200

    data = res.get_json()
    assert data["message"] == "Subject deleted successfully"