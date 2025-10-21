# Email Generator & Verifier

This project generates potential email addresses for a given name and domain, verifies deliverability via SMTP, and provides a LinkedIn search query.

## Endpoints

- **GET /**  
  Returns a basic HTML message.

- **GET /generate**  
  Parameters: `first`, `last`, `domain`  
  Example: `/generate?first=John&last=Doe&domain=example.com`  
  Returns JSON with email verification results and LinkedIn search query.

## Deployment

1. Push this repository to GitHub.
2. Connect it to Railway.
3. Railway will automatically detect `requirements.txt` and install dependencies.
4. It will use `Procfile` to start the web server.
