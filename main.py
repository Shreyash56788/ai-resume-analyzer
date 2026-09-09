from app.resume_processor import load_and_split_resume
from app.embeddings import create_embeddings
from app.retriever import create_faiss_index
from app.job_analyzer import analyze_job
from app.evaluator import evaluate_skills
from app.scorer import calculate_match_score
from app.suggestions import generate_suggestions

chunks = load_and_split_resume("data/Ajit.pdf")

print("Chunks:", len(chunks))

texts = [chunk.page_content for chunk in chunks]

embeddings = create_embeddings(texts)

print("Embeddings shape:", embeddings.shape)

index = create_faiss_index(embedding_matrix)

print("Vector Stored:" , index.ntotal)

job_description = """
We are looking for an AI Engineer.

Required Skills:
- Python
- Machine Learning
- Deep Learning
- LLM
- Docker
- AWS

The candidate should have experience building AI/ML projects
and working with modern AI technologies.
"""

requirements, skill_weights = analyze_job(job_description)

print("\nJob Requirements")
print(requirements)

print("\nSkill Weights")
for skill in skill_weights.skills:
    print(
        skill.skill,"->",
        skill.weight,"%", "|",
        skill.reason
    )

results = evaluate_skills(
    chunks,
    index,
    requirements.required_skills
)

print("\nSKILL EVALUATION")

for result in results:
    print("\nSkill:", result.skill)
    print("Match:", result.match)
    print("Confidence:", result.confidence)
    print("Explanation:", result.explanation)

match_score  = calculate_match_score(
    results,
    skill_weights
)

print("\n===============")
print("Final Resume Match Score")
print("================")
print(f"{match_score}/100")

missing_skills = [
    result.skill
    for result in results
    if not result.match
]

print("\nMissing Skills:")

if missing_skills:
    for skill in missing_skills:
        print("-", skill)
else:
    print("No missing skills")

suggestions = generate_suggestions(missing_skills)

print("\nIMPROVEMENT SUGGESTIONS")

for suggestion in suggestions.suggestions:
    print("\nSkill:", suggestion.skill)
    print("Suggestion:", suggestion.suggestion)
    print("Priority:", suggestion.priority)

    