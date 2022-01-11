cd folder
git clone https://github.com/Nurlan-Bolayev/captcha.git
Type code . (open in vscode)
Press ctrl + ' to open terminal
Type powershell
Type ./cap_env/Scripts/activate
pip install Flask
pip freeze > requirements.txt
pip install -r requirements.txt
Type $env:FLASK_APP = 'ex'
Type flask run (this will start dev server)
Open in browser (http://localhost:5000)