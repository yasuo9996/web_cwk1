# web_cwk1
Home page: http://127.0.0.1:8000/
Health check: http://127.0.0.1:8000/health
Swagger: http://127.0.0.1:8000/docs
CRUD interfaces (with version prefix):
Create: POST /v1/listening/log
List: GET /v1/listening
Details: GET /v1/listening/{record_id}
Update: PUT /v1/listening/{record_id}
Delete: DELETE /v1/listening/{record_id}

Automatically create tables upon startup (tracks / user_profiles / listening_records)
Automatically insert a default Track (to avoid a 404 error when immediately creating a listening record due to the non-existence of the track)

finished things
Users can submit a listening record (such as "I listened to which song", "I liked/ skipped which song"). They can view all the records.
They can also check a specific record by its ID. If they make a mistake (for example, they intended to "listen" but mistakenly chose "like"), they can update it.
Erroneous submitted records can be deleted.

undoing things
Examine the acoustic features of a certain song
Find similar songs (using cosine similarity)
View the user's music taste profile (insights)
View the analysis of the overall feature distribution (analytics)
