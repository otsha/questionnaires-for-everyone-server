# Questionnaires for Everyone (SERVER)

The backend component for our web application designed for questionnaire translation. Handles translation and prompting GPT-4 for translation quality evaluation.

Translations are performed by calling the DeepL API. The evaluation methods offered are GEMBA-DA\[noref\] (Kocmi & Federmann, 2023) and a custom semantic similarity assessment ("SSA"). The latter prompts a verbal evaluation of how semantically close the translation is to the original, as this is often the most important factor in questionnaire translation compared to, say, exact word-by-word match (Su & Parham, 2002).

The application frontend is available [here](https://github.com/otsha/questionnaires-for-everyone).

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

> Su, C. T., & Parham, L. D. (2002). Generating a valid questionnaire translation for cross-cultural use. *The American Journal of Occupational Therapy, 56*(5), 581-585.
