# What Taylor Swift Era are You?

Using Spotify's APIs to: <br />
- Read user's top 50 medium term played songs (medium term = past 6 months)
- Filter JSON to find top song from Taylor Swift
- The album of the user's top Taylo song is their Taylor Era!
- If the user does not have a Taylor Swift song in their top 50, they will get their era from a multi linear regression model that predicts their era, based on the audio features of Taylor's songs and the audio features of the users top 5 medium term played songs
<br />

### Next Steps

Right now, the app is in development mode and will only run for users registered in the Development Dashboard.  Next steps include requesting a quota extension to open the app up to the public.  

### Tools and Languages Used

- Spotify Web API 
- Spotipy (for data exploration) 
- Python
    - Pandas
    - Sklearn 
- Jupyter Notebook
- Flask 
- HTML
- CSS



### HTML Preview

**Home page that appears when you first enter the app**
<br /> 

![homepage](/Images/homepage_desktop.png)

<br /> 

**Results page that appears after you log into your Spotify account**

<br /> 

![resultspage](/Images/results_desktop.png)

<br /> 

**Mobile View**


<br /> 


![homemobile](/Images/homepage_mobile.png)

![resultsmobile](/Images/results_mobile.png)

<br /> 
