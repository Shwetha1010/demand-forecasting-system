def recommend(pred):
    if pred > 8000:
        return "Increase inventory"
    elif pred < 3000:
        return "Run promotion / discount"
    else:
        return "Maintain stock"