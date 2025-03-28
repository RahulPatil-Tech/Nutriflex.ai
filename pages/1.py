import google.generativeai as genai

genai.configure(api_key="AIzaSyB6RH6l9QkG-7YO4Pq6mkuac_lmSEAzHPc")
# Convert generator to a list
models = list(genai.list_models())

# Print all available model names
for model in models:
    print(model.name)