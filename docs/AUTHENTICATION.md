# Demo authentication

At startup, Gradebook reads two demo passwords from the environment. The app
hashes them and creates the synthetic `lecturer` and `student` accounts in
memory. With neither password configured, it starts without demo accounts.

The browser submits the login form to `/auth/login`. Flask checks the form's
CSRF token and verifies the password against the account's hash. On success,
Flask puts the user's ID into a signed session cookie. On subsequent requests,
the server retrieves the account and its role using that ID. The session cookie
is signed to detect tampering and contains the ID and CSRF token.

`/auth/me` shows the signed-in user's ID, username, and role. Future gradebook
routes will use `g.user.id` as the actor ID. The repository still decides which
courses and grades that account may access. Sign out using the button on the
login page, which clears the browser's session.

## Local check in PowerShell

With your virtual environment active, set a signing key and two synthetic
passwords in the same terminal where you will start Flask.

```powershell
$env:SECRET_KEY = python -c "import secrets; print(secrets.token_hex(32))"
$env:DEMO_LECTURER_PASSWORD = [System.Net.NetworkCredential]::new('', (Read-Host 'Lecturer demo password' -AsSecureString)).Password
$env:DEMO_STUDENT_PASSWORD = [System.Net.NetworkCredential]::new('', (Read-Host 'Student demo password' -AsSecureString)).Password
python -m flask --app wsgi run --port 8000
```

The first command generates the signing key. The next two read hidden input
into environment variables. Flask reads these settings at startup.

Open `http://127.0.0.1:8000/auth/login`. Sign in as each role, check the JSON
identity, and return to the login page to sign out. After signing out,
`/auth/me` should return 401. Try a wrong password and verify that `/health`
and `/ready` still respond.

For deployment, supply the signing key and demo passwords through the platform's
secret settings and set `SESSION_COOKIE_SECURE=true` for HTTPS. Browser requests
that change state require a CSRF token. The signed cookie expires after two
hours of inactivity.
