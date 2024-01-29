# Questionnaire Translator Tool (Backend)

## Running the Server Locally

You need to have Python installed.

Create a `.env` file in the root folder with the following:
```env
OPENAI_AUTH_KEY=YOUR-API-KEY-HERE
DEEPL_AUTH_KEY=YOUR-API-KEY-HERE
FRONTEND_URL=http://localhost:5173 (if you're using the default settings of the application frontend)
```

Install dependencies from `requirements.txt`:
```bash
pip install -r requirements.txt
```

Start the server by running the following in the root folder:
```bash
flask run
```

## Deploy

With the current `Procfile`, the server should be deployable directly to Heroku from GitHub. Other platforms may have other requirements. 

**Remember to set your environment variables appropriately!**

## API

- `/translate`
    - `POST`
    - Translate a list of statements. from one language to another.
- `/evaluate`
    - `POST`
    - Run the translation quality metrics on a list of statements.

## References

> Kocmi, T., & Federmann, C. (2023). Large language models are state-of-the-art evaluators of translation quality. *arXiv preprint*. arXiv:2302.14520.