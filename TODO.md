# TODOs

## Security

To prevent unwanted calling a BMI web service we should add an API Key and https.

To use https the server should have a self-signed certificate. 
The client should trust that self-signed certificate.

In BmiClientApptainer and BmiClientDocker we should generate a random API Key and pass it to the container using the `BMI_API_KEY` environment variable.
