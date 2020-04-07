# covida

### Requerimientos:

- pip install bs4
- pip install requests
- Flask: https://flask.palletsprojects.com/en/1.1.x/installation/

### Ejemplo:

Iniciar flask https://flask.palletsprojects.com/en/1.1.x/quickstart/
y luego ingresar en el navegador o en Postman  
http://127.0.0.1:5000/papersOfInterest?word_in_title=mask&word_in_paper=COVID-19

Esto retorna un JSON con los papers resultantes de buscar 'mask' en el título y 'COVID-19' en su contenido.