def calculate_approval_rates(reviews):
    """Calculate the approval rates of a list of reviews."""
    if reviews.count():
        return (reviews.filter(rating__gte=3).count() / reviews.count()) * 100
    return 0
