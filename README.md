# LLM integration with internet search and internal database

## Requirements
To run this program, you gonna need to install [uv](https://docs.astral.sh/uv/getting-started/installation/)
You're also gonna need to have accounts (and money on those accounts) on both [Anthropic Console](https://console.anthropic.com/) and [VoyageAi](https://www.voyageai.com/)
Do not forget to create an `.env` file with the API keys from Anthropic and Voyage. You can check `.env.base` for exemple

## How to run
Just run `make run` on your terminal.

## Endpoints
GET /status
It is a simple healthcheck. It shall return one object with the health check of the application and the integration with other services.
Exemple of return
```
{"status": "ok"}
```

POST /queries/
This endpoint will receive one question and will return an answer for it after consulting the LLM, our internal database, and the internet
Example of request body
```
{
 "query": "What is diversification?"
}
```
Example of return body
```
{
    "answer": "Based on our internal knowledge, diversification is an investment strategy that involves spreading your investments across various asset classes, such as stocks, bonds, and real estate, to reduce risk. \n\nThe key concept behind diversification is that by not putting all your money into one type of investment, you can help protect your portfolio from significant losses if one investment performs poorly. This is often summarized by the phrase \"don't put all your eggs in one basket.\"\n\nDiversification works because different asset classes tend to perform differently under various economic conditions. For example, when stocks are declining, bonds might be stable or rising. By holding both, you can potentially reduce the overall volatility of your portfolio.\n\nDiversification can occur at multiple levels:\n- Across asset classes (stocks, bonds, real estate, commodities, etc.)\n- Within asset classes (different sectors of the stock market, different types of bonds)\n- Geographically (domestic and international investments)\n- By investment style (growth vs. value, large-cap vs. small-cap)\n\nWhile diversification doesn't guarantee profits or protect against all losses, it's generally considered a fundamental principle of sound investing to manage risk."
}
```
It returns status code 200 if your request is valid. Otherwise, it will return a 422 with more information on why your request was not successful

## Future Steps/TODOs
Currently, this solution is very basic and needs some fixes to get production-ready.
- Write unit tests
- Write integration tests
- Find a better way to present the returned value to the user, with the sources used to generate the answer
- The vector database that we use to augment the agent with our internal knowledge is loaded in the memory of the application. We need to set a proper vector database and a proper way to add and remove information there
- We can create new tools to retrieve precise information (like money conversion) instead of using an internet search
- There is still work to be done in our status to guarantee that the application has a stable connection with all of their integrations

## Deployment
Currently, there is no deployment strategy allocated for this application. Since this application does not need to download any LLM or embedding models (all our solutions are external), we could easily utilize a CI/CD service like [GitHub Actions](https://docs.github.com/en/actions) to deploy new versions in our Cloud application. On AWS, we could use EC2, or other solutions built upon that, like Elastic Bean Stalker or Lightsail.
It is always recommended to use a canary strategy for the deployment, since we can monitor what is going on with the new instances.
Do not forget that we still need to create a vector database for our internal knowledge base. We could use a 3rd party database like [Pinecone](https://www.pinecone.io/) or have our own Postgres instance running [pgvector](https://www.postgresql.org/about/news/pgvector-050-released-2700/)