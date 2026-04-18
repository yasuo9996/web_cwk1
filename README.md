# web_cwk1
First, complete the closed loop of "listening to music to gain insights".
After users record their behaviors, they can immediately see "my preference profile".
Output: Preference energy range, preference danceability range, average tempo.
Realize "similar song recommendations".
When users provide a song, the system returns a list of similar songs and similarity scores.
Emphasize explainability: why similar (based on feature vectors).
Realize "music library statistical analysis".
Users can view the distribution of features such as energy/danceability (histogram data).
Suitable for demonstrating analytical capabilities.

plan
Add the write interface for tracks
At least add POST /v1/tracks (it would be better to have GET /v1/tracks as well)
The current music library data is too limited, which makes the demonstration of similar/analytics less convincing
Unify the error return format
For example, unify {code, message, detail} to enhance professionalism
Basic testing
Cover listening CRUD + similar + insights + analytics
At least 8 to 12 interface tests
Data import script
Batch import several tracks from CSV (to demonstrate stability and more realistic results)
