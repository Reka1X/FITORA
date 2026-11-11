from features.recommendations.models import (
    CapsuleRecommendation,
    ColorMatchRecommendation,
    OccasionMatchRecommendation,
)


RECOMMENDATION_CLASSES = {
    "Color match": ColorMatchRecommendation,
    "Occasion match": OccasionMatchRecommendation,
    "Capsule": CapsuleRecommendation,
}


def generate(items, recommendation_type, style, occasion):
    recommendation_class = RECOMMENDATION_CLASSES[recommendation_type]

    # Capsule suggestions retain a small, varied selection of available items
    # so the result can be combined in more than one way.
    selected = list(items)
    if recommendation_type == "Capsule":
        selected.sort(
            key=lambda item: (
                item["style"] != style,
                item["item_type"],
                item["name"],
            )
        )
        selected = selected[:8]

    recommendation = recommendation_class(selected)
    score = recommendation.calculate_score(style, occasion)
    explanation = recommendation.explain_score(style, occasion, score)

    if recommendation_type == "Capsule":
        title = f"{style} capsule for {occasion}"
    elif recommendation_type == "Color match":
        title = f"Color match for {occasion}"
    else:
        title = f"{occasion} outfit suggestion"

    return {
        "score": score,
        "explanation": explanation,
        "title": title,
        "items": selected,
        "type": recommendation.recommendation_type,
    }