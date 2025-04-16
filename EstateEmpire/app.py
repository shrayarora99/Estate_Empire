import os
import logging
from datetime import datetime
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, flash, abort, jsonify
import random
import json
from models import Property, Tenant

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "estate-empire-secret-key")

# Initialize default properties
properties = []
tenants = []

# Load sample properties
def initialize_data():
    global properties
    properties = [
        Property(
            id=1,
            title="Modern Studio in Chelsea",
            price=2500,
            location="Chelsea, Manhattan",
            pets_allowed=True,
            min_income=75000,
            min_credit_score=680,
            immediate_availability=True,
            neighborhood="Chelsea",
            image_url="https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80",
            description="A bright and modern studio apartment in the heart of Chelsea, featuring hardwood floors and stainless steel appliances."
        ),
        Property(
            id=2,
            title="Spacious 1BR in Williamsburg",
            price=3200,
            location="Williamsburg, Brooklyn",
            pets_allowed=True,
            min_income=96000,
            min_credit_score=700,
            immediate_availability=False,
            neighborhood="Williamsburg",
            image_url="https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1980&q=80",
            description="Spacious 1-bedroom apartment with exposed brick, high ceilings, and a private balcony. Close to all the best restaurants and shops."
        ),
        Property(
            id=3,
            title="Luxury 2BR in Upper East Side",
            price=4500,
            location="Upper East Side, Manhattan",
            pets_allowed=False,
            min_income=135000,
            min_credit_score=720,
            immediate_availability=True,
            neighborhood="Upper East Side",
            image_url="https://images.unsplash.com/photo-1512917774080-9991f1c4c750?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80",
            description="Elegant 2-bedroom apartment in a doorman building with in-unit laundry, marble bathrooms, and a chef's kitchen."
        ),
        Property(
            id=4,
            title="Cozy 1BR in Astoria",
            price=2200,
            location="Astoria, Queens",
            pets_allowed=True,
            min_income=66000,
            min_credit_score=650,
            immediate_availability=True,
            neighborhood="Astoria",
            image_url="https://images.unsplash.com/photo-1493809842364-78817add7ffb?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80",
            description="Charming 1-bedroom apartment in a quiet neighborhood with great dining options. Recently renovated kitchen and bathroom."
        ),
        Property(
            id=5,
            title="Historic Brownstone 3BR",
            price=5800,
            location="Park Slope, Brooklyn",
            pets_allowed=False,
            min_income=174000,
            min_credit_score=740,
            immediate_availability=False,
            neighborhood="Park Slope",
            image_url="https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80",
            description="Stunning 3-bedroom apartment in a historic brownstone with original details, a backyard garden, and proximity to Prospect Park."
        ),
        Property(
            id=6,
            title="Budget Studio in Washington Heights",
            price=1800,
            location="Washington Heights, Manhattan",
            pets_allowed=True,
            min_income=54000,
            min_credit_score=620,
            immediate_availability=True,
            neighborhood="Washington Heights",
            image_url="https://images.unsplash.com/photo-1493663284031-b7e3aefcae8e?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80",
            description="Affordable studio apartment with good natural light and easy access to public transportation. Perfect for students or young professionals."
        )
    ]

# Initialize the data when the app starts
initialize_data()

# Routes
@app.route('/')
def index():
    """Homepage showing featured listings."""
    try:
        return render_template('index.html', properties=properties)
    except Exception as e:
        logging.error(f"Error rendering index page: {str(e)}")
        return render_template('loading.html')

@app.route('/debug')
def debug():
    """Debug page to help diagnose loading issues."""
    try:
        return render_template('debug.html')
    except Exception as e:
        logging.error(f"Error rendering debug page: {str(e)}")
        return "Debug page error: " + str(e), 500

@app.route('/loading')
def loading():
    """Show a simple loading page."""
    return render_template('loading.html')

@app.route('/ready')
def ready():
    """Simple endpoint to check if the application is running."""
    return "Application is running", 200

@app.route('/prescreening', methods=['GET', 'POST'])
def prescreening():
    """Pre-screening form for tenants."""
    neighborhoods = ["Chelsea", "Williamsburg", "Upper East Side", "Astoria", "Park Slope", "Washington Heights"]
    
    if request.method == 'POST':
        # Process the form submission
        try:
            full_name = request.form.get('full_name')
            preferred_neighborhoods = request.form.getlist('preferred_neighborhoods')
            max_rent = int(request.form.get('max_rent'))
            move_in_date = request.form.get('move_in_date')
            credit_score = int(request.form.get('credit_score'))
            annual_income = int(request.form.get('annual_income'))
            employment_status = request.form.get('employment_status')
            has_pets = 'has_pets' in request.form
            has_guarantor = 'has_guarantor' in request.form
            
            # Calculate days until move-in
            move_in_date_obj = datetime.strptime(move_in_date, '%Y-%m-%d')
            days_until_move = (move_in_date_obj - datetime.now()).days
            
            # Calculate tenant score
            score = calculate_tenant_score(
                credit_score, annual_income, max_rent,
                employment_status, days_until_move,
                has_guarantor, has_pets
            )
            
            # Create a new tenant
            tenant = Tenant(
                id=len(tenants) + 1,
                full_name=full_name,
                preferred_neighborhoods=preferred_neighborhoods,
                max_rent=max_rent,
                move_in_date=move_in_date,
                credit_score=credit_score,
                annual_income=annual_income,
                employment_status=employment_status,
                has_pets=has_pets,
                has_guarantor=has_guarantor,
                score=score
            )
            
            # Add tenant to the list
            tenants.append(tenant)
            
            # Store tenant info in session
            session['tenant_id'] = tenant.id
            
            # Redirect to results page
            return redirect(url_for('results', tenant_id=tenant.id))
        
        except Exception as e:
            logging.error(f"Error processing form: {str(e)}")
            flash(f"There was an error processing your form: {str(e)}", "danger")
            return render_template('prescreening.html', neighborhoods=neighborhoods)
    
    return render_template('prescreening.html', neighborhoods=neighborhoods)

@app.route('/results/<int:tenant_id>')
def results(tenant_id):
    """Display match results for a tenant."""
    # Find the tenant
    tenant = next((t for t in tenants if t.id == tenant_id), None)
    
    if not tenant:
        flash("Tenant not found. Please fill out the form again.", "danger")
        return redirect(url_for('prescreening'))
    
    # Match properties to tenant
    perfect_matches = []
    good_fits = []
    not_matches = []
    
    for prop in properties:
        # Check if property is in preferred neighborhoods
        in_preferred_neighborhood = any(n in tenant.preferred_neighborhoods for n in [prop.neighborhood])
        
        # Check basic requirements
        meets_requirements = (
            prop.price <= tenant.max_rent and
            tenant.annual_income >= prop.min_income and
            tenant.credit_score >= prop.min_credit_score and
            (not prop.pets_allowed or not tenant.has_pets)
        )
        
        # Calculate match percentage (simplified)
        match_percentage = tenant.score
        
        # Categorize the property
        if meets_requirements and match_percentage > 80 and in_preferred_neighborhood:
            perfect_matches.append((prop, match_percentage))
        elif meets_requirements and match_percentage >= 60:
            good_fits.append((prop, match_percentage))
        else:
            not_matches.append((prop, match_percentage))
    
    # Sort by match percentage
    perfect_matches.sort(key=lambda x: x[1], reverse=True)
    good_fits.sort(key=lambda x: x[1], reverse=True)
    not_matches.sort(key=lambda x: x[1], reverse=True)
    
    return render_template(
        'results.html',
        tenant=tenant,
        perfect_matches=perfect_matches,
        good_fits=good_fits,
        not_matches=not_matches
    )

@app.route('/landlord')
def landlord():
    """Simple landlord view showing top tenants per property."""
    property_tenants = []
    
    for prop in properties:
        # Find matching tenants
        matching_tenants = [
            t for t in tenants if
            t.max_rent >= prop.price and
            t.annual_income >= prop.min_income and
            t.credit_score >= prop.min_credit_score and
            (prop.pets_allowed or not t.has_pets)
        ]
        
        # Sort by score
        matching_tenants.sort(key=lambda x: x.score, reverse=True)
        
        # Take top 3
        top_tenants = matching_tenants[:3] if matching_tenants else []
        
        property_tenants.append((prop, top_tenants))
    
    return render_template('landlord.html', property_tenants=property_tenants)

# Helper functions
def calculate_tenant_score(credit_score, annual_income, max_rent, employment_status, days_until_move, has_guarantor, has_pets):
    """Calculate the tenant credential score (out of 100)."""
    score = 0
    
    # Credit Score (25 points)
    if credit_score >= 750:
        score += 25
    elif credit_score >= 700:
        score += 20
    elif credit_score >= 650:
        score += 15
    elif credit_score >= 600:
        score += 10
    else:
        score += 5
    
    # Income-to-Rent Ratio (25 points)
    monthly_income = annual_income / 12
    ratio = monthly_income / max_rent
    
    if ratio >= 4:
        score += 25
    elif ratio >= 3:
        score += 20
    elif ratio >= 2.5:
        score += 15
    elif ratio >= 2:
        score += 10
    else:
        score += 5
    
    # Employment Status (10 points)
    if employment_status == "full-time":
        score += 10
    elif employment_status == "part-time":
        score += 7
    elif employment_status == "freelancer":
        score += 5
    else:  # student
        score += 3
    
    # Move-In Date (10 points)
    if days_until_move <= 30:
        score += 10
    elif days_until_move <= 60:
        score += 7
    elif days_until_move <= 90:
        score += 5
    else:
        score += 3
    
    # Guarantor Present (10 points)
    if has_guarantor:
        score += 10
    
    # Pet Ownership (10 points)
    if not has_pets:
        score += 10
    
    # Completeness Bonus (10 points) - always give this for now
    score += 10
    
    return score
