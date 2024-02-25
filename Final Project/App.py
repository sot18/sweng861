from flask import Flask, render_template, request
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

app = Flask(__name__)

spotify_client_secret = '720e07d85ea744ad8f195cf54cb5e1d6'
spotify_client_id = '88e3455249104bd9b4fe3436a2adda0a'

credentials_manager = SpotifyClientCredentials(client_id=spotify_client_id, client_secret=spotify_client_secret)
APICall = spotipy.Spotify(client_credentials_manager=credentials_manager)


@app.route('/get_selected_option', methods=['POST'])
#Gets the user selected option and returns the results based on that. So it could e information about a song or an artist
def get_selected_option():
    option = request.form.get('option') #Gets the selected option by the user

    #Initializes a variable to use it later
    no_results_message = None

    #IF the selected option is artist
    if option == 'artist':
        #Sets artist name to what the user has typed
        artist_name = request.form.get('inputName')
        #Makes an API call to get results for that artist
        results = APICall.search(q=f"artist:{artist_name}", type="artist", limit=1)

        #Id tehre are any results
        if results['artists']['items']:
            #sets the results to artist to info so we can use it to assign to variables
            indexing_variable = results['artists']['items'][0]
            #This is what gets printed out
            details = {
                 #Sets the popularity score
                "Popularity": indexing_variable['popularity'],
                #Sets the name of the artist
                "Artist": indexing_variable['name'],
                #Sets the total number of followers
                "Followers": indexing_variable['followers']['total'],
                #Gets a link to his spotify page
                "External URLs": indexing_variable['external_urls'],
                #Gets a url of his picture so we can use it later
                "Images": indexing_variable['images']
            }

            # Gets the top 10 songs written by the artist based on popularity score 
            top_songs = APICall.artist_top_tracks(indexing_variable['id'])
            final_top_songs = [{'Track': track['name'], 'Popularity': track['popularity']} for track in top_songs['tracks']]
            details["Top 10 Songs"] = final_top_songs

            #returns all of this information in the artist_info.html page
            return render_template('artist_info.html', artist_details=details)
        else:
            #If there are no results then it prints out this message
            no_results_message = "No results found for the given artist input. Please try again."


    #If selected option is song
    elif option == 'song':
        #Sets the name of the song to the user input
        song_name = request.form.get('inputName')
        #Makes the API call
        results = APICall.search(q=f"track:{song_name}", type="track", limit=1)

        #If there are any resuts
        if results['tracks']['items']:
            #Sets the results to this variable
            indexing_variable2 = results['tracks']['items'][0]
            #Indexes and assigned everything to it's own variable
            song_details = {
                #Sets the song name
                "Song": indexing_variable2['name'],
                #Sets the album name
                "Album": indexing_variable2['album']['name'],
                #Sets the artist name
                "Artist": indexing_variable2['artists'][0]['name'],
                "Explicit": indexing_variable2['explicit'],
                #Sets the popularity
                "Popularity": indexing_variable2['popularity'],
                #Sets the time everyone spent listening to the song
                "Duration (ms)": indexing_variable2['duration_ms'],
                #This is the spotify link
                "External URLs": indexing_variable2['external_urls'],
                #This is the song preview link so I can play a clip of the song
                "Preview URL": indexing_variable2['preview_url'],
                #Sets the release date to the variable
                "Release Date": indexing_variable2['album']['release_date'] 
            }

            #Returns all of this informaiton in song_info html if everything goes well
            return render_template('song_info.html', song_details=song_details)
        else:
            #If not returns this message in this index.html page
            no_results_message = "No results found for the given song input. Please try again."

    #This is where the error message goes
    return render_template('index.html', no_results_message=no_results_message)


@app.route('/')
#Renders the main template
def mainPage():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
