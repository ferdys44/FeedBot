import streamlit as st
from dataclasses import dataclass
from typing import Dict, Optional, List
import pandas as pd

# ============================================================================
# Data Models
# ============================================================================

@dataclass
class FeedIngredient:
    name: str
    protein: float      # g/kg
    energy: float       # MJ/kg
    cost: float         # per kg

@dataclass
class RationRequirement:
    protein: float
    energy: float
    total_weight: float

# ============================================================================
# Feed Optimization Logic
# ============================================================================

class FeedOptimizer:
    def __init__(self):
        self.ingredients: List[FeedIngredient] = []
    
    def add_ingredient(self, ingredient: FeedIngredient):
        """Add an ingredient to the list"""
        self.ingredients.append(ingredient)
    
    def remove_ingredient(self, index: int):
        """Remove an ingredient by index"""
        if 0 <= index < len(self.ingredients):
            self.ingredients.pop(index)
    
    def optimize_ration(self, requirement: RationRequirement) -> Optional[Dict]:
        """
        Find the combination with lowest cost meeting requirements.
        Uses brute-force optimization for 2 ingredients.
        """
        if len(self.ingredients) < 2:
            return None
        
        ing1 = self.ingredients[0]
        ing2 = self.ingredients[1]
        
        best_cost = float('inf')
        best_mix = None
        
        # Try all combinations of weights (0-total_weight in 0.1kg increments)
        step_size = 0.1
        w1 = 0
        while w1 <= requirement.total_weight:
            w2 = requirement.total_weight - w1
            
            # Calculate weighted averages
            total_protein = (ing1.protein * w1 + ing2.protein * w2) / requirement.total_weight
            total_energy = (ing1.energy * w1 + ing2.energy * w2) / requirement.total_weight
            total_cost = ing1.cost * w1 + ing2.cost * w2
            
            # Check if requirements are met and cost is better
            if (total_protein >= requirement.protein and 
                total_energy >= requirement.energy and 
                total_cost < best_cost):
                best_cost = total_cost
                best_mix = {
                    'mix': {ing1.name: round(w1, 2), ing2.name: round(w2, 2)},
                    'protein': round(total_protein, 2),
                    'energy': round(total_energy, 2),
                    'cost': round(total_cost, 2)
                }
            
            w1 += step_size
        
        return best_mix

# ============================================================================
# Streamlit App
# ============================================================================

st.set_page_config(page_title="Feed Rations Optimizer", layout="wide")

st.title("🌾 Feed Rations Optimizer")
st.markdown("Optimize animal feed rations with lowest cost while meeting nutritional requirements.")

# Initialize session state
if 'optimizer' not in st.session_state:
    st.session_state.optimizer = FeedOptimizer()

if 'optimized_result' not in st.session_state:
    st.session_state.optimized_result = None

# ============================================================================
# Sidebar: Add Ingredients
# ============================================================================

st.sidebar.header("➕ Add Ingredient")

with st.sidebar.form("add_ingredient_form"):
    name = st.text_input("Ingredient Name")
    protein = st.number_input("Protein (g/kg)", min_value=0.0, step=0.1)
    energy = st.number_input("Energy (MJ/kg)", min_value=0.0, step=0.1)
    cost = st.number_input("Cost (per kg)", min_value=0.0, step=0.01)
    
    if st.form_submit_button("Add Ingredient"):
        if name:
            ingredient = FeedIngredient(name=name, protein=protein, energy=energy, cost=cost)
            st.session_state.optimizer.add_ingredient(ingredient)
            st.success(f"✓ {name} added!")
        else:
            st.error("Please enter ingredient name")

# ============================================================================
# Main Content: Ingredients List & Optimization
# ============================================================================

col1, col2 = st.columns([1, 1])

# Left column: Ingredients
with col1:
    st.header("📋 Ingredients")
    
    if st.session_state.optimizer.ingredients:
        # Display ingredients in a table
        df_data = []
        for i, ing in enumerate(st.session_state.optimizer.ingredients):
            df_data.append({
                'Name': ing.name,
                'Protein (g/kg)': ing.protein,
                'Energy (MJ/kg)': ing.energy,
                'Cost ($/kg)': ing.cost
            })
        
        df = pd.DataFrame(df_data)
        st.dataframe(df, use_container_width=True)
        
        # Remove ingredient
        st.markdown("---")
        selected_idx = st.selectbox("Select ingredient to remove:", 
                                    range(len(st.session_state.optimizer.ingredients)),
                                    format_func=lambda x: st.session_state.optimizer.ingredients[x].name)
        
        if st.button("🗑️ Remove Selected"):
            st.session_state.optimizer.remove_ingredient(selected_idx)
            st.rerun()
    else:
        st.info("No ingredients added yet. Add some from the sidebar to get started!")

# Right column: Requirements & Optimization
with col2:
    st.header("⚙️ Requirements & Optimization")
    
    with st.form("optimize_form"):
        protein_req = st.number_input("Required Protein (g/kg)", min_value=0.0, step=0.1)
        energy_req = st.number_input("Required Energy (MJ/kg)", min_value=0.0, step=0.1)
        total_weight = st.number_input("Total Weight (kg)", min_value=0.1, step=0.1)
        
        if st.form_submit_button("🚀 Optimize Ration"):
            if len(st.session_state.optimizer.ingredients) < 2:
                st.error("Need at least 2 ingredients to optimize!")
            else:
                requirement = RationRequirement(
                    protein=protein_req,
                    energy=energy_req,
                    total_weight=total_weight
                )
                result = st.session_state.optimizer.optimize_ration(requirement)
                st.session_state.optimized_result = result

# ============================================================================
# Results
# ============================================================================

if st.session_state.optimized_result:
    st.markdown("---")
    st.header("✅ Optimal Ration")
    
    result = st.session_state.optimized_result
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Cost", f"${result['cost']}")
    with col2:
        st.metric("Protein", f"{result['protein']} g/kg")
    with col3:
        st.metric("Energy", f"{result['energy']} MJ/kg")
    with col4:
        st.metric("Total Weight", f"{sum(result['mix'].values())} kg")
    
    st.markdown("**Feed Mix:**")
    mix_data = []
    for ingredient_name, weight in result['mix'].items():
        mix_data.append({'Ingredient': ingredient_name, 'Weight (kg)': weight})
    
    st.dataframe(pd.DataFrame(mix_data), use_container_width=True)
else:
    st.info("📊 Fill in requirements and click 'Optimize Ration' to see results")

# ============================================================================
# Footer
# ============================================================================

st.markdown("---")
st.markdown("""
**Feed Rations Optimizer** • v1.0 | 
*Optimize your animal feed rations for cost efficiency while meeting nutritional requirements.*
""")
