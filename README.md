## Python Flask Skeleton for Google App Engine

## Setup

SENDER_ID is the GroupMe user-id you would like everyone to automatically "Like"
GROUP_ID is the GroupMe ID for the group you would like this sender's messages to be "Liked" in

To get a list of available groups: curl https://api.groupme.com/v3/groups/1683521?token={token}

Must create a "bot" in the group that you'd like to receive the webhook:
curl -X POST -d '{"bot": { "name": "Your bot name", "group_id": {group_id}, "callback_url": "https://{project_id}.appspot.com/webhook/" }}' -H 'Content-Type: application/json' https://api.groupme.com/v3/bots?token={token}

The bot is used to listen to all messages posted. For every message sent on the group, if the sender is the one you have specified then all folks who have gone through the oauth workflow will like each message as it is posted

## Run Locally
1. Install the [App Engine Python SDK](https://developers.google.com/appengine/downloads).
See the README file for directions. You'll need python 2.7 and [pip 1.4 or later](http://www.pip-installer.org/en/latest/installing.html) installed too.

2. Clone this repo with

   ```
   git clone https://github.com/GoogleCloudPlatform/appengine-python-flask-skeleton.git
   ```
3. Install dependencies in the project's lib directory.
   Note: App Engine can only import libraries from inside your project directory.

   ```
   cd appengine-python-flask-skeleton
   pip install -r requirements.txt -t lib
   ```
4. Run this project locally from the command line:

   ```
   dev_appserver.py .
   ```

Visit the application [http://localhost:8080](http://localhost:8080)

See [the development server documentation](https://developers.google.com/appengine/docs/python/tools/devserver)
for options when running dev_appserver.

## Deploy
To deploy the application:

1. Use the [Admin Console](https://appengine.google.com) to create a
   project/app id. (App id and project id are identical)
1. [Deploy the
   application](https://developers.google.com/appengine/docs/python/tools/uploadinganapp) with

   ```
   appcfg.py -A <your-project-id> --oauth2 update .
   ```
1. Congratulations!  Your application is now live at your-app-id.appspot.com
