from neo4j import GraphDatabase
import os
import openai

openai.api_key = os.environ.get('OPENAI_KEY')

host = 'bolt://neo4j:'
user = 'admin'
password = 'password'
driver = GraphDatabase.driver(host, auth=(user, password))

examples = """
"""

def read_query(query, params={}):
    with driver.session() as session:
        result = session.run(query, params)
        response = [r.values()[0] for r in result]
        return response


def get_article_text(title):
    text = read_query(
        "MATCH (a:Article {webTitle:$title}) RETURN a.bodyContent as response", {'title': title})
    return text


def generate_response(prompt):
    completions = openai.Completion.create(
        engine="text-davinci-003",
        prompt=examples + "\n#" + prompt,
        max_tokens=1000,
        n=1,
        stop=None,
        temperature=0.5,
    )
    cypher_query = completions.choices[0].text
    message = read_query(cypher_query)
    return message, cypher_query


user_input = ""
output, cypher_query = generate_response(user_input)

