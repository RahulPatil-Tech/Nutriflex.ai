import google.generativeai as genai

genai.configure(api_key="Api_KEY")
# Convert generator to a list
models = list(genai.list_models())

# Print all available model names
for model in models:
    print(model.name)
