import settings
import todoist

api = todoist.TodoistAPI(settings.TODOIST_TOKEN)

api.sync_token = '*'

response = api.sync()

p = {}

for z in response['projects']:
	p[z['id']]=z['name'].encode('utf-8')

for z in response['items']:
	print "{0} ({1})".format(z['content'].encode('utf-8'),p[z['project_id']])