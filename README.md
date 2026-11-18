# 📊 MavenTech B2B Sales Performance & Revenue Analytics

An end-to-end B2B sales analytics project built to uncover revenue drivers, pipeline bottlenecks, sales team efficiency, and customer trends for **MavenTech**, a computer hardware company.

This repository bridges **Business Intelligence (Power BI)** and **Data Science (Python)**—featuring a complete Jupyter Notebook (`main.ipynb`) for data cleaning and exploratory analysis alongside a live, interactive web dashboard (`app.py`) built with Streamlit and Plotly.

---

## 🎯 What This Project Solves
Sales teams often track thousands of deals across multiple regions and products, making it hard to see where money is being made or lost. This project answers four key business questions in plain language:
1. **How is the sales pipeline performing?** Are deals moving smoothly from initial contact to closed sales, or are they getting stuck?
2. **Who are our top performers?** Which sales agents bring in the most revenue, and which ones have the highest success rate at closing deals?
3. **Which hardware products sell best?** Are certain product lines driving most of our revenue while others lag behind?
4. **Who are our best customers?** Which industries (sectors) buy the most hardware, and do larger companies spend more with us?

---

## 📈 Key Business Insights Discovered
* **$10.01M Total Revenue:** Generated across all closed-won hardware deals.
* **48% Overall Win Rate:** Nearly half of all completed negotiations end in a successful sale.
* **11.8% End-to-End Conversion:** While closing efficiency is strong, a large drop-off happens between initial prospecting and final negotiation—highlighting a clear opportunity for better pipeline follow-up.
* **Top Performers vs. Efficient Closers:** **Darcel Schlecht** leads overall revenue ($1.15M+), while **Reed Clapper (65%)** and **Garret Kinder (61%)** maintain the highest win rates.
* **Flagship Products & Sectors:** The **GTXPro**, **GTX Plus Pro**, and **MG Advanced** hardware lines generate the bulk of revenue, with **Retail**, **Technology**, and **Medical** standing out as the top-buying industries.

---

## 🗂️ Repository Structure

Here is what every file in this repository does:

```text
├── main.ipynb              # Step-by-step Jupyter Notebook: data loading, cleaning, EDA & static charts
├── app.py                  # Interactive Streamlit web dashboard replicating the Power BI layout
├── requirements.txt        # List of Python libraries needed to run the code
├── sales_pipeline.csv      # Core dataset of sales opportunities, stages, dates, and deal values
├── products.csv            # Hardware product catalog, series, and retail prices
├── accounts.csv            # Client company details, industry sectors, and annual revenue
├── sales_teams.csv         # Sales representatives, managers, and regional offices
└── data_dictionary.csv     # Reference guide explaining every column in the datasets
```

---

## 🛠️ How the Data Works (Star Schema)
To keep the analysis fast and organized, the four datasets are connected using a **Star Schema** model:
* **Center (`sales_pipeline`):** Tracks every individual sales deal.
* **Connected Details:** Linked to `products` (what was sold), `sales_teams` (who sold it), and `accounts` (who bought it).

---

## 🚀 How to Run This Project on Your Computer

Even if you are new to Python, you can run this entire project locally in four simple steps:

### 1. Download the Project
Clone this repository to your computer:
```bash
git clone https://github.com/habiburrahmantanim/maventech-sales-dashboard.git
cd maventech-sales-dashboard
```

### 2. Install Required Libraries
Install Pandas, NumPy, Matplotlib, Seaborn, Plotly, and Streamlit using the included `requirements.txt` file:
```bash
pip install -r requirements.txt
```

### 3. Explore the Data Cleaning & Analysis (`main.ipynb`)
Open `main.ipynb` in **VS Code** or **Jupyter Notebook** and click **Run All** to see how the raw CSV files are dynamically loaded, cleaned, merged, and analyzed.

### 4. Launch the Interactive Web Dashboard (`app.py`)
Run the following command in your terminal to open the interactive dashboard in your web browser:
```bash
streamlit run app.py
```

---

## 🧰 Tools & Technologies Used
* **Data Cleaning & Exploratory Analysis:** Python, Pandas, NumPy, Matplotlib, Seaborn (`main.ipynb`)
* **Interactive Web Dashboard:** Streamlit, Plotly (`app.py`)
* **Business Intelligence Version:** Microsoft Power BI (Custom DAX measures, Star Schema modeling, Dark Theme UI)
* **Environment & Version Control:** VS Code, Jupyter Notebook, Git & GitHub

---

## 👤 Author

**Habibur Rahman**  
* Software Engineer & Data Analyst  
* GitHub: [@habiburrahmantanim](https://github.com/habiburrahmantanim)
