
import webapp2
import cgi

form = """
<!DOCTYPE html>
<html>
<head>
<title>SignUp Unit2 Homework2</title>
</head>

<body>
  <form method="post">
  <h1>Sign Up</h1>
      <label><b>User Name:</b>
        <input type="text" name="username" value="%(username)s"
                           style="height: 20px; width: 200px">&nbsp;<div style="color: red">%(username_error)s</div>
      </label>
  <br>
      <label><b>Password:</b>
        <input type="password" name="password"
                           style="height: 20px; width: 200px">&nbsp;<div style="color: red">%(password_error)s</div>
     </label>
  <br>
      <label><b>Verify Password:</b>
        <input type="password" name="password2"
                           style="height: 20px; width: 200px">&nbsp;<div></div>
      </label>
  <br>
      <label><b>Email (Optional):</b>
      <input type="email" name="email" value="%(email)s"
                           style="height: 20px; width: 200px">&nbsp;<div style="color: red">%(email_error)s</div>
      </label>
  <br>
    <p><input type="submit" value="Submit"></p>
</form>
</body>
<footer>
</footer>
</html>
"""

def escape_html(s):
    return cgi.escape(s, quote = True)

def valid_name(name):
    if  not " " in name:
        return True
    else:
        return False

def valid_email(email):
    if "@" in email and "." in email:
        return True
    else:
        return False

class MainSignUpHandler(webapp2.RequestHandler):
    def write_form(self, username = "", email = "", username_error = "", password_error = "", password2_error = "", email_error = ""):
        self.response.out.write(form % {"username": username,
                                        "email": email,
                                        "username_error": username_error,
                                        "password_error": password_error,
                                        "password2_error": password2_error,
                                        "email_error": email_error})

    def get(self):
        self.write_form()

    def post(self):
        user_name = self.request.get('username')
        user_password = self.request.get('password')
        user_password2 = self.request.get('password2')
        user_email = self.request.get('email')

        username = escape_html(user_name)
        password = escape_html(user_password)
        password2 = escape_html(user_password2)
        email = escape_html(user_email)

        username_error = ""
        password_error = ""
        password2_error = None
        email_error = ""

        if not username or not valid_name(username):
            username_error = "Invalid username."
        if email and not valid_email(email):
            email_error = "Invalid email address!"
        if password != password2:
            password_error = "Passwords don't match."
        if not password:
            password_error = "Password required."
        if not password2:
            password2_error = "Password verification required."

        if username_error or password_error or password2_error or email_error:
            self.write_form(username, email, username_error, password_error, password2_error, email_error)
        else:
            self.redirect('/welcome?username=' + username)

class Welcome(webapp2.RequestHandler):
    def get(self):
        username = self.request.get('username')
        self.response.write('Hello ' + username + "!")

app = webapp2.WSGIApplication([
    ('/', MainSignUpHandler),
    ('/welcome', Welcome)
], debug=True)
