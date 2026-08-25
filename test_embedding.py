from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim


model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)


text1 = "dishwasher drain pump"

text2 = "part that removes water from a dishwasher"

text3 = "chocolate cake recipe"


embedding1 = model.encode(text1)
embedding2 = model.encode(text2)
embedding3 = model.encode(text3)


print(
    "pump vs water:",
    cos_sim(embedding1, embedding2)
)

print(
    "pump vs cake:",
    cos_sim(embedding1, embedding3)
)
