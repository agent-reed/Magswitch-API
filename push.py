import time, os, db
from apns import APNs, Frame, Payload

cert_path = os.path.join(os.path.dirname(__file__), 'apns-pro-cert.pem')
key_path = os.path.join(os.path.dirname(__file__), 'apns-pro-key.pem')
apns = APNs(use_sandbox=False, cert_file=cert_path, key_file=key_path)
# payload = Payload(alert='Hi Lea', sound="default", badge=1)
# apns.gateway_server.send_notification('55f417c532d0f905b7e1d2617152fc498e7df162eab73f463ca309d4ab81a0c7', payload)
# Send a notification
def pushNotificationById(pnType, message):

	payload = Payload(alert=message, sound="default", badge=1)

	if pnType == "Everybody":
		con = db.createDBConnection()
		cur = con.cursor()
		cur.execute("SELECT tokenid FROM users")
		tokens = cur.fetchall()
		print(tokens)

		for token in tokens:
			apns.gateway_server.send_notification(token, payload)

		return len(tokens)

	if pnType == "Welding":
		con = db.createDBConnection()
		cur = con.cursor()
		cur.execute("SELECT tokenid FROM users WHERE interest = Welding")
		tokens = cur.fetchall()
		print(tokens)

		for token in tokens:
			apns.gateway_server.send_notification(token, payload)

		return len(tokens)


	if pnType == "Annie":
		token = 'cb0b4f60e1be2f773e76ecdae2022c96e25f9f35a137feac1faa2053c6454e9d'
		apns.gateway_server.send_notification(token, payload)

		return 1

def pushNotificationByGroups(groups, message, link):

	groupTokens = []

	payload = Payload(alert=message, sound="default", badge=1, custom={'link':link})

	if "Everybody" in groups:
		print("Notifying Everybody")
		con = db.createDBConnection()
		cur = con.cursor()
		cur.execute("SELECT tokenid FROM users")
		tokens = cur.fetchall()
		for token in tokens:
			if token[0] != None:
				print("Will Send %s" %token[0])
				groupTokens.append(token[0])
				apns.gateway_server.send_notification(token[0], payload)

		users = len(groupTokens)
		return ("Sent notifications to Everybody. (%s users)" %users)

	else:
		con = db.createDBConnection()
		cur = con.cursor()

		for group in groups:
			cur.execute("SELECT tokenid FROM users WHERE interest=%s", (group,))
			tokens = cur.fetchall()

			for token in tokens:
				if token[0] != None:
					groupTokens.append(token[0])

		filteredTokens = list(set(groupTokens))

		for token in groupTokens:
			print("Will Send to %s" %token)
		 	apns.gateway_server.send_notification(token, payload)
		users = len(groupTokens)

		return ("Sent notifications to the folowing groups: \n %s \n [%s users total]" %(groups,users
			))

# Send multiple notifications in a single transmission
# frame = Frame()
# identifier = 1
# expiry = time.time()+3600
# priority = 10
# frame.add_item('b5bb9d8014a0f9b1d61e21e796d78dccdf1352f23cd32812f4850b87', payload, identifier, expiry, priority)
# apns.gateway_server.send_notification_multiple(frame)