from flask import Flask, render_template, request
from openai import OpenAI

app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)

# =====================================
# Paste your OpenRouter API Key here
# =====================================
API_KEY = ""

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=API_KEY
)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/explain", methods=["POST"])
def explain():

    code = request.form.get("code", "").strip()

    if code == "":
        return render_template(
            "index.html",
            error="Please enter source code."
        )

    prompt = f"""
You are an AI Code Explainer.

Analyze the following source code and provide:

1. Programming Language
2. Simple Explanation
3. Algorithm
4. Time Complexity
5. Space Complexity
6. Improvements
7. Best Practices

Code:

{code}
"""

    try:

        response = client.chat.completions.create(
            model="openai/gpt-oss-20b:free",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3
        )

        result = response.choices[0].message.content

        return render_template(
            "index.html",
            result=result,
            code=code
        )

    except Exception as e:

        return render_template(
            "index.html",
            error=str(e),
            code=code
        )


if __name__ == "__main__":
    app.run(
        host="127.0.0.2",
        port=8000,
        debug=True
    )