'''3.Implement OAuth2 authentication to allow users to log in using their Google or Facebook accounts.'''
# Code


from flask import Flask,render_template, redirect, url_for
from flask_dance.contrib.google import make_google_blueprint, google
from flask_dance.contrib.facebook import make_facebook_blueprint, facebook

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Google configuration
google_bp = make_google_blueprint(client_id='your_google_client_id',
                                  client_secret='your_google_client_secret',
                                  redirect_to='google_login')
app.register_blueprint(google_bp, url_prefix='/google_login')

# Facebook configuration
facebook_bp = make_facebook_blueprint(client_id='your_facebook_app_id',
                                      client_secret='your_facebook_app_secret',
                                      redirect_to='facebook_login')
app.register_blueprint(facebook_bp, url_prefix='/facebook_login')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login():
    return '<a href="/google_login">Login with Google</a> | <a href="/facebook_login">Login with Facebook</a>'

@app.route('/logout')
def logout():
    # Handle logout logic if needed
    return 'Logged out'

@app.route('/google_login')
def google_login():
    if not google.authorized:
        return redirect(url_for('google.login'))
    resp = google.get('/plus/v1/people/me')
    assert resp.ok, resp.text
    return 'Logged in as Google user: {0}'.format(resp.json()['displayName'])

@app.route('/facebook_login')
def facebook_login():
    if not facebook.authorized:
        return redirect(url_for('facebook.login'))
    resp = facebook.get('/me?fields=id,name,email')
    assert resp.ok, resp.text
    return 'Logged in as Facebook user: {0}'.format(resp.json()['name'])


if __name__ == '__main__':
    app.run(host="0.0.0.0")





