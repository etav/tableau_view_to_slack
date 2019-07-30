#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 27 14:18:51 2019

@author: Ernest Tavares III

@twitter: etav3

@linkedin:https://www.linkedin.com/in/ernesttavares/
"""

import tableauserverclient as tsc
import yaml
import io
from slackclient import SlackClient

# import tableau & slack resources from yaml file:
with open("config.yml", 'r') as yml:
    config = yaml.load(yml, Loader=yaml.FullLoader)

# tableau resources
tab = ['user', 'pass', 'server', 'png_path', 'view']
usr, pwd, svr, path, view_name = [config['tableau'][x] for x in tab]

# slack resources
slack_token, slack_channel = config['slack']['token'], config['slack']['channel']
slack_client = SlackClient(slack_token)

# tableau auth
tableau_auth = tsc.TableauAuth(usr, pwd)

# tableau server
server = tsc.Server(svr)

# set tableau server version
server.use_server_version()

# sign in to tableau
with server.auth.sign_in(tableau_auth):

    # initialize filter object
    req_option = tsc.RequestOptions(pagesize=1000)

    # filter for specific "view_name"
    req_option.filter.add(tsc.Filter(tsc.RequestOptions.Field.Name, tsc.RequestOptions.Operator.Equals, view_name))
    my_view, pagination_item = server.views.get(req_option)

    if not my_view:
        raise LookupError("View {} was not found.".format(view_name))
        # end session
        exit(1)
    else:

        # unpack view from list
        my_view = my_view[0]

        # populate and save the preview image as png
        server.views.populate_image(my_view)

        file_name = 'view_image_{}.png'.format(view_name)
        with open(path+file_name, 'wb') as f:
            f.write(my_view.image)
            print('Success! PNG generated for view: {}'.format(view_name))
            print('{} file generated at {}'.format(file_name, path))

# post png to slack
try:
    file_path = path+file_name
    with open(file_path, 'rb') as f:
        slack_client.api_call(
            "files.upload",
            channels=slack_channel,
            filename=file_name,
            title='Tableau Image Preview for view: {}'.format(view_name),
            initial_comment=':mag: Click to enlarge:',
            file=io.BytesIO(f.read())
        )
        print('Successfully posted view image: "{}" to slack channel: "{}"'.format(file_name, slack_channel))
except Exception as e:
    raise e



