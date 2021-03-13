"""Plant routes"""
from flask import render_template
from app import app
from generator.generator import get_plant_info

@app.route('/plant/<slug>')
def plant_detail(slug):
    """Show details about plant. 
    Plant will be 'False' if API call fails. This is handled in the template."""

    plant = get_plant_info(slug)
    search_slug = slug.replace('-', '+')

    return render_template('plant_detail.html', 
                        plant=plant, 
                        search_slug=search_slug)