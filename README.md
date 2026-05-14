# FeedBot

# 🌾 Feed Rations Optimizer - Streamlit App

A web application for optimizing animal feed rations to meet nutritional requirements while minimizing costs.

## Features

- ✨ **Add Multiple Ingredients** - Input feed ingredients with their nutritional and cost data
- 📊 **Optimize Rations** - Find the lowest-cost feed mixture that meets requirements
- 📈 **Interactive UI** - User-friendly Streamlit interface
- 💾 **Session State** - Maintains your ingredients and results during the session

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/ferdys44/FeedBot.git
cd FeedBot
```

2. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the App

```bash
streamlit run app.py
```

The app will open in your default browser at `http://localhost:8501`

## How to Use

1. **Add Ingredients**:
   - Enter ingredient name, protein content (g/kg), energy content (MJ/kg), and cost (per kg)
   - Click "Add Ingredient"

2. **View Ingredients**:
   - All added ingredients are displayed in a table
   - You can remove ingredients by selecting and clicking "Remove Selected"

3. **Optimize**:
   - Enter nutritional requirements (protein and energy per kg)
   - Enter total weight needed (in kg)
   - Click "Optimize Ration"

4. **View Results**:
   - See the optimal mix of ingredients
   - View total cost and nutritional metrics
   - Ingredient weights are shown in kg

## Example

Try these sample ingredients:
- **Corn**: Protein 8g/kg, Energy 12 MJ/kg, Cost $0.15/kg
- **Soybean Meal**: Protein 45g/kg, Energy 8 MJ/kg, Cost $0.45/kg
- **Oats**: Protein 12g/kg, Energy 10 MJ/kg, Cost $0.20/kg

Set requirements like:
- Protein: 16 g/kg
- Energy: 10 MJ/kg
- Total Weight: 100 kg

## Technical Details

- **Framework**: Streamlit (Python web framework)
- **Algorithm**: Brute-force optimization with 0.1kg increments
- **Data Storage**: Session state (no database required)

For large-scale applications, consider using linear programming libraries like `PuLP` or `SciPy`.

## Future Enhancements

- [ ] Support for multiple ingredient combinations (not just 2)
- [ ] Advanced optimization using linear programming
- [ ] Cost and nutritional constraint graphs
- [ ] Save/load ration designs
- [ ] Export ration reports to CSV/PDF

## License

MIT License - Feel free to use and modify!
