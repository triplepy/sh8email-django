def add_recip_to_session(client, recipient):
    session = client.session
    session['recipient'] = recipient
    session.save()
