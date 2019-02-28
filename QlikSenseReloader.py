import json
import sys
from websocket import create_connection

error = False

# Get path to app
if len(sys.argv) > 2:
	url = sys.argv[1]
	path = sys.argv[2]
else:
	url = input("\nEnter Qlik Server URL (e.g. ws://localhost:4848/app/)\n")
	path = input("\nEnter path to Qlik Sense app (e.g. C:/users/myapp.qvf)\n")

# Open connection
print("\nConnecting to Qlik Sense engine...")
try:
	ws = create_connection(url)
except Exception as e:
	print("Error while connecting to the Qlik Sense engine. Check that Qlik Sense Desktop is open.")
	print(e)
	sys.exit(1)

# Open app
print("Opening app...")
try:
	request = {
		"jsonrpc": "2.0",
		"id": 0,
		"method": "OpenDoc",
		"handle": -1,
		"params": [
			path,
			""
		]
	}

	ws.send(json.dumps(request))
	response =  ws.recv()
	response =  json.loads(ws.recv())
	try:
		errorMessage = response["error"]["message"]
		print("Error:", errorMessage)
		error = True
	except:
		pass
	if error: 
		ws.close()
		sys.exit(1)
except Exception as e:
	print("Error while opening the app.")
	print(e)
	ws.close()
	sys.exit(1)
	
# Check app
print("Checking app status...")
try:
	request = {
		"jsonrpc": "2.0",
		"id": 1,
		"method": "GetActiveDoc",
		"handle": -1,
		"params": []
	}

	ws.send(json.dumps(request))
	response =  json.loads(ws.recv())
	try:
		errorMessage = response["error"]["message"]
		print("Error:", errorMessage)
		error = True
	except:
		pass
	if error: 
		ws.close()
		sys.exit(1)
except Exception as e:
	print("Error while checking app status.")
	print(e)
	ws.close()
	sys.exit(1)
	
# Reload app
print("Starting reload...")
try:
	request = {
		"handle": 1,
		"method": "DoReloadEx",
		"params": {},
		"id": 2,
		"jsonrpc": "2.0"
	}

	ws.send(json.dumps(request))
	response =  json.loads(ws.recv())
	try:
		errorMessage = response["error"]["message"]
		print("Error:", errorMessage)
		error = True
	except:
		pass
	if error: 
		ws.close()
		sys.exit(1)
except Exception as e:
	print("Error while starting reload.")
	print(e)
	ws.close()
	sys.exit(1)

# Get reload status
try:
	status = response["result"]["qResult"]["qSuccess"]
	print("Reload completed")
except:
	print("Error. Reload failed.")
	try:
		logFile = response["result"]["qResult"]["qScriptLogFile"]
		print("See log at ", logFile)
	except:
		print("No log was generated")
	ws.close()
	sys.exit(1)

# Save app
print("Saving app...")
try:
	request = {
		"jsonrpc": "2.0",
		"id": 6,
		"method": "DoSave",
		"handle": 1,
		"params": []
	}

	ws.send(json.dumps(request))
	response =  json.loads(ws.recv())
	try:
		errorMessage = response["error"]["message"]
		print("Error:", errorMessage)
		error = True
	except:
		pass
	if error: sys.exit(1)
except Exception as e:
	print("Error while saving the app.")
	print(e)
	ws.close()
	sys.exit(1)
	
# Close connection
ws.close()