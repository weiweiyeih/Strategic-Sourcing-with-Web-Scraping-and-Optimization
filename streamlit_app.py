import pulp
import streamlit as st
import pandas as pd
import json
import time
from scraper import scrape_origins

# Define the optimization function
def optimize_min_cost(total_demand, target_quality, target_lead_time):
    # Problem setup
    prob = pulp.LpProblem("Minimize_cost", pulp.LpMinimize)
    
    # Supplier data
    suppliers = [origin1, origin2, origin3, origin4]
    costs = {
        origin1: cost_origin1,
        origin2: cost_origin2,
        origin3: cost_origin3,
        origin4: cost_origin4
    }
    quality = {
        origin1: quality_origin1,
        origin2: quality_origin2,
        origin3: quality_origin3,
        origin4: quality_origin4
    }
    lead_time = {
        origin1: lead_time_origin1,
        origin2: lead_time_origin2,
        origin3: lead_time_origin3,
        origin4: lead_time_origin4
    }
    
    max_supply = {
        origin1: max_supply_origin1,
        origin2: max_supply_origin2,
        origin3: max_supply_origin3,
        origin4: max_supply_origin4
    }
    
    # Decision variables for units sourced from each supplier
    units = pulp.LpVariable.dicts("units", suppliers, lowBound=0, cat='Integer')
    
    # Objective: Minimize total cost (including both product cost and freight)
    prob += pulp.lpSum([(costs[i]) * units[i] for i in suppliers]), "Total Cost"
    
    # Constraint 1: Meet the total demand
    prob += pulp.lpSum([units[i] for i in suppliers]) == total_demand, "Total Demand"
    
    # Constraint 2: Average quality score must be at least target_quality
    prob += (pulp.lpSum([quality[i] * units[i] for i in suppliers]) / total_demand) >= target_quality, "Average Quality"
    
    # Constraint 3: Average lead time must be no more than target_lead_time
    prob += (pulp.lpSum([lead_time[i] * units[i] for i in suppliers]) / total_demand) <= target_lead_time, "Average Lead Time"
    
    # Constraint 4: Each supplier can only supply up to their maximum capacity
    for i in suppliers:
        prob += units[i] <= max_supply[i], f"Max Supply {i}"
    
    # Solve the problem
    prob.solve()
    
    # Results
    status = pulp.LpStatus[prob.status]
    results = {i: units[i].varValue for i in suppliers}
    total_cost = pulp.value(prob.objective)
    
    return status, results, total_cost


# ------------------------------ Intro ------------------------------
# merge technologies and business
# demo 2 use cases: web scraping and sourcing optimization
# which are related to procurement and supply chain management
st.title("Leveraging Technology for Strategic Decision-Making in Procurement and Supply Chain Management")
st.write("""
         In today’s fast-paced global market, effective procurement and supply chain management require a seamless integration of technology and business strategy. Two critical tools that can empower strategic decision-making are web scraping and sourcing optimization. In this demonstration, I will showcase two practical use cases: leveraging web scraping to streamline ingredient sourcing and applying linear programming for sourcing optimization. Both approaches highlight how automation and data-driven decision-making can enhance efficiency in procurement and supply chain management.
         """)

# ------------------------------ Web scraping ------------------------------

st.title("Leveraging Web Scraping for Efficient Sourcing")
st.write("""
         In the evolving world of global sourcing, access to accurate, real-time product information is essential for informed decision-making. By using web scraping techniques, companies can automate the process of gathering key data from supplier websites, such as ingredient availability, pricing, and market trends. This streamlines procurement efforts and provides a competitive edge by enabling businesses to quickly adapt to changes in the market.

As an example, I will demonstrate how web scraping can be applied to extract product details from the Ingredient Brothers website (https://ingredientbrothers.com/), showing how this technology can automate data collection for sourcing professionals.
""")
st.caption("Disclaimer: This web scraping demonstration is solely for demo purposes and to highlight my technical skills. There is no intent to misuse, manipulate, or interfere with the data or operations of the Ingredient Brothers website. All extracted data is used for demonstration purposes only, while respecting the integrity of the website and its content.")

# load json to dict
with open('products.json', 'r') as f:
    products = json.load(f)
    
# save product names to list
product_names = [product['title'] for product in products]

# Create a dropdown (selectbox) using the list
selected_product = st.selectbox('Select a product from Ingredient Brothers', product_names, index=10)

# Display the selected option


for product in products:
    if product['title'] == selected_product:
        img_url = product['img']
        product_url = product['url']
        # st.image(product['img'], caption=product['title'])
        # st.write(f"Product URL: {product['url']}")
        origins = scrape_origins(product_url)
        
        # Create two columns
        col_l, col_r = st.columns(2)
        with col_l:
            st.image(img_url, caption='The product image from Ingredient Brothers')
        with col_r:
            st.subheader(selected_product)
            st.write(f"Origins: {', '.join(origins)}")
            
        


# ------------------------------ Sourcing Optimization ------------------------------
st.title("Strategic Sourcing Optimization")
st.write(f"""
         Beyond data collection, making effective sourcing decisions requires optimization to balance various factors such as cost, quality, and delivery times. Linear programming provides an efficient way to achieve this, enabling companies to optimize sourcing strategies across multiple suppliers.
         
         In this example, we will focus on optimizing the sourcing of the ingredient you have just selected, considering factors such as cost, quality and lead time. For demonstration purposes, we limit the number of origins to four suppliers (Please select a product with at least 4 origins). This allows us to showcase how linear programming helps find the best balance between different supplier attributes to meet business needs efficiently.

        This method can be adapted to various ingredients and applied to different procurement goals, such as minimizing costs, maximizing supply, or reducing lead times. Through these optimization techniques, companies can achieve more strategic and data-driven sourcing decisions that align with broader business objectives.
""")

if len(origins) < 4:
    st.warning("Please select a product with at least four origins to proceed with the sourcing optimization. e.g. 'Bulk Air Dried Kale Powder (OG)' or 'Bulk Amaranth Puffs'")
else:
    
    # Interactive inputs for suppliers' data
    st.header("Input Supplier Capabilities")
    st.caption("""To effectively optimize our sourcing strategy, please provide your assumptions regarding the capabilities of each supplier. Use the sliders below to input the following metrics for each supplier:
    """)
    st.caption("""
    - Cost per Unit: The expected cost of each unit sourced from the supplier.
    - Quality Score: A rating of the supplier’s product quality, on a scale of 1 to 10, where 10 represents the highest quality.
    - Lead Time: The estimated time (in days) required for delivery from the supplier.
    - Max Supply: The maximum supply capacity of the supplier (in units).
    """)

    # Create columns for each supplier
    # Create 2x2 layout
    col1, col2 = st.columns(2)
    st.markdown("<hr>", unsafe_allow_html=True)
    col3, col4 = st.columns(2)

    origin1 = origins[0]
    origin2 = origins[1]
    origin3 = origins[2]
    origin4 = origins[3]

    # Create sliders for each supplier's cost, quality, lead time, max supply, and freight cost
    # Sliders in columns for each supplier
    with col1:
        
        st.subheader(origin1)
        cost_origin1 = st.slider("Cost per Unit (USD)", 1500, 3000, 2000)
        quality_origin1 = st.slider("Quality Score (1-10)", 1, 10, 8)
        lead_time_origin1 = st.slider("Lead Time (days)", 15, 45, 25)
        max_supply_origin1 = st.slider("Max Supply (unit)", 100, 1000, 500)
        
    with col2:

        st.subheader(origin2)
        cost_origin2 = st.slider("Cost per Unit (USD)", 1500, 3000, 2100)
        quality_origin2 = st.slider("Quality Score (1-10)", 1, 10, 9)
        lead_time_origin2 = st.slider("Lead Time (days)", 15, 45, 28)
        max_supply_origin2 = st.slider("Max Supply (unit)", 100, 1000, 600)
        

    with col3:
        st.subheader(origin3)
        cost_origin3 = st.slider("Cost per Unit (USD)", 1500, 3000, 2200)
        quality_origin3 = st.slider("Quality Score (1-10)", 1, 10, 7)
        lead_time_origin3 = st.slider("Lead Time (days)", 15, 45, 20)
        max_supply_origin3 = st.slider("Max Supply (unit)", 100, 1000, 400)
        
            
    with col4:
        st.subheader(origin4)
        cost_origin4 = st.slider("Cost per Unit (USD)", 1500, 3000, 2300)
        quality_origin4 = st.slider("Quality Score (1-10)", 1, 10, 6)
        lead_time_origin4 = st.slider("Lead Time (days)", 15, 45, 30)
        max_supply_origin4 = st.slider("Max Supply (units)", 100, 1000, 700)



    # Create a DataFrame for displaying the slider data in a table
    data = {
        'Origin': [origin1, origin2, origin3, origin4],
        'Cost per Unit (USD)': [cost_origin1, cost_origin2, cost_origin3, cost_origin4],
        'Quality Score (1-10)': [quality_origin1, quality_origin2, quality_origin3, quality_origin4],
        'Lead Time (days)': [lead_time_origin1, lead_time_origin2, lead_time_origin3, lead_time_origin4],

        'Max Supply (units)': [max_supply_origin1, max_supply_origin2, max_supply_origin3, max_supply_origin4]
    }

    # Create DataFrame
    df = pd.DataFrame(data)
    # Display the table
    st.header("Supplier Capabilities Overview")
    st.caption("The table below summarizes the capabilities of each supplier based on your input. ")
    # not displaying the index
    st.write(df.to_html(index=False), unsafe_allow_html=True)


    all_costs = [cost_origin1, cost_origin2, cost_origin3, cost_origin4]
    all_qualities = [quality_origin1, quality_origin2, quality_origin3, quality_origin4]
    all_lead_times = [lead_time_origin1, lead_time_origin2, lead_time_origin3, lead_time_origin4]
    all_supplies = [max_supply_origin1, max_supply_origin2, max_supply_origin3, max_supply_origin4]

    # col_min, col_mx = st.columns(2)

    # with col_min:
    st.header("Minimize Cost")
    st.caption("In this scenario, our goal is to minimize the total cost while ensuring that the demand quantity is met. Please adjust the inputs as necessary to reflect your assumptions. Once you’re ready, press the “Minimize Cost” button to optimize the sourcing strategy based on your criteria.")
    # Set the total demand, target average quality, and lead time
    total_demand_min = st.slider("Total Demand (units)", 1, sum(all_supplies), min(all_supplies))
    target_quality_min = st.slider("Target Average Quality", float(min(all_qualities)), float(max(all_qualities)), float(sum(all_qualities) / len(all_qualities)))
    target_lead_time_min = st.slider("Target Average Lead Time (days)", float(min(all_lead_times)), float(max(all_lead_times)), float(sum(all_lead_times) / len(all_lead_times)))

    # Button for minimizing cost
    if st.button("Minimize Cost"):
        status, results, total_cost = optimize_min_cost(total_demand_min, target_quality_min, target_lead_time_min)
        
        # Display results
        if status == "Optimal":
            st.success("Optimization successful!")
            st.subheader(f"Total Cost: {total_cost} USD")
            for supplier in results:
                st.write(f"Source {results[supplier]:.2f} units from {supplier}")
        else:
            st.error("Optimization failed. Please adjust your inputs.")



# Footer
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown(
    """
    <div style='text-align: center;'>
        <p>Made with 🫶 by William Yeh 👉 https://www.linkedin.com/in/william-rw-yeh/</p>
    </div>
    """, 
    unsafe_allow_html=True
)