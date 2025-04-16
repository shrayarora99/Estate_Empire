class Property:
    def __init__(self, id, title, price, location, pets_allowed, min_income, min_credit_score, 
                 immediate_availability, neighborhood, image_url, description):
        self.id = id
        self.title = title
        self.price = price
        self.location = location
        self.pets_allowed = pets_allowed
        self.min_income = min_income
        self.min_credit_score = min_credit_score
        self.immediate_availability = immediate_availability
        self.neighborhood = neighborhood
        self.image_url = image_url
        self.description = description

class Tenant:
    def __init__(self, id, full_name, preferred_neighborhoods, max_rent, move_in_date, 
                 credit_score, annual_income, employment_status, has_pets, has_guarantor, score):
        self.id = id
        self.full_name = full_name
        self.preferred_neighborhoods = preferred_neighborhoods
        self.max_rent = max_rent
        self.move_in_date = move_in_date
        self.credit_score = credit_score
        self.annual_income = annual_income
        self.employment_status = employment_status
        self.has_pets = has_pets
        self.has_guarantor = has_guarantor
        self.score = score
        self.verified = score > 75
