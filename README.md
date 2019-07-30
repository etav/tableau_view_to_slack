# Post Tableau Views to Slack with Python
A simple program which leverages Tableau's client server python module (TSC) [link] and slack API module (SlackClient)[link] to delivery Tableau Views to Slack. 

### Project Goal:
At the end of the program you will be able to query tableau server client for a specific view. You will then download this view as a png image and post it to a specific slack channel.


### Requirements: 
1. Python3
2. [Tableau Client Server](https://tableau.github.io/server-client-python/) (with credentials) 
3. [Slack API Token](https://api.slack.com/tokens)

### Getting Started:
1. Download the repo by running `git clone https://github.com/etav/tableau_view_to_slack.git`
2. Activate virtual env
3 OR install modules contained in the requirements.txt file to your local python version by running `pip install -r requirements.txt` in that directory.
4. Edit the "config.ini" file with the following info for Tableau:
	a) user: tableau username to log into the server.
	b) pass: tableau password to log into the server.
	c) server: the url for your tableau server, ie: **http://tab.mydomain.com**.
	d) view: the name of the view you'd like to send to slack.
	e) png_path: the desired download path for the png file. 
5. Edit the "config.ini" file with the following info for Slack:
	a) token: A slack token you created previously.
	b) channel: The name of an existing slack channel. 
6. Run the program & head to the slack channel to view the png.


### Code Breakdown:

#### import tableau & slack resources from yaml file:
Opening yaml config file to unpack assets for slack & tableau
```python 
with open("config.yml", 'r') as yml:
    config = yaml.load(yml, Loader=yaml.FullLoader)
```

#### Querying Tableau using TSC
Sign into tableau using authentication resources defined in the yaml file and filter for specific view name on the site's server. 
```python 
with server.auth.sign_in(tableau_auth):

# initialize filter object
req_option = tsc.RequestOptions(pagesize=1000)

# filter for specific "view_name"
req_option.filter.add(tsc.Filter(tsc.RequestOptions.Field.Name, tsc.RequestOptions.Operator.Equals, view_name))
my_view, pagination_item = server.views.get(req_option)
```

#### Populate view image
However, we once we find the view we need to populate it with the image data, using the following: 
	```python
	# populate view image
        server.views.populate_image(my_view)

        file_name = 'view_image_{}.png'.format(view_name)
        with open(path+file_name, 'wb') as f:
            f.write(my_view.image)
            print('Success! PNG generated for view: {}'.format(view_name))
            print('{} file generated at {}'.format(file_name, path))
	    ```



