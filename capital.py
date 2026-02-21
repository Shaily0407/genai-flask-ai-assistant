import ssl
ssl._create_default_https_context = ssl._create_unverified_context

from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames

credentials = Credentials(
    url="https://us-south.ml.cloud.ibm.com"
)

params = {
    GenTextParamsMetaNames.DECODING_METHOD: "greedy",
    GenTextParamsMetaNames.MAX_NEW_TOKENS: 50
}

model = ModelInference(
    model_id='meta-llama/llama-4-maverick-17b-128e-instruct-fp8',
    params=params,
    credentials=credentials,
    project_id="skills-network"
)

text = """
Only reply with the answer. What is the capital of Canada?
"""

response = model.generate(text)
output = response['results'][0]['generated_text'].strip().split("\n")[0]

print(output)